class RoojableType(type):

    registered_roojables = {}

    def __new__(cls, name, bases, cdict):
        new_class = super(RoojableType, cls).__new__(cls, name, bases, cdict)

        if name in RoojableType.registered_roojables:
            raise KeyError('Roojable class has duplicate name: {name}'.format(
                **locals())
            )

        RoojableType.registered_roojables[name] = new_class
        return new_class

    @classmethod
    def get_roojable_class(cls, name):
        return cls.registered_roojables[name]
