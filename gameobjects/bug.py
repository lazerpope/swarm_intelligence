from .entity import Entity, Point
from random import randint,choice
import pygame as pg
import settings
import math
from typing import List
import pygame.gfxdraw as gf


class Bug(Entity):
    nose_length = settings.BUG_NOSE_LENGTH
    max_spd:int = settings.BUG_MAX_SPEED
    min_spd:int = settings.BUG_MIN_SPEED
    size: int = settings.BUG_SIZE
    base_types: list = []
    bases: list = []
    
    def __init__(
        self,
        pos: Point | None = None,  # Ensure that the default is None
        spd: float = 1.0,
        direction: float|None = None,
        color: tuple[int, int, int] = (88, 88, 88),               
        scream_radius = settings.BUG_SCREAM_RADIUS,
        sway: float|None = None
    ):
        if pos is None:
            pos = Point(randint(10,settings.RESOLUTION_X-10),randint(10,settings.RESOLUTION_Y-10)) 
            
        if direction is None :
            direction = randint(0,360)

        self.sway = sway if sway is not None else randint(-50, 400) / 600

        
        self.scream_radius = scream_radius
        
        if self.base_types.__len__() == 0:
            raise ValueError('Bases not found, run initBases() first')
        
        self.counters = {}
        for key in self.base_types:
            self.counters[key] = 10000

        self.target = choice(self.base_types)
        
        super().__init__(
            pos=pos,
            spd=spd,
            direction=direction,
            color=color,
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



    def scream(self,chunks , screen:pg.Surface):
        
        x = int(self.pos.x / self.scream_radius)
        y = int(self.pos.y / self.scream_radius)
        if self.pos.x == settings.RESOLUTION_X:
            x = int((self.pos.x-1) / self.scream_radius)
        if self.pos.y == settings.RESOLUTION_Y:
            y = int((self.pos.y-1) / self.scream_radius)


        x_bound = math.ceil(settings.RESOLUTION_X/self.scream_radius)
        y_bound = math.ceil(settings.RESOLUTION_Y/self.scream_radius)
        
        candidates = [(x-1,y+1),(x,y+1),(x+1,y+1),   (x-1,y-1),(x,y-1),(x+1,y-1),   (x-1,y),(x+1,y)]
        
        neighbours = [
            (x_c, y_c) for x_c, y_c in candidates
            if 0 <= x_c < x_bound and 0 <= y_c < y_bound
        ]

       
        neighbouring_entities = [
            ent for candidate in neighbours for ent in chunks[candidate[0]][candidate[1]]
        ]

        # print(neighbouring_entities.__len__())   
        if len(neighbouring_entities) < 2:
            return
        message = choice(self.base_types)
        for other in neighbouring_entities:
            if other is self:
                continue
            if self.pos.distance_to(other.pos) >= self.scream_radius:
                continue
            if self.counters[message]+self.scream_radius >= other.counters[message]:
                continue
            other.counters[message] = self.counters[message] + self.scream_radius
        
            gf.line(screen,  int(self.pos.x), int(self.pos.y), int(other.pos.x), int(other.pos.y) , (200,240,240)) 

            if message == other.target:
                other.dir = math.degrees(math.atan2(self.pos.y - other.pos.y, self.pos.x - other.pos.x))







    def render(self, screen:pg.Surface): 
        for base in self.bases:
            if base.type == self.target:
                color = base.color
                break
        else:
            color = (255, 255, 255)

        gf.circle(screen,  int(self.pos.x), int(self.pos.y) , self.size, color,)
 
        rad = math.radians(self.dir)
        end_x = int(self.pos.x + self.nose_length * math.cos(rad))
        end_y = int(self.pos.y + self.nose_length * math.sin(rad))
       
        gf.line(screen,  int(self.pos.x), int(self.pos.y), end_x, end_y,  self.color) 









class Base(Entity):
    
    
    def __init__(
        self,
        pos: Point | None = None,  # Ensure that the default is None
        spd: float = 1.0,
        direction: float = 0,
        color: tuple[int, int, int] = (123, 230, 123),        
        size: int = 40,
        type: str = ""
    ):
        if pos is None:
            pos = Point()  # Create a new Point if pos is None
        
        self.size = size


        self.type = type
        if type == '':
            raise ValueError('Base must have type')

        super().__init__(
            pos=pos,
            spd=spd,
            direction=direction,            
            color=color,
        )
        

    def update(self): ...


    def render(self, screen: pg.Surface):
        pg.draw.circle(screen, self.color, self.pos.as_tuple, self.size)
        
        font = pg.font.Font(None, self.size*2)  # You can specify a different font and size if needed
        text_surface = font.render(self.type, True, (255, 255, 255))  # Render the text in white
        text_rect = text_surface.get_rect(center=(int(self.pos.x), int(self.pos.y)))  # Center the text
        
        screen.blit(text_surface, text_rect)  # Draw the text on the screen
        