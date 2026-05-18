import os
import re

# Simulated local database of known CVEs
VULNERABLE_PACKAGES = {
    "flask": {
        "version": "2.0.0",
        "cve": "CVE-2023-30861",
        "severity": "HIGH",
        "desc": "Improper session leakage prevention."
    },
    "requests": {
        "version": "2.26.0",
        "cve": "CVE-2023-32681",
        "severity": "MEDIUM",
        "desc": "Credential leakage through Authorization header during HTTPS redirects."
    },
    "django": {
        "version": "3.2.0",
        "cve": "CVE-2021-35042",
        "severity": "CRITICAL",
        "desc": "SQL injection through QuerySet subqueries."
    },
    "pyyaml": {
        "version": "5.3.1",
        "cve": "CVE-2020-14343",
        "severity": "CRITICAL",
        "desc": "Arbitrary code execution through insecure deserialization."
    }
}

def scan_dependencies(requirements_path="requirements.txt"):
    """Reads requirements.txt and checks dependencies against the vulnerability database."""
    
    dependency_findings = []

    if not os.path.exists(requirements_path):
        return dependency_findings

    try:
        with open(requirements_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()

                # Ignores comments and empty lines
                if not line or line.startswith("#"):
                    continue

                # Captures the standardized 'name==version' format
                match = re.match(r"^([a-zA-Z0-9_-]+)==([0-9.]+)", line)

                if match:
                    pkg_name = match.group(1).lower()
                    pkg_version = match.group(2)

                    # Checks whether the package exists in the vulnerable database
                    if pkg_name in VULNERABLE_PACKAGES:
                        vuln_info = VULNERABLE_PACKAGES[pkg_name]

                        # Verifies whether the installed version is vulnerable
                        if pkg_version <= vuln_info["version"]:
                            dependency_findings.append({
                                "package": pkg_name,
                                "version": pkg_version,
                                "cve": vuln_info["cve"],
                                "severity": vuln_info["severity"],
                                "description": vuln_info["desc"],
                                "line": line_num
                            })

    except Exception as e:
        print(f"[ERROR] Failed to analyze dependencies: {e}")

    return dependency_findings
