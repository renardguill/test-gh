import os
import json
from types import SimpleNamespace
from github import Github
from github import Auth

# convert GITHUB_CONTEXT to object
github_context = json.loads(os.environ.get('GITHUB_CONTEXT'), object_hook=lambda d: SimpleNamespace(**d))


update_clusters_matrix = { "include": []}
create_clusters_matrix = { "include": []}
max_parallel = 6
is_ephemeral = True

auth = Auth.Token(github_context.token)
github_api = Github(auth=auth)
github_repo = github_api.get_repo(github_context.repository)


if github_context.event_name == "pull_request":
    print("pull request")
    max_parallel = 5
    pr = github_repo.get_pull(github_context.event.number)
    print("pr files:")
    for file in pr.get_files():
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            print(file.status)
            if file.status == "added":
                print("added cluster files:")
                print(file.filename)
                content = pr.head.repo.get_contents(file.filename, ref=github_context.head_ref)
                download_url = content.download_url
                create_clusters_matrix['include'] = create_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "_") + github_context.run_id, "ManifestUrl": download_url, "ChangeType": "Create"}]
            if file.status == "modified":
                print("modified cluster files:")
                print(file.filename)
                print("Get previous_contents:")
                previous_content = pr.base.repo.get_contents(file.filename, ref=github_context.base_ref)
                download_url = previous_content.download_url
                create_clusters_matrix['include'] = create_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "_") + github_context.run_id, "ManifestUrl": download_url, "ChangeType": "Create"}]
                content = pr.head.repo.get_contents(file.filename, ref=github_context.head_ref)
                download_url = content.download_url
                update_clusters_matrix['include'] = update_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "_") + github_context.run_id, "ManifestUrl": download_url, "ChangeType": "Update"}]
            if file.status == "deleted":
                print("deleted cluster files:")
                print(file.filename)
                print("delete cluster is not allowed")
elif github_context.event_name == "push":
    print("On tag")
    is_ephemeral = False
    commit = github_repo.get_commit(sha=github_context.sha)
    print("commit files:")
    for file in commit.files:
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            if file.status == "added" or file.status == "modified":
                content = github_repo.get_contents(file.filename, ref=github_context.ref)
                download_url = content.download_url
            if file.status == "added":
                print("added cluster files:")
                print(file.filename)
                create_clusters_matrix['include'] = create_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "_") + github_context.run_id, "ManifestUrl": download_url, "ChangeType": "Create"}]
            if file.status == "modified":
                print("modified cluster files:")
                print(file.filename)
                update_clusters_matrix['include'] = update_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "_") + github_context.run_id, "ManifestUrl": download_url, "ChangeType": "Update"}]
            if file.status == "deleted":
                print("deleted cluster files:")
                print(file.filename)
                print("delete cluster is not allowed")
else:
    print("Not supported event")
    exit(1)

# Set Github Output
createClustersMatrixString = json.dumps(create_clusters_matrix).strip().replace(" ", "")
updateClustersMatrixString = json.dumps(update_clusters_matrix).strip().replace(" ", "")
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("max-parallel=" + str(max_parallel))
    f.write("\n")
    f.write("create-clusters-matrix=" + createClustersMatrixString)
    f.write("\n")
    f.write("update-clusters-matrix=" + updateClustersMatrixString)
    f.write("\n")
    f.write("is-ephemeral=" + str(is_ephemeral).lower())
    f.write("\n")
    f.write("need-create-clusters=" + str(len(create_clusters_matrix['include']) > 0).lower())
    f.write("\n")
    f.write("need-update-clusters=" + str(len(update_clusters_matrix['include']) > 0).lower())
