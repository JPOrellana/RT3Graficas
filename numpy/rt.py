from math import pi, tan, atan2, acos
from materials import *
from numpyPablo import producto_punto, fresnel, calcular_refraccion, reflexion_interna_total, normalizar_vector, add_vector,subtract_vector, reflectVector, vector_scalar_mult
import pygame
import random

MAX_RECURSION_DEPTH = 3


class Raytracer(object):

    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()

        self.scene = [] 
        self.lights = [] 
        
        self.camPosition = [0,0,0]
        self.rtViewport(0, 0, self.width, self.height)
        self.rtProjection()
        
        self.rtColor(1,1,1)
        self.rtClearColor(0,0,0)
        self.rtClear()

        self.environmentMap = None


    def rtViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height


    def rtProjection(self, fov = 60, n = 0.1):
        aspectRatio = self.vpWidth / self.vpHeight

        self.nearPlane = n

        self.topEdge = tan((fov * pi / 180) / 2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio


    def rtClearColor(self, r,g,b):
        self.clearColor = (r*255, g*255, b*255)


    def rtClear(self):
        
        self.screen.fill((self.clearColor[0],
                          self.clearColor[1],
                          self.clearColor[2]))


    def rtColor(self, r, g, b):
        self.currColor = (r*255, g*255, b*255)

    
    def rtPoint(self, x, y, color = None):
        y = self.height - y

        if (0 <= x < self.width) and (0 <= y <self.height):
            if color:
                color = (int(color[0] * 255),
                         int(color[1] * 255),
                         int(color[2] * 255))
                self.screen.set_at((x,y), color)
            else:
                self.screen.set_at((x,y), self.currColor)


    def rtCastRay(self, origin, direction, sceneObj = None, recursion = 0):

        if recursion >= MAX_RECURSION_DEPTH:
            return None

        depth = float('inf')
        intercept = None
        hit = None

        for obj in self.scene:
            if sceneObj != obj:
                intercept = obj.ray_intersect(origin, direction)
                if intercept:
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance
        
        return hit


    def rtRayColor(self, intercept, rayDirection, recursion = 0):

        if intercept == None:
            if self.environmentMap:
                x = (atan2(rayDirection[2], rayDirection[0]) / (2 * pi) + 0.5) * self.environmentMap.get_width()
                y = acos(rayDirection[1]) / pi * self.environmentMap.get_height()

                environmentColor = self.environmentMap.get_at((int(x),int(y)))

                return [environmentColor[i] / 255 for i in range(3)]

            else:
                return None


        material = intercept.obj.material

        surfaceColor = material.diffuse

        if material.texture and intercept.texcoords:
            tX = intercept.texcoords[0] * material.texture.get_width()
            tY = intercept.texcoords[1] * material.texture.get_height()
            
            texColor = material.texture.get_at((int(tX),int(tY)))
            texColor = [i / 255 for i in texColor]
            surfaceColor = [surfaceColor[i] * texColor[i] for i in range(3)]


        reflectColor = [0,0,0]

        refractColor = [0,0,0]

        ambientColor = [0,0,0]
        diffuseColor = [0,0,0]
        specularColor =[0,0,0]

        finalColor = [0,0,0]

        if material.type == OPAQUE:
            
            for light in self.lights:
                if light.type == "Ambient":
                    ambientColor = [ambientColor[i] + light.getLightColor()[i] for i in range(3)]
                else:
                               
                    lightDirection = None

                    if light.type == "Directional":
                        lightDirection = [i * -1 for i in light.direction]
                    elif light.type == "Point":
                        lightDirection = subtract_vector(light.point, intercept.point)
                        lightDirection = normalizar_vector(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, lightDirection, intercept.obj)

                    if shadowIntersect == None:
                        diffuseColor = [diffuseColor[i] + light.getDiffuseColor(intercept)[i] for i in range(3)]
                        specularColor = [specularColor[i] + light.getSpecularColor(intercept, self.camPosition)[i] for i in range(3)]


        elif material.type == REFLECTIVE:
            reflect = reflectVector(intercept.normal, [i * -1 for i in rayDirection])
            refractIntercept = self.rtCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            reflectColor = self.rtRayColor(refractIntercept, reflect, recursion + 1)

            for light in self.lights:
                if light.type != "Ambient":

                    lightDirection = None

                    if light.type == "Directional":
                        lightDirection = [i * -1 for i in light.direction]

                    elif light.type == "Point":
                        lightDirection = subtract_vector(light.point, intercept.point)
                        lightDirection = normalizar_vector(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, lightDirection, intercept.obj)

                    if shadowIntersect == None:
                        specularColor = [specularColor[i] + light.getSpecularColor(intercept, self.camPosition)[i] for i in range(3)]

        elif material.type == TRANSPARENT:
            outside = producto_punto(rayDirection, intercept.normal) < 0
            bias = vector_scalar_mult(0.0001, intercept.normal)

            reflect = reflectVector(intercept.normal, vector_scalar_mult(-1, rayDirection))
            reflectOrigin = add_vector(intercept.point, bias) if outside else subtract_vector(intercept.point, bias)
            reflectIntercept = self.rtCastRay(reflectOrigin, reflect, None, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion + 1)

            for light in self.lights:
                if light.type != "Ambient":

                    lightDirection = None

                    if light.type == "Directional":
                        lightDirection = [i * -1 for i in light.direction]

                    elif light.type == "Point":
                        lightDirection = subtract_vector(light.point, intercept.point)
                        lightDirection = normalizar_vector(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, lightDirection, intercept.obj)

                    if shadowIntersect == None:
                        specularColor = [specularColor[i] + light.getSpecularColor(intercept, self.camPosition)[i] for i in range(3)]


            if not reflexion_interna_total(intercept.normal, rayDirection, 1.0, material.ior):
                refract = calcular_refraccion(intercept.normal, rayDirection, 1.0, material.ior)
                refractOrigin = subtract_vector(intercept.point, bias) if outside else add_vector(intercept.point, bias)
                refractIntercept = self.rtCastRay(refractOrigin, refract, None, recursion + 1)
                refractColor = self.rtRayColor(refractIntercept, refract, recursion + 1)

                Kr, Kt = fresnel(intercept.normal, rayDirection, 1.0, material.ior)
                reflectColor = vector_scalar_mult(Kr, reflectColor)
                refractColor = vector_scalar_mult(Kt, refractColor)


        lightColor = [ambientColor[i] + diffuseColor[i] + specularColor[i] + reflectColor[i] + refractColor[i] for i in range(3)]
        finalColor = [min(1, surfaceColor[i] * lightColor[i]) for i in range(3)]

        return finalColor



    def rtRender(self):


        indeces = [(i, j) for i in range(self.vpWidth) for j in range(self.vpHeight)]
        random.shuffle(indeces)

        for i, j in indeces:
            x = i + self.vpX
            y = j + self.vpY

            if (0 <= x < self.width) and (0 <= y < self.height):
                Px = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                Py = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1
                    
                Px *= self.rightEdge
                Py *= self.topEdge

                direction = [Px, Py, -self.nearPlane]
                direction = normalizar_vector(direction)

                intercept =  self.rtCastRay(self.camPosition, direction)
                    
                rayColor = self.rtRayColor(intercept, direction)
                
                if rayColor:
                    self.rtPoint(x,y, rayColor)
                    pygame.display.flip()