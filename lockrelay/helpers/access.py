import cherrypy
from cfg import API_TOKEN

def is_token_valid(token):
    if token == API_TOKEN:
        return True
    return False

def check_auth():
    needs_auth = cherrypy.request.config.get('auth.require', False)

    if not needs_auth:
        return

    # process token auth
    token_header = cherrypy.request.headers.get('X-HTTP-APIKEY')
    if token_header and is_token_valid(token_header):
        return

    # return error
    cherrypy.response.status = 401
    cherrypy.response.headers['WWW-Authenticate'] = 'Basic realm="insert realm"'
    raise cherrypy.HTTPError(401)
