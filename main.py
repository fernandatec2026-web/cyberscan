import argparse
import os
from scanner.secrets_scan import scan_directory
from scanner.dependency_scan import scan_dependencies
from scanner.github_scan import clone_public_repo, cleanup_repo
from scanner.ai_analysis import generate_ai_summary
from scanner.report import generate_html_report

def main():
    print("=========================================")
    print("     CyberScan AI - Segurança Ativa      ")
    print("=========================================\n")
    
    parser = argparse.ArgumentParser(description="Interface CLI do CyberScan AI.")
    parser.add_argument("--path", type=str, default=".", help="Diretório local a ser analisado.")
    parser.add_argument("--url", type=str, default=None, help="URL de um repositório público do GitHub.")
    args = parser.parse_args()
    
    target_path = args.path
    is_remote = False
    
    if args.url:
        cloned_dir = clone_public_repo(args.url)
        if not cloned_dir:
            return
        target_path = cloned_dir
        is_remote = True

    if not os.path.exists(target_path):
        print(f"[ERRO] O caminho '{target_path}' não foi localizado.")
        return

    print(f"[*] Iniciando varredura em: {os.path.abspath(target_path)}")
    
    secrets_found = scan_directory(target_path)
    
    req_file = os.path.join(target_path, "requirements.txt")
    deps_found = scan_dependencies(req_file)
    
    # Executa a Fase 5: Inteligência Artificial
    print("[*] Inteligência Artificial: Gerando insights e correções automáticas...")
    ai_summary = generate_ai_summary(secrets_found, deps_found)
    print(f"\n🤖 Resumo da IA:\n{ai_summary}\n")
    
    if secrets_found or deps_found:
        print(f"[!] Varredura concluída com alertas.")
        generate_html_report(secrets_found, deps_found, ai_summary)
    else:
        print("[+] Varredura concluída. Código limpo e dependências seguras.")
        generate_html_report(secrets_found, deps_found, ai_summary)
        
    if is_remote:
        cleanup_repo(target_path)

if __name__ == "__main__":
    main()
