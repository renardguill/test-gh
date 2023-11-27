import json
import os
from types import SimpleNamespace

import github_action_utils as gha_utils
from github import Auth, Github

github_context = json.loads(os.environ.get("GITHUB_CONTEXT"), object_hook=lambda d: SimpleNamespace(**d))


dryrun_clusters_matrix = {"include": []}
create_clusters_matrix = {"include": []}
update_clusters_matrix = {"include": []}
max_parallel = 6
is_ephemeral = True

auth = Auth.Token(github_context.token)
github_api = Github(auth=auth)
github_repo = github_api.get_repo(github_context.repository)


if github_context.event_name == "pull_request":
    pr = github_repo.get_pull(github_context.event.number)
    for file in pr.get_files():
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            cluster_name = os.path.basename(file.filename).replace(".yaml", "")
            ephemeral_cluster_name = cluster_name + "_" + github_context.run_id + "_tmp"
            if file.status == "added":
                gha_utils.notice(message=ephemeral_cluster_name + " need to be created", title="Added cluster", file=file.filename)
                content = pr.head.repo.get_contents(file.filename, ref=github_context.head_ref)
                dryrun_clusters_matrix["include"] = dryrun_clusters_matrix.get("include", []) + [{"ClusterName": cluster_name, "ManifestUrl": content.download_url, "ChangeType": "Create"}]
                create_clusters_matrix["include"] = create_clusters_matrix.get("include", []) + [{"ClusterName": ephemeral_cluster_name, "ManifestUrl": content.download_url, "ChangeType": "Create"}]
            if file.status == "modified":
                gha_utils.notice(message=ephemeral_cluster_name + " need to be updated", title="Modified cluster", file=file.filename)
                previous_content = pr.base.repo.get_contents(file.filename, ref=github_context.base_ref)
                dryrun_clusters_matrix["include"] = dryrun_clusters_matrix.get("include", []) + [{"ClusterName": cluster_name, "ManifestUrl": previous_content.download_url, "ChangeType": "Create"}]
                create_clusters_matrix["include"] = create_clusters_matrix.get("include", []) + [{"ClusterName": ephemeral_cluster_name, "ManifestUrl": previous_content.download_url, "ChangeType": "Create"}]
                content = pr.head.repo.get_contents(file.filename, ref=github_context.head_ref)
                update_clusters_matrix["include"] = update_clusters_matrix.get("include", []) + [{"ClusterName": ephemeral_cluster_name, "ManifestUrl": content.download_url, "ChangeType": "Update"}]
            if file.status == "deleted":
                gha_utils.notice(message=ephemeral_cluster_name + " need to be deleted", title="Deleted cluster", file=file.filename)
                gha_utils.warning("Delete cluster is not allowed", "Deleted cluster", file.filename)
elif github_context.event_name == "push":
    is_ephemeral = False
    commit = github_repo.get_commit(sha=github_context.sha)
    for file in commit.files:
        if file.filename.startswith("clusters/") and file.filename.endswith(".yaml"):
            cluster_name = os.path.basename(file.filename).replace(".yaml", "")
            if file.status == "added" or file.status == "modified":
                content = github_repo.get_contents(file.filename, ref=github_context.ref)
            if file.status == "added":
                gha_utils.notice(message=cluster_name + " need to be created", title="Added cluster", file=file.filename)
                create_clusters_matrix["include"] = create_clusters_matrix.get("include", []) + [{"ClusterName": cluster_name, "ManifestUrl": content.download_url, "ChangeType": "Create"}]
            if file.status == "modified":
                gha_utils.notice(message=cluster_name + " need to be updated", title="Modified cluster", file=file.filename)
                update_clusters_matrix["include"] = update_clusters_matrix.get("include", []) + [{"ClusterName": cluster_name, "ManifestUrl": content.download_url, "ChangeType": "Update"}]
            if file.status == "deleted":
                gha_utils.notice(message=cluster_name + " need to be deleted", title="Deleted cluster", file=file.filename)
                gha_utils.warning("Delete cluster is not allowed", "delete-cluster", file.filename)
else:
    gha_utils.error("Not supported event: " + github_context.event_name)
    exit(1)

# Set Github Outputs
gha_utils.set_output("max-parallel", str(max_parallel))
gha_utils.set_output("create-clusters-matrix", json.dumps(create_clusters_matrix))
gha_utils.set_output("update-clusters-matrix", json.dumps(update_clusters_matrix))
gha_utils.set_output("dryrun-clusters-matrix", json.dumps(dryrun_clusters_matrix))
gha_utils.set_output("is-ephemeral", str(is_ephemeral).lower())
gha_utils.set_output("need-create-clusters", str(len(create_clusters_matrix["include"]) > 0).lower())
gha_utils.set_output("need-update-clusters", str(len(update_clusters_matrix["include"]) > 0).lower())
gha_utils.set_output("need-dryrun-clusters", str(len(dryrun_clusters_matrix["include"]) > 0).lower())

