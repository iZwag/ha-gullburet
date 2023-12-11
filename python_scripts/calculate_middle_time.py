# Get the input values from the data dictionary
inp_time1 = data.get("time1")
inp_time2 = data.get("time2")
entity_id = data.get("entity_id")

"""
# Convert input times to datetime objects
time1 = datetime.strptime(inp_time1, "%H:%M:%S")
time2 = datetime.strptime(inp_time2, "%H:%M:%S")
# Calculate middle time
middle_time = time1 + ((time2 - time1) / 2)
"""

# Convert input times to seconds since midnight
time1_parts = inp_time1.split("T")[1].split(":")
time2_parts = inp_time2.split("T")[1].split(":")
seconds1 = int(time1_parts[0]) * 3600 + int(time1_parts[1]) * 60
seconds2 = int(time2_parts[0]) * 3600 + int(time2_parts[1]) * 60

# Calculate middle time in seconds since midnight
middle_seconds = (seconds1 + seconds2) // 2
# Convert middle time back to hours and minutes
middle_hours = middle_seconds // 3600
middle_minutes = (middle_seconds % 3600) // 60

"""
# Format middle time
result = middle_time.strftime("%H:%M")

# Service call to set the input_datetime entity
service_data = {
    "entity_id": entity_id,
    "time": result
}
"""
"""
h_str = str(h).zfill(2)
m_str = str(m).zfill(2)
result = f"{h_str}:{m_str}"
""" 

"""
# Format middle time
result = middle_time.strftime("%H:%M")
"""

# Format middle time
result = f"{str(middle_hours).zfill(2)}:{str(middle_minutes).zfill(2)}"

# Get Middle time as local time
local_result = dt_util.as_local(dt_util.parse_datetime(inp_time2.split("T")[0] + "T" + result + ":00+00:00"))

service_data = {
    "entity_id": entity_id,
    "datetime": local_result
}

#local_time = str(local_result).split(" ")[1].split(":")
# Set the input_datetime entity
#hass.states.set(entity_id, local_time[0]+":"+local_time[1])

hass.services.call(domain="input_datetime", service="set_datetime", service_data=service_data)