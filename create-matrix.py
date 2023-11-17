import os
import json

cluster_matrix = {
    "include": [ 
        {"name": "cluster-1", "manifestPath": "cluster-1.yaml",},
        {"name": "cluster-2", "manifestPath": "cluster-2.yaml",},
        {"name": "cluster-3", "manifestPath": "cluster-3.yaml",},
    ],
}

with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("clusters-matrix=" + json.dumps(cluster_matrix).strip().replace(" ", ""))
