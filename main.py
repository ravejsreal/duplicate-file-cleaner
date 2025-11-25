import os
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread

def hash_file(path, max_size=50*1024*1024):
    try:
        if os.path.getsize(path) > max_size:
            return None
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None

def scan_folder(folder, progress_cb, done_cb):
    duplicates = {}
    total_files = sum(len(files) for _, _, files in os.walk(folder))
    scanned = 0
    seen = {}
    for root, _, files in os.walk(folder):
        for name in files:
            fp = os.path.join(root, name)
            if not os.path.isfile(fp):
                continue
            try:
                size = os.path.getsize(fp)
            except:
                continue
            file_hash = hash_file(fp)
            key = (root, size, file_hash)
            if file_hash is None:
                scanned += 1
                progress_cb(scanned, total_files)
                continue
            if key in seen:
                duplicates.setdefault(root, set())
                duplicates[root].add(seen[key])
                duplicates[root].add(fp)
            else:
                seen[key] = fp
            scanned += 1
            progress_cb(scanned, total_files)
    for k in duplicates:
        duplicates[k] = sorted(list(duplicates[k]))
    done_cb(duplicates)

root = tk.Tk()
root.title("file cleaner")
root.geometry("900x550")

folder_var = tk.StringVar()
folder_var.set(os.path.join(os.path.expanduser("~"), "downloads"))

top = tk.Frame(root)
top.pack(fill="x", pady=5)

tk.Label(top, text="folder:").pack(side="left")
tk.Entry(top, textvariable=folder_var, width=50).pack(side="left", padx=5)

def browse_folder():
    f = filedialog.askdirectory()
    if f:
        folder_var.set(f)

tk.Button(top, text="browse", command=browse_folder).pack(side="left", padx=5)

progress = ttk.Progressbar(top, length=200)
progress.pack(side="left", padx=10)

scan_btn = tk.Button(top, text="scan", width=10)
scan_btn.pack(side="left", padx=5)

delete_all_btn = tk.Button(top, text="delete all duplicates", width=20)
delete_all_btn.pack(side="left", padx=5)

tree = ttk.Treeview(root)
tree["columns"] = ("group", "path")
tree.heading("#0", text="")
tree.heading("group", text="duplicate group")
tree.heading("path", text="file path")
tree.column("group", width=120)
tree.column("path", width=700)
tree.pack(fill="both", expand=True)

warning_label = tk.Label(root, text="⚠️ double check before deleting anything, since it may be inaccurate", fg="red")
warning_label.pack(pady=5)

duplicates_data = {}

def update_progress(scanned, total):
    def _update():
        progress["value"] = int(scanned / total * 100)
    root.after(0, _update)

def done_scan(dups):
    global duplicates_data
    duplicates_data = dups
    def _update_tree():
        tree.delete(*tree.get_children())
        group_id = 1
        for folder, files in dups.items():
            for f in files:
                tree.insert("", "end", values=(f"group {group_id}", f))
            group_id += 1
        messagebox.showinfo("scan finished", "scan complete. double check files before deleting")
    root.after(0, _update_tree)

def start_scan():
    progress["value"] = 0
    tree.delete(*tree.get_children())
    t = Thread(target=scan_folder, args=(folder_var.get(), update_progress, done_scan))
    t.start()

def delete_selected():
    item = tree.selection()
    if not item:
        return
    path = tree.item(item, "values")[1]
    try:
        os.remove(path)
        tree.delete(item)
    except:
        messagebox.showerror("error", f"could not delete file: {path}")

def delete_all_duplicates():
    for files in duplicates_data.values():
        if len(files) < 2:
            continue
        for f in files[1:]:
            try:
                os.remove(f)
            except:
                pass
    start_scan()

scan_btn.config(command=start_scan)
delete_all_btn.config(command=delete_all_duplicates)

delete_btn = tk.Button(root, text="delete selected", command=delete_selected)
delete_btn.pack(side="right", padx=10, pady=5)

root.mainloop()
