import pygame
from Behavior import *
from Objects import *

class Mouse(Entity, Behavior):

    def __init__(self, group) -> None:
        super().__init__(pygame.mouse.get_pos(), 64, 64, group, 'Assets\crosshair.png')
        Behavior.__init__(self)
        self.group = group

    def dev_mode(self, surface, offset=pygame.Vector2(0, 0)):
        # pygame.draw.rect(surface, 'blue', pygame.Rect(self.rect.left - offset.x, self.rect.top - offset.y, self.rect.width, self.rect.height))
        pass

    def update(self, **kargs) -> None:
        pos = pygame.mouse.get_pos()
        self.rect.topleft = (pos[0] - (self.rect.width/2), pos[1] - (self.rect.height/2))
        self.rect.topleft += self.group.get_offset()