# import os
# import subprocess
# from github import Github, GithubException
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Get GitHub token
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# if not GITHUB_TOKEN:
#     raise ValueError("⚠️ Please set GITHUB_TOKEN in your .env file")

# # Ask user for GitHub username
# username = input("Enter your GitHub username: ").strip()

# # Authenticate with GitHub
# g = Github(GITHUB_TOKEN)
# try:
#     user = g.get_user()
# except GithubException as e:
#     raise SystemExit(f"❌ Failed to authenticate with GitHub: {e}")

# # Detect local folder name as repo name
# repo_name = os.path.basename(os.getcwd())
# print(f"📂 Detected local folder name as repo: {repo_name}")

# # Check if repo exists on GitHub
# try:
#     repo = user.get_repo(repo_name)
#     print(f"✅ Repo '{repo_name}' already exists: {repo.html_url}")
# except GithubException:
#     print(f"🚀 Creating new repo '{repo_name}'...")
#     try:
#         repo = user.create_repo(
#             name=repo_name,
#             description=f"Auto-created repo for {repo_name}",
#             private=False  # Change to True if you want private repo
#         )
#         print(f"✅ Repo created: {repo.html_url}")
#     except GithubException as e:
#         raise SystemExit(f"❌ Failed to create repo: {e}")

# # Initialize Git if not already
# if not os.path.exists(".git"):
#     subprocess.run(["git", "init"], check=True)
#     print("📌 Initialized Git repository locally.")

# # Add remote origin if not exists
# try:
#     remotes = subprocess.check_output(["git", "remote"]).decode().splitlines()
#     if "origin" not in remotes:
#         subprocess.run(["git", "remote", "add", "origin", repo.clone_url], check=True)
#         print(f"📌 Added remote origin: {repo.clone_url}")
#     else:
#         subprocess.run(["git", "remote", "set-url", "origin", repo.clone_url], check=True)
#         print(f"ℹ️ Remote 'origin' updated to: {repo.clone_url}")
# except subprocess.CalledProcessError as e:
#     raise SystemExit(f"❌ Failed to configure remote: {e}")

# # Ask for commit message
# commit_msg = input("Enter commit message (or leave blank for default): ").strip()
# if not commit_msg:
#     commit_msg = "Initial commit by GitHub agent"

# # Git add, commit, push
# try:
#     subprocess.run(["git", "add", "."], check=True)
#     subprocess.run(["git", "commit", "-m", commit_msg], check=True)
#     subprocess.run(["git", "branch", "-M", "main"], check=True)
#     subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
#     print(f"🎉 Successfully pushed code to {repo.html_url}")
# except subprocess.CalledProcessError as e:
#     raise SystemExit(f"❌ Git command failed: {e}")
#################################################################################
# import os
# import subprocess
# from github import Github, GithubException
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Get GitHub token
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# if not GITHUB_TOKEN:
#     raise ValueError("⚠️ Please set GITHUB_TOKEN in your .env file")

# # Authenticate with GitHub
# g = Github(GITHUB_TOKEN)
# try:
#     user = g.get_user()
# except GithubException as e:
#     raise SystemExit(f"❌ Failed to authenticate with GitHub: {e}")

# # Ask user for folder path
# folder_path = input("📂 Enter the folder path you want to push: ").strip()
# if not os.path.exists(folder_path):
#     raise SystemExit(f"❌ Folder '{folder_path}' does not exist.")

# # Detect repo name from folder
# repo_name = os.path.basename(os.path.normpath(folder_path))
# print(f"📂 Using folder name as repo: {repo_name}")

# # Check if repo exists, otherwise create it
# try:
#     repo = user.get_repo(repo_name)
#     print(f"✅ Repo '{repo_name}' already exists: {repo.html_url}")
# except GithubException:
#     print(f"🚀 Creating new repo '{repo_name}'...")
#     try:
#         repo = user.create_repo(
#             name=repo_name,
#             description=f"Auto-created repo for {repo_name}",
#             private=False
#         )
#         print(f"✅ Repo created: {repo.html_url}")
#     except GithubException as e:
#         raise SystemExit(f"❌ Failed to create repo: {e}")

# # Change directory into folder
# os.chdir(folder_path)

# # Initialize Git if needed
# if not os.path.exists(".git"):
#     subprocess.run(["git", "init"], check=True)
#     print("📌 Initialized Git repository locally.")

# # Configure remote origin
# subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)
# subprocess.run(["git", "remote", "add", "origin", repo.clone_url], check=True)
# print(f"📌 Remote 'origin' set to: {repo.clone_url}")

# # Ask for commit message
# commit_msg = input("💬 Enter commit message (or leave blank): ").strip()
# if not commit_msg:
#     commit_msg = f"Initial commit of {repo_name} via GitHub agent"

# # Git add, commit, push
# try:
#     subprocess.run(["git", "add", "."], check=True)
#     subprocess.run(["git", "commit", "-m", commit_msg], check=True)
#     subprocess.run(["git", "branch", "-M", "main"], check=True)
#     subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
#     print(f"🎉 Successfully pushed folder '{repo_name}' to {repo.html_url}")
# except subprocess.CalledProcessError as e:
#     raise SystemExit(f"❌ Git command failed: {e}")
############################################################################
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

# Ask user for folder path
folder_path = input("📂 Enter folder path to push: ").strip()

if not os.path.exists(folder_path):
    raise FileNotFoundError(f"❌ Folder '{folder_path}' does not exist!")

# Absolute path + repo name
folder_path = os.path.abspath(folder_path)
repo_name = os.path.basename(folder_path)
print(f"📂 Using folder '{repo_name}' as GitHub repo name")

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
try:
    user = g.get_user()
except GithubException as e:
    raise SystemExit(f"❌ GitHub authentication failed: {e}")

# Create repo if not exists
try:
    repo = user.get_repo(repo_name)
    print(f"✅ Repo '{repo_name}' already exists: {repo.html_url}")
except GithubException:
    print(f"🚀 Creating repo '{repo_name}'...")
    try:
        repo = user.create_repo(
            name=repo_name,
            description=f"Auto-created repo for {repo_name}",
            private=False  # Change True if you want private repo
        )
        print(f"✅ Repo created: {repo.html_url}")
    except GithubException as e:
        raise SystemExit(f"❌ Failed to create repo: {e}")

# Go inside folder
os.chdir(folder_path)

# Create/Update .gitignore to protect sensitive files
gitignore_path = os.path.join(folder_path, ".gitignore")
with open(gitignore_path, "w") as f:
    f.write(".env\n")
    f.write("__pycache__/\n")
    f.write("*.pyc\n")
    f.write("*.pyo\n")
    f.write("*.pyd\n")
    f.write(".Python\n")
    f.write("env/\n")
    f.write("venv/\n")
    f.write("*.sqlite3\n")
    f.write(".DS_Store\n")
print("🛡️  .gitignore created (secrets & junk files ignored).")

# Init git if not already
if not os.path.exists(".git"):
    subprocess.run(["git", "init"], check=True)
    print("📌 Initialized Git repository inside folder.")

# Add or update remote origin
try:
    remotes = subprocess.check_output(["git", "remote"]).decode().splitlines()
    if "origin" not in remotes:
        subprocess.run(["git", "remote", "add", "origin", repo.clone_url], check=True)
        print(f"📌 Added remote origin: {repo.clone_url}")
    else:
        subprocess.run(["git", "remote", "set-url", "origin", repo.clone_url], check=True)
        print(f"ℹ️ Remote origin updated: {repo.clone_url}")
except subprocess.CalledProcessError as e:
    raise SystemExit(f"❌ Remote setup failed: {e}")

# Git add, commit, push all files
commit_msg = "Initial commit by GitHub agent"
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "--allow-empty", "-m", commit_msg], check=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
    print(f"🎉 Successfully pushed ALL safe files from '{folder_path}' to {repo.html_url}")
except subprocess.CalledProcessError as e:
    raise SystemExit(f"❌ Git push failed: {e}")
