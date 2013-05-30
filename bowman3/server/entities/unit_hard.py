from .unit import Unit

class Light(Unit):
    ATACK = 80
    DEFENSEL = 20
    DEFENSEB = 30
    DEFENSEH = 20
    HEALTH = 1600
    SPEED = 1.0
    RANGE = 2
    MISSCHANCE = 10
    def __init__(player):
        self.player = player