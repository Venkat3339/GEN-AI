import os
import requests

class GitHubClient:
    def __init__(self, token: str | None = None):
        self.base_url = "https://api.github.com"
        self.session = requests.Session()

        if token is None:
            token = os.getenv("")

        if token:
            self.session.headers.update({
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json"
            })

    def get_user(self, username: str):
        url = f"{self.base_url}/users/{username}"
        resp = self.session.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()

    def create_repo(self, name: str, private: bool = True):
        url = f"{self.base_url}/user/repos"
        payload = {"name": name, "private": private}
        resp = self.session.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        return resp.json()

# ------------------------ CALL HERE ------------------------
if __name__ == "__main__":
    client = GitHubClient(token="")

    # 1. Fetch user info
    user = client.get_user("octocat")
    print(user)

    # 2. Create a repo (uncomment to test)
    # repo = client.create_repo("my-new-auto-repo")
    # print(repo)
