# What is this?
This project holds a basic simulation engine for computing planets and suns movement in a solar system. This project makes use of
several shortcuts from a theoretical point of view. To read about these, please follow this [link](Physics.md)

This project should be considered only for demonstration purpose.

# Installation
You must have a valid Python 3.10 installation. No other 3d parts libraries are needed for the moment.

# Example
A basic example with an unstable system which sees the two planets collides after 9 revolutions:
```python
from pysolarsys.simulator import Simulator
from pysolarsys.types import Point, Vector

sim = Simulator((1400, 1050), max_iteration=5000)
sim.add_white_dwarf('HIP_XYZ', 10_000, Point(-200, 0), Vector(0, 3.5))
sim.add_white_dwarf('HIP_ZYW', 10_000, Point(200, 0), Vector(0, -3.5))
sim.add_planet('P1', mass=20, position=Point(50, 0), velocity=Vector(0, 11))
sim.add_planet('P2', mass=3, position=Point(-350, 0), velocity=Vector(0, -10))

sim.run()
```

# Credits
The overall physics logic comes from *Stephen Gruppetta* and his article on [Python Coding Book](Simulating Orbiting Planets in a Solar System Using Python).
