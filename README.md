# Home Assistant // Gullburet

The nickname of our apartment is Gullburet.

## Hardware

The system is compromised of many hardware devices, obviously. 

### The system's central processor
- Raspberry Pi 4 model B 2GB
- Powered with 5V @3A USB-C PSU
- Kingston KC600 256GB SSD, connected to RPi with SATA-to-USB3 adapter
- Connected to Router with CAT-6 network cable
- ConBee II Stick (as Zigbee-controller)
- Aeotec Z-Stick 7 (as Z-Wave-controller)

### Router
The network router is of type Asus RT-AC88U.

### Wi-Fi Devices
- Mill Heaters
- Philips Hue
- Sonos

### Z-Wave Devices
- Fibaro Dimmer Switch 2
- Fibaro Switch 2
- Heat-it Z-TRM3

### Zigbee Devices
- TRÅDFRI Transformers
- IKEA Lightbulbs

## Software 

### Dashboard services
To display relevant info about life in Oslo and Norway, here are some public APIs we are consuming:
- Entur (Ruter): Public transportation
- Met.no (Yr): Weather
- Tibber: Local electricity ratings, including fees