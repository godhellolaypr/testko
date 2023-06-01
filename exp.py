import gitlab
import os

# Set up the GitLab connection
gl = gitlab.Gitlab('https://erx-gitlab.centralindia.cloudapp.azure.com/', private_token='77Ri15K11vN8V4AaXb9U')

def clone_project(project):
    # Create a directory for the project
    os.makedirs(project.name, exist_ok=True)
    os.chdir(project.name)

    # Clone the project repository
    os.system(f'git clone {project.http_url_to_repo}')

    # Go back to the parent directory
    os.chdir('..')

def clone_projects_in_group(group):
    # Retrieve the projects in the group
    projects = group.projects.list(all=True)

    # Clone each project
    for project in projects:
        clone_project(project)

    # Retrieve the subgroups in the group
    subgroups = group.subgroups.list(all=True)

    # Clone projects in each subgroup recursively
    for subgroup in subgroups:
        subgroup_obj = gl.groups.get(subgroup.id)
        clone_projects_in_group(subgroup_obj)

# Retrieve the group
group = gl.groups.get('42')

# Clone projects in the group and its subgroups recursively
clone_projects_in_group(group)
