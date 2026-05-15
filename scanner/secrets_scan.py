import os
import re

patterns = {
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Token": r"ghp_[A-Za-z0-9]{36}",
    "Generic API Key": r"api[_-]?key\s*=\s*['\"](.*?)['\"]"
}

def scan_file(filepath):

    findings = []

    try:

        with open(filepath, "r", encoding="utf-8") as file:

            content = file.read()

            for name, pattern in patterns.items():

                matches = re.findall(pattern, content)

                if matches:
                    findings.append((name, matches))

    except:
        pass

    return findings


def scan_directory(directory):

    results = []

    for root, dirs, files in os.walk(directory):

        for file in files:

            if file.endswith((".py", ".txt", ".env", ".js")):

                fullpath = os.path.join(root, file)

                findings = scan_file(fullpath)

                if findings:
                    results.append((fullpath, findings))

    return results


if __name__ == "__main__":

    results = scan_directory(".")

    if results:

        print("\n[!] POSSÍVEIS SECRETS ENCONTRADOS:\n")

        for filepath, findings in results:

            print(f"Arquivo: {filepath}")

            for secret_type, matches in findings:

                print(f"  -> {secret_type}: {matches}")

            print()

    else:
        print("Nenhum secret encontrado.")
        