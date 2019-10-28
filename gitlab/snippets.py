from api import gitlab
from logging import info
from utilities import types


def all_snippets(projects):
    snippets = {}
    for project in projects:
        for key, value in project.items():
            details = gitlab.get_project_snippets(key)
            for item in details:
                snippets.update({item['id']: item['web_url']})
    return snippets


def get_snippet_raw(snippet_id):
    return gitlab.get_snippet_raw(snippet_id)


def sniff_secrets(snippets):
    if len(snippets.keys()) == 0:
        return []
    secrets = []
    monitor = types.SecretsMonitor()
    for snippet_id, snippet_url in snippets.items():
        raw_content = gitlab.get_snippet_raw(snippet_id)
        found_secrets = monitor.get_secrets(raw_content)
        for secret_type, secret in found_secrets.items():
            secrets.append(types.Secret(secret_type, secret, snippet_url))
    return secrets
