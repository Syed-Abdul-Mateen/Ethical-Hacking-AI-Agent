import os
import pickle
import subprocess

# VULNERABLE: Hardcoded secrets
API_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD = "super_secret_password_2024"

# VULNERABLE: Command injection
def run_command(user_input):
    os.system("ls " + user_input)
    subprocess.call("echo " + user_input, shell=True)

# VULNERABLE: SQL injection (Python)
def get_user(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()

# VULNERABLE: Insecure deserialization
def load_data(data):
    return pickle.loads(data)

# VULNERABLE: Path traversal
def read_file(filename):
    with open("/var/www/files/" + filename, "r") as f:
        return f.read()

# VULNERABLE: Weak cryptography
import hashlib
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# VULNERABLE: Debug/eval
def process(expr):
    return eval(expr)
