from pygame import *
from Behavior import *
from Objects import *

class Enemy(Entity, Behavior):

    def __init__(self, pos, group=None) -> None:
        super().__init__(pos, 64, 64, group, 'Assets\Enemy.png', 4, 10, 100, 100)
        Behavior.__init__(self)

    def dev_mode(self, surface, offset=pygame.Vector2(0, 0)):
        # pygame.draw.rect(surface, 'black', pygame.Rect(self.rect.left - offset.x, self.rect.top - offset.y, self.rect.width, self.rect.height))
        pass

    def update(self, pl, mobs, scene, entitys, dt, **kwargs) -> None:
        self.move.towardtarget(pl)
        self.behavior(self, mobs, entitys, scene.Objects, dt)