from suds.client import Client
from suds import WebFault

from model.project import Project


class SoapHelper:
    def __init__(self, app):
        self.app = app
        self.wsdl = "http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl"

    def can_login(self, username, password):
        client = Client(self.wsdl)
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self, username, password):
        client = Client(self.wsdl)
        projects = client.service.mc_projects_get_user_accessible(username, password)
        list_to_return = []
        for project in projects:
            list_to_return.append(Project(project_name=project["name"], project_id=project["id"]))
        return list_to_return
