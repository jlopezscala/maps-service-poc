from src.domain import model


class ProjectRepository:
    def __init__(self, session):
        self.session = session

    def add(self, project):
        self.session.add(project)

    def get(self, project_id):
        return self.session.get(model.Project, project_id)
