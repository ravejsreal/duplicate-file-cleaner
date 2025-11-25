# 🗂️ duplicate file cleaner

a simple python app to find and remove duplicate files in a folder. fast, safe, and easy to use. duplicates are detected based on **file size + content hash**. always double-check files before deleting.

---

## features

- scan any folder for duplicates  
- browse folder easily  
- progress bar shows scanning status  
- view duplicates grouped together  
- delete selected files or delete all duplicates  
- skips very large files automatically for speed  
- warning shown to avoid accidental deletion  

---

## requirements

- python 3.10+  
- tkinter (usually included with python)  

---

## usage

1. clone or download the repo  

2. run the app:

python main.py


3. select a folder or use the default downloads folder  
4. click **scan** to find duplicates  
5. review duplicates in the list  
6. delete selected files or delete all duplicates  

> ⚠️ always double-check before deleting anything. mistakes can happen.

---

## how it works

- recursively scans the selected folder  
- checks each file size and computes a hash (md5) for files under ~50MB  
- groups duplicates by **same folder + same size + same hash**  
- displays groups in a tree view with easy delete buttons  

---

## notes

- very large files are skipped for faster scanning  
- only detects duplicates in the **same folder / subfolders**  
- filenames like `file.txt` and `file (1).txt` are **not considered duplicates** unless content matches  

---

## license

free to use, modify, and share. use responsibly.
