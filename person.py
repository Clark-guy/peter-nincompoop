#person class. superclass for both npc and player


class person(object):
    def __init__(self, name, brave, maxHealth, health, sprite, facingLeft):
        self.name = name
        self.brave = brave
        self.maxHealth = maxHealth
        self.health = health
        self.sprite = sprite
        self.facingLeft = facingLeft
        self.lastUpdated = 0

    def get_brave(self):
        return self.brave

    def get_maxhealth(self):
        return self.maxHealth

    def get_health(self):
        return self.health

    def get_sprite(self):
        return self.sprite
    
    def get_facing(self):
        return self.facingLeft
    
    def set_facing(self, LR):
        self.facingLeft = LR

    def get_last_updated(self):
        return self.lastUpdated

    def set_last_updated(self, value):
        self.lastUpdated = value

class player(person):
    def __init__(self, name, brave, maxHealth, health, sprite, facingLeft):
        super().__init__(name, brave, maxHealth, health, sprite, facingLeft)

class npc(person):
    def __init__(self, name, brave, maxHealth, health, sprite, facingLeft):
        super().__init__(name, brave, maxHealth, health, sprite, facingLeft)

