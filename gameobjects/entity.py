from abc import ABC
import math



class Point:
    def __init__(self, x:float=0, y:float=0) -> None:
        self.x = x
        self.y = y

    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    @property
    def as_tuple(self)-> tuple[float,float]:
        return (self.x, self.y)



class Entity(ABC):
    size: int = 3


    def __init__(
        self,
        pos: Point,
        spd: float = 1.0,
        direction:float=0,
        random_tick_dir_change: int = 1,
        color: tuple[int, int, int] = (123, 123, 123),
    ):
        self.pos = pos
        self.spd = spd
        self.color = color
        self._direction = direction
        self.random_tick_dir_change = random_tick_dir_change
        

    def update(self): ...

    def render(self, screen): ...

    @property
    def dir(self) -> int:
        return int(self._direction)

    @dir.setter
    def dir(self, value: float) -> None:
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("Direction must be an integer or float.")

        self._direction = value % 360
