from pygame import *
from Behavior import *
from Objects import *

class Bullet(Entity, Behavior):

    def __init__(self, spawn_pos, target_pos, damage, group, filename='Assets\Bullet.png') -> None:
        self.group = group
        self.spawn_pos = self.get_spawn_pos(spawn_pos)
        self.target_pos = self.get_target_pos(target_pos)

        super().__init__(self.spawn_pos.topleft, 32, 32, group, filename, 12, damage)
        Behavior.__init__(self)

        self.calculatesdirection()

    def get_target_pos(self, target_pos) -> pygame.Rect:
        target = pygame.Rect(target_pos)
        return target

    def get_spawn_pos(self, spawn_pos) -> pygame.Rect:
        spawn = pygame.Rect(spawn_pos)
        spawn.x += spawn_pos.w // 4
        spawn.y += spawn_pos.h // 4
        return spawn

    def calculatesdirection(self) -> None:
        spawn_pos_center = self.spawn_pos.center
        target_pos_center = self.target_pos.center
        directionx, directiony = target_pos_center[0] - spawn_pos_center[0], target_pos_center[1] - spawn_pos_center[1]
        magnitude =  (directionx**2 + directiony**2)**0.5
        self.direction = [directionx / magnitude, directiony / magnitude]

    def dev_mode(self, surface, offset=pygame.Vector2(0, 0)):
        # pygame.draw.line(surface, 'green', self.spawn_pos.center - offset, self.target_pos.center - offset, 2)
        # pygame.draw.rect(surface, 'pink', pygame.Rect(self.target_pos.left - offset.x, self.target_pos.top - offset.y, self.target_pos.width, self.target_pos.height))
        pass

    def update(self, enemys, entitys, scene, dt, **kargs) -> None:
        self.move.destroyOnCollision()
        self.action.deal_damage(enemys)
        self.behavior(self, enemys, entitys, scene.Objects, dt)