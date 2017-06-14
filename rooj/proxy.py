from .roojable import Roojable


class RoojProxy(Roojable):

    @property
    def proxied_class(self):
        return type(self._obj).__name__

    @property
    def rooj_self(self):
        return self._obj.rooj_self

    def __init__(self, obj):
        super(RoojProxy, self).__init__()
        self._obj = obj
