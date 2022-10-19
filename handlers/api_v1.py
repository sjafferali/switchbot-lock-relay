import cherrypy
from swlock import swdev
from decorators import needsauth
from cfg import LOCKID

DEVICE_CACHE = {}

class DeviceHandler(object):
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, device_id=None, **kwargs):
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'
        swdevice = DEVICE_CACHE.get(device_id)
        if not swdevice:
            swdevice = swdev.Lock(device_id)
            DEVICE_CACHE[device_id] = swdevice
        return swdevice.status()

    @needsauth()
    @cherrypy.tools.json_out()
    def POST(self, device_id=None, action=None, **kwargs):
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'

        assert device_id, f"{device_id} not passed"
        assert action in ["lock", "unlock"], f"{action} is invalid (valid: lock/unlock)"

        swdevice = DEVICE_CACHE.get(device_id)
        if not swdevice:
            swdevice = swdev.Lock(device_id)
            DEVICE_CACHE[device_id] = swdevice

        if action == "lock":
            return swdevice.lock()
        else:
            return swdevice.unlock()


class WebhookHandler(object):
    exposed = True


    @cherrypy.tools.json_in()
    def POST(self, **kwargs):
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'

        input_json = cherrypy.request.json
        context = input_json["context"]
        if context.get("deviceType") != "WoLock":
            return

        device_id = context.get("deviceMac")
        swdevice = DEVICE_CACHE.get(device_id)
        if not swdevice:
            swdevice = swdev.Lock(device_id)
            DEVICE_CACHE[device_id] = swdevice

        swdevice.update_status(context["lockState"])


class V1(object):
    exposed = True
    device = DeviceHandler()
    webhook = WebhookHandler()
