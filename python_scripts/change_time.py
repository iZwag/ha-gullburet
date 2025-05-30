DAY_IN_SECONDS = 60 * 60 * 24

# Get the input values from the data dictionary
delta_minutes = data.get("delta_minutes")
entity_id = data.get("entity_id")

time_state = hass.states.get(entity_id).state.split(":")

time_seconds = int(time_state[0]) * 3600 + int(time_state[1]) * 60

new_time = time_seconds + (delta_minutes * 60)

if new_time < 0:
    new_time += DAY_IN_SECONDS
elif new_time >= DAY_IN_SECONDS:
    new_time -= DAY_IN_SECONDS

new_time_hours = new_time // 3600
new_time_mins = (new_time % 3600) // 60

time_result = f"{str(new_time_hours).zfill(2)}:{str(new_time_mins).zfill(2)}:00"

service_data = {
    "entity_id": entity_id,
    "time": time_result
}

hass.services.call(domain="input_datetime", service="set_datetime", service_data=service_data)
