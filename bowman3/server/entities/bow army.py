from .army import Army

class BowArmy(Army):
    COUNT = 8
    ATACK = 20
    DEFENSEL = 10
    DEFENSEB = 15
    DEFENSEH = 10
    HEALTH = [80 for x in range (0, 10)]
    SPEED = 1
    RANGE = 8
    MISSCHANCE = 20
    def __init__(player):
        self.player = player