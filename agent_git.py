import os
import subprocess
from github import Github, GithubException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("⚠️ Please set GITHUB_TOKEN in your .env file")

# Ask user for GitHub username
username = input("Enter your GitHub username: ").strip()

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
try:
    user = g.get_user()
except GithubException as e:
    raise SystemExit(f"❌ Failed to authenticate with GitHub: {e}")

# Detect local folder name as repo name
repo_name = os.path.basename(os.getcwd())
print(f"📂 Detected local folder name as repo: {repo_name}")

# Check if repo exists on GitHub
try:
    repo = user.get_repo(repo_name)
    print(f"✅ Repo '{repo_name}' already exists: {repo.html_url}")
except GithubException:
    print(f"🚀 Creating new repo '{repo_name}'...")
    try:
        repo = user.create_repo(
            name=repo_name,
            description=f"Auto-created repo for {repo_name}",
            private=False  # Change to True if you want private repo
        )
        print(f"✅ Repo created: {repo.html_url}")
    except GithubException as e:
        raise SystemExit(f"❌ Failed to create repo: {e}")

# Initialize Git if not already
if not os.path.exists(".git"):
    subprocess.run(["git", "init"], check=True)
    print("📌 Initialized Git repository locally.")

# Add remote origin if not exists
try:
    remotes = subprocess.check_output(["git", "remote"]).decode().splitlines()
    if "origin" not in remotes:
        subprocess.run(["git", "remote", "add", "origin", repo.clone_url], check=True)
        print(f"📌 Added remote origin: {repo.clone_url}")
    else:
        subprocess.run(["git", "remote", "set-url", "origin", repo.clone_url], check=True)
        print(f"ℹ️ Remote 'origin' updated to: {repo.clone_url}")
except subprocess.CalledProcessError as e:
    raise SystemExit(f"❌ Failed to configure remote: {e}")

# Ask for commit message
commit_msg = input("Enter commit message (or leave blank for default): ").strip()
if not commit_msg:
    commit_msg = "Initial commit by GitHub agent"

# Git add, commit, push
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
    print(f"🎉 Successfully pushed code to {repo.html_url}")
except subprocess.CalledProcessError as e:
    raise SystemExit(f"❌ Git command failed: {e}")
