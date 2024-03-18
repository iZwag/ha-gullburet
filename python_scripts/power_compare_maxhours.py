def get_date(date_str: str):
    return date_str.split("T")[0]

def set_power(entity: str, value: float):
    service_data = {
        "entity_id": entity,
        "value": value
    }
    hass.services.call(domain="input_number", service="set_value", service_data=service_data)

def set_time(entity: str, time_str: str):
    service_data = {
        "entity_id": entity,
        "datetime": time_str
    }
    hass.services.call(domain="input_datetime", service="set_datetime", service_data=service_data)

# Import inputs
newhour_value = data.get("newhour_value")
newhour_time = data.get("newhour_time")

maxhour_1_entity = data.get("top_maxhour_val_1")
maxhour_2_entity = data.get("top_maxhour_val_2")
maxhour_3_entity = data.get("top_maxhour_val_3")
maxhour_1_time_entity = data.get("top_maxhour_time_1")
maxhour_2_time_entity = data.get("top_maxhour_time_2")
maxhour_3_time_entity = data.get("top_maxhour_time_3")

# Get current state values for the entities
# kWh
maxhour_1 = hass.states.get(maxhour_1_entity).state
maxhour_2 = hass.states.get(maxhour_2_entity).state
maxhour_3 = hass.states.get(maxhour_3_entity).state
# datetime
maxhour_1_time = hass.states.get(maxhour_1_time_entity).state
maxhour_2_time = hass.states.get(maxhour_2_time_entity).state
maxhour_3_time = hass.states.get(maxhour_3_time_entity).state

maxhours = [
    {'power': float(maxhour_1), 'time': maxhour_1_time},
    {'power': float(maxhour_2), 'time': maxhour_2_time},
    {'power': float(maxhour_3), 'time': maxhour_3_time}
]

new_date = True

# Loop and check if any of the maxhours are on the same date
for i in range(len(maxhours)):
    # Check if on the same date
    if (get_date(maxhours[i]['time']) == get_date(newhour_time)):
        # Set the new time and power
        maxhours[i]['time'] = newhour_time
        maxhours[i]['power'] = newhour_value
        # Sort the top maxhours by power-value in descending order
        maxhours.sort(key=lambda x: x['power'], reverse=True)
        # New-hour is added and handled, skip the next section
        new_date = False
        break

# If its a new date, add the new entry, sort the maxhours
#  and remove the last element to end up with 3 entries again.
if new_date:
    maxhours.append({'power': newhour_value, 'time': newhour_time})
    maxhours.sort(key=lambda x: x['power'], reverse=True)
    maxhours.pop()

set_power(maxhour_1_entity, maxhours[0]['power'])
set_power(maxhour_2_entity, maxhours[1]['power'])
set_power(maxhour_3_entity, maxhours[2]['power'])
set_time(maxhour_1_time_entity, maxhours[0]['time'])
set_time(maxhour_2_time_entity, maxhours[1]['time'])
set_time(maxhour_3_time_entity, maxhours[2]['time'])