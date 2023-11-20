import os
import json
from types import SimpleNamespace
from github import Github
from github import Auth

# convert json string from env variable GITHUB_CONTEXT to object
github_context = json.loads(os.environ.get('GITHUB_CONTEXT'), object_hook=lambda d: SimpleNamespace(**d))


clusters_matrix = {}
max_parallel = 3

# using an access token
auth = Auth.Token(github_context.token)
# Public Web Github
github_api = Github(auth=auth)
github_repo = github_api.get_repo(github_context.repository)


if github_context.event_name == "pull_request":
    print("pull request")
    max_parallel = 1
    pr = github_repo.get_pull(github_context.event.number)
    print("pr files:")
    for file in pr.get_files():
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):

            print("contents_url: " + file.contents_url)
            print("contents" + pr.head.repo.get_contents(file.filename, ref=github_context.head_ref))
            print("previous_contents: " + pr.base.repo.get_contents(file.filename, ref=github_context.base_ref))
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id, "ManifestPath": file.filename + " in base ref: " + github_context.base_ref, "ChangeType": "Create"}]
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id, "ManifestPath": file.filename + " in head ref: " + github_context.head_ref, "ChangeType": "Update"}]
else:
    print("On tag")
    commit = github_repo.get_commit(sha=github_context.sha)
    print("commit files:")
    for file in commit.files:
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            clusters_matrix['include'] = clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", ""), "ManifestPath": file.filename, "ChangeType": "CreateOrUpdate"}]
            print(file.status + " " + file.filename)

# Set Github Output
clustersMatrixString = json.dumps(clusters_matrix).strip().replace(" ", "")
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("max-parallel=" + str(max_parallel) + "\n")
    f.write("clusters-matrix=" + clustersMatrixString)