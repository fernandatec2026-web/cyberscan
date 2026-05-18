import argparse
import os

from scanner.secrets_scan import scan_directory
from scanner.dependency_scan import scan_dependencies
from scanner.github_scan import clone_public_repo, cleanup_repo
from scanner.ai_analysis import generate_ai_summary
from scanner.report import generate_html_report


def main():
    print("=========================================")
    print("     CyberScan AI - Active Security      ")
    print("=========================================\n")

    parser = argparse.ArgumentParser(
        description="CyberScan AI CLI Interface."
    )

    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Local directory to scan."
    )

    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="GitHub repository URL."
    )

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
        print(f"[ERROR] Path '{target_path}' was not found.")
        return

    print(f"[*] Starting scan in: {os.path.abspath(target_path)}")

    secrets_found = scan_directory(target_path)

    req_file = os.path.join(target_path, "requirements.txt")
    deps_found = scan_dependencies(req_file)

    # Execute AI analysis phase
    print("[*] Artificial Intelligence: Generating insights and automated fixes...")

    ai_summary = generate_ai_summary(secrets_found, deps_found)

    print(f"\n🤖 AI Summary:\n{ai_summary}\n")

    if secrets_found or deps_found:
        print("[!] Scan completed with alerts.")
        generate_html_report(secrets_found, deps_found, ai_summary)

    else:
        print("[+] Scan completed. Clean code and secure dependencies.")
        generate_html_report(secrets_found, deps_found, ai_summary)

    if is_remote:
        cleanup_repo(target_path)


if __name__ == "__main__":
    main()
