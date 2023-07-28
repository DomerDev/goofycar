from ursina import *
from ursina.prefabs import editor_camera
import numpy as np
from random import randint

app = Ursina()
window.borderless = False
window.exit_button.visible = False
window.cog_button.visible = False

earth = Entity(model='sphere', texture="grass", scale=(22, 22, 22), collider='sphere')
carPoint = Entity()
car = Entity(model='cube', color=color.hex("#E01B3E"), scale=(1, 2, 1), position=(0, 0, 11), collider='box')
gameover = Text("{} secs\nSPACE\nto try again", scale=2, origin=(0, 0), background=True, visible=False)
asteroids = []


class Asteroid(Entity):
    def on_enable(self):
        asteroidPoint = Entity()
        self.asteroidPoint = asteroidPoint
        self.parent = asteroidPoint
        self.position = (50, 0, 0)
        asteroidPoint.rotation = (0, randint(0, 360), randint(0, 360))
        self.parent = None

        self.model = "sphere"
        self.collider = "sphere"
        self.texture = "asteroid"
        self.scale = (2.5, 2.5, 2.5)
    def update(self):
        if not self.intersects(earth):
            self.lookAt(earth)
            self.world_position += self.forward * asteroidSpeed * time.dt
        else:
            self.alpha -= asteroidAlphaSpeed * time.dt
            if self.alpha <= 0.15:
                destroy(self.asteroidPoint)
                destroy(self)
        if self.intersects(car):
            gameover.text = "{} secs\nSPACE\nto try again".format(str(round(g_time, 2)))
            gameover.visible = True
            application.paused = True

car.parent = carPoint
camera.parent = carPoint
camera.position = (0, 0, 31)
camera.lookAt(carPoint)
camera.fov = 90

carRotSpeed = 90
g_time = 0

carSpeed = 80
carPointRotSpeed = 45 ##car steer speed
asteroidAlphaSpeed = 0.5
asteroidSpeed = 5
tickSpeed = .5

def tick():
    global asteroidAlphaSpeed
    global asteroidSpeed
    global carSpeed
    global carPointRotSpeed
    global tickSpeed
    asteroids.append(Asteroid())
    if asteroidAlphaSpeed >= 0.02:
        asteroidAlphaSpeed -= 0.01
    asteroidSpeed += 0.015
    carSpeed += 0.02
    carPointRotSpeed += 0.03
    tickSpeed -= 0.001
    if not application.paused:
        invoke(tick, delay=tickSpeed)

pause_handler = Entity(ignore_paused=True)

tick()
def update():
    global g_time
    g_time += time.dt
    carPoint.rotate((-carSpeed*time.dt, 0, 0))

    if held_keys['a']:
        car.rotation_z+=carRotSpeed*time.dt
        carPoint.rotation_z+=carPointRotSpeed*time.dt
    elif held_keys['d']:
        car.rotation_z-=carRotSpeed*time.dt
        carPoint.rotation_z -= carPointRotSpeed * time.dt
    elif car.rotation_z!=0:
        car.rotation_z += (carRotSpeed if car.rotation_z<0 else -carRotSpeed)*time.dt
    car.rotation_z = np.clip(car.rotation_z, -12, 12)

def pause_input(key):
    global asteroidAlphaSpeed
    global asteroidSpeed
    global carSpeed
    global carPointRotSpeed
    global tickSpeed
    global g_time
    if key == "space": ##restart
        application.paused = False
        gameover.visible = False
        for a in asteroids:
            destroy(a)
        carSpeed = 80
        carPointRotSpeed = 45  ##car steer speed
        asteroidAlphaSpeed = 0.5
        asteroidSpeed = 5
        tickSpeed = .5
        g_time = 0
        tick()
pause_handler.input = pause_input
Sky()
app.run()