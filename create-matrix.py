import os
import json
from types import SimpleNamespace
from github import Github
from github import Auth

# convert GITHUB_CONTEXT to object
github_context = json.loads(os.environ.get('GITHUB_CONTEXT'), object_hook=lambda d: SimpleNamespace(**d))


create_or_update_clusters_matrix = { "include": []}
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
            if file.status != "added":
                print("previous_contents:")
                previous_contents = pr.base.repo.get_contents(file.filename, ref=github_context.base_ref)
                print(previous_contents)
                previous_download_url = previous_contents.download_url
                print(previous_download_url)
                create_clusters_matrix['include'] = create_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id, "ManifestPath": previous_download_url, "ChangeType": "Create"}]

            print("new_contents:")
            new_contents = pr.head.repo.get_contents(file.filename, ref=github_context.head_ref)
            print(new_contents)
            new_download_url = new_contents.download_url
            print(new_download_url)
            create_or_update_clusters_matrix['include'] = create_or_update_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", "-") + github_context.run_id, "ManifestPath": new_download_url, "ChangeType": "CreateOrUpdate"}]
else:
    print("On tag")
    is_ephemeral = False
    commit = github_repo.get_commit(sha=github_context.sha)
    print("commit files:")
    for file in commit.files:
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            create_or_update_clusters_matrix['include'] = create_or_update_clusters_matrix.get('include', []) + [{"ClusterName": file.filename.replace("clusters/", "").replace("/", "-").replace(".yaml", ""), "ManifestPath": file.filename, "ChangeType": "CreateOrUpdate"}]
            print(file.status + " " + file.filename)

# Set Github Output
createClustersMatrixString = json.dumps(create_clusters_matrix).strip().replace(" ", "")
createOrUpdateClustersMatrixString = json.dumps(create_or_update_clusters_matrix).strip().replace(" ", "")
with open(os.environ.get('GITHUB_OUTPUT'), 'a') as f:
    f.write("max-parallel=" + str(max_parallel))
    f.write("\n")
    f.write("create-clusters-matrix=" + createClustersMatrixString)
    f.write("\n")
    f.write("create-or-update-clusters-matrix=" + createOrUpdateClustersMatrixString)
    f.write("\n")
    f.write("is-ephemeral=" + str(is_ephemeral).lower())

print(json.dumps(create_or_update_clusters_matrix, indent=4))