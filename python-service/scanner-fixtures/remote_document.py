import requests
from flask import Request


def load_remote_document(request: Request) -> str:
    target_url = request.args.get("url", "")

    # INTENTIONAL SSRF SCANNER FIXTURE:
    # A user-controlled URL is requested by the server.
    response = requests.get(target_url, timeout=10)

    return response.text