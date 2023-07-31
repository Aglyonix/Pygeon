import pygame
from Behavior import Behavior
from Objects import *
from Bullets import *

class Player(Entity, Behavior):

    def __init__(self, pos=(0, 0), group=None) -> None:
        super().__init__(pos, 64, 64, group, 'Assets/CubePlayer.png', 6, 10)
        Behavior.__init__(self)

    def input(self) -> None:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_z] and not keys[pygame.K_s]:
            self.direction.y = -1
        elif keys[pygame.K_s] and not keys[pygame.K_z]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_q] and not keys[pygame.K_d]:
            self.direction.x = -1
        elif keys[pygame.K_d] and not keys[pygame.K_q]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def shoot(self, entitys, cursor, group) -> None:
        entitys.append(Bullet(self.rect, cursor.rect, self.damage, group))

    def dev_mode(self, surface, offset=pygame.Vector2(0, 0)):
        # pygame.draw.rect(surface, 'blue', pygame.Rect(self.rect.left - offset.x, self.rect.top - offset.y, self.rect.width, self.rect.height))
        pass

    def update(self, mobs, entitys, scene, dt, **kargs) -> None:
        self.input()
        self.move.stopOnCollision()
        self.behavior(self, mobs, entitys, scene.Objects, dt)