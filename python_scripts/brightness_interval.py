brightness = data.get('brightness')
entity_id = data.get('entity_id')

if entity_id is None:
    logger.error("Entity_id not provided")
    exit()

try:
    brightness = int(brightness)
except (TypeError, ValueError):
    brightness = 0

'''
if isinstance(brightness, dict):
    brightness = 0
elif isinstance(brightness, int):
    brightness = int(brightness)
elif brightness == "null":
    brightness = 0
else:
    try:
        brightness = int(brightness)
    except (TypeError, ValueError):
        brightness = 0
'''

#brightness = int(brightness)

# Convert the brightness (0-255) to percentage and round it
brightness_percent = round((brightness / 255) * 100)

if brightness_percent <= 0:
    interval = 0
elif 0 < brightness_percent <= 5:
    interval = 5
elif 5 < brightness_percent <= 10:
    interval = 10
elif 10 < brightness_percent <= 15:
    interval = 15
elif 15 < brightness_percent <= 20:
    interval = 20
elif 20 < brightness_percent <= 25:
    interval = 25
elif 25 < brightness_percent <= 30:
    interval = 30
elif 30 < brightness_percent <= 40:
    interval = 40
elif 40 < brightness_percent <= 50:
    interval = 50
elif 50 < brightness_percent <= 60:
    interval = 60
elif 60 < brightness_percent <= 70:
    interval = 70
elif 70 < brightness_percent <= 80:
    interval = 80
elif 80 < brightness_percent <= 90:
    interval = 90
elif 90 < brightness_percent:
    interval = 100
else:
    interval = 0

# Set the state of the specified sensor entity
current_attributes = hass.states.get(entity_id).attributes if hass.states.get(entity_id) else {}
hass.states.set(entity_id, interval, current_attributes)