import math
import uuid
from typing import List

from pysolarsys.types import BodyType, Vector, Point

counter = 0


def make_body_name() -> str:
    global counter
    counter += 1
    return f'BDY{counter:02}'


class Body:
    def __init__(self, name: str, mass: float, initial_position: Point,
                 velocity: Vector, body_type: BodyType) -> None:
        self.__name: str = name
        self.__mass: float = mass
        self.__radius: float = max(math.log(self.__mass, 1.1), 10)
        self.__vel: Vector = velocity
        self.__pos: Point = initial_position
        self.__type: BodyType = body_type
        self.__oid: str = str(uuid.uuid4())
        self.__exists = True

    def __repr__(self) -> str:
        return f'<pysolarsys.physics.body<{self.body_type.title}, {self.name}, {self.position}, {self.velocity}>' \
               f' (mass={self.mass} | radius={self.radius})'

    @property
    def exists(self) -> bool:
        return self.__exists

    @exists.setter
    def exists(self, value: bool) -> None:
        self.__exists = value

    @property
    def oid(self) -> str:
        return self.__oid

    @property
    def body_type(self) -> BodyType:
        return self.__type

    @property
    def is_planet(self) -> bool:
        return self.__type == BodyType.PLANET
    
    @property
    def is_sun(self) -> bool:
        return self.__type != BodyType.PLANET

    @property
    def radius(self) -> float:
        return self.__radius

    @property
    def position(self) -> Point:
        return self.__pos

    @position.setter
    def position(self, value: Point) -> None:
        self.__pos = value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def mass(self) -> float:
        return self.__mass

    @mass.setter
    def mass(self, value: float) -> None:
        self.__mass = value

    @property
    def velocity(self) -> Vector:
        return self.__vel

    @velocity.setter
    def velocity(self, value: Vector) -> None:
        self.__vel = value

    def distance(self, body: 'Body') -> float:
        return self.position.distance(body.position)


class SolarSystem:
    def __init__(self) -> None:
        self.__bodies: List[Body] = []
    
    def add(self, body: Body) -> 'SolarSystem':
        self.__bodies.append(body)
        return self
    
    def remove(self, body: Body) -> 'SolarSystem':
        # self.__bodies.remove(body)
        body.exists = False
        return self

    def __iter__(self) -> Body:
        for body in self.__bodies:
            yield body

    def handle_collisions(self, first: Body, second: Body) -> None:
        if (first.distance(second)) < (first.radius + second.radius) / 2:
            if first.is_planet:
                self.remove(first)
            if second.is_planet:
                self.remove(second)
            if first.is_sun and second.is_sun:
                # Create a new sun and remove previous ones
                mass = first.mass + second.mass
                vel = Vector(0, 0)
                p = first.position
                p.x += (second.position.x - p.x) / 2
                p.y += (second.position.y - p.y) / 2
                p.z += (second.position.z - p.z) / 2
                sun_type = BodyType.from_value(max(first.body_type.value, second.body_type.value))
                new_sun = Body(name=make_body_name(), mass=mass, initial_position=p, velocity=vel, body_type=sun_type)
                self.remove(first).remove(second).add(new_sun)
            elif first.is_sun:
                first.mass = second.mass + first.mass
            elif second.is_sun:
                second.mass = first.mass + second.mass

    def compute_next_step(self) -> None:
        bodies_copy = list(filter(lambda b: b.exists, self.__bodies.copy()))
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                self.accelerate(first, second)
                self.handle_collisions(first, second)

        for body in self.__bodies:
            body.position = body.position.move_by(body.velocity)

    @staticmethod
    def accelerate(first: Body, second: Body) -> None:
        f = first.mass * second.mass / (first.distance(second) ** 2)
        v = Vector(second.position.x - first.position.x, second.position.y - first.position.y)
        ang = math.atan2(v.y, v.x)
        reverse = 1
        for body in first, second:
            a = f / body.mass
            a_x = a * math.cos(ang)
            a_y = a * math.sin(ang)
            body.velocity = Vector(body.velocity.x + reverse * a_x, body.velocity.y + reverse * a_y)
            reverse = -1
