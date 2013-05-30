class World:
    _instance = None

    @staticmethod
    def getInstance():
        if World._instance is not None:
            return World._instance
        else:
            instance = World()
            World._instance = instance
