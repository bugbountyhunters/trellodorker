# Trellodorker
A tool developed to automate part of the Trello dorking process.

Trellodorker is a command-line tool. It automatically Google-dorks for public Trello boards, then fetches all members of the first 10 exposed boards, and returns all of the boards that those members are on. By doing this, you are able to access boards that are public, but may not be indexed by Google.

## Installation

To install, just use the following commands.

`git clone https://github.com/bugbountyhunters/trellodorker.git`

`cd trellodorker`

And you should be good to go.

## Usage

To run this, you need a file called `creds.txt` in the same directory. This file must contain your Trello API key on the first line, and your Trello token on the second line.
You also need to install the Python Google module using `pip install google`. If you have trouble installing the Google module, figure it out yourself.

### Using the tool

The `-i` flag specifies your initial dork, such as `example.com`. The `-o` flag specifies the output, such as `output.txt`. Finally, the optional flag `-a` lets you add additional arguments to your inital dork. 

### Examples

The following dorks for Trello boards mentioning `example.com`.

`python trellodorker.py -i example.com -o output.txt`

The following dorks for Trello boards mentioning `example.com` that also mention "admin" and "password".

`python trellodorker.py -i example.com -o output.txt -a admin,password`

The tool fetches all boards matching those conditions, then fetches every member of each board. It then fetches all boards that those members are on, and writes the name and URL of each board to your specified output file.
