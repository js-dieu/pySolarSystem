import itertools
import turtle
from pysolarsys.physics import SolarSystem
from pysolarsys.types import Vector, WindowRange, BodyType, Point


stop_requested = False
pause_requested = False


def stop_request():
    global stop_requested
    stop_requested = True


def toggle_pause():
    global pause_requested
    pause_requested = not pause_requested


class DisplayInfo:
    def __init__(self) -> None:
        self.positions = False
        self.names = False
        self.velocities = False

    def __bool__(self) -> bool:
        return any((self.positions, self.names, self.velocities))

    def __call__(self, name, x, y, vel) -> str | None:
        infos = []
        if self.names:
            infos.append(name)
        if self.positions:
            infos.append(f'{x:.2} {y:.2}')
        if self.velocities:
            infos.append(f'{vel[0]:.2} {vel[1]:.2}')
        if not infos:
            return None
        return "".join(infos)


class BodyView(turtle.Turtle):
    Planet_Colors = itertools.cycle([(181, 167, 167), (227, 187, 118), (59, 93, 56), (226, 123, 88), (200, 139, 58),
                                     (197, 171, 110), (213, 251, 252), (62, 84, 232), (255, 241, 213)])
    Sun_Color = (0, 0, 220)
    White_Dwarf_Color = (240, 240, 240)
    Giant_Color = (251, 189, 20)
    Super_Giant_Color = (255, 87, 79)

    def __init__(self, name: str, radius: float, position: Vector, body_type: BodyType) -> None:
        super().__init__()
        self.__name = name
        self.__display_size = int(radius)
        self.setposition(position.x, position.y)
        if body_type.value == BodyType.PLANET.value:
            self.color(next(BodyView.Planet_Colors))
        elif body_type.value == BodyType.STAR:
            self.color(*BodyView.Sun_Color)
        elif body_type.value == BodyType.WHITE_DWARF_STAR:
            self.color(*BodyView.White_Dwarf_Color)
        elif body_type.value == BodyType.SUPER_GIANT_STAR:
            self.color(*BodyView.Super_Giant_Color)
        elif body_type.value == BodyType.GIANT_STAR:
            self.color(*BodyView.Giant_Color)
        else:
            self.color((0, 255, 0))
        self.penup()
        self.hideturtle()

    def remove_from_screen(self):
        self.clear()

    def draw(self, position: Point):
        self.clear()
        self.goto(position.x, position.y)
        self.dot(self.__display_size)

    @property
    def name(self) -> str:
        return self.__name


class Display:
    def __init__(self, width: int = 1200, height: int = 900) -> None:
        self.__screen = turtle.Screen()
        self.__screen.tracer(0)
        self.__screen.colormode(255)
        self.__screen.setup(width, height)
        self.__screen.bgcolor(25, 25, 25)
        self.__screen.update()
        self.__display_info = DisplayInfo()
        self.__bodies = {}

    @staticmethod
    def stop_requested():
        global stop_requested
        return stop_requested

    @staticmethod
    def is_paused():
        global pause_requested
        return pause_requested

    def toggle_velocities(self) -> None:
        self.__display_info.velocities = not self.__display_info.velocities

    def toggle_names(self) -> None:
        self.__display_info.names = not self.__display_info.names

    def toggle_positions(self) -> None:
        self.__display_info.positions = not self.__display_info.positions

    def init(self, simulator: SolarSystem):
        turtle.onkey(toggle_pause, 'p')
        turtle.onkey(stop_request, 'q')
        for body in simulator:
            self.__bodies[body.oid] = BodyView(body.name, body.radius, body.position, body.body_type)
            self.__bodies[body.oid].draw(body.position)

    @property
    def width(self) -> float:
        return self.__screen.window_width()
    
    @property
    def height(self) -> float:
        return self.__screen.window_height()

    @property
    def width_window(self) -> WindowRange:
        w = self.width / 2
        return -w, w
    
    @property
    def height_window(self) -> WindowRange:
        h = self.height / 2
        return -h, h
    
    def draw_and_listen(self, solar_system: SolarSystem):
        for i, body in enumerate(solar_system):
            if body.oid not in self.__bodies:
                self.__bodies[body.oid] = BodyView(body.name, body.radius, body.position, body.body_type)
            if body.exists:
                self.__bodies[body.oid].draw(body.position)
            else:
                self.__bodies[body.oid].remove_from_screen()
        self.__screen.update()
        self.__screen.listen()
