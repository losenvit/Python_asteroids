
import math
import random

import pyglet
from pyglet import gl

# CONSTANTS
WIDTH = 800
HEIGHT = 600
ROTATION_SPEED = 100
ACCELERATION = 100

# IMAGES
def load_image(filename):
    image = pyglet.image.load(filename)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

spaceship_img = load_image('Include/PNG/playerShip2_red.png')

main_batch = pyglet.graphics.Batch()

pressed_keys = set()
objects = []

class Spaceship:
    def __init__(self, window, image, batch = main_batch):
        self.x = window.width / 2
        self.y = window.height / 2
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = random.randint(0, 360)
        self.sprite = pyglet.sprite.Sprite(image, batch = batch)
        self.window = window

    def delete(self):
        if self in objects:
            objects.remove(self)
            self.sprite.delete()

    def tick(self, dt):
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt

        self.sprite.x = self.x
        self.sprite.y = self.y

        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += dt * ROTATION_SPEED
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= dt * ROTATION_SPEED
        if pyglet.window.key.UP in pressed_keys:
            rotation_radians = math.radians(self.rotation)
            self.x_speed += dt * ACCELERATION * math.cos(rotation_radians)
            self.y_speed += dt * ACCELERATION * math.sin(rotation_radians)

        self.sprite.rotation = 90 - self.rotation

        if self.x < 0:
            self.x += self.window.width
        if self.y < 0:
            self.y += self.window.height
        if self.x > self.window.width:
            self.x -= self.window.width
        if self.y > self.window.height:
            self.y -= self.window.height

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

spaceship = Spaceship(window, spaceship_img)
objects.append(spaceship)
spaceship = Spaceship(window, spaceship_img)
objects.append(spaceship)
spaceship = Spaceship(window, spaceship_img)
objects.append(spaceship)
pyglet.clock.schedule(tick)
pyglet.app.run()
