import pygame

class CameraGroup(pygame.sprite.Group):

    def __init__(self, dev_mode=False) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] //2
        self.half_h = self.display_surface.get_size()[1] //2

        self.dev_mode = dev_mode

    def center_target_camera(self, target) -> None:
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def get_offset(self) -> tuple:
        return self.offset

    def display(self, target) -> None:

        self.center_target_camera(target)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset

            if self.dev_mode:
                try:
                    sprite.dev_mode(self.display_surface, offset_pos)
                except AttributeError:
                    pass

            self.display_surface.blit(sprite.image, offset_pos)
            # pygame.draw.rect(self.display_surface , sprite.color, pygame.Rect(sprite.rect.left - self.offset.x, sprite.rect.top - self.offset.y, sprite.rect.width, sprite.rect.height))
        
class GUIGroup(pygame.sprite.Group):

    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def display(self) -> None:
        for sprite in self.sprites():
            try:
                self.display_surface.blit(sprite.image, sprite.rect)
            except AttributeError:
                pygame.draw.rect(self.display_surface , sprite.color, sprite.get_rect())