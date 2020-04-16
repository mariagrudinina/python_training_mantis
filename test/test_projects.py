import random
from datetime import datetime

from model.project import Project


def test_add_project(app):
    username = "administrator"
    password = "root"
    app.session.login(username, password)
    old_projects = app.soap.get_projects_list(username, password)
    project = Project(project_name="My test project " + str(datetime.now()))
    app.project.create(project)
    old_projects.append(project)
    new_projects = app.soap.get_projects_list(username, password)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
    app.session.logout()


def test_delete_project(app):
    username = "administrator"
    password = "root"
    app.session.login(username, password)
    old_projects = app.soap.get_projects_list(username, password)
    if len(old_projects) == 0:
        app.project.create(Project(project_name="My test project " + str(datetime.now())))
        old_projects = app.soap.get_projects_list(username, password)
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.project_id)
    old_projects.remove(project)
    new_projects = app.soap.get_projects_list(username, password)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
    app.session.logout()
