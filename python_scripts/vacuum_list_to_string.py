rooms = {
    "kitchen": "Kitchen",       # 17
    "living": "Living room",    # 18
    "entry": "Entry",           # 16
    "guest": "Guest room",      # 19
    "bedroom": "Bedroom",       # 20
    "office": "Office"          # 21
 }

# Convert the keys of rooms to a list
# These are also expected inputs to the Python script
input_fields = list(rooms.keys())

rooms_str = ""

# All input rooms are checked if they are selected
# That means each corresponding input_boolean are turned "on"
# First word keeps its capital letter
# Wordlist gets comma-seperated
for room in input_fields:
    if data.get(room, "off") == "on":
        if len(rooms_str) > 0:
            rooms_str += rooms[room].lower() + ", "
        else:
            rooms_str += rooms[room] + ", "

# Remove last two characters ", "
if len(rooms_str) > 0:
    rooms_str = rooms_str[:-2]

output["rooms_str"] = rooms_str