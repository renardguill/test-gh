import os
import json
from types import SimpleNamespace
from github import Github
from github import Auth
from github import PullRequest

clusters_matrix = {
    "include": [ 
        {"ClusterName": "cluster-1", "ManifestPath": "cluster-1.yaml",},
        {"ClusterName": "cluster-2", "ManifestPath": "cluster-2.yaml",},
        {"ClusterName": "cluster-3", "ManifestPath": "cluster-3.yaml",},
    ],
}

# clustersMatrixString = json.dumps(clusters_matrix).strip().replace(" ", "")
# with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
#     f.write("max-parallel=3" + "\n")
#     f.write("clusters-matrix=" + clustersMatrixString)


# get string content of file context.json
with open("context.json") as f:
    context = f.read()

# convert json string from file context.json to object
context = json.loads(context, object_hook=lambda d: SimpleNamespace(**d))
print("context:")
print(context)


# convert json string from env variable GITHUB_CONTEXT to object
github = json.loads(os.environ.get('GITHUB_CONTEXT'), object_hook=lambda d: SimpleNamespace(**d))
print("diff_url:")
print(github.event.pull_request.diff_url)


# using an access token
auth = Auth.Token(os.environ.get('GITHUB_TOKEN'))
# Public Web Github
g = Github(auth=auth)
repo = g.get_repo(github.repository)
pr = repo.get_pull(github.event.number)
print("pr files:")
for file in pr.get_files():
    print(file.filename)


print("GITHUB_ENV:")
# print content of file in env variable GITHUB_ENV
with open(os.environ.get('GITHUB_ENV')) as f:
    print(f.read())