from shapely.geometry import Polygon


def calculate_overlap(
    hazard_coordinates,
    cell_coordinates
):

    # Shapely uses (longitude, latitude)
    hazard_points = [
        (point[1], point[0])
        for point in hazard_coordinates
    ]

    cell_points = [
        (point[1], point[0])
        for point in cell_coordinates
    ]

    hazard = Polygon(hazard_points)

    cell = Polygon(cell_points)

    if not cell.is_valid:
        cell = cell.buffer(0)

    if not hazard.is_valid:
        hazard = hazard.buffer(0)

    intersection = hazard.intersection(cell)

    if cell.area == 0:
        return 0

    overlap_percentage = (
        intersection.area / cell.area
    ) * 100

    return round(overlap_percentage, 2)

from shapely.geometry import Point


def find_user_cell(
    latitude,
    longitude,
    cells
):

    point = Point(
        longitude,
        latitude
    )


    for cell in cells:

        cell_points = [
            (p[1], p[0])
            for p in cell["area"]
        ]


        polygon = Polygon(
            cell_points
        )


        if polygon.contains(point):

            return cell["id"]


    return None