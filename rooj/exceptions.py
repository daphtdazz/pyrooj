class UnroojableObjectException(Exception):
    def __init__(self, obj):
        super(UnroojableObjectException, self).__init__(
            'Unroojable object: %r' % (obj,)
        )
