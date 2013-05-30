from .army import Army

class HardArmy(Army):
    COUNT = 5
    ATACK = 15
    DEFENSEL = 30
    DEFENSEB = 40
    DEFENSEH = 25
    HEALTH = [300 for x in range (0, 10)]
    SPEED = 1
    RANGE = 1
    MISSCHANCE = 15
    def __init__(player):
        self.player = player