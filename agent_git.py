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
import os
import subprocess
import requests
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI


# Load API keys
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def git_tool(command: str):
    """Run Git command and return output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip() or "✅ Command executed successfully"
        else:
            return f"⚠️ Error: {result.stderr.strip()}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"


def create_github_repo(username: str, repo_name: str):
    """Create GitHub repo if not exists."""
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # ✅ Check if repo exists
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        print(f"✅ Repo already exists: {repo_name}")
        return True

    # ❌ If not exists, create it
    print(f"📦 Repo not found, creating new repo: {repo_name}")
    url = "https://api.github.com/user/repos"
    data = {"name": repo_name, "private": False}
    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code == 201:
        print(f"✅ Repo created successfully: {repo_name}")
        return True
    else:
        print(f"❌ Failed to create repo: {resp.text}")
        return False


# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

tools = [
    Tool(
        name="GitHub Tool",
        func=git_tool,
        description="Run git commands like add, commit, push, pull"
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)


if __name__ == "__main__":
    folder = input("📂 Enter folder path to push: ").strip()
    if not os.path.exists(folder):
        print("❌ Invalid folder path")
        exit(1)

    os.chdir(folder)

    username = input("👤 Enter your GitHub username: ").strip()
    branch = input("🌿 Enter branch name (default: main): ").strip() or "main"

    repo_name = os.path.basename(folder).replace(" ", "-")
    print(f"📂 Using repo name: {repo_name}")

    # ✅ Auto-create repo if not exists
    if not create_github_repo(username, repo_name):
        exit(1)

    # ✅ Add .env to gitignore
    with open(".gitignore", "a") as f:
        f.write("\n.env\n")

    git_tool("git rm --cached -f .env")

    commands = [
        "git init",
        "git add .",
        'git commit -m "Initial commit by GitHub agent"',
        f"git branch -M {branch}",
    ]

    remotes = git_tool("git remote -v")
    if "origin" in remotes:
        print("🔄 Remote 'origin' already exists, removing it...")
        git_tool("git remote remove origin")

    commands.append(f"git remote add origin https://github.com/{username}/{repo_name}.git")
    commands.append(f"git push -u origin {branch} --force")

    for cmd in commands:
        print(f"\n➡️ Running: {cmd}")
        response = git_tool(cmd)
        print(response)
