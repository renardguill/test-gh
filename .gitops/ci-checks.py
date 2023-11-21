import os
import sys
import yaml
from glob import glob

if len(sys.argv) < 2:
    print("No arguments passed")
    sys.exit(1)

if len(sys.argv) > 2:
    print("Too many arguments passed")
    sys.exit(1)

if sys.argv[1] == '--check-files-names':
    for file in glob('clusters/**/*.yaml'):
        with open(file, 'r') as yaml_file:
            cluster = yaml.safe_load(yaml_file)
        file_name = os.path.basename(file)
        if file_name.replace(".yaml", "") != cluster['name']:
            print("File " + file_name + " does not match cluster name: " + cluster['name'])
            sys.exit(1)