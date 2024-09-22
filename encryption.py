import os
import tkinter as tk
from tkinter import filedialog
import secrets
from datetime import datetime

def encrypt_files(directory):
    encrypted_data = b''
    file_info = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            with open(file_path, 'rb') as f:
                file_data = f.read()
                file_info.append((relative_path, len(file_data)))
                encrypted_data += file_data
    
    key = secrets.token_bytes(16)
    
    output_file = os.path.join(directory, f'{datetime.now().strftime('%M%Y%m%d%H%M%S')}.dir')
    with open(output_file, 'wb') as f:
        f.write(key)
        f.write(len(file_info).to_bytes(4, 'big'))
        for path, size in file_info:
            f.write(len(path).to_bytes(2, 'big'))
            f.write(path.encode())
            f.write(size.to_bytes(8, 'big'))
        
        encrypted_data = bytes(b ^ key[i % len(key)] for i, b in enumerate(encrypted_data))
        f.write(encrypted_data)
    
    return key.hex()

root = tk.Tk()
root.withdraw()

directory = filedialog.askdirectory()

if directory:
    key = encrypt_files(directory)
    print(key)