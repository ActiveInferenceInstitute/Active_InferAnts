import subprocess
import sys
import os
from typing import Union, List, Dict, Any

def execute_command(command: List[str]) -> None:
    """
    Executes a given command using subprocess and handles errors.
    
    Parameters:
    - command (List[str]): The command to execute as a list of strings.
    """
    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode()
        print(f"Command execution failed with error: {error_msg}", file=sys.stderr)
        sys.exit(1)

def clone_repo(git_url: str, target_dir: str, use_ssh: bool = False) -> None:
    """
    Clones a single GitHub repository into the specified target directory.
    
    Parameters:
    - git_url (str): The GitHub repository URL to clone.
    - target_dir (str): The directory to clone the repository into.
    - use_ssh (bool): Whether to use SSH for cloning instead of HTTPS.
    """
    repo_name = git_url.split('/')[-1].split('.')[0]  # Extracts repo name from URL
    # Sanitize + contain: never allow a repo name to escape the target dir.
    if repo_name in ('', '.', '..') or '/' in repo_name or os.sep in repo_name:
        raise ValueError(f"Unsafe repository name derived from URL: {git_url!r}")
    full_path = os.path.abspath(os.path.join(target_dir, repo_name))
    if os.path.commonpath([os.path.abspath(target_dir), full_path]) != os.path.abspath(target_dir):
        raise ValueError(f"Clone target escapes target directory: {full_path}")
    
    if use_ssh:
        # Convert HTTPS URL to SSH URL
        ssh_url = f"git@github.com:{'/'.join(git_url.split('/')[-2:])}"
        clone_command = ["git", "clone", ssh_url, full_path]
    else:
        clone_command = ["git", "clone", git_url, full_path]
    
    execute_command(clone_command)
    print(f"Successfully cloned {git_url} into {full_path}.")

def clone_repos(repo_urls: Union[List[str], Dict[str, str]], target_dir: str = "repos/", use_ssh: bool = False) -> None:
    """
    Clones a list or dictionary of GitHub repositories into the specified target directory.
    If no target directory is specified, it clones into the 'repos/' directory.
    
    Parameters:
    - repo_urls (Union[List[str], Dict[str, str]]): A list or dictionary of GitHub repository URLs to clone.
    - target_dir (str, optional): The directory to clone the repositories into.
    - use_ssh (bool): Whether to use SSH for cloning instead of HTTPS.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    if isinstance(repo_urls, dict):
        repo_urls = list(repo_urls.values())
    
    for git_url in repo_urls:
        clone_repo(git_url, target_dir, use_ssh)

# Flags to determine which categories to clone
CLONE_THEBRAIN = False
CLONE_NOSTR = False
CLONE_SYNERGETICS = False
CLONE_ANTS = False
CLONE_ACTIVE_INFERENCE = False
CLONE_MULTIAGENT_LLM = False
CLONE_TASK_EXECUTION_AI_AGI = False
CLONE_MULTIAGENT_AI = False
CLONE_GENERAL_LLM_RESOURCES = False
CLONE_SOCIAL_MEDIA_INTEROPERABILITY = False
CLONE_HOLOCHAIN = True

# Repositories to clone
repos_to_clone = {
    "TheBrain": [
        "https://github.com/TheBrainTech/thebrain-api-quickstart-python"
    ],
    "Nostr": [
        "https://github.com/nostr-protocol/nostr",
        "https://github.com/fiatjaf/nostr-tools",
        "https://github.com/limina1/indextr-client",
        "https://github.com/fiatjaf/quill-asciidoc",
        "https://github.com/fiatjaf/svelte-asciidoc",
        "https://github.com/github-tijlxyz/wikinostr",
        "https://github.com/aljazceru/awesome-nostr",
        "https://github.com/nostr-connect/connect"
    ],
    "Synergetics": [
        "https://github.com/4dsolutions/MartianMath",
        "https://github.com/4dsolutions/m4w",
        "https://github.com/4dsolutions/python_camp",
        "https://github.com/4dsolutions/School_of_Tomorrow",
        "https://github.com/4dsolutions/DigitalMathematics",
        "https://github.com/4dsolutions/Curriculum_Development"
    ],
    "Ants": [
        "https://github.com/Social-Insect-Genomics/",
        "https://github.com/johnssproul/Insect_REs",
        "https://github.com/pbfrandsen/insect_genome_assemblies",
        "https://github.com/PeterMulhair/DToL_insects",
        "https://github.com/fohebert/GenomeAnnotation",
        "https://github.com/guillemylla/Crickets_Genome_Annotation"
    ],
    "ActiveInference": [
        "https://github.com/ActiveInferenceInstitute/ActiveBlockference",
        "https://github.com/infer-actively/pymdp",
        "https://github.com/cadCAD-org/cadcad-ri"
    ],
    "MultiagentLLM": [
        "https://github.com/nickm980/smallville",
        "https://github.com/chatarena/chatarena",
        "https://github.com/OpenGVLab/GITM",
        "https://github.com/OpenBMB/AgentVerse",
        "https://github.com/BladeTransformerLLC/OvercookedGPT",
        "https://github.com/101dotxyz/GPTeam",
        "https://github.com/mkturkcan/generative-agents"
    ],
    "TaskExecutionAIAGI": [
        "https://github.com/Significant-Gravitas/Auto-GPT",
        "https://github.com/SamurAIGPT/Camel-AutoGPT",
        "https://github.com/Josh-XT/AGiXT",
        "https://github.com/reworkd/AgentGPT",
        "https://github.com/muellerberndt/mini-agi",
        "https://github.com/enricoros/big-agi",
        "https://github.com/TransformerOptimus/SuperAGI"
    ],
    "MultiagentAI": [
        "https://github.com/deepmind/open_spiel",
        "https://github.com/NeuralMMO/environment",
        "https://github.com/datamllab/rlcard",
        "https://github.com/Farama-Foundation/MAgent2",
        "https://github.com/salesforce/ai-economist"
    ],
    "GeneralLLMResources": [
        "https://github.com/filipecalegario/awesome-generative-ai",
        "https://github.com/EmbraceAGI/Awesome-AGI",
        "https://github.com/tigerneil/awesome-deep-rl",
        "https://github.com/wel3kxial/AIGC_Resources",
        "https://github.com/imaurer/awesome-decentralized-llm",
        "https://github.com/gabriben/awesome-generative-information-retrieval",
        "https://github.com/hwchase17/langchain",
        "https://github.com/Mooler0410/LLMsPracticalGuide",
        "https://github.com/microsoft/LMOps",
        "https://github.com/ennucore/clippy"
    ],
    "SocialMediaInteroperability": [
        "https://github.com/42wim/matterbridge"
    ],
    "Holochain": [
        "https://github.com/holochain/holochain",
        "https://github.com/f13end/Holochain-Projects",
        "https://github.com/holochain-apps/holochain-apps",
        "https://github.com/holochain/scaffolding",
        "https://github.com/holochain/holochain-client-rust",
        "https://github.com/holochain/holochain-client-js",
        "https://github.com/holochain/launcher-tauri",
        "https://github.com/holochain/wind-tunnel",
        "https://github.com/Holo-Host/hpos-service-crates",
        "https://github.com/Holo-Host/host-console-ui",
        "https://github.com/Holo-Host/ui-common-library",
        "https://github.com/Holo-Host/holo-auto-installer"
    ]
}

# Enhanced cloning process with category-based organization
if __name__ == "__main__":
    target_dir = input("Enter the target directory (default is 'repos/'): ").strip() or "repos/"
    use_ssh = input("Use SSH for cloning? (y/n, default is n): ").strip().lower() == 'y'
    
    if CLONE_THEBRAIN:
        print("Cloning TheBrain repositories...")
        clone_repos(repos_to_clone["TheBrain"], os.path.join(target_dir, "TheBrain"), use_ssh)
    
    if CLONE_NOSTR:
        print("Cloning Nostr repositories...")
        clone_repos(repos_to_clone["Nostr"], os.path.join(target_dir, "Nostr"), use_ssh)
    
    if CLONE_SYNERGETICS:
        print("Cloning Synergetics repositories...")
        clone_repos(repos_to_clone["Synergetics"], os.path.join(target_dir, "Synergetics"), use_ssh)
    
    if CLONE_ANTS:
        print("Cloning Ants repositories...")
        clone_repos(repos_to_clone["Ants"], os.path.join(target_dir, "Ants"), use_ssh)
    
    if CLONE_ACTIVE_INFERENCE:
        print("Cloning Active Inference repositories...")
        clone_repos(repos_to_clone["ActiveInference"], os.path.join(target_dir, "ActiveInference"), use_ssh)
    
    if CLONE_MULTIAGENT_LLM:
        print("Cloning Multiagent LLM repositories...")
        clone_repos(repos_to_clone["MultiagentLLM"], os.path.join(target_dir, "MultiagentLLM"), use_ssh)
    
    if CLONE_TASK_EXECUTION_AI_AGI:
        print("Cloning Task Execution AI and AGI repositories...")
        clone_repos(repos_to_clone["TaskExecutionAIAGI"], os.path.join(target_dir, "TaskExecutionAIAGI"), use_ssh)
    
    if CLONE_MULTIAGENT_AI:
        print("Cloning Multiagent AI repositories...")
        clone_repos(repos_to_clone["MultiagentAI"], os.path.join(target_dir, "MultiagentAI"), use_ssh)
    
    if CLONE_GENERAL_LLM_RESOURCES:
        print("Cloning General LLM resources repositories...")
        clone_repos(repos_to_clone["GeneralLLMResources"], os.path.join(target_dir, "GeneralLLMResources"), use_ssh)
    
    if CLONE_SOCIAL_MEDIA_INTEROPERABILITY:
        print("Cloning Social Media Interoperability repositories...")
        clone_repos(repos_to_clone["SocialMediaInteroperability"], os.path.join(target_dir, "SocialMediaInteroperability"), use_ssh)
    
    if CLONE_HOLOCHAIN:
        print("Cloning Holochain repositories...")
        clone_repos(repos_to_clone["Holochain"], os.path.join(target_dir, "Holochain"), use_ssh)