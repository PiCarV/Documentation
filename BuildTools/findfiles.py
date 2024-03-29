# get all files in a directory and subdirectories that end with tex

import os, sys

def set_action_output(name: str, value: str):
    sys.stdout.write(f'::set-output name={name}::{value}\n')

file_array = []
file_count = 0

for root, dirs, files in os.walk(top = './'):
    for file in files:
        if file.endswith('.tex'):
            file_array.append(os.path.join(root, file))
            file_count += 1
    

print(f'{file_count} files found')
set_action_output('files', str(file_array))
set_action_output('file_count', str(file_count))


