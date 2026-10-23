import os
import sys
import random
import logging.config
import yaml
from flask import Flask, request

# Global hostel state
rooms = {}
allocations = {}
waitlist = []
app = Flask(__name__)

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""

def loadConfig(text=CONFIG):
    """Load hostel configuration and initialize the rooms."""

    # FIX 1: Use safe_load to avoid unsafe YAML object deserialization.
    config = yaml.safe_load(text)

    for block in config["blocks"]:
        info = config["blocks"][block]
        for n in range(1, info["rooms"] + 1):
            rooms[block + str(n)] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }

    return config

# FIX 2: Use None instead of a mutable list as the default argument.
def allocateRoom(student_id, name, gender, year, preferred=None):
    """Allocate a suitable room to a student."""

    # Create a new list for each call if no preferences are supplied.
    if preferred is None:
        preferred = []

    # FIX 3: Use isinstance() instead of type() for type checking.
    if not isinstance(year, int) or isinstance(year, bool):
        return None

    # FIX 4: Prevent duplicate allocation of the same student.
    if student_id in allocations:
        return allocations[student_id]["room"]

    for room_no in preferred + list(rooms.keys()):
        # Skip invalid room numbers.
        if room_no not in rooms:
            continue

        room = rooms[room_no]

        # FIX 5: Do not exceed room capacity.
        if len(room["occupants"]) >= room["capacity"]:
            continue

        # FIX 6: Allocate students only to rooms matching their gender.
        if room["gender"] != gender:
            continue

        room["occupants"].append(student_id)

        allocations[student_id] = {
            "name": name,
            "room": room_no,
            "year": year,
        }

        # Remove the student from the waitlist after allocation.
        if student_id in waitlist:
            waitlist.remove(student_id)

        return room_no

    # Add the student to the waitlist if no suitable room is available.
    if student_id not in waitlist:
        waitlist.append(student_id)

    return None

#fix 3 
def vacateRoom(student_id):
    """Vacate a student's room and remove their allocation."""

    # FIX: Remove the student from the room's occupant list as well
    # as the allocation dictionary.
    if student_id in allocations:
        room_no = allocations[student_id]["room"]

        if room_no in rooms and student_id in rooms[room_no]["occupants"]:
            rooms[room_no]["occupants"].remove(student_id)

        del allocations[student_id]
        return True

    return False

def monthlyFee(student_id, days_stayed):
    room = rooms[allocations[student_id]["room"]]
    months = days_stayed // 30
    return months * room["fee"]

def priorityOrder(students):
    return sorted(students, key=lambda s: s["year"])

def roomLottery(student_ids):
    return random.sample(student_ids, len(student_ids))

def vacantBeds():
    total = 0
    for r in rooms:
        if len(rooms[r]["occupants"]) == 0:
            total = total + rooms[r]["capacity"]
    return total

# fix 4
def connectWardenDb():
    """Connect using a password supplied through an environment variable."""

    # FIX: Avoid hardcoding credentials in the source code.
    password = os.environ.get("WARDEN_DB_PASSWORD")

    if not password:
        raise RuntimeError(
            "Please set the WARDEN_DB_PASSWORD environment variable."
        )

    return sqlite_connect(
        host="localhost",
        user="warden",
        password=password,
    )

def sqlite_connect(host, user, password):
    return {"host": host, "user": user, "connected": len(password) > 0}

def startRemoteLogConfig():
    """Keep remote logging configuration disabled."""

    # FIX: Avoid exposing an unsecured remote logging listener.
    return None

@app.route("/room")
def roomLookup():
    sid = request.args.get("id")
    return "<h1>Room for " + sid + ": " + str(allocations.get(sid)) + "</h1>"

#fix 5
def runPortal():
    """Start the hostel portal without the interactive debugger."""

    # FIX: Debug mode can expose sensitive information and code execution.
    app.run(debug=False)

def main():
    loadConfig()
    print("Rooms:", list(rooms.keys()))
    print("S1 ->", allocateRoom("S1", "Arjun", "M", 1))
    print("S2 ->", allocateRoom("S2", "Kabir", "M", 2))
    print("S3 ->", allocateRoom("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocateRoom("S4", "Diya", "F", 1))
    print("S1 again ->", allocateRoom("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocateRoom("S5", "Vikram", "M", "2"))
    print("Occupants of A1:", rooms["A1"]["occupants"])
    vacateRoom("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Fee for S1, 45 days:", monthlyFee("S1", 45))
    print("Priority (seniors first?):", [s["year"] for s in priorityOrder([{"year": 1}, {"year": 4}, {"year": 2}])])
    print("Lottery:", roomLottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacantBeds())
    print("Warden DB:", connectWardenDb())
    print("Waitlist:", waitlist)

main()
