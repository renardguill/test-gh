import json
matrix = {
    "include": [ 
        {"cluster": "cluster-1",},
        {"cluster": "cluster-2",},
        {"cluster": "cluster-3",},
    ],
}
print("::set-output name=matrix::" + json.dumps(matrix))