## Autocomplete Cheat Sheets 

acs is a fork of [https://raw.githubusercontent.com/cheat/cheat/cheat-python](https://raw.githubusercontent.com/cheat/cheat/cheat-python) which add the autocompletion feature

### Principe of Cheat 
`cheat` allows you to create and view interactive cheatsheets on the
command-line. It was designed to help remind \*nix system administrators of
options for commands that they use frequently, but not frequently enough to
remember.

![The obligatory xkcd](http://imgs.xkcd.com/comics/tar.png 'The obligatory xkcd')


## Installation and first run

### Debian

    $ su // or sudo su
    # git clone https://github.com/Marcel-Brouette/acs.git /opt/acs/ 
    # ln -s /opt/acs/acs.py /usr/local/bin/acs
    # chown root:root /usr/local/bin/acs /opt/acs/acs.py
    # chmod 555 /usr/local/bin/acs /opt/acs/acs.py

    # apt update
    # apt install python python-pip xclip bash-completion python-pyperclip python-argcomplete python-args
    # activate-global-python-argcomplete

    // bash_completion must be run by your user's .bashrc
    // run a new terminal in order to enable the python completion

    $ acs

### Enable completion on zsh

    // in .zsh file : 
    autoload bashcompinit
    bashcompinit
    eval "$(register-python-argcomplete /usr/local/bin/acs)"

## Usage

        acs  cheatsheet  Display the cheatsheet
        acs  -h          Help
        acs  -e E_SHEET  Create or edit a cheatsheet
        acs  -d D_SHEET  Delete a cheatsheet.
        acs  -l          List cheatsheets and paths
        acs  -s KEYWORD  Search for <keyword> in cheatsheets content.




