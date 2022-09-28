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


def get_ALS():
    """ takes no arguments and returns a list of (filename, linenumber, linestring) """
    
    home_dir = get_home_directory()
    
    home_file = check_aliases(home_dir)
    
    flstrings = enumerate_alias_file(home_file)

    return flstrings


def enumerate_alias_file(target):
    """ returns a list of (alias_file, line_number, alias_string)"""

    username = os.getlogin()

    file_str = f"/home/{username}/{target}"
    
    file = open(file_str,'r')
    
    file_line_strings = []
    
    lines = file.readlines()

    for line_number, alias_string in enumerate(lines):
        
        if alias_string.startswith("alias"):
            file_line_strings.append((target, alias_string, index))

    real_file_line_strings = file_line_strings[4:]

    return real_file_line_strings


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
    except:pass
    try:
        help0 = re.search('aliases.py help', command).span()
        my_option = help0
    except:pass
    try:
        show = re.search('aliases.py show', command).span()
        my_option = show
    except:pass
    try:
        _list = re.search('aliases.py list', command).span()
        my_option = _list
    except:pass
    try:
        edit = re.search('aliases.py edit', command).span()
        my_option = edit
    except:pass
    try:
        delete = re.search('aliases.py delete', command).span()
        my_option = delete
    except:pass
    try:
        update = re.search('aliases.py update', command).span()
        my_option = update
    except:pass

    try:
        doctor = re.search('aliases.py doctor', command).span()
        my_option = doctor
    except:pass

    # add help show list edit delete update doctor
    if my_option == 'x':
        show_help()
        exit()
    else:
        start,end = int(my_option[0]), int(my_option[1])
        tag = command[start:end]
        try:args = command[end:]
        except:args = ''
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


def edit_specific_alias(command, new_name, new_command):
    """ checks your aliases for specific alias <command>, if it exists, returns the fls """

    x = str(command).strip()
    
    x = x + "="

    aliases = get_current_aliases_aslist()
    
    # check for alias
    found = False
    my_alias = ""
    
    for alias in aliases:
        
        if alias.startswith(x):
            found = True
            
            my_alias = alias
    if found == False:
        print("alias not found")
        
        exit()
    else:
        pattern = re.compile(alias)
        
        alias_files = get_home_directory()
        
        afile = check_aliases(alias_files)
        found_lines = []
        for x, line in enumerate(open(afile)):
            
            for match in re.finditer(pattern,line):
                print(int(x), line, match.group())
                found_lines.append(x)
        # read the file
        _file = open(afile,'r')
        _lines = _file.readlines()
        _file.close()
        # remove the lines
        __lines = _lines
        for linenum in found_lines:
            __lines.remove(__lines[int(linenum)])
        new_lines = __lines

        alias_str = f"alias {new_name}='{new_command}'\n"
        new_lines.append(alias_str)
        __file = open(afile,'w')
        for line in new_lines:
            __file.write(line)
        __file.close()

        print(f"alias {command} replaced with {new_name} - {new_command}")


def get_specific_alias(arg):
    """ takes the alias name and returns the string """

    x = str(arg).strip()
    x = x + "="
    my_line = ""
    aliases = get_current_aliases_aslist()
    for line in aliases:
        xline = str(line)
        if xline.startswith(x):
            my_line = xline

    return my_line


def show_specific_alias(arg):
    """ takes the list of arguments and prints the matching alias """


    x = str(arg).strip()
    x = x + "="
    
    aliases = get_current_aliases_aslist()
    for line in aliases:
        xline = str(line)
        if xline.startswith(x):
            print(line)
            return
    
    



def decide_fate(tag, arguments):

    if tag == 'aliases.py list':
        display_aliases()
    elif tag == 'aliases.py help':
        show_help()
    elif tag == 'aliases.py add':
        create_new_alias_string(arguments)
    elif tag == 'aliases.py show':
        show_specific_alias(arguments)
    elif tag == 'aliases.py edit':
        my_alias = edit_specific_alias(arguments)
    elif tag == 'aliases.py delete':
        pass
    elif tag == 'aliases.py update':
        pass
    elif tag == 'aliases.py doctor':
        pass
    else:
        show_help()


if __name__ == '__main__':
    t, a =  match_command()
    decide_fate(t, a)
    exit()
