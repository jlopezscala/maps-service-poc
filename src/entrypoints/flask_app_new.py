from http import HTTPStatus

from flask import Flask
import json
import os

from src.adapters import orm
from src.domain.model import Project, Polygon
from src.service.unit_of_work import SqlAlchemyUnitOfWork

app = Flask(__name__)
geo_filename = os.path.join(app.static_folder, "data", "geo_map.json")
orm.start_mappers()


@app.route("/projects", methods=["POST"])
def create_project():
    with open(geo_filename) as geo_json_file:
        geo_data = json.load(geo_json_file)

    project = Project(name="aProject", description="aDescription")

    polygon_data = geo_data["features"][0]["geometry"]["coordinates"][0]
    # 'POLYGON((0 0,1 0,1 1,0 1,0 0))' formatting. Might not be needed if using PostGIS functions.
    polygon_repr = "POLYGON(({}))".format(
        ",".join([" ".join(map(str, point)) for point in polygon_data])
    )
    polygon = Polygon(name="aName", geom=polygon_repr)
    project.add_feature(polygon)
    with SqlAlchemyUnitOfWork() as uow:
        uow.projects.add(project)
        uow.commit()
        project_id = project.id

    return str(project_id), HTTPStatus.CREATED


@app.route("/projects/<project_id>", methods=["GET"])
def get_project(project_id):
    with SqlAlchemyUnitOfWork() as uow:
        return str(uow.projects.get(project_id))


if __name__ == "__main__":
    app.run()
