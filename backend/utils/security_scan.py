import os
import re

def run_security_scan():
    print("=== SECURITY SECRET SCAN ===")
    secret_pattern = re.compile(r'(api_key|token|secret|password)\s*=\s*["\'][A-Za-z0-9_\-]{8,}["\']', re.IGNORECASE)
    found_secrets = False
    
    for root, dirs, files in os.walk('.'):
        if any(ign in root for ign in ['node_modules', '.git', '__pycache__', 'dist', '.pytest_cache']):
            continue
        for f in files:
            if f.endswith(('.py', '.js', '.jsx', '.html', '.env', '.example', '.md')):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        matches = secret_pattern.findall(content)
                        if matches:
                            print(f"[WARNING] Potential secret pattern in {path}: {matches}")
                            found_secrets = True
                except Exception as e:
                    pass
    if not found_secrets:
        print("[SUCCESS] No hardcoded secrets or API tokens found in codebase.")

if __name__ == '__main__':
    run_security_scan()
