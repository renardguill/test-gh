import json
import os
from types import SimpleNamespace

import github_action_utils as gha_utils
from github import Auth, GithubIntegration

repository_owner = os.environ.get("GITHUB_REPOSITORY_OWNER")
repository_fullname = os.environ.get("GITHUB_REPOSITORY")
repository_name = os.path.basename(repository_fullname)

app_id = os.environ.get("GITHUB_APP_ID")
private_key = os.environ.get("GITHUB_APP_PRIVATE_KEY")

app_auth = Auth.AppAuth(app_id, private_key)
github_intergration = GithubIntegration(auth=app_auth)
installation = github_intergration.get_repo_installation(repository_owner, repository_name)
github_api = installation.get_github_for_installation()

github_repo = github_api.get_repo(repository_fullname)

clusters_matrix = json.loads(json.loads(os.environ.get("CLUSTERS_MATRIX")), object_hook=lambda d: SimpleNamespace(**d))
for cluster in clusters_matrix.include:
    if cluster.ClusterName.endswith("_tmp"):
        github_repo.delete_environment(cluster.ClusterName)
        gha_utils.notice(message="deleted environment: " + cluster.ClusterName, title="Delete environments")
