from model.project import Project
import re


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php")):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    project_cache = None

    def get_projects_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.project_cache = []
            all_rows = wd.find_elements_by_css_selector(".width100 .row-1") + wd.find_elements_by_css_selector(
                ".width100 .row-2")
            for row in all_rows:
                name_cell = row.find_elements_by_tag_name("td")[0]
                name_link = name_cell.find_element_by_tag_name("a")
                name = name_link.text
                link = name_link.get_attribute("href")
                project_id_full = re.search(r"project_id=\d+", link).group()
                project_id = re.sub("project_id=", "", project_id_full)
                self.project_cache.append(Project(project_name=name, project_id=project_id))
        return list(self.project_cache)

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_xpath("//td[@class='form-title']//input[@class='button-small']").click()
        self.fill_project_form(project)
        wd.find_element_by_class_name("button").click()
        self.open_projects_page()
        self.project_cache = None

    def fill_project_form(self, project):
        self.change_field_value("name", project.project_name)
        self.change_field_value("description", project.description)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_projects_page()
        self.select_project_by_id(id)
        wd.find_element_by_xpath("//div[@class='border center']//input[@class='button']").click()
        wd.find_element_by_xpath("//input[@class='button']").click()
        self.open_projects_page()
        self.project_cache = None

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath("//table[@class='width100']//a[contains(@href, 'project_id=%s')]" % id).click()
