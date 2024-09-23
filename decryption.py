import os
import tkinter as tk
from tkinter import filedialog

def decrypt_files(encrypted_file, key_info):
    num_files, key, *key_positions = key_info.split()
    num_files = int(num_files)
    if len(key_positions) != 16 * num_files:
        raise ValueError("!")
    key = bytes.fromhex(key)
    key_positions = list(map(int, key_positions))

    with open(encrypted_file, 'rb') as f:
        stored_num_files = int.from_bytes(f.read(4), 'big')
        if stored_num_files != num_files:
            raise ValueError("!")
        
        file_info = []
        for _ in range(num_files):
            path_length = int.from_bytes(f.read(2), 'big')
            path = f.read(path_length).decode()
            size = int.from_bytes(f.read(8), 'big')
            file_info.append((path, size))
        
        encrypted_data = bytearray(f.read())
    
    for pos in reversed(key_positions):
        if encrypted_data[pos] != key[key_positions.index(pos)]:
            raise ValueError("!")
        del encrypted_data[pos]
    
    output_dir = os.path.dirname(encrypted_file)
    
    offset = 0
    for path, size in file_info:
        file_data = encrypted_data[offset:offset+size]
        offset += size
        
        output_path = os.path.join(output_dir, path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(file_data)

root = tk.Tk()
root.withdraw()

encrypted_file = filedialog.askopenfilename(filetypes=[("DIR files", "*.dir")])

if encrypted_file:
    key_info = input(':')
    try:
        decrypt_files(encrypted_file, key_info)
    except ValueError as e:
        print(e)