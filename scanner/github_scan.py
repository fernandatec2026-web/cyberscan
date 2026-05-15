import os
import subprocess
import shutil

def clone_public_repo(repo_url):
    """Clona um repositório público do GitHub em uma pasta temporária."""
    target_dir = os.path.join("reports", "temp_repo")
    
    # Se já existir uma varredura anterior, limpa a pasta antes de clonar
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
        
    print(f"[*] Clonando repositório remoto: {repo_url}...")
    try:
        # Executa o comando git clone diretamente pelo sistema
        result = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, target_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            print("[+] Repositório clonado com sucesso!")
            return target_dir
        else:
            print(f"[ERRO] Falha ao clonar o repositório: {result.stderr.strip()}")
            return None
            
    except Exception as e:
        print(f"[ERRO] O comando 'git' não pôde ser executado: {e}")
        return None

def cleanup_repo(target_dir):
    """Remove os arquivos temporários clonados após o término do scan."""
    if target_dir and os.path.exists(target_dir):
        print("[*] Limpando arquivos temporários do repositório remoto...")
        shutil.rmtree(target_dir)
