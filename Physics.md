# Simulating planets orbits

A solar system consists of one or more suns and other bodies orbiting around suns. This simulator allows you to include suns and planets though it should be feasible to extend it to include other bodies such as moons, comets, and asteroids.
The gravitational pull between the bodies determines the movement of all the bodies in the solar system.

At any point in time, a solar system body has a position and a velocity. The simulator is only able to simulate a 2D solar system. Therefore, all the bodies in the solar system will exist in a 2D plane.
The position of each body is represented by the `Point` object. The velocity of a body represent the components of the velocity along the x- and y-axes. A `Vector` object is used for this purpose.

Any two bodies have a [gravitational force](https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation) that pulls them towards each other. The gravitational force $F$ is given by:

<img src="https://render.githubusercontent.com/render/math?math=F = G \frac{m_{1}m_{2}}{r^{2}}">

<img src="https://render.githubusercontent.com/render/math?math=G"> is the gravitational constant, which we will be able to ignore for this simulation since we will work in arbitrary units. The gravitational force depends on the mass of the two objects, <img src="https://render.githubusercontent.com/render/math?math=m_{1}"> and <img src="https://render.githubusercontent.com/render/math?math=m_{2}"> and the distance between the objects <img src="https://render.githubusercontent.com/render/math?math=r">.
Although the masses are normally measured in kg and the distance in m, we use arbitrary units in the simulator. This means that we use unitless values for representing mass and distance. 


## Gravity

Since we are using arbitrary units in this example, the force between two bodies can be simplified as:
<img src="https://render.githubusercontent.com/render/math?math=F=\frac{m_1m_2}{r^2}">

The effect of a force is to accelerate the object. The relationship between the force exerted on a body, the acceleration and the body's mass is given by:
<img src="https://render.githubusercontent.com/render/math?math=F = ma">
The term $a$ represents the acceleration. If you have both force and mass, the acceleration can be found using
<img src="https://render.githubusercontent.com/render/math?math=a=\frac{F}{m}">

Therefore, you can work out the gravitational force between two objects and then calculate the acceleration this force causes for each body.

The force has a direction, too. It acts in the direction of the line joining the centres of the two bodies. The acceleration of the two bodies also acts along this same direction.
However, you’re dealing with the x– and y-components of the velocity. Therefore, you’ll need to find the x– and y-components of the acceleration, too. You can achieve this through trigonometry:

<img src="https://render.githubusercontent.com/render/math?math=a_x = a\cos{\theta}">

<img src="https://render.githubusercontent.com/render/math?math=a_y = a\sin{\theta}">

where <img src="https://render.githubusercontent.com/render/math?math=\theta"> represents the angle that the line joining the two bodies makes with the horizontal.
