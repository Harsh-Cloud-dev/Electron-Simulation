import asyncio
import pygame, simpy, random, math

FPS = 30
WIDTH, HEIGHT = 1000, 800
SCALE = 1e-4
NUM_ELECTRONS = 10
TIME_STEP = 5e-7
E_COLOR = (255,255,0)
RADIUS = 10
BACKGROUND = (0,0,0)
V0 = 1e3
ELECTRON_MASS = 9.109e-31
ELECTRON_CHARGE = -1.602e-19
K_CONST = 8.99e9

class ElectronSim:
    def __init__(self, env):
        self.env = env
        self.positions = [[random.random()*WIDTH*SCALE, random.random()*HEIGHT*SCALE] for _ in range(NUM_ELECTRONS)]
        self.velocities = [[random.uniform(-V0,V0), random.uniform(-V0,V0)] for _ in range(NUM_ELECTRONS)]
        env.process(self.sim())

    def sim(self):
        while True:
            forces = [[0.0,0.0] for _ in range(len(self.positions))]
            n = len(self.positions)
            for i in range(n):
                x1,y1 = self.positions[i]
                for j in range(i+1, n):
                    x2,y2 = self.positions[j]
                    dx,dy = x1-x2, y1-y2
                    dist = math.hypot(dx,dy)
                    if dist<1e-12: continue
                    f = K_CONST*ELECTRON_CHARGE**2/dist**2
                    fx, fy = f*dx/dist, f*dy/dist
                    forces[i][0]+=fx; forces[i][1]+=fy
                    forces[j][0]-=fx; forces[j][1]-=fy
            for i in range(n):
                fx, fy = forces[i]
                ax, ay = fx/ELECTRON_MASS, fy/ELECTRON_MASS
                self.velocities[i][0]+=ax*TIME_STEP
                self.velocities[i][1]+=ay*TIME_STEP
                self.positions[i][0]+=self.velocities[i][0]*TIME_STEP
                self.positions[i][1]+=self.velocities[i][1]*TIME_STEP
            max_x,max_y = WIDTH*SCALE, HEIGHT*SCALE
            for i in range(n):
                x,y = self.positions[i]; vx,vy = self.velocities[i]
                if x<=0 or x>=max_x: vx=-vx
                if y<=0 or y>=max_y: vy=-vy
                self.positions[i]=[max(0,min(x,max_x)), max(0,min(y,max_y))]
                self.velocities[i]=[vx,vy]

            yield self.env.timeout(TIME_STEP)

    def draw(self, screen):
        for x,y in self.positions:
            pygame.draw.circle(screen, E_COLOR, (int(x/SCALE), int(y/SCALE)), RADIUS)

    def add_electron(self):
        self.positions.append([random.random()*WIDTH*SCALE, random.random()*HEIGHT*SCALE])
        self.velocities.append([random.uniform(-V0,V0), random.uniform(-V0,V0)])

    def remove_electron(self):
        if self.positions:
            self.positions.pop()
            self.velocities.pop()


async def main_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Electron Simulation")
    env = simpy.Environment()
    sim = ElectronSim(env)
    running=True

    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    sim.add_electron()
                elif event.key == pygame.K_l:
                    sim.remove_electron()

        env.step()
        screen.fill(BACKGROUND)
        sim.draw(screen)
        pygame.display.flip()
        await asyncio.sleep(1/FPS)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main_loop())
