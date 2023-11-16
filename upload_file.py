import base64
import os
import requests
import uuid
from datetime import datetime


# Environment variables
hostname = os.environ.get("COMPUTERNAME")  # For Windows
if hostname is None:
    hostname = os.environ.get("RUNNER_NAME")  # For GitHub runner

# Base API URL
owner = os.environ.get("OWNER")
repo = os.environ.get("REPO")
api_url = f"https://api.github.com/repos/{owner}/{repo}"

# Set request headers
gh_pat = os.environ.get("GH_PAT")
headers = {
    "Authorization": f"Bearer {gh_pat}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}


# ==========================================================================
# Create new file
content_url = f"{api_url}/contents"
random_number = uuid.uuid4()
filename = f"tests/{random_number}.txt"
content = f"{random_number} - I am a test"
base64_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
post_req_body = {
    "message": f"Create {random_number}.txt - {hostname}",
    "content": base64_content
}

r = requests.put(url=f"{content_url}/{filename}",
                 headers=headers,
                 json=post_req_body)
date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
assert r.status_code == 201
file_sha = r.json().get("content").get("sha")
assert file_sha is not None
print(f"{date} UTC - File {random_number}.txt has been created.")
