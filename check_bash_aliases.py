import os



def get_home_directory():
    username = os.getlogin()
    homedir = f"/home/{username}/"
    home_files = os.listdir(homedir)

    ret_files = []
    for home_file in home_files:
        if home_file.startswith("."):
            ret_files.append(home_file)
    return ret_files


def check_aliases(files):
    afiles = files
    if '.bash_aliases' in afiles:
        ret =  '.bash_aliases'
    elif '.bashrc' in afiles:
        ret = '.bashrc'
    elif '.zprofile' in afiles:
        ret = '.zprofile'
    else:
        print("could not locate aliases")
        ret = afiles
    return ret
    
def read_alias_file(target):
    username = os.getlogin()
    file_str = f"/home/{username}/{target}"
    file = open(file_str,'r')
    ret_aliases = []
    lines = file.readlines()
    
    for line in lines:
        if line.startswith('alias'):
            ret_aliases.append(line)
    
    file.close()
    aliases = []
    for ret_aliase in ret_aliases:
        alias = ret_aliase[6:]
        aliases.append(alias)
 
    real_aliases = aliases[3:]
    for x in real_aliases:
        print(f"\033[32m{x}\033[0m")
        
    
    return aliases

    


def main():
    alias_files = get_home_directory()

    afile = check_aliases(alias_files)
    if isinstance(afile, str):
        read_alias_file(afile)
    else:
        print("could not register alias")

if __name__ == '__main__':
    main()