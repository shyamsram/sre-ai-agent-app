# mcp_github_client.py

import requests
import os
from dotenv import load_dotenv

class MCPGithubClient:
    def __init__(self, api_url="https://api.github.com"):
        load_dotenv()
        self.api_url = api_url
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def get_user(self):
        url = f"{self.api_url}/user"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_repos(self, username=None):
        if not username:
            user = self.get_user()
            username = user["login"]
        url = f"{self.api_url}/users/{username}/repos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_repo_issues(self, owner, repo):
        url = f"{self.api_url}/repos/{owner}/{repo}/issues"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
