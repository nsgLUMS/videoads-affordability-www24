import os

# define the directory path to iterate over
directory_path = "./"

# get a list of all the directories in the specified path
directories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]

# remove empty directories
for d in directories:
    dir_path = os.path.join(directory_path, d)
    if not os.listdir(dir_path):
        os.rmdir(dir_path)
        directories.remove(d)

# sort directories alphabetically and rename them in numerical order
directories.sort()
for i, d in enumerate(directories):
    dir_path = os.path.join(directory_path, d)
    new_dir_name = f"{i+1:03d}"
    os.rename(dir_path, os.path.join(directory_path, new_dir_name))
