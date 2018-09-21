# -*-: coding utf-8 -*-
""" Philips Hue skill for Snips. """

import requests
import json
import time
from hue_setup import HueSetup
from hue_scene import HueScenes

class SnipsHue:
    """ Philips Hue skill for Snips. """

    def __init__(self, hostname=None, username=None, locale=None):
        """ Initialisation.

        :param hostname: Philips Hue hostname
        :param username: Philips Hue username
        :param light_ids: Philips Hue light ids
        """
        self.username  = username
        self.hostname  = hostname
        if hostname is None or username is None:
            setup = HueSetup(hostname, username)
            url = setup.bridge_url
            self.username  = setup.get_username()
            self.hostname  = setup.get_bridge_ip()
            print(setup.bridge_url)
            print str(url)
        else:
            url = 'http://{}/api/{}'.format(hostname, username)

        self.lights_endpoint = url + "/lights"
        self.groups_endpoint = url + "/groups"
        self.config_endpoint = url + "/config"
        self.scenes_endpoint = url + "/scenes"

        # from <room_name> -> <room_id>
        self.roomName_roomId = self._get_room_id_table()

    #### section -> action handlers
    def light_on(self, room):
        if self.roomName_roomId.get(room) is None:
            return
        print ("[HUE] turn on")
        self._put_group_state({"on": True, "bri": 200, "hue": 39392,"sat": 13}, self.roomName_roomId[room])

    def light_on_all(self):
        for room in self.roomName_roomId.keys():
            self.light_on(room)

    def light_off(self, room):
        if self.roomName_roomId.get(room) is None:
            return
        print ("[HUE] turn off")
        self._put_group_state({"on": False}, self.roomName_roomId[room])

    def light_off_all(self):
        for room in self.roomName_roomId.keys():
            self.light_off(room)

    def light_brightness(self, percent, room):
        if self.roomName_roomId.get(room) is None:
            return
        print ("[HUE] set brightness")
        """ Set a specified brightness [percent] to a hue light in [room] """
        brightness = int(round(percent * 254/100))
        self._put_group_state({"on": True, "bri": brightness}, self.roomName_roomId[room])

    def light_brightness_all(self, percent):
        for room in self.roomName_roomId.keys():
           self.light_brightness(percent, room) 

    def light_color(self, color_code, room):
        if self.roomName_roomId.get(room) is None:
            return
        print ("[HUE] set color")
        """ Set a specified [color] to a hue light in [room] """
        hue = int(color_code.split('x')[0])
        sat = int(color_code.split('x')[1])
        group_id = self.roomName_roomId[room]
        if self._is_group_on(group_id):
            self._put_group_state({"on": True, "sat": sat, "hue": hue}, group_id)
        else:
            self._put_group_state({"on": True, "bri": 200, "sat": sat, "hue": hue}, group_id)

    def light_color_all(self, color_code):
        for room in self.roomName_roomId.keys():
            self.light_color(color_code, room)

    def light_scene(self, scene_code, room):
        if self.roomName_roomId.get(room) is None:
            return
        print ("[HUE] set scene")
        """ Set a specified [scene] to a hue light in [room] """
        bri = int(scene_code.split('x')[0])
        hue = int(scene_code.split('x')[1])
        sat = int(scene_code.split('x')[2])
        
        self._put_group_state({"on": True, "bri":bri, "hue":hue, "sat":sat}, self.roomName_roomId[room])

    def light_scene_all(self, scene_code):
        for room in self.roomName_roomId.keys():
            self.light_scene(scene_code, room)
    
    def light_up(self, percent, room):
        if self.roomName_roomId.get(room) is None:
            return
        print ("[HUE] shift up, percent: "+ str(percent))

        cur_brightness = self._get_group_brightness(self.roomName_roomId[room])
        print cur_brightness
        if cur_brightness is None:
            return
        delt = int(round(percent * 254/100))

        new_bri = cur_brightness + delt

        if new_bri > 254:
            new_bri = 254
        if new_bri < 0:
            new_bri = 0
 
        self._put_group_state({"on": True, "bri": new_bri}, self.roomName_roomId[room])

    def light_up_all(self, percent):
        for room in self.roomName_roomId.keys():
            self.light_up(percent, room)
        
    def light_down(self, percent, room):
        if self.roomName_roomId.get(room) is None:
            return
        print ("[HUE] shift down, percent: "+ str(percent))

        cur_brightness = self._get_group_brightness(self.roomName_roomId[room])
        if cur_brightness is None:
            return
        delt = int(round(percent * 254/100))

        new_bri = cur_brightness - delt

        if new_bri > 254:
            new_bri = 254
        if new_bri < 0:
            new_bri = 0
 
        self._put_group_state({"on": True, "bri": new_bri}, self.roomName_roomId[room])

    def light_down_all(self, percent):
        for room in self.roomName_roomId.keys():
            self.light_down(percent, room)

    #### section -> send command to device
    def _put_group_state(self, payload, group_id):
        print("[HUE] Setting for group "+ str(group_id) + ": " + str(payload))

        try:
            url = "{}/{}/action".format(self.groups_endpoint, group_id)
            res = requests.put(url, data=json.dumps(payload), headers=None)
            print(res.text)
        except Exception as e:
            print(e)
            print("[HUE] Request timeout. Is the Hue Bridge reachable?")
            pass

    #### section -> get different info
    def _get_group_status(self, group_id):
        try:
            url = "{}/{}/".format(self.groups_endpoint, group_id)
            group_status = requests.get(url).json()
            return group_status
        except Exception as e:
            print(e)
            print("[HUE] Request timeout. Is the Hue Bridge reachable?")
            pass
    def _get_group_brightness(self, group_id):
        status = self._get_group_status(group_id)
        if status["action"].get("bri"):
            return status["action"]["bri"]
        else:
            return None
    def _is_group_on(self, group_id):
        status = self._get_group_status(group_id)

        if (status["state"]["all_on"] is True) or (status["state"]["any_on"] is True):
            return True
        else:
            return False
    def _get_room_id_table(self):
        groups = requests.get(self.groups_endpoint).json()
        room_id_table = {}
        for key, value in groups.iteritems():
            group = value
            if group.get("class") is not None:
                room_id_table[str.lower(str(group["class"]))] = str(key)
            if group.get("name") is not None:
                room_id_table[str.lower(str(group["name"].encode('utf-8')))] = str(key)
                # colletc room name, nlu injection
        print "[HUE] Available rooms: \n" + ("\n".join(room_id_table.keys()))
        return room_id_table