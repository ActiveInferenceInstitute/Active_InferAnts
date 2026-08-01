import subprocess
import sys
import os
import requests
from typing import Union, List, Dict

class GitHubRepoCloner:
    """
    A class to clone GitHub repositories.
    """
    
    @staticmethod
    def clone_repo(git_url: str, target_dir: str) -> None:
        """
        Clones a single GitHub repository into the specified target directory.
        
        Parameters:
        - git_url (str): The GitHub repository URL to clone.
        - target_dir (str): The directory to clone the repository into.
        """
        repo_name = git_url.split('/')[-1]  # Extracts repo name from URL
        # Sanitize: strip a trailing .git and reject anything that could escape
        # the target directory (e.g. a traversal/special name from an
        # attacker-influenced URL).
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        if repo_name in ('', '.', '..') or '/' in repo_name or os.sep in repo_name:
            raise ValueError(f"Unsafe repository name derived from URL: {git_url!r}")
        full_path = os.path.abspath(os.path.join(target_dir, repo_name))
        target_abs = os.path.abspath(target_dir)
        if os.path.commonpath([target_abs, full_path]) != target_abs:
            raise ValueError(f"Clone target escapes target directory: {full_path}")
        clone_command = ["git", "clone", git_url, full_path]
        
        try:
            subprocess.run(clone_command, check=True, capture_output=True)
            print(f"Successfully cloned {git_url} into {full_path}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {git_url}. Error: {e.stderr.decode()}", file=sys.stderr)

    @staticmethod
    def get_user_repos(username: str) -> List[str]:
        """
        Fetches all public repository URLs of a given GitHub user.
        
        Parameters:
        - username (str): The GitHub username to fetch repositories for.
        
        Returns:
        List[str]: A list of repository clone URLs.
        """
        repos_url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(repos_url)
        repos = response.json()
        return [repo['clone_url'] for repo in repos]

    @staticmethod
    def clone_user_repos(username: str, target_dir: str) -> None:
        """
        Clones all public repositories of a given GitHub user into the specified target directory.
        
        Parameters:
        - username (str): The GitHub username whose repositories to clone.
        - target_dir (str): The directory to clone the repositories into.
        """
        repo_urls = GitHubRepoCloner.get_user_repos(username)
        for git_url in repo_urls:
            GitHubRepoCloner.clone_repo(git_url, target_dir)

if __name__ == "__main__":
    users_to_clone = {

        # Example: just bringing the work of Python (pymdp) and Julia (RxInfer) repos, see below for more Active Inference usernames.  
        "ActiveInference_PyMDP_RxInfer": ["biaslab","infer-actively"],
        
        # Uncheck the following lists of users, and/or edit these lists. 
        # Thank you for using reusing/developing context & patterns!

        # Users for Active Inference code
        # ["biaslab", "infer-actively", "ago109", "daphnedemekas", "conorheins", "ChampiB", "zfountas", "alec-tschantz", "schwartenbeckph", "tejparr", "rssmith33", "HMCL-UNIST", "AP6YC", "fabio-deep", "BerenMillidge" , "fgregoretti", "cpezzato", "edluyuan", "djcrw", "spm", "wmkouw", "tomekkorbak", "ActiveInferenceInstitute"]
        
        # Users for Cognitive Security
        # "CognitiveSecurity": ["deepfates"],
        # Users for Civic code
        # "Civic": ["datamade", "usdoj", "MuckRock", "18F", "kinlane", "usagov", "usgpo", "GSA"],
        
        # Users for Synergetics & Quadrays code
        # "Synergetics": ["4dsolutions"],
        
        # Users for Ant and genomics code
        # "Ants": ["Social-Insect-Genomics", "cdanielcadena", "cooplab", "johnssproul", "pbfrandsen", "PeterMulhair", "fohebert", "guillemylla", "guo-cheng"],
  
        # Visualization, Statistics, Canvas, Cryptography, Wolfram, Complexity, Physics, cadCAD/BlockScience, Linux, Network, Neuroscience, etc.... 
  
        # Users for Agents and autonomous systems code
        #"Agents": ["Anthropic", "OpenAI", "Significant-Gravitas", "yoheinakajima", "TransformerOptimus", "Paitesanshi", "kyrolabs", "lafmdp", "Jenqyang", "e2b-dev", "OpenBMB"]
    }
    
    target_dir = input("Enter the target directory (default is 'repos/'): ").strip() or "repos/"
    
    for category, usernames in users_to_clone.items():
        print(f"Cloning {category} repositories...")
        for username in usernames:
            user_target_dir = os.path.join(target_dir, category, username)
            if not os.path.exists(user_target_dir):
                os.makedirs(user_target_dir)
            GitHubRepoCloner.clone_user_repos(username, user_target_dir)

