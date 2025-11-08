# Get the input values from the data dictionary
inp_time1 = data.get("time1")
inp_time2 = data.get("time2")
entity_id = data.get("entity_id")

# Convert input times to seconds since midnight
time1_parts = inp_time1.split("T")[1].split(":")
time2_parts = inp_time2.split("T")[1].split(":")

# Simple timezone offset calculation based on date
# Get month from the timestamp to determine if we're in DST
month = int(inp_time2.split("T")[0].split("-")[1])
day = int(inp_time2.split("T")[0].split("-")[2])

# Norway DST rules: Last Sunday in March to last Sunday in October
# Simplified: March-October = CEST (+2), November-February = CET (+1)
if month >= 4 and month <= 9:
    # Definitely daylight saving time
    timezone_offset = 2
elif month == 3:
    # March: DST starts last Sunday, roughly after day 25
    timezone_offset = 2 if day >= 25 else 1
elif month == 10:
    # October: DST ends last Sunday, roughly after day 25
    timezone_offset = 1 if day >= 25 else 2
else:
    # November, December, January, February: standard time
    timezone_offset = 1

# Convert UTC times to local time seconds since midnight
seconds1 = int(time1_parts[0]) * 3600 + int(time1_parts[1]) * 60
seconds2 = int(time2_parts[0]) * 3600 + int(time2_parts[1]) * 60

# Apply timezone offset
local_seconds1 = (seconds1 + timezone_offset * 3600) % (24 * 3600)
local_seconds2 = (seconds2 + timezone_offset * 3600) % (24 * 3600)

# Calculate middle time in seconds since midnight (local time)
middle_seconds = (local_seconds1 + local_seconds2) // 2
# Convert middle time back to hours and minutes
middle_hours = middle_seconds // 3600
middle_minutes = (middle_seconds % 3600) // 60

# Format middle time
result = f"{str(middle_hours).zfill(2)}:{str(middle_minutes).zfill(2)}"

# For all entities, use the time format since we've already converted to local time
service_data = {
    "entity_id": entity_id,
    "time": result + ":00"
}

hass.services.call(domain="input_datetime", service="set_datetime", service_data=service_data)