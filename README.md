# Home Assistant // Gullburet

This repo contains (the shareable part of) my smart-home configuration. Orhcestration is handled by [Home Assistant](https://www.home-assistant.io/). 

What is *Gullburet*? It's the nickname of our apartment, and it means "the golden cage".

## Hardware

The system is compromised of many hardware devices, obviously. 

### The system's central processor
- Raspberry Pi 4 model B 2GB
- OS: Home Assistant OS
- PSU: 5V/3A USB-C
- Storage: Kingston KC600 256GB SSD, connected to RPi with SATA-to-USB3 adapter
- Network: CAT-6 network cable and Wi-Fi to router
- USB: ConBee II Stick (as Zigbee-controller)
- USB: Aeotec Z-Stick 7 (as Z-Wave-controller)

### Router
Asus RT-AC88U

### Wi-Fi/Network Devices
- Heating: Mill Heat (panel heaters, movable floor-unit)
- Lights: Philips Hue (bulbs, switches, sensors)
- Speakers: Sonos (Play:1, One, Beam)
- Robot vacuum: Roborock S7 Plus
- TV: Samsung The Frame 55"
- Tablet, wall-mounted dashboard: Lenovo Tab M10 FHD Plus

### Z-Wave Devices
- Fibaro Dimmer Switch 2
- Fibaro Switch 2
- Heat-it Z-TRM3

### Zigbee Devices
- IKEA TRÅDFRI: Transformers, lightbulbs, sockets, switches

## Software 

### Dashboard services
To display relevant info about life in Oslo and Norway, here are some public APIs we are consuming:
- Entur (Ruter): Public transportation
- Met.no (Yr): Weather
- Tibber: Local electricity ratings, including fees