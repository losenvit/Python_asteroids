
import math
import random

import pyglet
from pyglet import gl

# CONSTANTS
WIDTH = 800
HEIGHT = 600

ROTATION_SPEED = 100
ACCELERATION = 100
SPACESHIP_RADIUS = 45

ASTEROID_MAX_SPEED = 200
ASTEROID_RADIUSES = {1: 7, 2: 11, 3: 19, 4: 42}

# IMAGES
def load_image(filename):
    image = pyglet.image.load(filename)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

spaceship_img = load_image('Include/PNG/playerShip2_red.png')

asteroid_imgs = {
    1:  [load_image('Include/PNG/Meteors/meteorBrown_tiny1.png'),
         load_image('Include/PNG/Meteors/meteorBrown_tiny2.png'),
         load_image('Include/PNG/Meteors/meteorGrey_tiny1.png'),
         load_image('Include/PNG/Meteors/meteorGrey_tiny2.png'),],
    2:  [load_image('Include/PNG/Meteors/meteorBrown_small1.png'),
         load_image('Include/PNG/Meteors/meteorBrown_small2.png'),
         load_image('Include/PNG/Meteors/meteorGrey_small1.png'),
         load_image('Include/PNG/Meteors/meteorGrey_small1.png'),],
    3:  [load_image('Include/PNG/Meteors/meteorBrown_med1.png'),
         load_image('Include/PNG/Meteors/meteorBrown_med2.png'),
         load_image('Include/PNG/Meteors/meteorGrey_med1.png'),
         load_image('Include/PNG/Meteors/meteorGrey_med1.png'),],
    4:  [load_image('Include/PNG/Meteors/meteorBrown_big1.png'),
         load_image('Include/PNG/Meteors/meteorBrown_big2.png'),
         load_image('Include/PNG/Meteors/meteorBrown_big3.png'),
         load_image('Include/PNG/Meteors/meteorBrown_big4.png'),
         load_image('Include/PNG/Meteors/meteorGrey_big1.png'),
         load_image('Include/PNG/Meteors/meteorGrey_big2.png'),
         load_image('Include/PNG/Meteors/meteorGrey_big3.png'),
         load_image('Include/PNG/Meteors/meteorGrey_big4.png'),],
}

main_batch = pyglet.graphics.Batch()

pressed_keys = set()
objects = []

# temporary
def draw_circle(x, y, radius):
    iterations = 20
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    for i in range(iterations+1):
        gl.glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    gl.glEnd()
#

# static functions
def distance(a, b, dimension_size):
    dist = abs(a - b)
    if dist > dimension_size / 2:
        dist = dimension_size - dist
    return dist

def is_Overlapped(obj1, obj2):
    obj2obj_distance = (distance(obj1.x, obj2.x, window.width) ** 2 +
                       distance(obj1.y, obj2.y, window.height) ** 2)
    contact_distance = (obj1.radius + obj2.radius) ** 2
    return obj2obj_distance < contact_distance
#

class SpaceObject:
    def __init__(self, window, image, x, y, radius, x_speed = 0, y_speed = 0,
                rotation = 0, batch = main_batch):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotation = rotation
        self.radius = radius
        self.sprite = pyglet.sprite.Sprite(image, batch = batch)
        self.window = window

    def tick(self, dt):
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt
        self.sprite.x = self.x
        self.sprite.y = self.y

        self.sprite.rotation = 90 - self.rotation

        if self.x < 0:
            self.x += self.window.width
        if self.y < 0:
            self.y += self.window.height
        if self.x > self.window.width:
            self.x -= self.window.width
        if self.y > self.window.height:
            self.y -= self.window.height

    def spaceship_colision(self, spaceship):
        return

class Spaceship(SpaceObject):
    def __init__(self, window, rotation = 0):
        super().__init__(window = window,
                         image = spaceship_img,
                         rotation = random.uniform(0, 360),
                         radius = SPACESHIP_RADIUS,
                         x = window.width / 2,
                         y = window.height / 2,
                         )

    def delete(self):
        if self in objects:
            objects.remove(self)
            self.sprite.delete()

    def tick(self, dt):
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += dt * ROTATION_SPEED
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= dt * ROTATION_SPEED
        if pyglet.window.key.UP in pressed_keys:
            rotation_radians = math.radians(self.rotation)
            self.x_speed += dt * ACCELERATION * math.cos(rotation_radians)
            self.y_speed += dt * ACCELERATION * math.sin(rotation_radians)
        if pyglet.window.key.DOWN in pressed_keys:
            rotation_radians = math.radians(self.rotation)
            self.x_speed -= dt * ACCELERATION * math.cos(rotation_radians)
            self.y_speed -= dt * ACCELERATION * math.sin(rotation_radians)

        super().tick(dt)

        for obj in objects:
            if is_Overlapped(obj, self):
                obj.spaceship_colision(self)

class Asteroid(SpaceObject):
    def __init__(self, window, size):
        # choose starting position
        zero_dimension = random.choice(['x', 'y'])
        if zero_dimension == 'x':
            x = 0
            y = random.randrange(window.height)
        else:
            x = random.randrange(window.width)
            y = 0

        img = random.choice(asteroid_imgs[size])
        super().__init__(window = window,
                         radius = ASTEROID_RADIUSES[size],
                         image = img,
                         x = x,
                         y = y,
                         x_speed = random.uniform(-ASTEROID_MAX_SPEED,
                                                  ASTEROID_MAX_SPEED),
                         y_speed = random.uniform(-ASTEROID_MAX_SPEED,
                                                  ASTEROID_MAX_SPEED),
                         )

    def spaceship_colision(self, spaceship):
        spaceship.delete()


def key_pressed(key, mod):
    pressed_keys.add(key)

def key_released(key, mod):
    pressed_keys.discard(key)

def draw():
    window.clear()
    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            # Remember the current state
            gl.glPushMatrix()
            # Move everything drawn from now on by (x_offset, y_offset, 0)
            gl.glTranslatef(x_offset, y_offset, 0)

            # Draw
            main_batch.draw()
            for obj in objects:
                draw_circle(obj.x, obj.y, obj.radius)
            # Restore remembered state (this cancels the glTranslatef)
            gl.glPopMatrix()

def tick(dt):
    for obj in objects:
        obj.tick(dt)

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
window.push_handlers(
    on_draw=draw,
    on_key_press=key_pressed,
    on_key_release=key_released,
)

spaceship = Spaceship(window)
objects.append(spaceship)

asteroid = Asteroid(window, 1)
objects.append(asteroid)
asteroid = Asteroid(window, 2)
objects.append(asteroid)
asteroid = Asteroid(window, 3)
objects.append(asteroid)
asteroid = Asteroid(window, 4)
objects.append(asteroid)



pyglet.clock.schedule_interval(tick, 1/60)
pyglet.app.run()
