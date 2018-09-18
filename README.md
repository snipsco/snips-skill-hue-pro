# Snips hue skill

This skill is designed for Philips Hue smart lights. It allows you to control the light in the different rooms/ group by using your voice. This skill support color control/ built-in scene control/ brightness control. The basic control unit is group(room). More fcuntionality, for e.g. to control each individual light/ more customized scenes, please follow the developing section to customise your own bundle and app.

# Useage of the documentation
The documentation is made for both end-user and voice app developer.

If you are an ***end-user***, you may only read the following sections:
- Installation with sam
- User configuration
- Troubleshooting

If you are a ***developer***, all the parts will be helpful. Especially the following sections:
- Manual installation
- Bundle design
- Coding archtecture

# Installation with sam (Assistant & Action code)
> we suppose that you have already have [sam]() installed on your device. If not, please refer to [this page]()

Run the following command to install assistant and its action code:
```
sam install assistant
```
Then select the assistant which contains `Smart Light - Hue` bundle.

# Installation with sam (Action code only)
If you are a snips-app developer, you may need to only install the action code from time to time.

> we suppose that you have already have [sam]() installed on your device. If not, please refer to [this page]()

Run the following command to install from `snips-skill-hue-pro` git repo:
```
sam install actions -g https://github.com/snipsco/snips-skill-hue-pro.git
```

Then `sam` will take care of the dependencies installation and put the skill at path `/var/lib/snips/skills/`. It will be run by the `snips-skill-server` component automatically.

# Manual installation (Action code only)
If you do not run your snips assistant on a `armv7l` or `armv6l` micro computer,`sam` will not work. But you can manually clone the skill repo to `/var/lib/snips/skills/` directory where the `snips-skill-server` based on. Please do:
```
cd /var/lib/snips/skills/
```
Then run: 
```
git cloen https://github.com/snipsco/snips-skill-hue-pro.git
```
Go to action code directory
```
cd snips-skill-hue-pro
```
Install:
> To be able to run the following code, you need to have `virtualenv` installed, if not please refer to [this page](https://virtualenv.pypa.io/en/stable/installation/)

```
sudo ./setup.sh
```



# Intents handler design
| Intent Name | turnOn |
| --- | --- |
| Slots | `house_room` |
| Purpose | Turn on the light |

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

