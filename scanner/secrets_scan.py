import os
import re

# Padrões de Secrets Expandidos (Padrão de Mercado para AppSec)
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
    """Analisa um arquivo individual procurando por segredos expostos."""
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
        print(f"[ERRO] Falha ao ler {filepath}: {e}")
    return findings

def scan_directory(directory="."):
    """Varre o diretório ignorando pastas pesadas e arquivos de configuração."""
    results = {}
    
    # Pastas e arquivos comuns a serem ignorados para performance e evitar falsos positivos
    ignore_dirs = {"venv", ".git", "__pycache__", "node_modules", "reports"}
    ignore_files = {"requirements.txt", "README.md"}

    for root, dirs, files in os.walk(directory):
        # Filtra os diretórios inline para evitar que o os.walk entre neles
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file in ignore_files:
                continue
                
            filepath = os.path.join(root, file)
            findings = scan_file(filepath)
            
            if findings:
                results[filepath] = findings

    return results
    