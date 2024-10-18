# Input fields to the script
entity_id = data.get("entity_id")
room_id = data.get('room_id')

current_ids = hass.states.get(entity_id).state

# Remove brackets
current_ids = current_ids.replace("[", "")
current_ids = current_ids.replace("]", "")

# If current_ids is not empty, split into a list, else start with an empty list
if current_ids:
    room_ids = current_ids.split(',')
else:
    room_ids = []

# Check if room_id is in the list
if room_id in room_ids:
    # If room_id is in the list, remove it
    room_ids.remove(room_id)

    # Join the list back into a comma-separated string and set the input_text value
    hass.services.call('input_text', 'set_value', {
        'entity_id': entity_id,
        'value': '[' + ','.join(room_ids) + ']'
    })
