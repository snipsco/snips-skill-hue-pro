# Introduction

***The full documentation, please out [here](https://snips.gitbook.io/documentation/snips-app/smart-light-hue)***

This app is designed for Philips Hue smart lights. It allows a user to control lights in different rooms/ groups with Snips. This app supports color selection, built-in scenes, and brightness control. 

More functionality, for e.g. controling each individual light/ more bespoke scenes, please follow the "developer" section in order to customise your own bundle and action code.

<<<<<<< HEAD
# Usage of the documentation
The documentation is made for both end-user and voice app developer.
=======
# Useage of the documentation
>>>>>>> 6ac1e2bada23dff56e44d27dec8e2f687ff52941

If you are a ***maker***, you may only read the following sections:
- Installation with sam
- User configuration
- Troubleshooting

If you are a ***developer***, all the parts above will be helpful. Especially the following sections:
- Manual installation
- APP bundle design
- APP action code

# Installation with sam (Assistant & Action code)
> we suppose that you have already had [sam]() installed on your device. If not, please refer to [this page]()

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
If you do not run your snips assistant on an `armv7l` or `armv6l` microcomputer,`sam` will not work. But you can manually clone the skill repo to `/var/lib/snips/skills/` directory where the `snips-skill-server` based on. Please do:
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

# APP bundle design

When designing an intent, please follow the clean code rules in your mind. Which means that you should name your intent and its slots properly so that a third person beyond you and your user can also understand it.

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

# APP action code 

There are mainly two parts of code required. One for handling the intents from the mqtt bus, which usually named `action-{{action_name}.py`. The other one is usually the `class` of the devices, which contains all the functional methods/ attributes.

In this example we have `action-philips_hue.py` and `snipshue.py`. Moreover, there is a `snipshelpers` directory, which contains `config_parser` and `thread_handler` class. This two class are provided in the action code template within `action-{{action_name}.py` file. 

All the necessary files are listed below: 
```
└── snips-skill-hue-pro								
    ├── action-philips_hue.py       # main handler for intents
    ├── config.ini                  # app configuration
    ├── requirements.txt            # requirements for dependencies
    ├── setup.sh                    # setup script
    ├── snipshelpers                # useful tools
    │   ├── __init__.py 		
    │   ├── config_parser.py
    │   ├── singleton.py
    │   └── thread_handler.py
    └── snipshue                    # snipshue class
        ├── __init__.py
        ├── hue_setup.py
        └── snipshue.py
```

# Default handling

As we may have different default situation of slots, this section will explain the strategy used by this action code. There is no specific rule to handle this, so please refer to your use-case when making your design choice.

There are typically 3 different slot types in this bundle design. Different types need to be handled in different ways. 

<<<<<<< HEAD
### house_room (All the intent)
This slot exists in all the intents of this bundle, it is used to indicate the location of operation. 
=======
### § `house_room` (All the intent)
This slot exist in all the intents of this bundle, it is used to indicate the location of operation. 
>>>>>>> 6ac1e2bada23dff56e44d27dec8e2f687ff52941

As most of the user will set their room light by saying the room in the query, so we have made the following chart to explain what will happen under different defaults. 


<<<<<<< HEAD
> If you are targeting the user who is using the satellite configuration, the default `house_room` value also can be the `siteId` of the audio device. 

### percent (shiftUp, shiftDown)
This slot exists in the intent `shiftUp` and `shiftDown`, it is used to indicate the amount of the brightness change. 

We can say both "***please make room lighter***" or "***turn up the light by 50% ***"(based on the current brightness, add 50% of max more brightness). So we have made the following strategy to handle it.
=======
![flow chart](https://blobscdn.gitbook.com/v0/b/gitbook-28427.appspot.com/o/assets%2F-L5OxUOD7uLDGd059vYc%2F-LMh4F4vYg2kUqQW15fY%2F-LMh843PseFasjCNDeu1%2Fimage.png?alt=media&token=b1f283c5-851c-4b5e-812e-93e766a3b0c7)

### § `percent` (shiftUp, shiftDown)
This slot exist in the intent `shiftUp` and `shiftDown` , it is used to indicate the amount of the brightness change. 

We can say both "***please give me more ligth***" or "***turn up the light by 50%***"(based on the current brightness, add 50% of max more brightness). So we have made the following strategy to handle it.
>>>>>>> 6ac1e2bada23dff56e44d27dec8e2f687ff52941

![flow chart](https://blobscdn.gitbook.com/v0/b/gitbook-28427.appspot.com/o/assets%2F-L5OxUOD7uLDGd059vYc%2F-LMh4F4vYg2kUqQW15fY%2F-LMh8jtq500rdSXZ4UeE%2Fimage.png?alt=media&token=44e3b62c-b51f-40d5-9358-0001191f7445)

<<<<<<< HEAD
### percent (setBrightness), scene, color
All of the 3 slots exist in the intent for setting this info, so it does not make sense to have a `setColor` / `setScene` / `setBrightness` intent detected but there is no key info provided. To handle this kind of defaults, we decided that either make this slot mandatory when designing the intent or ignore this situation as nothing happened.
=======
### § `percent` (setBrightness), `scene`, `color`
All of the 3 slots exist in the intent for setting this info, so it does not make sense to have a `setColor` / `setScene` / `setBrightness` intent detected but there is no key info provided. To handle this kind of defaults, we decided that either to make this slot mandatory when design the intnet or ignore these situation like nothing happened.
>>>>>>> 6ac1e2bada23dff56e44d27dec8e2f687ff52941


