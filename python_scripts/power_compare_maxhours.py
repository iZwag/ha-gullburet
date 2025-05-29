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
newhour_value = float(data.get("newhour_value"))
newhour_time = data.get("newhour_time")

maxhour_1_entity = data.get("top_maxhour_val_1")
maxhour_2_entity = data.get("top_maxhour_val_2")
maxhour_3_entity = data.get("top_maxhour_val_3")
maxhour_4_entity = data.get("top_maxhour_val_4")
maxhour_1_time_entity = data.get("top_maxhour_time_1")
maxhour_2_time_entity = data.get("top_maxhour_time_2")
maxhour_3_time_entity = data.get("top_maxhour_time_3")
maxhour_4_time_entity = data.get("top_maxhour_time_4")

# Get current state values for the entities
# kWh - example: 1.23 kWh
maxhour_1 = hass.states.get(maxhour_1_entity).state
maxhour_2 = hass.states.get(maxhour_2_entity).state
maxhour_3 = hass.states.get(maxhour_3_entity).state
maxhour_4 = hass.states.get(maxhour_4_entity).state
# datetime - example: "2025-05-01T23:00:00"
maxhour_1_time = hass.states.get(maxhour_1_time_entity).state
maxhour_2_time = hass.states.get(maxhour_2_time_entity).state
maxhour_3_time = hass.states.get(maxhour_3_time_entity).state
maxhour_4_time = hass.states.get(maxhour_4_time_entity).state

maxhours = [
    {'power': float(maxhour_1), 'time': maxhour_1_time},
    {'power': float(maxhour_2), 'time': maxhour_2_time},
    {'power': float(maxhour_3), 'time': maxhour_3_time},
    {'power': float(maxhour_4), 'time': maxhour_4_time}
]

inserted = False

# Loop through the list of maxhours, descending
for i in range(len(maxhours)):

    # Quit comparing if new_value is less than an exists value and its the same date
    if (newhour_value < maxhours[i]['power']) and (get_date(maxhours[i]['time']) == get_date(newhour_time)):
        break

    # Compare newhour_value to maxhours(i) - Insert if found
    if (newhour_value > maxhours[i]['power']) and not inserted:
        maxhours.insert(i, {'power': float(newhour_value), 'time': newhour_time})
        inserted = True
        # Go to next loop iteration to not trigger the following if
        continue
    
    # Value been inserted, looking for same date - Remove if found
    if (get_date(maxhours[i]['time']) == get_date(newhour_time)) and inserted:
        maxhours.pop(i)
        # Loop can end: new_value inserted, same date handled, list has 4 elements
        break

# Handle if 5 elements
if len(maxhours) > 4:
    maxhours.pop(4)

set_power(maxhour_1_entity, maxhours[0]['power'])
set_power(maxhour_2_entity, maxhours[1]['power'])
set_power(maxhour_3_entity, maxhours[2]['power'])
set_power(maxhour_4_entity, maxhours[3]['power'])
set_time(maxhour_1_time_entity, maxhours[0]['time'])
set_time(maxhour_2_time_entity, maxhours[1]['time'])
set_time(maxhour_3_time_entity, maxhours[2]['time'])
set_time(maxhour_4_time_entity, maxhours[3]['time'])