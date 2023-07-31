import pygame
from Camera import *
from Player import *
from Enemys import *
from Mouse import *
from Bullets import *
from Map import *

class App:

    def __init__(self, dev_mode=False) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))
        self.clock = pygame.time.Clock()
        self.camera_group = CameraGroup(dev_mode)
        self.gui_group = GUIGroup()
        self.frame_rate = self.clock.get_fps()
        self.delta = 0

        self.half_w = self.screen.get_size()[0] //2
        self.half_h = self.screen.get_size()[1] //2
        self.dev_mode = dev_mode

        self.Entitys = []
        
        self.Map = Map(self.camera_group, self.Entitys)
        self.Map.load()
        
        self.player = Player(((self.Map.data['points'][0].x)*8, (self.Map.data['points'][0].y)*8), self.camera_group)
        self.Entitys.append(self.player)

        self.Mouse = Mouse(self.camera_group)
        pygame.mouse.set_visible(False)


    def __call__(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                # Oe c ici qu'on shoot je varai plus trad pour modifier
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.shoot(self.Entitys, self.Mouse, self.camera_group)

            self.screen.fill('#71ddee')

            self.update()
            self.display()

            pygame.display.update()

            self.frame_rate = self.clock.get_fps()
            self.clock.tick(60)
            if self.frame_rate != 0.0:
                self.delta = 1 / self.frame_rate

    def update(self) -> None:
        self.camera_group.update(pl=self.player, enemys=self.get_entitys(Enemy), mobs=self.get_entitys((Player, Enemy)), bullets=self.get_entitys(Bullet), entitys=self.Entitys, scene=self.Map, dt=self.delta)
        self.gui_group.update()

    def display(self) -> None:
        self.camera_group.display(self.player)
        self.gui_group.display()
        if self.dev_mode:
            self.Map.display(self.camera_group.get_offset())

    def get_entitys(self, __class) -> list:
        l = []
        for e in self.Entitys:
            if isinstance(e, __class):
                l.append(e)
        return l
