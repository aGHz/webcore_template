from web.core import Controller

log = __import__('logging').getLogger(__name__)


class RootController(Controller):
    def __default__(self, *args, **kwargs):
        log.info('-- Request --')
        return '__project__'
