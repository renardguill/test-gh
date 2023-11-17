import os
import json
matrix = {
    "include": [ 
        {"cluster": "cluster-1",},
        {"cluster": "cluster-2",},
    ],
}
github_output = os.environ.get('GITHUB_OUTPUT')

# append to the existing out file
if github_output:
    with open(github_output, 'a') as f:
        f.write("matrix=" + json.dumps(matrix).replace(" ", ""))
