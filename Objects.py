import pygame

class Object(pygame.sprite.Sprite):

    def __init__(self, pos=(0, 0), widht=32, height=32, group=None, filename=None) -> None:
        super().__init__(group)
        self.x = pos[0]
        self.y = pos[1]
        self.w = widht
        self.h = height
        self.direction = pygame.math.Vector2()

        if filename != None:
            self.image = pygame.image.load(filename).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            self.rect = self.image.get_rect(topleft=pos)
        else:
            self.rect = pygame.rect.Rect(pos[0], pos[1], self.w, self.h)


class Entity(Object):

    def __init__(self, pos=(0, 0), widht=32, height=32, group=None, filename=None, speed=0, damage=10, health=100, max_health=100) -> None:
        super().__init__(pos, widht, height, group, filename)
        self.max_h = max_health
        self.health = health

        self.damage = damage
        self.speed = speed