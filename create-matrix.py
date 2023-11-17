import os
import json
matrix = {
    "include": [ 
        {"cluster": "cluster-1",},
        {"cluster": "cluster-2",},
    ],
}
os.environ["GITHUB_OUTPUT"] = json.dumps(matrix).replace('"', '\\"').replace(" ", "")
