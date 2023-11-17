import os
import json

clusters_matrix = {
    "include": [ 
        {"name": "cluster-1", "manifestPath": "cluster-1.yaml",},
        {"name": "cluster-2", "manifestPath": "cluster-2.yaml",},
        {"name": "cluster-3", "manifestPath": "cluster-3.yaml",},
    ],
}

clustersMatrixString = json.dumps(clusters_matrix).strip().replace(" ", "")
print(clustersMatrixString)
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("clusters-matrix=" + clustersMatrixString)
