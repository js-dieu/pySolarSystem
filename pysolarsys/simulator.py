import turtle
from typing import Tuple
from pysolarsys.physics import Body, SolarSystem
from pysolarsys.graphic import Display
from pysolarsys.types import BodyType, Point, Vector


class Simulator:
    def __init__(self, display_size: Tuple[int, int], max_iteration: int | None = None):
        self.__max_iter = max_iteration
        self.__solar_system = SolarSystem()
        self.__display = Display(display_size[0], display_size[1])

    def add_sun(self, name: str, mass: float, position: Point, velocity: Vector):
        sun = Body(name, mass, initial_position=position, velocity=velocity, body_type=BodyType.STAR)
        self.__solar_system.add(sun)

    def add_giant_star(self, name: str, mass: float, position: Point, velocity: Vector):
        sun = Body(name, mass, initial_position=position, velocity=velocity, body_type=BodyType.GIANT_STAR)
        self.__solar_system.add(sun)

    def add_super_giant_star(self, name: str, mass: float, position: Point, velocity: Vector):
        sun = Body(name, mass, initial_position=position, velocity=velocity, body_type=BodyType.SUPER_GIANT_STAR)
        self.__solar_system.add(sun)

    def add_white_dwarf(self,  name: str, mass: float, position: Point, velocity: Vector):
        sun = Body(name, mass, initial_position=position, velocity=velocity, body_type=BodyType.WHITE_DWARF_STAR)
        self.__solar_system.add(sun)

    def add_planet(self,  name: str, mass: float, position: Point, velocity: Vector):
        planet = Body(name, mass=mass, initial_position=position, velocity=velocity, body_type=BodyType.PLANET)
        self.__solar_system.add(planet)

    def run(self):
        it = 0
        stop = False

        self.__display.init(self.__solar_system)

        while not stop:
            if not self.__display.is_paused():
                self.__solar_system.compute_next_step()
            else:
                it += 1
            self.__display.draw_and_listen(self.__solar_system)
            stop = self.__max_iter is not None and it > self.__max_iter
            stop = stop or self.__display.stop_requested()
        turtle.exitonclick()
