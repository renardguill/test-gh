import os
import sys
from glob import glob

import github_action_utils as gha_utils
import yaml

if len(sys.argv) < 2:
    gha_utils.error("No arguments passed")
    exit(1)

if len(sys.argv) > 2:
    gha_utils.error("Too many arguments passed")
    exit(1)

if sys.argv[1] == '--check-files-names':
    for file in glob('clusters/**/*.yaml'):
        with open(file, 'r') as yaml_file:
            cluster = yaml.safe_load(yaml_file)
        file_name = os.path.basename(file)
        if file_name.replace(".yaml", "") != cluster['name']:
            gha_utils.error("File " + file_name + " does not match cluster name: " + cluster['name'], "check-files-names", file)
            exit(1)