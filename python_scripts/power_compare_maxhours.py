# The purpose of this script is to compare the most recent hour's energy
#  consumption to the top 4 highest recorded energy-hours, and insert it if it
#  is higher than any of the existing records.
#
# Both the energy-value for the hour, and the date/time of when the hour started
#  are stored (in respective input_number and input_datetime entities).
# 
# Same date constraint:
#  - Only one record per date is allowed. So if the new hour is higher than an
#  existing record, but the same date already exists with a higher energy-value, 
# then the new hour will not be inserted. 


def get_date(date_str: str):
    if not date_str:
        return ""

    date_value = str(date_str).strip()
    if "T" in date_value:
        return date_value.split("T", 1)[0]
    if " " in date_value:
        return date_value.split(" ", 1)[0]
    return date_value[:10]

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

# Normalize existing top list first: only keep highest value per date.
by_date = {}
for record in maxhours:
    record_date = get_date(record['time'])
    existing = by_date.get(record_date)
    if existing is None or record['power'] > existing['power']:
        by_date[record_date] = {'power': record['power'], 'time': record['time']}

# Apply current hour with same-date replacement rule.
newhour_date = get_date(newhour_time)
existing_same_date = by_date.get(newhour_date)
if existing_same_date is None or newhour_value > existing_same_date['power']:
    by_date[newhour_date] = {'power': float(newhour_value), 'time': newhour_time}

# Build final ranked list and enforce exactly 4 output entries.
maxhours = sorted(by_date.values(), key=lambda item: item['power'], reverse=True)[:4]
while len(maxhours) < 4:
    maxhours.append({'power': 0.0, 'time': newhour_time})

set_power(maxhour_1_entity, maxhours[0]['power'])
set_power(maxhour_2_entity, maxhours[1]['power'])
set_power(maxhour_3_entity, maxhours[2]['power'])
set_power(maxhour_4_entity, maxhours[3]['power'])
set_time(maxhour_1_time_entity, maxhours[0]['time'])
set_time(maxhour_2_time_entity, maxhours[1]['time'])
set_time(maxhour_3_time_entity, maxhours[2]['time'])
set_time(maxhour_4_time_entity, maxhours[3]['time'])