import os
import json
matrix = {
    "include": [ 
        {"cluster": "cluster-1",},
        {"cluster": "cluster-2",},
        {"cluster": "cluster-3",},
    ],
}
os.environ["GITHUB_OUTPUT"] = "matrix=" + json.dumps(matrix).replace('"', '\\"').replace(" ", "")