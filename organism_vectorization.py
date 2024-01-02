import numpy as np
import pygame
import time
#import numexpr as ne
from multiprocessing import Pool

class Particle:
    def __init__(self, coord = None, dv = None, FPS = 30, mass = 1, colour = (200,200,200)): # first index - index of elemnt, second index of coordinate
        self.coord = coord
        self.dv = dv
        self.fps = FPS
        self.mass = mass
        self.colour = colour
        self.Bound = True
        self.multiplayer = 2
    def update(self):
        if self.Bound and (np.any(self.coord[:,0] < 0) or np.any(self.coord[:,0]  > 1)):
            self.dv[(self.coord[:,0]  < 0),0] *= -self.multiplayer 
            self.dv[(self.coord[:,0]  > 1),0] *= -self.multiplayer 
        if self.Bound and (np.any(self.coord[:,1] < 0) or np.any(self.coord[:,1]  > 1)):
            self.dv[(self.coord[:,1]  < 0),1] *= -self.multiplayer 
            self.dv[(self.coord[:,1]  > 1),1] *= -self.multiplayer 
        self.coord += self.dv/self.fps
    
    def rand_init(self, num, speed_factor):
        self.coord = np.random.rand(num,2)
        self.dv = (np.random.rand(num,2)*2 - 1)/(speed_factor*self.mass)

class Gravity:
    def __init__(self, G, EPS, FPS):
        self.G = G
        self.eps = EPS
        self.fps = FPS
        self.reduce = 1 - 1/50
        self.porog = 10**4
    # gravitation force betveen two set of particles
    @staticmethod
    def _update(prtc1_cord, prtc2_cord, prtc2_dv, prct1_mass, polyarity, coeff, G, eps, fps, porog, red): #particle - object class Particle
        mass = prct1_mass
        r = prtc2_cord[:, np.newaxis] - prtc1_cord # r
        r_norm = np.sum((r**2),axis=2)
        r_norm = r_norm**(3/2)
        masked_r = (r_norm < eps)
        r_norm = np.expand_dims(np.reciprocal(r_norm + eps), axis = 2) # 1/|r|^2
        r_norm[masked_r] = 0
        r_norm[r_norm > porog] = 0
        gamma = coeff*G*mass*polyarity/fps
        prtc2_dv += np.sum(r*r_norm, axis = 1)*gamma # F = -G*r/|r|^2
        prtc2_dv *= red

    def update(self, particle1, particle2, polyarity, coeff):

        self._update(prtc1_cord = particle1.coord, prtc2_cord = particle2.coord,
                     prtc2_dv = particle2.dv, prct1_mass = particle1.mass, polyarity = polyarity, coeff = coeff,
                      G = self.G, eps = self.eps, fps = self.fps, porog = self.porog, red = self.reduce)
            


class System:
    def __init__(self,h, w, FPS, G, EPS):
       self.particles = []
       self.polyarity_matrix = []
       self.gravity = Gravity(G, EPS, FPS)
       self.G, self.EPS, self.FPS = G, EPS, FPS
       self.fps = FPS
       self.h = h
       self.w = w
       self.stars = []
       self.speeding = 0
       self.collision_factor = 1/10*3

    def add_particles(self, number_particels, polyarity_matrix, colours, mass = None, speed_dactor = 2):
        for i, num in enumerate(number_particels):
            self.particles.append(Particle(self.fps, mass = mass[i], colour = colours[i]))
            self.particles[-1].rand_init(num, speed_dactor)
        self.polyarity_matrix = polyarity_matrix


    def collision(self, cord1, cord2, dv2):
        r = cord2[:, np.newaxis] - cord1 # r
        r_norm = np.linalg.norm((r**2), axis=2)
        masked_r = np.logical_and((r_norm < self.collision_factor),(r_norm > self.EPS))
        #r[masked_r]

    def update(self):
        for i in range(len(self.particles)):
            for j in range(len(self.particles)):
                self.gravity.update(self.particles[i], self.particles[j], self.polyarity_matrix[i][j], int(i==j) + 1)
        for p in self.particles:
            p.update()


    def draw(self, window):
        for particle in self.particles:
           for cord in particle.coord:
               x, y = cord
               pygame.draw.circle(window, particle.colour, (int(self.w * x), int(self.h * y)), int(5*(particle.mass)**(1/5)))