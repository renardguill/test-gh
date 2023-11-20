import os
import json
import glob
from types import SimpleNamespace
from github import Github
from github import Auth
from git import Repo

# convert json string from env variable GITHUB_CONTEXT to object
github_context = json.loads(os.environ.get('GITHUB_CONTEXT'), object_hook=lambda d: SimpleNamespace(**d))


clusters_matrix = {}
max_parallel = 3
# GetEnvironmentString("GITHUB_EVENT_NAME") == "pull_request"
if github_context.event_name == "pull_request":
    print("pull request")
    max_parallel = 1
    # using an access token
    auth = Auth.Token(github_context.token)
    # Public Web Github
    github_api = Github(auth=auth)
    github_repo = github_api.get_repo(github_context.repository)
    pr = github_repo.get_pull(github_context.event.number)
    print("pr files:")
    for file in pr.get_files():
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            file_name = file.filename
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id, "ManifestPath": file_name + " in base ref: " + github_context.base_ref, "ChangeType": "Create"}]
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id, "ManifestPath": file_name + " in head ref: " + github_context.head_ref, "ChangeType": "Update"}]
            print(file.status + " " + file.filename)
    print("commit files:")
    commit = github_repo.get_commit(sha=github_context.sha)
    for file in commit.files:
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            file_name = file.filename
            # clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id, "ManifestPath": file_name, "ChangeType": "CreateOrUpdate"}]
            print(file.status + " " + file.filename)
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
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file_name.replace("clusters/", "").replace("/", "-").replace(".yaml", ""), "ManifestPath": file_name, "ChangeType": "CreateOrUpdate"}]

clustersMatrixString = json.dumps(clusters_matrix).strip().replace(" ", "")
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("max-parallel=" + max_parallel + "\n")
    f.write("clusters-matrix=" + clustersMatrixString)