import pygame

class Tiles:

    def __init__(self, target_surface):
        """Target_surface can be a image then input the file name or a Surface"""
        if isinstance(target_surface, pygame.Surface):
            self.sheet = target_surface.convert_alpha()
        else:
            self.sheet = pygame.image.load(target_surface).convert_alpha()

        self.width = self.sheet.get_width()
        self.height = self.sheet.get_height()

    # Load a specific image from a specific rectangle
    def load_image_at(self, rectangle: tuple, colorkey = None):
        "Loads image from x, y, x+offset, y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill((0, 0, 0, 0))
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    # Load a whole bunch of images and return them as a list
    def load_images_at(self, rects: list[tuple], colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.load_image_at(rect, colorkey) for rect in rects]
    
    # Load a whole strip of images
    def load_allimages(self, image_size: int, colorkey = None):
        "Divide the whole images in tiles of the size input and return them as a list"
        assert self.width%image_size == 0 and self.height%image_size == 0, 'The image size must be a multiple of the height and width of your Surface'
        lenght_w = self.width // image_size
        lenght_h = self.height // image_size

        tups = [(image_size*x, image_size*y, image_size, image_size) for y in range(lenght_h) for x in range(lenght_w)]
        return self.load_images_at(tups, colorkey)