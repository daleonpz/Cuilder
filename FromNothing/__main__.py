"""FromNothing Project Builder for Embedded Applications

Usage:
------
    $ FromNothing [options] [id] [id ...]

Create a project for your embedded application:
    $ FromNothing myproject_config.yml
    
Available options are:
-h, --help         Show this help
-f, --file         Project file in YMAL 

Contact:
--------
- https://baremetallics.com

More information is available at:
- https://github.com/daleonpz/FromNothing

Version:
--------
- FromNothing v0.0.1
"""

from FromNothing import *
import sys
import getopt

def parse_arg(argv):
    yml_file = ''
    yml_file_found = False
    try:
        opts, args = getopt.getopt(argv,"hf:",["file="])
    except getopt.GetoptError:
        print('FromNothing -f <project_yaml_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('FromNothing -f <project_yaml_file>')
            sys.exit()
        elif opt in ("-f", "--file"):
            yml_file = arg
            yml_file_found = True

    if yml_file_found: 
        return yml_file
    else:
        print("Not enough arguments...")
        print('FromNothing -f <project_yaml_file>')
        sys.exit(2)

def main():
    yml_file = parse_arg(sys.argv[1:])
    print("yml_file: " + yml_file)
    builder = FromNothing(yml_file)
    builder.new_project()

if __name__ == "__main__":
   main() 
