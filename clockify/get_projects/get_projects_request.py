from clockify.get_projects.get_project_model import ClockifyProject
from clockify.run_clockify_request import get_clockify_request, CLOCKIFY_URL


def get_all_projects(workspace_id, apikey: str) -> tuple[bool, list[ClockifyProject]]:
    url = f'{CLOCKIFY_URL}/workspaces/{workspace_id}/projects'
    response = get_clockify_request(url, apikey)

    if 299 < response.status_code:
        return False, []

    content = response.json()

    return True, [ClockifyProject(**project) for project in content if not project['archived']]
