"""
INTENTIONALLY VULNERABLE CODE FOR SECURITY-SCANNER TESTING ONLY.
Do not deploy this file to a real environment.
"""

import sqlite3
import subprocess
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)

# Finding 1: Hardcoded secret
API_TOKEN = "test-api-token-123456789-not-real"


# Finding 2: SQL injection
@app.get("/test/search")
def unsafe_search():
    username = request.args.get("username", "")

    connection = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE username = '{username}'"

    results = connection.execute(query).fetchall()
    return str(results)


# Finding 3: Command injection
@app.get("/test/command")
def unsafe_command():
    command = request.args.get("command", "whoami")

    output = subprocess.check_output(
        command,
        shell=True,
        text=True,
    )

    return output


# Finding 4: Path traversal
@app.get("/test/file")
def unsafe_file_read():
    filename = request.args.get("filename", "")

    file_path = Path("uploads") / filename
    return file_path.read_text()


# Finding 5: Reflected XSS
@app.get("/test/message")
def unsafe_message():
    message = request.args.get("message", "")

    return f"<html><body><h1>{message}</h1></body></html>"