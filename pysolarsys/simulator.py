import json
import pathlib
import turtle
from typing import Tuple
from pysolarsys.constants import SIMULATION_FILE
from pysolarsys.physics import Body, SolarSystem
from pysolarsys.graphic import Display
from pysolarsys.types import BodyType, Point, Vector


class Simulator:
    def __init__(self, name: str, display_size: Tuple[int, int], max_iteration: int | None = None):
        self.__max_iter = max_iteration
        self.__solar_system = SolarSystem()
        self.__display = Display(display_size[0], display_size[1])
        self.__simulation_name = name

    def load(self, simulation_name: str, file_path: pathlib.Path | None= None):
        p = file_path or pathlib.Path.cwd() / SIMULATION_FILE
        if not p.exists():
            raise FileNotFoundError(f'{p.as_posix()} cannot be found')
        try:
            all_data = json.loads(p.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            raise ValueError(f'{p.as_posix()} cannot be read as JSON')
        except OSError as err:
            raise ValueError(f'Cannot read from file {p.as_posix()}: {err}')

        if 'simulations' not in all_data:
            raise ValueError('Bad file format')

        if simulation_name not in all_data['simulations']:
            raise ValueError(f'Unknown simulation {simulation_name}')

        simu = all_data['simulations'][simulation_name]

        for planet in simu['planets']:
            self.add_planet(planet['name'], planet['mass'],
                            Point(*planet['initial_position']), Vector(*planet['velocity']))
        for sun in simu['suns']:
            body_type = BodyType.from_value(sun['body_type'])
            if BodyType.STAR == body_type:
                self.add_sun(sun['name'], sun['mass'], Point(*sun['initial_position']), Vector(*sun['velocity']))
            elif BodyType.GIANT_STAR == body_type:
                self.add_giant_star(sun['name'], sun['mass'], Point(*sun['initial_position']), Vector(*sun['velocity']))
            elif BodyType.SUPER_GIANT_STAR == body_type:
                self.add_super_giant_star(sun['name'], sun['mass'],
                                          Point(*sun['initial_position']), Vector(*sun['velocity']))
            elif BodyType.WHITE_DWARF_STAR == body_type:
                self.add_white_dwarf(sun['name'], sun['mass'],
                                     Point(*sun['initial_position']), Vector(*sun['velocity']))

        self.__simulation_name = simulation_name

    def save(self):
        p = pathlib.Path.cwd() / SIMULATION_FILE
        if not p.exists():
            p.touch()
        data = dict(planets=[], suns=[])
        for body in self.__solar_system.initial_conditions:
            body_data = dict(name=body.name, mass=body.mass, body_type=body.body_type.value,
                             initial_position=[body.position.x, body.position.y, body.position.z],
                             velocity=[body.velocity.x, body.velocity.y, body.velocity.z])
            if body.is_sun:
                data['suns'].append(body_data)
            else:
                data['planets'].append(body_data)
        else:
            all_data = dict(simulations=dict())
            try:
                all_data = json.loads(p.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                pass
            all_data['simulations'][self.__simulation_name] = data
            with p.open('w') as f:
                f.write(json.dumps(all_data))

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

        self.__solar_system.capture_initial_conditions()
        self.__display.init(self.__solar_system)

        while not stop:
            if self.__display.save_simulation():
                self.save()
                self.__display.reset_save_simulation_marker()
            if not self.__display.is_paused():
                self.__solar_system.compute_next_step()
            else:
                it += 1
            self.__display.draw_and_listen(self.__solar_system)
            stop = self.__max_iter is not None and it > self.__max_iter
            stop = stop or self.__display.stop_requested()
        self.__display.deinit()
        turtle.bye()
