import os
import json
import glob
from types import SimpleNamespace
from github import Github
from github import Auth
from git import Repo

git_repo = Repo(".")
commit = git_repo.commit("main")
for item in git_repo.index.diff(None):
    print(item.a_path)
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
    github_repo = github_api.get_repo(github_context.repository)
    pr = github_repo.get_pull(1)
    print("pr files:")
    for file in pr.get_files():
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            file_name = file.filename
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id + "-1", "ManifestPath": file_name + "in base ref: " + github_context.event.base_ref}]
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id + "-2", "ManifestPath": file_name + "in head ref: " + github_context.event.head_ref}]
            print(file)
else:
    # print("not a pull request")
    # for file_name in glob.glob("clusters/**/*.yaml", recursive=True):
    #     print(file_name)
    #     clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", ""), "ManifestPath": file_name}]
    git_repo = Repo(github_context.workspace)
    commit = git_repo.commit(github_context.ref_name)
    for item in git_repo.index.diff(None):
        print(item.a_path)
        if item.a_path.startswith("clusters/") and item.a_path.endswith(".yaml"):
            file_name = item.a_path
            print(file_name)
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", ""), "ManifestPath": file_name}]

clustersMatrixString = json.dumps(clusters_matrix).strip().replace(" ", "")
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("max-parallel=3" + "\n")
    f.write("clusters-matrix=" + clustersMatrixString)