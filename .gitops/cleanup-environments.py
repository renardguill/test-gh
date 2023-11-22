import os
import json
from types import SimpleNamespace
from github import Github
from github import Auth

auth = Auth.Token(os.environ.get("GITHUB_TOKEN"))
github_api = Github(auth=auth)
github_repo = github_api.get_repo(os.environ.get("GITHUB_REPOSITORY"))

# for environment in github_repo.get_environments():
#     if environment.name.endswith("_tmp"):
#         github_repo.delete_environment(environment.name)

clusters_matrix = json.loads(os.environ.get("CLUSTERS_MATRIX"))
clusters_matrix = json.loads(clusters_matrix, object_hook=lambda d: SimpleNamespace(**d))
print(clusters_matrix)
for cluster in clusters_matrix.include:
    if cluster.ClusterName.endswith("_tmp"):
        github_repo.delete_environment(cluster.ClusterName)
