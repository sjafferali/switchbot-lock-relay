#!/usr/bin/env python
import cherrypy
from handlers import ApiHandler
from helpers.access import check_auth

class App:
    api = ApiHandler()

    @cherrypy.expose
    def index(self):
        yield "<h2>Switchbot Lock</h2><br>"

    @cherrypy.expose
    def health_check(self):
        return "OK"

CP_ENCODING_CONFIGS = {
    "tools.encode.on": True,
    "tools.encode.encoding": "utf-8",
    "tools.encode.text_only": False,
}
cherrypy.config.update(CP_ENCODING_CONFIGS)
cherrypy.config.update({
    "server.socket_host": "0.0.0.0",
    "server.socket_port": 8080,
    "tools.auth.on": True
})

app_config = {
    '/api': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    },
}
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth, priority=50)

if __name__ == '__main__':
    cherrypy.quickstart(App(), config=app_config)
else:
    application = cherrypy.Application(App(), config=app_config)
