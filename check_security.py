#!/usr/bin/env python3
"""
Security check script for pre-commit hook
Checks for sensitive data before committing to Git
"""

import os
import sys
import re
import subprocess

def run_git_command(cmd):
    """Run git command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip().split('\n') if result.stdout else []
    except Exception as e:
        print(f"Error running git command: {e}")
        return []

def check_sensitive_patterns():
    """Check for sensitive patterns in staged files"""
    sensitive_patterns = [
        r'api_key\s*[:=]\s*["\'][^"\']+["\']',
        r'api_token\s*[:=]\s*["\'][^"\']+["\']',
        r'password\s*[:=]\s*["\'][^"\']+["\']',
        r'secret\s*[:=]\s*["\'][^"\']+["\']',
        r'token\s*[:=]\s*["\'][^"\']+["\']',
        r'credential\s*[:=]\s*["\'][^"\']+["\']',
        r'private_key\s*[:=]\s*["\'][^"\']+["\']',
        r'access_key\s*[:=]\s*["\'][^"\']+["\']',
        r'secret_key\s*[:=]\s*["\'][^"\']+["\']',
    ]
    
    staged_files = run_git_command('git diff --cached --name-only')
    
    for file_path in staged_files:
        if not file_path:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern in sensitive_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    print(f"❌ WARNING: Found sensitive data in {file_path}")
                    print(f"   Pattern: {pattern}")
                    return False
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
    
    return True

def check_env_files():
    """Check for .env files being committed"""
    staged_files = run_git_command('git diff --cached --name-only')
    
    for file_path in staged_files:
        if file_path and (file_path.endswith('.env') or '.env.' in file_path):
            print(f"❌ WARNING: Found .env file being committed: {file_path}")
            print("   Environment files should not be committed to version control.")
            print("   Please add them to .gitignore and use .env.example instead.")
            return False
    
    return True

def check_certificate_files():
    """Check for certificate/key files being committed"""
    staged_files = run_git_command('git diff --cached --name-only')
    
    cert_extensions = ['.pem', '.key', '.crt', '.p12', '.pfx']
    
    for file_path in staged_files:
        if file_path and any(file_path.endswith(ext) for ext in cert_extensions):
            print(f"❌ WARNING: Found certificate/key file being committed: {file_path}")
            print("   Certificate and key files should not be committed to version control.")
            return False
    
    return True

def main():
    """Main security check function"""
    print("🔍 Checking for sensitive data...")
    
    # Run all checks
    checks = [
        ("Sensitive patterns", check_sensitive_patterns),
        ("Environment files", check_env_files),
        ("Certificate files", check_certificate_files),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
            print(f"   ❌ {check_name} check failed")
        else:
            print(f"   ✅ {check_name} check passed")
    
    if all_passed:
        print("✅ All security checks passed. Proceeding with commit...")
        return 0
    else:
        print("\n❌ Security checks failed. Please review and fix issues before committing.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 