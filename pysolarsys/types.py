import math
import enum
from typing import Tuple


Tuple_2D = Tuple[float, float]
Tuple_3D = Tuple[float, float, float]

WindowRange = Tuple[float, float]


class BodyType(int, enum.Enum):
    PLANET = (0, 'Planet')
    STAR = (1, 'Star')
    WHITE_DWARF_STAR = (2, 'White Dwarf')
    GIANT_STAR = (3, 'Giant Star')
    SUPER_GIANT_STAR = (4, 'Super Giant')

    def __new__(cls, value, title):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.title = title

        return obj

    @staticmethod
    def from_value(value: int) -> 'BodyType':
        for bodies in BodyType:
            if bodies.value == value:
                return bodies
        raise TypeError


class Vector:
    def __init__(self, x: float, y: float, z: float = 0) -> None:
        self.__p = x, y, z
        self.__l = None
        self.__n = x, y, z
        self._norm()
    
    @property
    def x(self) -> float:
        return self.__p[0]

    @property
    def y(self) -> float:
        return self.__p[1]
    
    @property
    def z(self) -> float:
        return self.__p[2]
    
    def set(self, x: float, y: float, z: float = 0) -> 'Vector':
        self.__p = x, y, z
        self.__l = None
        self._norm()
        return self

    def dot(self, vector: 'Vector') -> float:
        return sum((a * b for a, b in zip(self.__p, vector.__p)))

    def ndot(self, vector: 'Vector') -> float:
        return sum((a * b for a, b in zip(self.__n, vector.__n)))

    def __repr__(self) -> str:
        return f'pysolarsys.types.Vector <{self.__p[0]}, {self.__p[1]}, {self.__p[2]}>'

    def length(self) -> float:
        if self.__l is None:
            self.__l = math.sqrt(sum((i * i for i in self.__p)))
        return self.__l

    def _norm(self):
        length = self.length()
        if length < 0.000001:
            return
        self.__n = self.__p[0] / length, self.__p[1] / length, self.__p[2] / length

    def angle_towards(self, vector: 'Vector') -> float:
        det = self.__n[0] * vector.__n[1] - self.__n[1] * vector.__n[0]
        dot = self.ndot(vector)
        return math.atan2(det, dot)


class Point:
    def __init__(self, x: float, y: float, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f'pysolarsys.types.Point <{self.x}, {self.y}, {self.z}>'

    def __iter__(self) -> float:
        for i in self.x, self.y, self.z:
            yield i

    def move_by(self, by: Vector) -> 'Point':
        self.x += by.x
        self.y += by.y
        self.z += by.z
        return self

    def translate(self, by: Vector) -> 'Point':
        p = Point(self.x + by.x, self.y + by.y, self.z + by.z)
        return p
    
    def distance(self, to: 'Point') -> float:
        v = Vector(*(a - b for a, b in zip(self, to)))
        return v.length()
