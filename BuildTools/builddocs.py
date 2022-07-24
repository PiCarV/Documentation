import os, sys
import zipfile

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

print("Starting to build docs!")

# loop through the file array, move into the directory, and run pdflatex on the file
for file in file_array:
    os.system(f'cd \"{os.path.dirname(file)}\" && pdflatex -shell-escape -halt-on-error \"{os.path.basename(file)}\"')

pdf_array = []
pdf_count = 0

for root, dirs, files in os.walk(top = './'):
    for file in files:
        if file.endswith('.pdf'):
            pdf_array.append(os.path.join(root, file))
            pdf_count += 1

if pdf_count != file_count:
    print(f'{pdf_count} pdf files found')
    print(f'{file_count} files found')
    print("Something went wrong, exiting!")
    sys.exit(1)
else:
    print(f'{pdf_count} pdf files found')
    print(f'{file_count} files found')
    print("All files built successfully!")

# loop through the pdf array, and move the file to the output directory using the same folder structure
# create an output directory if it doesn't exist
if not os.path.exists('./output'):
    os.makedirs('./output')

# move the pdf files to the output directory
for file in pdf_array:
    os.system(f'mv \"{file}\" \"{os.path.join("./output", os.path.basename(file))}\"')

# zip the output directory
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

with zipfile.ZipFile('output.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir('./output/', zipf)


print("Finished building docs!")
