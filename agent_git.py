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
import shutil
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

# Add/Update remote origin
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

# Ask user for a specific file/folder to push
user_path = input("📂 Enter folder OR file path to push (absolute or relative): ").strip()

# Handle absolute path outside repo
if os.path.isabs(user_path):
    if not os.path.exists(user_path):
        raise FileNotFoundError(f"❌ Path '{user_path}' does not exist!")

    basename = os.path.basename(user_path.rstrip("\\/"))
    target_path = os.path.join(os.getcwd(), basename)

    if os.path.exists(target_path):
        shutil.rmtree(target_path) if os.path.isdir(target_path) else os.remove(target_path)

    if os.path.isdir(user_path):
        shutil.copytree(user_path, target_path)
    else:
        shutil.copy2(user_path, target_path)

    relative_path = basename
    print(f"📥 Copied '{user_path}' into repo as '{relative_path}'")

else:
    target_path = os.path.join(os.getcwd(), user_path)
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"❌ Path '{target_path}' not found inside repo!")
    relative_path = user_path

# Update .gitignore to track only this path
gitignore_path = os.path.join(os.getcwd(), ".gitignore")
with open(gitignore_path, "w") as f:
    f.write("*\n")
    f.write(f"!/{relative_path}\n")
    f.write("!.gitignore\n")

print(f"📝 .gitignore updated to track only '{relative_path}'")

# Ask for commit message
commit_msg = input("Enter commit message (or leave blank for default): ").strip()
if not commit_msg:
    commit_msg = f"Update {relative_path}"

# Git add, commit, push
try:
    subprocess.run(["git", "add", "."], check=True)
    # Allow empty commits (avoids failure if no changes)
    subprocess.run(["git", "commit", "--allow-empty", "-m", commit_msg], check=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
    print(f"🎉 Successfully pushed '{relative_path}' to {repo.html_url}")
except subprocess.CalledProcessError as e:
    raise SystemExit(f"❌ Git command failed: {e}")
