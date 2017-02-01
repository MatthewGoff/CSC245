# CSC245
Repository for games and projects in CSC245. Everything in this repository is
for academic use only. Please do not share, reuse or sell any of this code.

Contains some class exercises, my own work. I may put some collaborative work
here.

Sources:

Transparancy: http://stackoverflow.com/questions/17581545/drawn-surface-transparency-in-pygame
Quadtree: https://gamedevelopment.tutsplus.com/tutorials/quick-tip-use-quadtrees-to-detect-likely-collisions-in-2d-space--gamedev-374
Collisions: http://vobarian.com/collisions/2dcollisions2.pdf

Angry Birds:
Sprites: http://stackoverflow.com/questions/13057901/how-do-i-bind-a-pyglet-sprite-with-a-pymunk-shape-so-they-rotate-together
https://github.com/viblo/pymunk/blob/master/examples/breakout.py
Getting collision events: https://github.com/viblo/pymunk/blob/master/examples/breakout.py

Images:


Sounds:


# TODO:

### Physics:
- Change the quadtree so garbage collection is more efficient
- Eliminate redundant collision checks (top down quadtree iteration)
- Introduce dynamic time steps
- Make Quad tree responsible for collisions
- Max speed, after which there is drag
- Check type of inheritance
- Conduct thurough test of collisions
- Introduce reduced tangential friction

### Aesthetics:
- Remove setters and getters (More pythonic ?)
