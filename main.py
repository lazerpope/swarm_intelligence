import pygame as pg

import settings
from gameobjects.bug import Bug, Base
from gameobjects.entity import Point


class App:
    def __init__(self, title="Pygame App"):
        self.width = settings.RESOLUTION_X
        self.height = settings.RESOLUTION_Y
        self.title = title
        self.screen: pg.Surface = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        pg.font.init()
        self.clock = pg.time.Clock()
        self.running = True
        self.entities = []
        self.bases = []
        self.target_clock = 60

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def startapp(self):
        self.bases.append(Base(type="A", pos=Point(200, 240), color=(123, 230, 123)))
        self.bases.append(Base(type="B", pos=Point(1100, 500), color=(233, 123, 123)))
        self.bases.append(Base(type="B", pos=Point(1000, 200), color=(233, 123, 123)))

        Bug.initBases(self.bases)
       
        self.entities = [Bug() for i in range(200)]

        #testing
        # self.entities[1].pos=Point(900, 500)
        self.entities[1].color = (255, 0, 0)
        # self.entities[1].dir = 0
        # self.entities[1].target = 'B'

        # self.entities[0].pos=Point(900, 500)
        # self.entities[0].dir = 90
        # self.entities[0].spd = 0
        # self.entities[1].target = 'B'

    def update(self):
        
        for entity in self.entities:
            entity.scream(self.entities, self.screen)
            entity.update()


        base_colors = set([base.type for base in self.bases])
        ent_count_by_color = {}
        for color in base_colors:
            ent_count_by_color[color] = 0

        for entity in self.entities:
            ent_count_by_color[entity.target] += 1
        s = ''
        for color in ent_count_by_color.keys():
            s+= f' {color}: {ent_count_by_color[color]}. '   
        pg.display.set_caption(f'Clock:[{self.clock.get_fps():.1f}] Traget:[{self.target_clock}] Entities: {s}')
        
        
        #testing
        # print(self.entities[1]._direction , self.entities[1].target)
        

    def render(self):
        
        for entity in self.entities:
            entity.render(self.screen)

        for entity in self.bases:
            entity.render(self.screen)

        self.entities[1].render(self.screen)

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.handle_events()
            self.update()
            self.render()
            pg.display.flip()
            self.clock.tick(self.target_clock)
        pg.quit()


if __name__ == "__main__":
    app = App()
    app.startapp()
    app.run()
