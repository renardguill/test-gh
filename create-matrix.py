import os
import json
import glob
from types import SimpleNamespace
from github import Github
from github import Auth


files = glob.glob("clusters/**/*.yaml", recursive=True)
for file in files:
    print(file)

# convert json string from env variable GITHUB_CONTEXT to object
github_context = json.loads(os.environ.get('GITHUB_CONTEXT'), object_hook=lambda d: SimpleNamespace(**d))


clusters_matrix = {}
# GetEnvironmentString("GITHUB_EVENT_NAME") == "pull_request"
if github_context.event_name == "pull_request":
    print("pull request")
    # using an access token
    auth = Auth.Token(github_context.token)
    # Public Web Github
    github_api = Github(auth=auth)
    repo = github_api.get_repo(github_context.repository)
    pr = repo.get_pull(1)
    print("pr files:")
    for file in pr.get_files():
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            file_name = file.filename
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", ""), "ManifestPath": file_name}]
            print(file)
else:
    print("not a pull request")
    for file_name in glob.glob("clusters/**/*.yaml", recursive=True):
        print(file_name)
        clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", ""), "ManifestPath": file_name}]

    print(github_context)

clustersMatrixString = json.dumps(clusters_matrix).strip().replace(" ", "")
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("max-parallel=3" + "\n")
    f.write("clusters-matrix=" + clustersMatrixString)