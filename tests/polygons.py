def test_polygon_creation():
    # Given
    points = [(1, 0), (1, 1), (2, 1), (2, 0), (1, 0)]

    # When
    result = Polygon(
        name="rectangle",
        points=points,
    )

    # Then
    geo_json = result.geo.json()

    assert geo_json["type"] == "Feature"
    assert geo_json["properties"] == {}
    assert geo_json["geometry"]["type"] == "Polygon"
    assert len(geo_json["geometry"]["coordinates"]) == len(points)
