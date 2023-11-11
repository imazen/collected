import os
import git
import re
import openai
from pathlib import Path
from markdown2 import markdown

# Constants
REPOSITORIES = ["https://github.com/imazen/imageflow", "https://github.com/imazen/resizer", "https://github.com/imazen/imageflow-dotnet", "https://github.com/imazen/imageflow-dotnet-server","https://github.com/imazen/imageflow-node", "https://github.com/imazen/imageflow-go", 
               "https://github.com/imazen/resizer-web", "https://github.com/imazen/sites"]
LOCAL_REPO_PATH = "local_repos"
ABSOLUTE_LOCAL_REPO_PATH = os.path.abspath(LOCAL_REPO_PATH)
OUTPUT_MARKDOWN_FILE = "all.md"

# GPT-4 API settings
client = OpenAI() #defaults to OPENAI_API_KEY

def get_repo_name(repo_url):
    """Extract the repository name from the URL."""
    return os.path.basename(repo_url).rstrip('.git')

def clone_repositories():
    for repo in REPOSITORIES:
        git.Repo.clone_from(repo, os.path.join(ABSOLUTE_LOCAL_REPO_PATH, get_repo_name(repo)))

def extract_and_convert_markdown(repo_path):
    md_files = Path(repo_path).rglob("*.md")
    markdown_content = ""

    for file in md_files:
        file_relative_path = os.path.relpath(file, ABSOLUTE_LOCAL_REPO_PATH)
        markdown_content += f"## Contents of file {file_relative_path}\n\n"
        with open(file, 'r') as f:
            markdown_content += markdown(f.read()) + "\n\n"

    return markdown_content

def main():
    clone_repositories()

    all_documentation = ""

    for repo_dir in os.listdir(LOCAL_REPO_PATH):
        repo_path = os.path.join(LOCAL_REPO_PATH, repo_dir)
        all_documentation += extract_and_convert_markdown(repo_path)

    with open(OUTPUT_MARKDOWN_FILE, "w") as f:
        f.write(all_documentation)

if __name__ == "__main__":
    main()
