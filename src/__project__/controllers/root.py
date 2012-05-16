from web.core import Controller

from __project__.util.response import *

log = __import__('logging').getLogger(__name__)


class RootController(Controller):
    def __default__(self, *args, **kwargs):
        log.info('-- Request --')
        return TEMPLATE('index', {'project_name': '__project__'})

