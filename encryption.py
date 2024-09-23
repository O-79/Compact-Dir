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
    
    num_files = len(file_info)
    key = secrets.token_bytes(16 * num_files)
    
    key_positions = []
    available_positions = list(range(len(encrypted_data)))
    for _ in range(16 * num_files):
        if not available_positions:
            break
        index = secrets.randbelow(len(available_positions))
        position = available_positions.pop(index)
        key_positions.append(position)
    key_positions.sort()
    
    output_file = os.path.join(directory, f'{datetime.now().strftime("%M%Y%m%d%H%M%S")}.dir')
    with open(output_file, 'wb') as f:
        f.write(num_files.to_bytes(4, 'big'))
        for path, size in file_info:
            f.write(len(path).to_bytes(2, 'big'))
            f.write(path.encode())
            f.write(size.to_bytes(8, 'big'))
        
        encrypted_data = bytearray(encrypted_data)
        for i, pos in enumerate(key_positions):
            encrypted_data.insert(pos, key[i])
        
        f.write(bytes(encrypted_data))
    
    return f"{num_files} {key.hex()} {' '.join(map(str, key_positions))}"

root = tk.Tk()
root.withdraw()

directory = filedialog.askdirectory()

if directory:
    key_info = encrypt_files(directory)
    print(key_info)