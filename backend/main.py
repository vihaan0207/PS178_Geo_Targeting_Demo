from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cells import cells
from hazards import flood_polygon
from geo_engine import (
    calculate_overlap,
    find_user_cell
)
from users import users

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "PS178 Geo Targeting Backend Running"
    }


@app.get("/sensors")
def get_sensors():

    sensors = [

        {
            "id": "H1",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "water_level": 42,
            "rainfall": 35,
            "temperature": 28
        },

        {
            "id": "H2",
            "latitude": 19.0800,
            "longitude": 72.8850,
            "water_level": 48,
            "rainfall": 42,
            "temperature": 28
        },

        {
            "id": "H3",
            "latitude": 19.0700,
            "longitude": 72.8900,
            "water_level": 37,
            "rainfall": 31,
            "temperature": 29
        },

        {
            "id": "H4",
            "latitude": 19.0850,
            "longitude": 72.8700,
            "water_level": 22,
            "rainfall": 18,
            "temperature": 29
        }

    ]

    return sensors

@app.get("/cells")
def get_cells():

    return cells

@app.get("/flood")
def get_flood():

    return {
        "risk": 91,
        "status": "HIGH",
        "polygon": flood_polygon
    }

@app.get("/targeting")
def get_targeting():

    results = []


    for cell in cells:

        overlap = calculate_overlap(
            flood_polygon,
            cell["area"]
        )


        if overlap >= 70:

            status = "IMMEDIATE DANGER"
            color = "red"


        elif overlap >= 30:

            status = "WARNING"
            color = "orange"


        else:

            status = "SAFE"
            color = "green"


        results.append({

            "cell_id": cell["id"],

            "overlap": overlap,

            "status": status,

            "color": color

        })


    return results

@app.get("/users")
def get_users():

    return users

@app.get("/alerts")
def get_alerts():

    targeting_results = []


    for cell in cells:

        overlap = calculate_overlap(
            flood_polygon,
            cell["area"]
        )


        if overlap >= 70:

            status = "EVACUATE"


        elif overlap >= 30:

            status = "PREPARE"


        else:

            status = "NO ALERT"


        targeting_results.append({

            "cell_id": cell["id"],

            "overlap": overlap,

            "status": status

        })


    alerts = []


    for user in users:

        user_cell = find_user_cell(
            user["latitude"],
            user["longitude"],
            cells
        )


        alert = "NO ALERT"


        for result in targeting_results:

            if result["cell_id"] == user_cell:

                alert = result["status"]


        alerts.append({

            "user_id": user["id"],

            "cell_id": user_cell,

            "alert": alert

        })


    return alerts