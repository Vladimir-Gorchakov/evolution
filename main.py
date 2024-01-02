#Global imports
import pygame
import numpy as np
#3 fps without numba 

#My project imports
from organism_vectorization import System
from utils import Render


pygame.init()

#for text rendering
render = Render()

#For custom FPS
clock = pygame.time.Clock()
FPS = 60

# Create a HxW window
h, w = 800, 1200
window = pygame.display.set_mode((w, h))

#set parameters
G = -1/10**3
EPS = 1/10**8
# Create a particle system
particle_system = System(h, w, FPS, G, EPS)

# Add a particle
num_particles = [200, 200, 100, 100]
#polyarity_matrix = [[ 1,-1, 1],
#                    [-1, 1, 1],
#                    [ 1, 1, 1]]
polyarity_matrix = list(np.random.rand(4,4)*2 - 1)
#print('polyarity_matrix ', polyarity_matrix)
colours = [(0,255,0),(255,0,0),(0,0,255),(255,0,255)]
mass = [1,1,1,1]
#num_particles = [3]
#polyarity_matrix = [[1]]
#colours = [(0,255,0)]
#mass = [1]

particle_system.add_particles(num_particles, polyarity_matrix, colours, mass, speed_dactor = 10)

# Main game loop
running = True
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_w:
            FPS+=10
         elif event.key == pygame.K_q:
          FPS-=10

   # Fill the screen with black
   window.fill((0, 0, 0))
   for i, num in enumerate(num_particles):
    render.render_text('number of particles{}: {}'.format(i,num), window)

   for i, p in enumerate(particle_system.particles):
    num = round(np.max(np.linalg.norm(p.dv, axis = 1)),3)
    render.render_text('max speed of particle{}: {}'.format(i,num), window) 
   render.render_text('FPS : curent {} basic {}'.format(int(clock.get_fps()), FPS), window)
   render.clear()

   # Update and draw the particle system
   particle_system.update()
   particle_system.draw(window)

   # Flip the display
   pygame.display.flip()

   # Limit the FPS by sleeping for the remainder of the frame time
   clock.tick(FPS)
   

pygame.quit()
