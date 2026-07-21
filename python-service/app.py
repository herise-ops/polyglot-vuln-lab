import os
import sqlite3
import subprocess
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)
APP_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("LAB_DB_PATH", APP_DIR / "data" / "lab.db"))
INIT_SQL_PATH = APP_DIR / "init.sql"

# Fake hardcoded values for secret scanning.
PAYMENTS_API_KEY = "sk_test_000000000000000000000000"
DATABASE_PASSWORD = "SuperSecret123!"


def initialize_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        with sqlite3.connect(DB_PATH) as connection:
            connection.executescript(INIT_SQL_PATH.read_text(encoding="utf-8"))


@app.get("/health")
def health():
    return jsonify(status="ok", service="python")


@app.get("/api/search")
def search_users():
    term = request.args.get("q", "")
    sql = "SELECT id, username, email, role FROM users WHERE username LIKE ? OR email LIKE ?"
    params = (f"%{term}%", f"%{term}%")
    try:
        with sqlite3.connect(DB_PATH) as connection:
            connection.row_factory = sqlite3.Row
            rows = [dict(row) for row in connection.execute(sql, params).fetchall()]
        return jsonify(query=sql, results=rows)
    except sqlite3.Error as error:
        return jsonify(error=str(error), query=sql), 400


@app.get("/api/diagnostics")
def diagnostics():
    host = request.args.get("host", "localhost")
    command = f"ping -c 1 {host}"

    # INTENTIONAL COMMAND-INJECTION SINK.
    # Compose defaults LAB_UNSAFE_MODE to false, so the reachable lab behavior is simulated.
    if os.environ.get("LAB_UNSAFE_MODE", "false").lower() == "true":
        completed = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=3)
        output = completed.stdout + completed.stderr
        mode = "unsafe-isolated-container"
    else:
        simulated = f"SIMULATED ONLY: would execute: {command}"
        output = simulated + "\n"
        mode = "simulation"

    return jsonify(mode=mode, command=command, output=output)


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5001)
