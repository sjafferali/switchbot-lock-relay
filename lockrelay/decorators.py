import cherrypy

def needsauth():
    '''A decorator that sets auth.require config
    variable.'''

    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'] = True
        return f

    return decorate
