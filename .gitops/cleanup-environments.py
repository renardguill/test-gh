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

clusters_matrix = json.loads(os.environ.get('CLUSTERS_MATRIX'), object_hook=lambda d: SimpleNamespace(**d))
print("clusters_matrix:")
print(clusters_matrix)