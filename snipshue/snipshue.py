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

        # from [room_name] -> [light_ids]
        self.lights_from_room = self._get_rooms_lights()
        # from [room_name] -> [room_id]
        self.roomName_roomId = self._get_rooms_id()

    #### section -> action handlers
    def light_on(self, room=None):
        print ("[HUE] turn on")
        """ Turn on Philips Hue lights in [room] """

        # By default, turn on the light and set its brightness around 80% of the max
        self._set_group_state({"on": True, "bri": 200}, self._get_group_id_from_room(room))

    def light_off(self, room=None):
        print ("[HUE] turn off")
        """ Turn off all Philips Hue lights in [room] """

        self._set_group_state({"on": False}, self._get_group_id_from_room(room))

    def light_brightness(self, percent, room=None):
        print ("[HUE] set brightness")
        """ Set a specified brightness [percent] to a hue light in [room] """
        print percent
        print type(percent)
        brightness = int(round(percent * 254/100))

        self._set_group_state({"on": True, "bri": brightness}, self._get_group_id_from_room(room))

    def light_color(self, color_code, room=None):
        print ("[HUE] set color")
        """ Set a specified [color] to a hue light in [room] """
        hue = int(color_code.split('x')[0])
        sat = int(color_code.split('x')[1])

        self._set_group_state({"on": True, "sat": sat, "hue": hue}, self._get_group_id_from_room(room))

    def light_scene(self, scene_code, room=None):
        print ("[HUE] set scene")
        """ Set a specified [scene] to a hue light in [room] """
        bri = int(scene_code.split('x')[0])
        hue = int(scene_code.split('x')[1])
        sat = int(scene_code.split('x')[2])
        
        self._set_group_state({"on": True, "bri":bri, "hue":hue, "sat":sat, "colormode":"xy"}, self._get_group_id_from_room(room))

    def light_up(self, percent, room=None):
        print ("[HUE] shift up")
        """ Increase Philips Hue lights' intensity. """

        cur_brightness = self._get_group_brightness(self._get_group_id_from_room(room))
        delt = int(round(percent * 254/100))

        if len(self._get_group_id_from_room(room)>0):
            
        for key,val in cur_brightness:
            new_bri = val + delt

            if new_bri > 254:
                new_bri = 254
            if new_bri < 0:
                new_bri = 0
 
            self._put_group_state({"on": True, "bri": new_bri}, self._get_group_id_from_room(room)[key])

        new_bri = bri + delt

        if new_bri > 254:
            new_bri = 254
        if new_bri < 0:
            new_bri = 0

        self._put_group_state({"on": True, "bri": new_bri}, self._get_group_id_from_room(room))

    # def light_down(self, perentage, room=None):
    #     print ("[HUE] shift down")
    #     """ Lower Philips Hue lights' intensity. """
    #     brightness = int(round(percent * 254))

    #     light_ids = self._get_light_ids_from_room(room)
    #     lights_config = self._get_lights_config(light_ids)

    #     for light_id in light_ids:
    #         intensity = lights_config[light_id]["bri"]
    #         if intensity < perentage:
    #             intensity = 0
    #         else:
    #             intensity -= perentage
    #         self._post_state({"bri": intensity}, light_id)

    #### section -> send command to device
    # def _post_state_to_ids(self, params, light_ids):
    #     """ Post a state update to specyfied Philips Hue lights. """
    #     try:
    #         for light_id in light_ids:
    #             self._post_state(params, light_id)
    #             time.sleep(0.2)
    #     except Exception as e:
    #         return

    # def _post_state(self, params, light_id):
    #     """ Post a state update to a given light.

    #     :param params: Philips Hue request parameters.
    #     :param light_id: Philips Hue light ID.
    #     """
    #     if (light_id is None) or (params is None):
    #         return

    #     print("[HUE] Setting state for light " +
    #           str(light_id) + ": " + str(params))
    #     try:
    #         url = "{}/{}/state".format(self.lights_endpoint, light_id)
    #         requests.put(url, data=json.dumps(params), headers=None)
    #     except:
    #         print("[HUE] Request timeout. Is the Hue Bridge reachable?")
    #         pass

    def _set_group_state(self, payload, group_id=None):
        if (payload is None) or (group_id is None) :
            return

        if len(group_id)>0:
            for i in group_id:
                self._put_group_state(i, payload)
                time.sleep(.1)
        else:
            self._put_group_state(group_id, payload)
        

    def _put_group_state(self, group_id, payload):
        print("[HUE] Setting scene for group "+ str(group_id) + ": " + str(payload))

        try:
            url = "{}/{}/action".format(self.groups_endpoint, group_id)
            res = requests.put(url, data=json.dumps(payload), headers=None)
            print("[HUE] payload: "+json.dumps(payload))
            print(res.text)
        except Exception as e:
            print(e)
            print("[HUE] Request timeout. Is the Hue Bridge reachable?")
            pass

    #### section -> get different info from bridge

    def _get_group_brightness(self, group_id):
        url = "{}/{}/".format(self.groups_endpoint, group_id)

        if len(group_id)>0
            
            for i in group_id:
                url = "{}/{}/".format(self.groups_endpoint, i)
                res.append(requests.get(url).json().get("action")["bri"])
            
            return res

        url = "{}/{}/".format(self.groups_endpoint, group_id)
        return requests.get(url).json().get("action")["bri"]
        

    def _get_group_id_from_room(self, room=None):
        if room is not None:
            room = room.lower()

        if room is None:
            return self._get_all_group_ids()

        if self.roomName_roomId.get(room) is None:
            return

        return self.roomName_roomId[room]
        

    def _get_all_group_ids(self):
        groups = requests.get(self.groups_endpoint).json()
        return groups.keys()

    def _get_lights_config(self, light_ids):
        """ Make a get request to get infos about the current state of the given lights """
        lights = {}

        for light_id in light_ids:
            current_config = requests.get(self.lights_endpoint + "/" + str(light_id)).json()["state"]
            lights[light_id] = current_config

        return lights

    def _get_all_lights(self):
        lights = requests.get(self.lights_endpoint).json()
        return lights.keys()

    def _get_all_lights_name(self):
        lights = requests.get(self.lights_endpoint).json()
        names = [(key, value.get("name")) for key, value in lights.iteritems()]
        return  names

    def _get_light_ids_from_room(self, room):
        """ Returns the list of lights in a [room] or all light_ids if [room] is None """
        if room is not None:
            room = room.lower()

        if room is None or self.lights_from_room.get(room) is None:
            return self._get_all_lights()

        return self.lights_from_room[room]

    def _get_rooms_lights(self):
        """ Returns a dict {"room_name": {"light1", "light2"}, ...} after calling the Hue API """
        groups = requests.get(self.groups_endpoint).json()
        ids_from_room = {}
        for key, value in groups.iteritems():
            group = value
            if group.get("class") is not None:
                ids_from_room[str.lower(str(group["class"]))] = [str(x) for x in group["lights"]]
            if group.get("name") is not None:
                ids_from_room[str.lower(str(group["name"].encode('utf-8')))] = [str(x) for x in group["lights"]]
        print "[HUE] Available rooms: \n" + ("\n".join(ids_from_room.keys()))

        return ids_from_room

    def _get_rooms_id(self):
        groups = requests.get(self.groups_endpoint).json()
        ids_from_room = {}
        for key, value in groups.iteritems():
            group = value
            if group.get("class") is not None:
                ids_from_room[str.lower(str(group["class"]))] = str(key)
            if group.get("name") is not None:
                ids_from_room[str.lower(str(group["name"].encode('utf-8')))] = str(key)
                # colletc room name, nlu injection

        return ids_from_room
    




