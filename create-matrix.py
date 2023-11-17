import os
import json
matrix = {
    "include": [ 
        {"cluster": "cluster-1",},
        {"cluster": "cluster-2",},
    ],
}
print("matrix=" + json.dumps(matrix).replace('"', '\\"').replace(" ", ""))
