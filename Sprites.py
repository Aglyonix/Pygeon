import pygame
import random

from Tiles import Tiles
from Behavior import Behavior

class Area(pygame.sprite.Sprite, Behavior):

    def __init__(self, group: object, tag={'rect':(0, 0, 200, 200), 'color':None, 'txt:':{'Font':None, 'Text':'', 'size':20 ,'antialias': False, 'color':'white'}}) -> None:
        super().__init__(group)
        Behavior.__init__(self)
        self.Font = pygame.font.Font(tag['txt']['Font'], tag['txt']['size'])
        self.Text = self.Font.render(tag['txt']['Text'], tag['txt']['antialias'], tag['txt']['color'])

        self.tag = tag
        self.color = tag['color']
        self.rect = pygame.Rect((tag['rect'][0], tag['rect'][1]),(tag['rect'][2], tag['rect'][3]))
    
class Grass(pygame.sprite.Sprite, Behavior):

    def __init__(self, pos: tuple, group: object, tag={}) -> None:
        super().__init__(group)
        Behavior.__init__(self)
        self.GrassPng = Tiles('Assets\Texture\TX Tileset Grass.png')
        self.AllGrassPng = self.GrassPng.load_image_at((0, 0, 128, 128))
        self.AllGrassPng = pygame.transform.scale(self.AllGrassPng, (256, 256))
        self.AllGrass = Tiles(self.AllGrassPng).load_allimages(64)

        self.image = self.AllGrass[random.randint(0, len(self.AllGrass)-1)]
        self.rect = self.image.get_rect(topleft = pos)

class Flower(pygame.sprite.Sprite, Behavior):

    def __init__(self, pos: tuple, group: object, tag={}) -> None:
        super().__init__(group)
        Behavior.__init__(self)
        self.GrassPng = Tiles('Assets\Texture\TX Tileset Grass.png')
        self.AllFlowerPng = self.GrassPng.load_image_at((128, 0, 128, 128))
        self.AllFlowerPng = pygame.transform.scale(self.AllFlowerPng, (256, 256))
        self.AllFlower = Tiles(self.AllFlowerPng).load_allimages(64)

        self.image = self.AllFlower[random.randint(0, len(self.AllFlower)-1)]
        self.rect = self.image.get_rect(topleft = pos)

class Path(pygame.sprite.Sprite, Behavior):

    def __init__(self, pos: tuple, group: object, tag={'form':'full' ,'angle':'' ,'damage_lvl':0}) -> None:
        super().__init__(group)
        Behavior.__init__(self)
        self.GrassPng = Tiles('Assets\Texture\TX Tileset Grass.png')
        self.PathPng = self.GrassPng.load_image_at((0, 128, 256, 128))
        self.PathPng = pygame.transform.scale(self.PathPng, (512, 256))
        self.SlicedPath = Tiles(self.PathPng).load_allimages(64)
        
        self.tag = tag
        self.image = self.select_path(tag)
        self.rect = self.image.get_rect(topleft = pos)

    def select_path(self, tag):
        """
        # Info
        Return the image of the path depending on the form of it ant the damage level, the damage level represent if the path is in good condition.


        # Input
        form = full or ''
        angle = right, left, top, bottom, angle_top_left, angle_top_right, angle_bottom_right, angle_bottom_left, corner_top_left, corner_top_right, corner_bottom_right, corner_bottom_left \n
        damage_lvl = 0 , 1 , 2 , 3 , 4, 5 
        """
        if tag['form'] == 'full':

            if tag['damage_lvl'] == 0:
                return self.SlicedPath[0]
            elif tag['damage_lvl'] == 1:
                return self.SlicedPath[1]
            elif tag['damage_lvl'] == 2:
                return self.SlicedPath[8]
            elif tag['damage_lvl'] == 3:
                return self.SlicedPath[9]
            elif tag['damage_lvl'] == 4:
                return self.SlicedPath[16]
            elif tag['damage_lvl'] == 5:
                return self.SlicedPath[17]
        else:

            # Sides
            if tag['angle'] == 'right':
                if tag['damage_lvl'] == 0:
                    return self.SlicedPath[3]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedPath[11]
                elif tag['damage_lvl'] == 2:
                    return self.SlicedPath[19]
                elif tag['damage_lvl'] == 3:
                    return self.SlicedPath[27]
            elif tag['angle'] == 'left':
                if tag['damage_lvl'] == 0:
                    return self.SlicedPath[2]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedPath[10]
                elif tag['damage_lvl'] == 2:
                    return self.SlicedPath[18]
                elif tag['damage_lvl'] == 3:
                    return self.SlicedPath[26]
            elif tag['angle'] == 'top':
                if tag['damage_lvl'] == 0:
                    return self.SlicedPath[4]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedPath[5]
                elif tag['damage_lvl'] == 2:
                    return self.SlicedPath[6]
                elif tag['damage_lvl'] == 3:
                    return self.SlicedPath[7]
            elif tag['angle'] == 'bottom':
                if tag['damage_lvl'] == 0:
                    return self.SlicedPath[12]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedPath[13]
                elif tag['damage_lvl'] == 2:
                    return self.SlicedPath[14]
                elif tag['damage_lvl'] == 3:
                    return self.SlicedPath[15]

            # Angles 
            elif tag['angle'] == 'angle_top_left':
                return self.SlicedPath[24]
            elif tag['angle'] == 'angle_top_right':
                return self.SlicedPath[25]
            elif tag['angle'] == 'angle_bottom_left':
                return self.SlicedPath[29]
            elif tag['angle'] == 'angle_bottom_right':
                return self.SlicedPath[28]
            
            # Corners 
            elif tag['angle'] == 'corner_top_left':
                return self.SlicedPath[23]
            elif tag['angle'] == 'corner_top_right':
                return self.SlicedPath[22]
            elif tag['angle'] == 'corner_bottom_left':
                return self.SlicedPath[21]
            elif tag['angle'] == 'corner_bottom_right':
                return self.SlicedPath[20]
            
class StoneGround(pygame.sprite.Sprite, Behavior):

    def __init__(self, pos: tuple, group: object, tag={}) -> None:
        super().__init__(group)
        Behavior.__init__(self)
        self.StoneGroundPng = Tiles('Assets\Texture\TX Tileset Stone Ground.png')
        self.StoneGroundPng = self.StoneGroundPng.load_image_at((0, 0, 256, 256))
        self.StoneGroundPng = pygame.transform.scale(self.StoneGroundPng, (512, 512))
        self.SlicedStoneGround = Tiles(self.StoneGroundPng).load_allimages(64)
        
        self.tag = tag
        self.image = self.SlicedStoneGround[9]
        self.rect = self.image.get_rect(topleft=pos)

class Wall(pygame.sprite.Sprite, Behavior):

    def __init__(self, pos: tuple, group: object, tag={'form':'exposed_wall_top', 'angle':'', 'damage_lvl':0, 'variation':0}) -> None:
        super().__init__(group)
        Behavior.__init__(self)
        self.WallPng = Tiles('Assets\Texture\TX Tileset Wall.png')
        self.WallPng = self.WallPng.load_image_at((0, 0, 288, 224))
        self.WallPng = pygame.transform.scale(self.WallPng, (576, 448))
        self.SlicedWall = Tiles(self.WallPng).load_allimages(64)
        
        self.tag = tag
        self.image = self.select_wall(tag)
        self.rect = self.image.get_rect(topleft=pos)

    def select_wall(self, tag):
        """
        # Info
        Return the image of the wall depending on the form of it ant the damage level, the damage level represent if the wall is in good condition.

        # Input
        Tag{ form, angle, damage_lvl, variation } \n
        form = exposed_wall_top, exposed_wall_bottom, hided_wall, left, right \n
        angle = intern_left, intern_right, outer_left, outer_right, intern, outer, shadow, window \n
        damage_lvl = 0, 1, 2, 3, 4 \n
        variation = 0, 1, 2, 3, 4, 5, 6 \n
        """

        if tag['form'] == 'exposed_wall_top':
            if tag['angle'] == 'left':
                if tag['damage_lvl'] == 0:
                    return self.SlicedWall[25]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedWall[32]
            elif tag['angle'] == 'right':
                if tag['damage_lvl'] == 0:
                    return self.SlicedWall[27]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedWall[33]
            elif tag['angle'] == 'shadow':
                return self.SlicedWall[5]
            elif tag['angle'] == 'window':
                return self.SlicedWall[48]
            else:
                if tag['damage_lvl'] == 0:
                    if tag['variation'] == 0:
                        return self.SlicedWall[6]
                    elif tag['variation'] == 1:
                        return self.SlicedWall[7]
                    elif tag['variation'] == 2:
                        return self.SlicedWall[26]
                    elif tag['variation'] == 3:
                        return self.SlicedWall[54]
                    elif tag['variation'] == 4:
                        return self.SlicedWall[55]
                    elif tag['variation'] == 5:
                        return self.SlicedWall[56]
                    elif tag['variation'] == 6:
                        return self.SlicedWall[57]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedWall[45]
                elif tag['damage_lvl'] == 2:
                    return self.SlicedWall[44]
                elif tag['damage_lvl'] == 3:
                    return self.SlicedWall[47]
                elif tag['damage_lvl'] == 4:
                    return self.SlicedWall[46]
                
        elif tag['form'] == 'exposed_wall_bottom':
            if tag['angle'] == 'left':
                if tag['damage_lvl'] == 0:
                    return self.SlicedWall[34]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedWall[42]
            elif tag['angle'] == 'right':
                if tag['damage_lvl'] == 0:
                    return self.SlicedWall[36]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedWall[43]
            elif tag['angle'] == 'shadow':
                return self.SlicedWall[17]
            elif tag['angle'] == 'window':
                return self.SlicedWall[53]
            else:
                if tag['damage_lvl'] == 0:
                    if tag['variation'] == 0:
                        return self.SlicedWall[18]
                    elif tag['variation'] == 1:
                        return self.SlicedWall[19]
                    elif tag['variation'] == 2:
                        return self.SlicedWall[35]
                    elif tag['variation'] == 3:
                        return self.SlicedWall[58]
                    elif tag['variation'] == 4:
                        return self.SlicedWall[59]
                    elif tag['variation'] == 5:
                        return self.SlicedWall[60]
                    elif tag['variation'] == 6:
                        return self.SlicedWall[61]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedWall[49]
                elif tag['damage_lvl'] == 2:
                    return self.SlicedWall[52]
                elif tag['damage_lvl'] == 3:
                    return self.SlicedWall[51]
                elif tag['damage_lvl'] == 4:
                    return self.SlicedWall[50]

        elif tag['form'] == 'hided_wall':
            if tag['angle'] == 'left':
                return self.SlicedWall[4]
            elif tag['angle'] == 'right':
                return self.SlicedWall[8]
            elif tag['angle'] == 'intern_left':
                return self.SlicedWall[37]
            elif tag['angle'] == 'intern_right':
                return self.SlicedWall[41]
            elif tag['angle'] == 'outer_left':
                if tag['damage_lvl'] == 0:
                    return self.SlicedWall[1]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedWall[23]
            elif tag['angle'] == 'outer_right':
                if tag['damage_lvl'] == 0:
                    return self.SlicedWall[3]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedWall[24]
            elif tag['angle'] == 'intern':
                if tag['variation'] == 0:
                    return self.SlicedWall[38]
                elif tag['variation'] == 1:
                    return self.SlicedWall[39]
                elif tag['variation'] == 2:
                    return self.SlicedWall[40]
            elif tag['angle'] == 'outer':
                if tag['damage_lvl'] == 0:
                    return self.SlicedWall[2]
                elif tag['damage_lvl'] == 1:
                    return self.SlicedWall[11]
                elif tag['damage_lvl'] == 2:
                    return self.SlicedWall[12]
                elif tag['damage_lvl'] == 3:
                    return self.SlicedWall[13]
                
        elif tag['form'] == 'left':
            if tag['damage_lvl'] == 0:
                if tag['variation'] == 0:
                    return self.SlicedWall[15]
                elif tag['variation'] == 1:
                    return self.SlicedWall[16]
                elif tag['variation'] == 2:
                    return self.SlicedWall[28]
            elif tag['damage_lvl'] == 1:
                return self.SlicedWall[10]
            elif tag['damage_lvl'] == 2:
                return self.SlicedWall[22]
            elif tag['damage_lvl'] == 3:
                return self.SlicedWall[31]

        elif tag['form'] == 'right':
            if tag['damage_lvl'] == 0:
                if tag['variation'] == 0:
                    return self.SlicedWall[14]
                elif tag['variation'] == 1:
                    return self.SlicedWall[20]
                elif tag['variation'] == 2:
                    return self.SlicedWall[29]
            elif tag['damage_lvl'] == 1:
                return self.SlicedWall[9]
            elif tag['damage_lvl'] == 2:
                return self.SlicedWall[21]
            elif tag['damage_lvl'] == 3:
                return self.SlicedWall[30]