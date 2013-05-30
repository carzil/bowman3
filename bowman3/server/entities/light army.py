from .army import Army

class LightArmy(Army):
    COUNT = 10
    ATACK = 25
    DEFENSEL = 20
    DEFENSEB = 10
    DEFENSEH = 15
    HEALTH = [100 for x in range (0, 10)]
    SPEED = 2
    RANGE = 1
    MISSCHANCE = 10
    def __init__(player):
        self.player = player