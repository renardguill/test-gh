import os
import json
from types import SimpleNamespace
from github import Github
from github import Auth

# convert json string from env variable GITHUB_CONTEXT to object
github_context = json.loads(os.environ.get('GITHUB_CONTEXT'), object_hook=lambda d: SimpleNamespace(**d))


clusters_matrix = {}
ephemeral_clusters_matrix = {}
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
            if file.status != "added":
                print("previous_contents:")
                previous_contents = pr.base.repo.get_contents(file.filename, ref=github_context.base_ref)
                previous_download_url = previous_contents.download_url
                print(previous_download_url)
                ephemeral_clusters_matrix['include'] = ephemeral_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id, "ManifestPath": previous_download_url, "ChangeType": "Update"}]

            print("new_contents:")
            new_contents = pr.head.repo.get_contents(file.filename, ref=github_context.head_ref)
            new_download_url = new_contents.download_url
            print(new_download_url)
            ephemeral_clusters_matrix['include'] = ephemeral_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id, "ManifestPath": new_download_url, "ChangeType": "CreateOrUpdate"}]
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
ephemeralClustersMatrixString = json.dumps(ephemeral_clusters_matrix).strip().replace(" ", "")
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("max-parallel=" + str(max_parallel))
    f.write("\n")
    f.write("clusters-matrix=" + clustersMatrixString)
    f.write("\n")
    f.write("ephemeral-clusters-matrix=" + ephemeralClustersMatrixString)