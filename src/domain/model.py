

class Polygon:
    def __init__(self, name: str, geom: list):
        self.name = name
        self.geom = geom or None
        self.geom_json = None

    def add_point(self, point: tuple):
        self.geom.append(point)


class Project:
    def __init__(self, name, description):
        self.id = None
        self.name = name
        self.description = description
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)
