form .army 

class LightArmy(Army):
    count = 10
    atack = 25
    defense = 0
    health = 0
    speed = 0
    def __init__(player):
        self.player = player