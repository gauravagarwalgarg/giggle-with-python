"""GitLab API snippets connect, list projects, create merge requests."""
import os
import requests

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
PRIVATE_TOKEN = os.getenv("GITLAB_TOKEN", "")


def get_headers():
    return {"PRIVATE-TOKEN": PRIVATE_TOKEN}


def list_projects(search=""):
    """List projects, optionally filtering by search term."""
    resp = requests.get(
        f"{GITLAB_URL}/api/v4/projects",
        headers=get_headers(),
        params={"search": search, "per_page": 20}
    )
    resp.raise_for_status()
    return resp.json()


def get_project(project_id: int):
    """Get details of a specific project."""
    resp = requests.get(
        f"{GITLAB_URL}/api/v4/projects/{project_id}",
        headers=get_headers()
    )
    resp.raise_for_status()
    return resp.json()


def list_branches(project_id: int):
    """List all branches for a project."""
    resp = requests.get(
        f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/branches",
        headers=get_headers(),
        params={"per_page": 100}
    )
    resp.raise_for_status()
    return resp.json()


def create_merge_request(project_id: int, source_branch: str,
                         target_branch: str = "main", title: str = ""):
    """Create a merge request."""
    resp = requests.post(
        f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests",
        headers=get_headers(),
        json={
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title or f"Merge {source_branch} into {target_branch}",
        }
    )
    resp.raise_for_status()
    return resp.json()


def list_merge_requests(project_id: int, state: str = "opened"):
    """List merge requests for a project.

    state: opened, closed, merged, all
    """
    resp = requests.get(
        f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests",
        headers=get_headers(),
        params={"state": state, "per_page": 20}
    )
    resp.raise_for_status()
    return resp.json()


def get_pipeline_status(project_id: int, ref: str = "main"):
    """Get latest pipeline status for a branch."""
    resp = requests.get(
        f"{GITLAB_URL}/api/v4/projects/{project_id}/pipelines",
        headers=get_headers(),
        params={"ref": ref, "per_page": 1}
    )
    resp.raise_for_status()
    pipelines = resp.json()
    return pipelines[0] if pipelines else None


def trigger_pipeline(project_id: int, ref: str = "main", variables: dict = None):
    """Trigger a pipeline manually."""
    payload = {"ref": ref}
    if variables:
        payload["variables"] = [{"key": k, "value": v} for k, v in variables.items()]

    resp = requests.post(
        f"{GITLAB_URL}/api/v4/projects/{project_id}/pipeline",
        headers=get_headers(),
        json=payload
    )
    resp.raise_for_status()
    return resp.json()


def list_project_members(project_id: int):
    """List all members of a project."""
    resp = requests.get(
        f"{GITLAB_URL}/api/v4/projects/{project_id}/members/all",
        headers=get_headers(),
        params={"per_page": 100}
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    if not PRIVATE_TOKEN:
        print("Set GITLAB_TOKEN environment variable first:")
        print("  export GITLAB_TOKEN='your-token-here'")
        print("  export GITLAB_URL='https://gitlab.example.com'  # optional")
        exit(1)

    projects = list_projects("my-project")
    for p in projects:
        print(f"{p['id']}: {p['name']} {p['web_url']}")
