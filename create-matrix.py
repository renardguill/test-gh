import os
import json
from types import SimpleNamespace
from github import Github
from github import Auth

# convert json string from env variable GITHUB_CONTEXT to object
github_context = json.loads(os.environ.get('GITHUB_CONTEXT'), object_hook=lambda d: SimpleNamespace(**d))

# GetEnvironmentString("GITHUB_EVENT_NAME") == "pull_request"
if github_context.event.name == "pull_request":
    # using an access token
    auth = Auth.Token(github_context.token)
    # Public Web Github
    github_api = Github(auth=auth)
    repo = github_api.get_repo(github_context.repository)
    pr = repo.get_pull(1)
    print("pr files:")
    for file in pr.get_files():
        print(file)


clusters_matrix = {
    "include": [ 
        {"ClusterName": "cluster-1", "ManifestPath": "cluster-1.yaml",},
        {"ClusterName": "cluster-2", "ManifestPath": "cluster-2.yaml",},
        {"ClusterName": "cluster-3", "ManifestPath": "cluster-3.yaml",},
    ],
}
clustersMatrixString = json.dumps(clusters_matrix).strip().replace(" ", "")
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("max-parallel=3" + "\n")
    f.write("clusters-matrix=" + clustersMatrixString)