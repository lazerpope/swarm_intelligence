from .entity import Entity, Point
from random import randint,choice
import pygame as pg
import settings
import math
from typing import List
class Bug(Entity):
    line_length = 10
    base_types: list = []
    bases: list = []
    max_spd:int = 55
    min_spd:int = 15
    
    def __init__(
        self,
        pos: Point | None = None,  # Ensure that the default is None
        spd: float = 1.0,
        direction: float = 0,
        dir_c:int = 0,
        random_tick_spd_change: int = 1,
        random_tick_dir_change: int = 100,
        color: tuple[int, int, int] = (88, 88, 88),
        counter:int = 10000 ,
        size: int = 3,
        scream_radius = 80
    ):
        if pos is None:
            pos = Point(randint(10,settings.RESOLUTION_X-10),randint(10,settings.RESOLUTION_Y-10)) 
        if direction == 0 :
            direction = randint(0,360)
        self.sway = randint(-50,400)/600
        self.dir_c = dir_c
        self.scream_radius = scream_radius
        
        if self.base_types.__len__() == 0:
            raise ValueError('Bases not found, run initBases() first')
        
        self.counters = {}
        for key in self.base_types:
            self.counters[key] = counter

        self.target = choice(self.base_types)
        
        super().__init__(
            pos=pos,
            spd=spd,
            direction=direction,
            random_tick_spd_change=random_tick_spd_change,
            random_tick_dir_change=random_tick_dir_change,
            color=color,
            size=size,
        )

        self.spd = randint(self.min_spd,self.max_spd)/10

    @staticmethod
    def initBases(bases):
        for base in bases:
            if base.type not in Bug.base_types:
                Bug.base_types.append(base.type)
        
        Bug.bases = bases
        
        

    def update(self):
        for key in self.counters.keys():
            self.counters[key] +=  1

        rad = math.radians(self.dir)
        self.pos.x += self.spd * math.cos(rad)
        self.pos.y += self.spd * math.sin(rad)
        
        if self.pos.x < 0:
            self.pos.x = 0
            self.dir += 180
        elif self.pos.x > settings.RESOLUTION_X:
            self.pos.x = settings.RESOLUTION_X
            self.dir += 180

        if self.pos.y < 0:
            self.pos.y = 0
            self.dir += 180
        elif self.pos.y > settings.RESOLUTION_Y:
            self.pos.y = settings.RESOLUTION_Y
            self.dir += 180
            
        # self.acc += self.dir 
        
        # if self.dir_c <= 0 :
        #     self.dir_c = 60
        #     self.dir += randint(-self.random_tick_dir_change,self.random_tick_dir_change)/100

        # if self.counters[self.target] > 300:   
        #     self.dir_c -= 1

        # f = randint(-self.random_tick_dir_change,self.random_tick_dir_change)/10000
        # self.dir += f
        self.dir += self.sway

        

        for base in self.bases:
            dist = self.pos.distance_to(base.pos)
            if dist < base.size * 0.9 and base.type == self.target :
                
                
                other_bases = [i for i in self.base_types]
                other_bases.remove(self.target)                
                new_target = choice(other_bases) 


                self.target = new_target
                self.dir += 180
                self.counters[base.type] = dist

        # print(randint(-1,1))


    
    def scream(self, others: List['Bug'], screen: pg.Surface ):
        message = choice(self.base_types)
        for other in others:
            if self.pos.distance_to(other.pos) < self.scream_radius:
                if self.counters[message]+self.scream_radius < other.counters[message]:
                    other.counters[message] = self.counters[message] + self.scream_radius
                    pg.draw.line(screen, (255,255,255), self.pos.as_tuple, other.pos.as_tuple, 1) 
                    if message == other.target:
                        other.dir = math.degrees(math.atan2(self.pos.y - other.pos.y, self.pos.x - other.pos.x))


    def render(self, screen:pg.Surface): 
        if self.target == "B":
            pg.draw.circle(screen, (240,50,50), self.pos.as_tuple, self.size)
        else:
            pg.draw.circle(screen, (40,250,50), self.pos.as_tuple, self.size)

        rad = math.radians(self.dir)
        end_x = self.pos.x + self.line_length * math.cos(rad)
        end_y = self.pos.y + self.line_length * math.sin(rad)
       
        pg.draw.line(screen, self.color, self.pos.as_tuple, (end_x, end_y), 1) 












class Base(Entity):
    
    
    def __init__(
        self,
        pos: Point | None = None,  # Ensure that the default is None
        spd: float = 1.0,
        direction: float = 0,
        random_tick_spd_change: int = 1,
        random_tick_dir_change: int = 1,
        color: tuple[int, int, int] = (123, 230, 123),        
        size: int = 40,
        type: str = ""
    ):
        if pos is None:
            pos = Point()  # Create a new Point if pos is None
        
        self.type = type
        if type == '':
            raise ValueError('Base must have type')

        super().__init__(
            pos=pos,
            spd=spd,
            direction=direction,
            random_tick_spd_change=random_tick_spd_change,
            random_tick_dir_change=random_tick_dir_change,
            color=color,
            size=size,
        )
        

    def update(self): ...


    def render(self, screen: pg.Surface):
        pg.draw.circle(screen, self.color, self.pos.as_tuple, self.size)
        
        font = pg.font.Font(None, self.size*2)  # You can specify a different font and size if needed
        text_surface = font.render(self.type, True, (255, 255, 255))  # Render the text in white
        text_rect = text_surface.get_rect(center=(int(self.pos.x), int(self.pos.y)))  # Center the text
        
        screen.blit(text_surface, text_rect)  # Draw the text on the screen
        