#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete
import os
import sys
import subprocess
import re
from sys import argv
from sys import stderr
from os.path import expanduser

app_name               = 'acs'
default_sheets_path    = expanduser("~") + f"/.{app_name}/"
regex_valid_sheet_name =  r'^([a-zA-Z\-\_\.0-9\/])+$'
description            = '########## Autocomplete Cheat Sheets #########'

##########################################################
################## ARGUMENTS SETTINGS ####################
##########################################################

def load_arguments():
    global args_parser

    args_parser = argparse.ArgumentParser(prog=app_name,add_help=False)
    args_parser.add_argument('cheatsheet', nargs='?', help="Display the cheatsheet").completer = autocomplete_sheet
    args_parser.add_argument('-h', dest='help', action='store_true', help="Help")
    args_parser.add_argument('-e', dest='e_sheet', help="Create or edit a cheatsheet").completer = autocomplete_sheet
    args_parser.add_argument('-d', dest='d_sheet', help="Delete a cheatsheet.").completer = autocomplete_sheet
    args_parser.add_argument('-l', dest='list', action='store_true', help="List cheatsheets and paths")
    args_parser.add_argument('-s', dest='keyword', default=argparse.SUPPRESS, help="Search for <keyword> in cheatsheets content.")
    argcomplete.autocomplete(args_parser, False)

######################################################
################# UTIL FUNCTIONS 
######################################################


def die(msg):
    stderr.write(msg + "\n")
    exit(1)

def TODO() : 
    print("TODO")

##############  CUSTOM HELP ##############

def print_help():
    header        = "\n##############################################\n"
    header       += f"{description}\n\n"
    global_usage  = "usage: \n"
    options_args  = "" 
    cut_help = args_parser.format_help().split('optional arguments:')
    if len(cut_help) > 1: 
        options_args = cut_help[1][:-1].replace('\n', f'\n  {argv[0]}')
    cut_help = cut_help[0].split('positional arguments:')
    if len(cut_help) > 1: 
        pos_args = cut_help[1][:-2].replace('\n', f'\n  {argv[0]}')
    custom_help = header + global_usage + pos_args + options_args + '\n'
    print(custom_help)



##############  functions  ##############

def is_valid_name(sheet):
    return re.match(regex_valid_sheet_name, sheet)

def sheets_path(): 
    return default_sheets_path

def list_sheet_paths():
    """ Assembles a dictionary of cheatsheets as name => file-path """
    cheats = {}

    cheats.update(
        dict([
            (cheat, os.path.join(sheets_path(), cheat))
            for cheat in os.listdir(sheets_path())
            if not cheat.startswith('.')
            and not cheat.startswith('__')
        ])
    )

    return cheats

def list_sheet_name():
    return list(list_sheet_paths().keys())

def autocomplete_sheet(prefix, parsed_args, **kwargs):
    return [sheet for sheet in list_sheet_paths().keys() if prefix in sheet and sheet != '']
    
def editor():
    """ Determines the user's preferred editor """

    # determine which editor to use
    editor = os.environ.get('CHEAT_EDITOR') \
        or os.environ.get('VISUAL')         \
        or os.environ.get('EDITOR')         \
        or False

    # assert that the editor is set
    if editor == False:
        die(
            'You must set a CHEAT_EDITOR, VISUAL, or EDITOR environment '
            'variable in order to create/edit a cheatsheet.'
        )

    return editor


def open_with_editor(filepath):
    """ Open `filepath` using the EDITOR specified by the environment variables """
    editor_cmd = editor().split()
    try:
        subprocess.call(editor_cmd + [filepath])
    except OSError:
        die('Could not launch ' + editor())


def exists(sheet):
    """ Predicate that returns true if the sheet exists """
    return sheet in list_sheet_paths() and os.access(path(sheet), os.R_OK)

def is_writable(sheet):
    """ Predicate that returns true if the sheet is writeable """
    return sheet in list_sheet_paths() and os.access(path(sheet), os.W_OK)

def path(sheet):
    """ Returns a sheet's filesystem path """
    return os.path.join(sheets_path(), sheet)

def edit(sheet):    
    """ Opens a cheatsheet for editing """
    open_with_editor(path(sheet))

def create(sheet):
    """ Creates a cheatsheet """
    new_sheet_path = os.path.join(sheets_path(), sheet)
    edit(new_sheet_path)


######################################################
################# MAIN FUNCTIONS 
######################################################

def list_sheet() :
    """ Lists the available cheatsheets """
    dict_sheets = list_sheet_paths()
    sheet_list = ''
    pad_length = max([len(x) for x in dict_sheets.keys()]) + 4
    for sheet in sorted(dict_sheets.items()):
        sheet_list += sheet[0].ljust(pad_length) + sheet[1] + "\n"
    return sheet_list

def delete(sheet):
    if not is_valid_name(sheet): 
        die("Invalid character in sheet name")
    if not is_writable(sheet):
        die("The sheet doesn't exist or you don't have enough right")
    resp = input("Are you sure? (Y/n)\n==> ")
    if resp.lower() == "y" or resp == '':
        os.remove(path(sheet))
        print("Sheet successfully deleted !")


def search(needle): 
    """ Searches all cheatsheets for the specified term """
    result = ''
    lowered_term = needle.lower()

    for cheatsheet in sorted(list_sheet_paths().items()):
        match = ''
        for line in open(cheatsheet[1]):
            if lowered_term in line.lower():
                match += '  ' + line

        if match != '':
            result += cheatsheet[0] + ":\n" + match + "\n"

    return result

def create_or_edit(sheet):
    """ Creates or edits a cheatsheet """
    if not is_valid_name(sheet): 
        die("Invalid character in sheet name")
    # if the cheatsheet does not exist
    if not exists(sheet):
        create(sheet)
    # if it exists and is in the default path, then just open itexists_in_default_path
    else:
        edit(sheet)

def read(sheet):
    if not is_valid_name(sheet): 
        die("Invalid character in sheet name")
    """ Returns the contents of the cheatsheet as a String """
    if not exists(sheet):
        die(f'No cheatsheet found for {sheet}')

    with open(path(sheet)) as cheatfile:
        return cheatfile.read()


######################################################
################# MAIN ROUTINE 
######################################################

def run():
    
    load_arguments()
    args = args_parser.parse_args()

    if args.list  :      
        print(list_sheet()) 

    elif "keyword" in args :    
        search(args.keyword) 

    elif args.e_sheet : 
        create_or_edit(args.e_sheet)

    elif args.d_sheet : 
        delete(args.d_sheet)

    elif args.cheatsheet : 
        print(read(args.cheatsheet))
    
    else: 
        print_help()

run()

