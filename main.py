import pygame as pg

import settings
from gameobjects.bug import Bug, Base
from gameobjects.entity import Point
import time
from logger import Logger
import math


class App:
    bug_scream_radius = settings.BUG_SCREAM_RADIUS
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
        self.chunks = []
        self.bases = []
        self.target_clock = 60
        self.logger = Logger()
        self.chunk_update_timer = 0

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEWHEEL:
                if event.y > 0:
                    self.target_clock += 5
                elif event.y < 0:
                    self.target_clock = max(5, self.target_clock - 5)

    def startapp(self):
        self.bases.append(Base(type="A", pos=Point(200, 240), color=(123, 230, 123)))
        self.bases.append(Base(type="B", pos=Point(1100, 500), color=(233, 123, 123)))
        self.bases.append(Base(type="B", pos=Point(1000, 200), color=(233, 123, 123)))

        Bug.initBases(self.bases)

        self.entities = [Bug() for i in range(settings.BUG_COUNT)]

        # testing
        self.entities[0].pos = Point(900, 500)
        self.entities[0].color = (255, 0, 255)
        self.entities[0].dir = 0
        self.entities[0].target = "B"

        # self.entities[0].pos=Point(900, 500)
        # self.entities[0].dir = 90
        # self.entities[0].spd = 0
        # self.entities[1].target = 'B'

    def update(self):
        base_colors = set([base.type for base in self.bases])
        ent_count_by_color = {}
        for color in base_colors:
            ent_count_by_color[color] = 0

        for entity in self.entities:
            ent_count_by_color[entity.target] += 1
        s = ""
        for color in ent_count_by_color.keys():
            s += f" {color}: {ent_count_by_color[color]}. "
        self.title += f"Clock_FPS:[{self.clock.get_fps():.1f}] Traget_FPS:[{self.target_clock}] Entities target: {s}"

        

        self.chunk_update_timer -= 1
        if self.chunk_update_timer < 0:
            self.chunk_update_timer = settings.CHUNK_UPDATE_AFTER_TICKS

            self.chunks = [
                [[] for i in range(math.ceil(settings.RESOLUTION_Y / self.bug_scream_radius))]
                for j in range(math.ceil(settings.RESOLUTION_X / self.bug_scream_radius))
            ]

            for entity in self.entities:
                x = int(entity.pos.x / self.bug_scream_radius)
                y = int(entity.pos.y / self.bug_scream_radius)
                if entity.pos.x == settings.RESOLUTION_X:
                    x = int((entity.pos.x - 1) / self.bug_scream_radius)
                if entity.pos.y == settings.RESOLUTION_Y:
                    y = int((entity.pos.y - 1) / self.bug_scream_radius)

                self.chunks[x][y].append(entity)
                pass

        for entity in self.entities:
            entity.scream(self.chunks, self.screen)
            entity.update()

    def render(self):

        for entity in self.entities:
            entity.render(self.screen)

        for entity in self.bases:
           entity.render(self.screen)

       

    def run(self):
        while self.running:
            total_start_time = time.perf_counter()
            self.screen.fill((0, 0, 0))
            self.title = ""

            start_time = time.perf_counter()
            self.handle_events()
            handle_events_time_ms = (time.perf_counter() - start_time) * 1000

            start_time = time.perf_counter()
            self.update()
            update_time_ms = (time.perf_counter() - start_time) * 1000

            start_time = time.perf_counter()
            self.render()
            render_time_ms = (time.perf_counter() - start_time) * 1000

            self.title += f"Perf stats: HE - {handle_events_time_ms:.1f} ms"
            self.title += f" U - {update_time_ms:.1f} ms"
            self.title += f" R - {render_time_ms:.1f} ms"

            total_time_ms = (
                (time.perf_counter() - total_start_time) * 1000
                - handle_events_time_ms
                - update_time_ms
                - render_time_ms
            )
            self.title += f" Other - {total_time_ms:.1f} ms"
            pg.display.set_caption(self.title)
            pg.display.flip()
            self.clock.tick(self.target_clock)

        pg.quit()


if __name__ == "__main__":
    app = App()
    app.startapp()
    app.run()
