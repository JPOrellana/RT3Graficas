import pygame
from pygame.locals import *
from rt import Raytracer
from figuras import *
from lights import *
from materials import *

width = 500
height = 500

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

raytracer = Raytracer(screen)

raytracer.rtClearColor(0.25, 0.25, 0.25)

TexturaSuelo = pygame.image.load("Cuarto/Piso1.jpg")
TexturaTecho = pygame.image.load("Cuarto/Techo1.jpg")
TexturaPared = pygame.image.load("Cuarto/Pared1.jpg")
TexturaFondo = pygame.image.load("Cuarto/Fondo1.jpg")


TexturaAzul = pygame.image.load("Texturas/azul.jpg")
TexturaMorada = pygame.image.load("Texturas/morado.jpg")


Pared = Material(spec = 5, Ks = 0.1, texture = TexturaPared)
Piso = Material(spec = 5, Ks = 0.2, texture = TexturaSuelo)
Techo = Material(spec = 5, Ks = 0.25, texture = TexturaTecho)
Fondo = Material(spec = 64, Ks = 0.9, texture = TexturaFondo)

morada = Material(spec = 32, Ks = 0.8, texture = TexturaMorada)
azul = Material(spec = 64, Ks = 0.9, texture = TexturaAzul)



# 
Espejo = Material(diffuse=(0.6, 0.7, 1), spec = 64, Ks = 0.2, matType = REFLECTIVE)



raytracer.scene.append(Plane(position = (0,-5,0), normal=(0,1,0), material =  Piso))       
raytracer.scene.append(Plane(position = (0,4,0), normal=(0,-1,0), material =  Techo))       
raytracer.scene.append(Plane(position = (-5,0,0), normal=(1,0,0), material =  Pared))        
raytracer.scene.append(Plane(position = (5,0,0), normal=(-1,0,0), material =  Pared))               
raytracer.scene.append(Plane(position = (0,0,-20), normal=(0,0,-1), material = Fondo))    


raytracer.scene.append(AABB(position = (-1.1,-1,-5), size = (1.3,1.3,1.3), material = azul))
raytracer.scene.append(AABB(position = (1.1,-1,-6), size = (1.3,1.3,1.3), material = morada))

raytracer.scene.append(Disk(position=(0,0,-10), normal=(0,0,1), radius = 1.2, material= Espejo))


raytracer.lights.append(AmbientLight(intensity = 0.7))


raytracer.rtClear()
raytracer.rtRender()

print("\n Render Time: ", pygame.time.get_ticks() / 1000, "secs")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                isRunning = False


rect = pygame.Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "output.jpg")

pygame.quit()