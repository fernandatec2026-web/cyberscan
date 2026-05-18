import os
import subprocess
import shutil

def clone_public_repo(repo_url):
    """Clones a public GitHub repository into a temporary folder."""
    
    target_dir = os.path.join("reports", "temp_repo")

    # Cleans previous temporary scan folder if it already exists
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    print(f"[*] Cloning remote repository: {repo_url}...")

    try:
        # Executes git clone directly through the system
        result = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, target_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            print("[+] Repository cloned successfully!")
            return target_dir

        else:
            print(f"[ERROR] Failed to clone repository: {result.stderr.strip()}")
            return None

    except Exception as e:
        print(f"[ERROR] Git command could not be executed: {e}")
        return None


def cleanup_repo(target_dir):
    """Removes temporary cloned repository files after scan completion."""

    if target_dir and os.path.exists(target_dir):
        print("[*] Cleaning temporary remote repository files...")
        shutil.rmtree(target_dir)
