"""
Vulnerable Code Sample for Testing
This file contains intentional security vulnerabilities for testing the scanner
"""

import sqlite3
import os
import subprocess
import hashlib
import random

# SQL Injection Vulnerabilities
def get_user_by_id_vulnerable(user_id):
    """VULNERABLE: SQL Injection via string formatting"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Vulnerability 1: String concatenation
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    
    # Vulnerability 2: String formatting with %
    query2 = "SELECT * FROM users WHERE username = '%s'" % user_id
    cursor.execute(query2)
    
    # Vulnerability 3: f-string
    query3 = f"SELECT * FROM users WHERE email = '{user_id}'"
    cursor.execute(query3)
    
    return cursor.fetchall()


# XSS Vulnerabilities
def render_user_profile_vulnerable(username):
    """VULNERABLE: XSS via unsafe rendering"""
    from flask import Flask, render_template_string
    
    # Vulnerability: Direct rendering without escaping
    html = f"<div class='profile'><h1>Welcome {username}</h1></div>"
    return render_template_string(html)


# Command Injection Vulnerabilities
def backup_file_vulnerable(filename):
    """VULNERABLE: Command injection"""
    # Vulnerability 1: os.system with user input
    os.system(f"tar -czf backup.tar.gz {filename}")
    
    # Vulnerability 2: subprocess with shell=True
    subprocess.call(f"cp {filename} /backup/", shell=True)


# Path Traversal Vulnerabilities
def read_user_file_vulnerable(filename):
    """VULNERABLE: Path traversal"""
    # Vulnerability: User-controlled file path
    with open(f"/var/www/uploads/{filename}", 'r') as f:
        return f.read()


# Hardcoded Secrets
def connect_to_database_vulnerable():
    """VULNERABLE: Hardcoded credentials"""
    # Vulnerability 1: Hardcoded password
    password = "MySecretPassword123!"
    
    # Vulnerability 2: Hardcoded API key
    api_key = "sk_live_51H7xYzAbCdEfGhIjKlMnOpQrStUvWxYz"
    
    # Vulnerability 3: Hardcoded database credentials
    db_password = "admin123"
    
    conn = sqlite3.connect('database.db')
    return conn


# Weak Cryptography
def hash_password_vulnerable(password):
    """VULNERABLE: Weak hashing algorithm"""
    # Vulnerability 1: MD5 is broken
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    # Vulnerability 2: SHA1 is weak
    hashed2 = hashlib.sha1(password.encode()).hexdigest()
    
    return hashed


def generate_token_vulnerable():
    """VULNERABLE: Insecure random number generation"""
    # Vulnerability: Using random instead of secrets for security token
    token = ''.join([str(random.randint(0, 9)) for _ in range(32)])
    return token


# eval/exec vulnerabilities
def execute_user_code_vulnerable(user_code):
    """VULNERABLE: Code injection via eval"""
    # Vulnerability: eval with user input
    result = eval(user_code)
    
    # Vulnerability: exec with user input
    exec(user_code)
    
    return result


if __name__ == "__main__":
    print("This is a vulnerable code sample for testing purposes only!")
    print("DO NOT use this code in production!")
