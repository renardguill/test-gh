import os
import json
from types import SimpleNamespace
from github import Github
from github import Auth

auth = Auth.Token(os.environ.get('GITHUB_TOKEN'))
github_api = Github(auth=auth)
github_repo = github_api.get_repo(os.environ.get('GITHUB_REPOSITORY'))

# for environment in github_repo.get_environments():
#     if environment.name.endswith("_tmp"):
#         github_repo.delete_environment(environment.id)
print("CLUSTERS_MATRIX:")
print(os.environ.get('CLUSTERS_MATRIX'))
print("CLUSTERS_MATRIX.replace:")
print(os.environ.get('CLUSTERS_MATRIX').replace('\\', ''))

clusters_matrix = json.loads(os.environ.get('CLUSTERS_MATRIX'), object_hook=lambda d: SimpleNamespace(**d))
print("clusters_matrix:")
print(clusters_matrix)
for cluster in clusters_matrix.include:
    if cluster.ClusterName.endswith("_tmp"):
        environmentId = github_repo.get_environment(cluster.ClusterName).id
        github_repo.delete_environment(environmentId)