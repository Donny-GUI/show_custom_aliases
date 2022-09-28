#[author]      : donald guiles
#[date]        : sept, 27 2022
#[description] : shows you all the custom aliases, linux only
#[language]    : python3
#[dependencies]: rich

import os
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from sys import argv
# prints aliases to the console

def check_os():
    """ returns true if posix """
    
    opsys = os.name()
    check = False
    if opsys == 'posix':
        check = True
    return check


def get_home_directory():
    """ gets all the . files from home as a list """

    username = os.getlogin()
    homedir = f"/home/{username}/"
    home_files = os.listdir(homedir)

    ret_files = []
    for home_file in home_files:
        if home_file.startswith("."):
            ret_files.append(home_file)
    return ret_files


def check_aliases(files):
    """ determines alias file from get_directory() """

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
    """ Returns all the aliases from the target file """

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
 
    real_aliases = aliases[4:]

    return real_aliases


def show_aliases(alias_lines):
    """ takes alias lines from file, returns a table of aliases """

    table = Table(title='Known Aliases')
    table.add_column("Command", justify='right', style='red')
    table.add_column("Executed String", justify='left', style='cyan')
    for x in alias_lines:
        myslice = re.search("='", x).span()
        alias_name = int(myslice[0])
        alias_command = int(myslice[1])
        name = x[0:alias_name]
        command = x[alias_command:]
        table.add_row(name, command)
    console = Console()
    console.print(table)


def show_help():
    print("         ")
    print("[ ali ]\n")
    print("  [description]")
    print("      alias and command manager ")
    print(" ")
    print("  [usage]")
    print("      ali show <command>")
    print("      ali add  <command name> '<command string>")
    print("      ali edit <command name>")
    print("      ali delete <command name>")
    print("      ali list")
    print("      ali doctor")
    print("      ")
    print("  [options]")
    print("      show   --  Show a particular alias or command  ")
    print("      add    --  add a new alias or command  ")
    print("      edit   --  edit an existing alias or command")
    print("      list   --  list a all commands or aliases")
    print("      delete --  delete a known alias or command")
    print("      doctor --  attempt to fix or clean ali\n")


def get_current_aliases_aslist():
    alias_files = get_home_directory()

    afile = check_aliases(alias_files)

    if isinstance(afile, str):

        x = read_alias_file(afile)
        return x


def display_aliases():

    alias_files = get_home_directory()

    afile = check_aliases(alias_files)

    if isinstance(afile, str):

        x = read_alias_file(afile)

        display = show_aliases(x)



def match_command():
    """ matches to 'help' 'add' 'list' """

    if argv == ['aliases.py']:
        show_help()
        exit()

    command = " ".join(argv)
    my_option = 'x'
    try:
        add = re.search('aliases.py add', command).span()
        my_option = add
    except:
        pass
    try:
        help0 = re.search('aliases.py help', command).span()
        my_option = help0
    except:
        pass
    try:
        show = re.search('aliases.py show', command).span()
        my_option = show
    except:
        pass
        try:
            _list = re.search('aliases.py list', command).span()
            my_option = _list
        except:
            pass


    if my_option == 'x':
        show_help()
        exit()
    else:
        start,end = int(my_option[0]), int(my_option[1])
        tag = command[start:end]
        try:
            args = command[end:]
        except:
            args = ''
        return tag, args
  

def create_new_alias_string(xargs):
    """ Creates the alias string, then determines the homedir, aliasfile and writes the addition """
    
    lengthof_args = len(xargs)
    
    if lengthof_args == '1':
        print("command string not given")
        show_help()
    else:
        my_command_list = xargs.split(" ")
        
        alias_name = my_command_list[1]
        
        alias_string = " ".join(my_command_list[2:])
        
        #actual string to be added to alias file
        alias_addition = f"alias {alias_name}='{alias_string}'"


        #get the home dir files
        home_files = get_home_directory()
        
        # determines the alias location
        myfile = check_aliases(home_files)


        #creates the alias string
        username = os.getlogin()
        
        my_alias_file = f"/home/{username}/{myfile}"

        # check if it already exists, exits if so
        currents = get_current_aliases_aslist()
        
        if alias_addition in currents:
            print("alias already exists!")
            exit()
        else:
            # write it out
            wfile = open(my_alias_file, 'a')
            wfile.write(alias_addition)
            wfile.write("\n")
            wfile.close()
            
            #update user
            os.system(f"source {my_alias_file}")
            print(f"{alias_name} \033[32mwritten to\033[0m {my_alias_file}")



def decide_fate(tag, arguments):

    if tag == 'aliases.py list' or tag == 'aliases.py show':
        display_aliases()
    elif tag == 'aliases.py help':
        show_help()
    elif tag == 'aliases.py add':
        create_new_alias_string(arguments)
    elif tag == 'aliases.py show':
        pass
    else:
        show_help()


if __name__ == '__main__':
    t, a =  match_command()
    decide_fate(t, a)
    exit()
