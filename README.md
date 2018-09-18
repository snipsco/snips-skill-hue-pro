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

# Bundle design

When design an intent, please follow the clean code rules in your mind. Which means that you should name your intent and its slots properly, so that a third person beyound you and your user can also understant it.

This table represent the bundle design of `Smart Light - Hue` :

| Intent | Slots | Description | 
| --- | --- | --- |
| turnOn | `house_room` | Turn on the light |
| turnOff| `house_room` | Turn off the light |
| setBrightness| `house_room` `percent` | Set the brightness |
| setColor| `house_room` `color` | Set the color |
| setScene| `house_room` `scene` | Set the light mode |
| shiftUp| `house_room` `percent` | Increase brightness |
| shiftDown| `house_room` `percent` | Decrease brightness |

# Coding archtecture 

There are mainly two parts of code required. One for handling the intents from mqtt bus, which usually named like `action-{{action_name}.py`. The other one is usually the `class` of the devices, which contains all the functional methods/ attributes.

In this example we have `action-philips_hue.py` and `snipshue.py`. 


# Default handler example for this bundle

As we may have different default situation of slots, this section will explain the strategy used by this action code. There is no sepcific rule to handle this, so pelase refer to your usecase to make your design choice.

There are typically 3 different slots type in this bundle design. Different types need to be handled in different ways. 

### house_room (All the intent)
This slot exist in all the intents of this bundle, it is used to indicate the location of operation. 

As most of the user will set their room light by saying the room in the query, so we have made the following chart to explain what will happen under different defaults. 

[flow chart]()

### percent (shiftUp, shiftDown)
This slot exist in the intent `shiftUp` and `shiftDown` , it is used to indicate the amount of the brightness change. 

We can say both "***please give me more ligth***" or "***turn up the light by 50%***"(based on the current brightness, add 50% of max more brightness). So we have made the following strategy to handle it.

[flow chart]()

### percent (setBrightness), scene, color
All of the 3 slots exist in the intent for setting this info, so it does not make sense to have a `setColor` / `setScene` / `setBrightness` intent detected but there is no key info provided. To handle this kind of defaults, we decided that either to make this slot mandatory when design the intnet or ignore these situation like nothing happened.


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

