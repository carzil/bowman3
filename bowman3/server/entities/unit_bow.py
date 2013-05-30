from .unit import Unit

class Light(Unit):
    ATACK = 100
    DEFENSEL = 20
    DEFENSEB = 20
    DEFENSEH = 20
    HEALTH = 600
    SPEED = 1.2
    RANGE = 8
    MISSCHANCE = 20
    def __init__(player):
        self.player = player