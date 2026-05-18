import os
import re

# Expanded secret patterns based on common AppSec industry standards
patterns = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Personal Access Token": r"ghp_[A-Za-z0-9]{36}",
    "Generic API Key": r"api[_-]?key\s*=\s*[\"']([^\"']+)[\"']",
    "OpenAI API Key": r"sk-[a-zA-Z0-9]{48}",
    "Google OAuth Essential": r"[0-9a-zA-Z-_]{24}\.apps\.googleusercontent\.com",
    "Slack Webhook": r"https://hooks\.slack\.com/services/T[A-Z0-9]{8}/B[A-Z0-9]{8}/[A-Za-z0-9]{24}",
    "PostgreSQL Connection String": r"postgres://[a-zA-Z0-9_-]+:[a-zA-Z0-9_-]+@[a-zA-Z0-9.-]+:[0-9]+/+[a-zA-Z0-9_-]+",
    "RSA Private Key": r"-----BEGIN RSA PRIVATE KEY-----"
}

def scan_file(filepath):
    """Scans a single file searching for exposed secrets."""
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            for line_num, line in enumerate(file, 1):
                for secret_type, pattern in patterns.items():
                    matches = re.findall(pattern, line)
                    if matches:
                        # Retorna o tipo, o que foi achado e a linha exata (Essencial para o relatório profissional)
                        for match in matches:
                            findings.append({
                                "type": secret_type,
                                "match": match if isinstance(match, str) else match[0],
                                "line": line_num
                            })
    except Exception as e:
        print(f"[ERROR] Failed to read {filepath}: {e}")
    return findings

def scan_directory(directory="."):
    """Scans the directory while ignoring heavy folders and config files."""
    results = {}
    
    # Common folders and files ignored to improve performance and reduce false positives
    ignore_dirs = {"venv", ".git", "__pycache__", "node_modules", "reports"}
    ignore_files = {"requirements.txt", "README.md"}

    for root, dirs, files in os.walk(directory):
        # Filters directories inline to prevent os.walk from entering them
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file in ignore_files:
                continue
                
            filepath = os.path.join(root, file)
            findings = scan_file(filepath)
            
            if findings:
                results[filepath] = findings

    return results
    