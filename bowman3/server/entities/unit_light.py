from .unit import Unit

class Light(Unit):
    ATACK = 125
    DEFENSEL = 20
    DEFENSEB = 10
    DEFENSEH = 30
    HEALTH = 800
    SPEED = 1.9
    RANGE = 2
    MISSCHANCE = 10
    def __init__(player):
        self.player = player