# ←←← ADD THESE 4 LINES AT THE VERY TOP (before any other import)
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"   # forces web canvas
import pygame
pygame.init()
# ←←← END OF REQUIRED CHANGES

import simpy
import random
import math

# CONFIGURATION
FPS = 30
WIDTH, HEIGHT = 1000, 800
SCALE = 1e-4       # meters per pixel (0.1 mm/px)
NUM_ELECTRONS =10
TIME_STEP = 5e-7   # simulation time step (seconds)
ELECTRON_MASS = 9.1093837e-31  # kg
ELECTRON_CHARGE = -1.602e-19   # C
K_CONST = 8.99e9   # N·m²/C²
RADIUS_PIXELS = 10
BACKGROUND = (0, 0, 0)
E_COLOR = (255, 255, 0)
V0 = 1e3          # initial max speed (m/s)

class ElectronSim:
    def __init__(self, env):
        self.env = env
        # Initialize positions (meters) and velocities (m/s)
        self.positions = [
            [random.uniform(0, WIDTH) * SCALE,
             random.uniform(0, HEIGHT) * SCALE]
            for _ in range(NUM_ELECTRONS)
        ]
        self.velocities = [
            [random.uniform(-V0, V0),
             random.uniform(-V0, V0)]
            for _ in range(NUM_ELECTRONS)
        ]
        env.process(self.simulation_process())

    def simulation_process(self):
        while True:
            # Reset forces
            forces = [[0.0, 0.0] for _ in range(NUM_ELECTRONS)]

            # Compute Coulomb forces pairwise
            for i in range(NUM_ELECTRONS):
                x1, y1 = self.positions[i]
                for j in range(i + 1, NUM_ELECTRONS):
                    x2, y2 = self.positions[j]
                    dx = x1 - x2
                    dy = y1 - y2
                    dist = math.hypot(dx, dy)
                    if dist < 1e-12:
                        continue  # avoid singularity
                    # Coulomb's law magnitude
                    force_mag = K_CONST * ELECTRON_CHARGE**2 / dist**2
                    fx = force_mag * (dx / dist)
                    fy = force_mag * (dy / dist)
                    # apply equal & opposite
                    forces[i][0] += fx
                    forces[i][1] += fy
                    forces[j][0] -= fx
                    forces[j][1] -= fy

            # Update velocities and positions
            for idx in range(NUM_ELECTRONS):
                fx, fy = forces[idx]
                ax = fx / ELECTRON_MASS
                ay = fy / ELECTRON_MASS
                # v = v + a*dt
                self.velocities[idx][0] += ax * TIME_STEP
                self.velocities[idx][1] += ay * TIME_STEP
                # x = x + v*dt
                self.positions[idx][0] += self.velocities[idx][0] * TIME_STEP
                self.positions[idx][1] += self.velocities[idx][1] * TIME_STEP

            # Boundary collisions: reflect at edges
            max_x = WIDTH * SCALE
            max_y = HEIGHT * SCALE
            for idx in range(NUM_ELECTRONS):
                x, y = self.positions[idx]
                vx, vy = self.velocities[idx]
                if x <= 0 or x >= max_x:
                    vx *= -1
                    x = max(0, min(x, max_x))
                if y <= 0 or y >= max_y:
                    vy *= -1
                    y = max(0, min(y, max_y))
                self.positions[idx] = [x, y]
                self.velocities[idx] = [vx, vy]

            # Advance SimPy time
            yield self.env.timeout(TIME_STEP)

    def draw(self, screen):
        for x, y in self.positions:
            px = int(x / SCALE)
            py = int(y / SCALE)
            pygame.draw.circle(screen, E_COLOR, (px, py), RADIUS_PIXELS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Electron Simulation")
    clock = pygame.time.Clock()

    # Create SimPy environment and simulation
    env = simpy.Environment()
    elsim = ElectronSim(env)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Step simulation and render
        env.step()
        screen.fill(BACKGROUND)
        elsim.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()