import os
import json

matrix = {
    "include": [ 
        {"cluster": "cluster-1",},
        {"cluster": "cluster-2",},
    ],
}

with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("matrix=" + json.dumps(matrix).strip().replace(" ", ""))
