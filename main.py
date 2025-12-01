import asyncio
import math
import random
import simpy
import pygame

# CONFIGURATION
FPS = 30
WIDTH, HEIGHT = 1000, 800

SCALE = 1e-4            # meters per pixel
NUM_ELECTRONS = 10
TIME_STEP = 5e-7        # simulation time step

ELECTRON_MASS = 9.109e-31
ELECTRON_CHARGE = -1.602e-19
K_CONST = 8.99e9

RADIUS = 10
E_COLOR = (255, 255, 0)
BACKGROUND = (0, 0, 0)

V0 = 1e3  # initial random velocity
# ---------------------------------------


class ElectronSim:
    def __init__(self, env):
        self.env = env

        # Random start positions
        self.positions = [
            [random.random() * WIDTH * SCALE,
             random.random() * HEIGHT * SCALE]
            for _ in range(NUM_ELECTRONS)
        ]

        # Random initial velocities
        self.velocities = [
            [random.uniform(-V0, V0),
             random.uniform(-V0, V0)]
            for _ in range(NUM_ELECTRONS)
        ]

        env.process(self.sim())

    def sim(self):
        while True:
            forces = [[0.0, 0.0] for _ in range(NUM_ELECTRONS)]

            # Pairwise Coulomb force calculation
            for i in range(NUM_ELECTRONS):
                x1, y1 = self.positions[i]
                for j in range(i + 1, NUM_ELECTRONS):
                    x2, y2 = self.positions[j]

                    dx = x1 - x2
                    dy = y1 - y2
                    dist = math.hypot(dx, dy)
                    if dist < 1e-12:
                        continue

                    force_mag = K_CONST * ELECTRON_CHARGE**2 / dist**2
                    fx = force_mag * (dx / dist)
                    fy = force_mag * (dy / dist)

                    forces[i][0] += fx
                    forces[i][1] += fy
                    forces[j][0] -= fx
                    forces[j][1] -= fy

            # Integrate motion
            for i in range(NUM_ELECTRONS):
                fx, fy = forces[i]
                ax = fx / ELECTRON_MASS
                ay = fy / ELECTRON_MASS

                self.velocities[i][0] += ax * TIME_STEP
                self.velocities[i][1] += ay * TIME_STEP

                self.positions[i][0] += self.velocities[i][0] * TIME_STEP
                self.positions[i][1] += self.velocities[i][1] * TIME_STEP

            # Boundary reflection
            max_x = WIDTH * SCALE
            max_y = HEIGHT * SCALE
            for i in range(NUM_ELECTRONS):
                x, y = self.positions[i]
                vx, vy = self.velocities[i]

                if x <= 0 or x >= max_x:
                    vx = -vx
                if y <= 0 or y >= max_y:
                    vy = -vy

                self.positions[i] = [
                    max(0, min(x, max_x)),
                    max(0, min(y, max_y))
                ]
                self.velocities[i] = [vx, vy]

            yield self.env.timeout(TIME_STEP)

    def draw(self, screen):
        for x, y in self.positions:
            px = int(x / SCALE)
            py = int(y / SCALE)
            pygame.draw.circle(screen, E_COLOR, (px, py), RADIUS)


async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Electron Simulation")

    env = simpy.Environment()
    sim = ElectronSim(env)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        env.step()

        screen.fill(BACKGROUND)
        sim.draw(screen)
        pygame.display.flip()

        await asyncio.sleep(1 / FPS)

    pygame.quit()


asyncio.run(main())
