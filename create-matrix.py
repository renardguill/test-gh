import os
import json

clusters_matrix = {
    "include": [ 
        {"ClusterName": "cluster-1", "ManifestPath": "cluster-1.yaml",},
        {"ClusterName": "cluster-2", "ManifestPath": "cluster-2.yaml",},
        {"ClusterName": "cluster-3", "ManifestPath": "cluster-3.yaml",},
    ],
}

clustersMatrixString = json.dumps(clusters_matrix).strip().replace(" ", "")
print(clustersMatrixString)
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("max-parallel=3" + "\n")
    f.write("clusters-matrix=" + clustersMatrixString)
