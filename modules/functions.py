import os

def expected_argc(comd, exp):
    argc = len(comd) - 1
    if not argc in exp:
        raise Exception(f"Expected {exp} arguments, found {argc}")
    return True

def rename_dir_elements(dirpath):
    # Remove dollar signs in names
    dirlist = os.listdir(dirpath)
    for name in dirlist:
        new_name = ''.join(list(filter(lambda x : x != '$', name)))
        os.rename(dirpath+name, dirpath+new_name)

def create_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)