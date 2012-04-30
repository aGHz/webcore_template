from web.core import Controller

class RootController(Controller):
    def __default__(self, *args, **kwargs):
        return '__project__'
