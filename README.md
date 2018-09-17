# Snips hue skill

This skill is designed for Philips Hue smart light

# Intent handler design

## turnOn
### Slots
`house_room` 

### Purpose
Turn on the light, set to 80% of max brightness

### Default handling
- `if the house_room is empty` then `turn all the lights on`
- `if the house_room not found` then `do nothing`


## turnOff
### Slots
`house_room` 

### Purpose
Turn on the light, set to 80% of max brightness

### Default handling
- `if the house_room is empty` then `turn all the lights off`
- `if the house_room does not exist` then `do nothing`


## setBrightness
### Slots
`house_room` `percent`
### Purpose
Turn the light to a specific brightness

### Default handling
- `if the house_room is empty` then `set the brightness for all the rooms`
- `if the house_room does not exist` then `do nothing`

## setColor
### Slots
`house_room` `color`
### Purpose
Set the light to a specific color
### Default handling
- `if the color is empty` then `do nothing`
- `if the house_room is empty` then `set the color to all the rooms`
- `if the house_room does not exist` then `do nothing`
- `if the light is on` then `apply the color`
- `if the light is off` then `turn on first, apply color secondly`


## setScene
### Slots
`house_room` `scene`
### Purpose
Set the light to a specific mode (e.g. sunset, concentrate, relax, sport..)
### Default handling
- `if the scene is empyt` then `do nothing`
- `if the house_room is empyt` then `apply to all the rooms`
- `if the house_room does not exist` then `do nothing`

## shiftUp
### Slots
`house_room` `percent`
### Purpose
Shift up the brightness based on the current brightness
### Default handling
- `if the house_room is empyt` then `apply to all the rooms`
- `if the house_room does not exist` then `do nothing`
- `if the percent is empty` then `consider it as 20% of max`

## shiftDown
### Slots
`house_room` `percent`
### Purpose
Shift down the brightness based on the current brightness
### Default handling
- `if the house_room is empty` then `apply to all the rooms`
- `if the house_room does not exist` then `do nothing`
- `if the percent is empty` then `consider it as 20% of max`

