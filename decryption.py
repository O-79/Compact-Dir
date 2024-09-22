import os
import tkinter as tk
from tkinter import filedialog

def decrypt_files(encrypted_file, key):
    with open(encrypted_file, 'rb') as f:
        file_key = f.read(16)
        if file_key != bytes.fromhex(key):
            raise ValueError("!")
        
        num_files = int.from_bytes(f.read(4), 'big')
        file_info = []
        
        for _ in range(num_files):
            path_length = int.from_bytes(f.read(2), 'big')
            path = f.read(path_length).decode()
            size = int.from_bytes(f.read(8), 'big')
            file_info.append((path, size))
        
        encrypted_data = f.read()
    
    decrypted_data = bytes(b ^ file_key[i % len(file_key)] for i, b in enumerate(encrypted_data))
    
    output_dir = os.path.dirname(encrypted_file)
    
    offset = 0
    for path, size in file_info:
        file_data = decrypted_data[offset:offset+size]
        offset += size
        
        output_path = os.path.join(output_dir, path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(file_data)

root = tk.Tk()
root.withdraw()

encrypted_file = filedialog.askopenfilename(filetypes=[("DIR files", "*.dir")])

if encrypted_file:
    key = input()
    try:
        decrypt_files(encrypted_file, key)
    except ValueError as e:
        print(e)