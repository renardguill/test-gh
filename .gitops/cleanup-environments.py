import os
import json
from types import SimpleNamespace
from github import Github
from github import Auth

# convert GITHUB_CONTEXT to object
github_context = json.loads(os.environ.get('GITHUB_CONTEXT'), object_hook=lambda d: SimpleNamespace(**d))

auth = Auth.Token(github_context.token)
github_api = Github(auth=auth)
github_repo = github_api.get_repo(github_context.repository)

# for environment in github_repo.get_environments():
#     if environment.name.endswith("_tmp"):
#         github_repo.delete_environment(environment.id)

clusters_matrix = json.loads(os.environ.get('CLUSTERS_MATRIX'), object_hook=lambda d: SimpleNamespace(**d))
for cluster in clusters_matrix:
    if cluster.ClusterName.endswith("_tmp"):
        environmentId = github_repo.get_environment(cluster.ClusterName).id
        github_repo.delete_environment(environmentId)