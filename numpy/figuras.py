from code import interact
from numpyPablo import add_vector, cross_product, vector_normal, producto_punto, subtract_vector, normalizar_vector, vector_scalar_mult
from math import pi, atan2, acos

class Intercept(object):
	def __init__(self, distance, point, normal, obj, texcoords):
		self.distance = distance
		self.point = point
		self.normal = normal
		self.obj = obj
		self.texcoords = texcoords



class Shape(object):

	def __init__(self, position, material):
		self.position = position
		self.material = material

	def ray_intersect(self, origin, direction):
		return None


class Sphere(Shape):

	def __init__(self, position, radius, material):
		self.radius = radius
		super().__init__(position, material)


	def ray_intersect(self, origin, direction):

		L = subtract_vector(self.position, origin)
		lengthL = vector_normal(L)
		tca = producto_punto(L, direction)
		d = (lengthL**2 - tca **2) ** 0.5

		if d > self.radius:
			return None

		thc = (self.radius ** 2 - d ** 2) ** 0.5

		t0 = tca - thc
		t1 = tca + thc

		if t0 < 0:
			t0 = t1

		if t0 < 0:
			return None
		
		D = vector_scalar_mult(t0,direction)
		P = add_vector(origin, D)
		point_normal = subtract_vector(P, self.position)
		point_normal = normalizar_vector(point_normal)

		u = atan2(point_normal[2], point_normal[0]) / (2 * pi) + 0.5
		v = acos(point_normal[1]) / pi

		return Intercept(distance = t0,
						 point = P,
						 normal = point_normal,
						 obj = self,
						 texcoords = (u,v))


class Plane(Shape):

	def __init__(self, position, normal, material):
		self.normal = normal
		if abs(self.normal[2]) < 0.999:
			self.u_vector = normalizar_vector(cross_product(self.normal, (0,0,1)))
		else:
			self.u_vector = normalizar_vector(cross_product(self.normal, (0,1,0)))
		
		self.v_vector = normalizar_vector(cross_product(self.normal, self.u_vector))
		self.v_vector = vector_scalar_mult(-1, self.v_vector)

		super().__init__(position, material)


	def ray_intersect(self, origin, direction):

		denom = producto_punto(direction, self.normal)

		if abs(denom) <= 0.0001:
			return None

		num = producto_punto(subtract_vector(self.position, origin), self.normal)
		
		t = num / denom

		if t < 0:
			return None

		D = vector_scalar_mult(t,direction)
		P = add_vector(origin, D)

		repeat = 0.09

		u = producto_punto(subtract_vector(P, self.position), self.u_vector) * repeat % 1
		v = producto_punto(subtract_vector(P, self.position), self.v_vector) * repeat % 1

		return Intercept(distance = t,
						 point = P,
						 normal = self.normal,
						 obj = self,
						 texcoords = (u,v))


class Disk(Plane):

	def __init__(self, position, normal, radius, material):
		self.radius = radius
		super().__init__(position, normal, material)


	def ray_intersect(self, origin, direction):
		planeIntersect = super().ray_intersect(origin, direction)
		
		if planeIntersect is None:
			return None

		contactVector = subtract_vector(planeIntersect.point, self.position)
		contactDistance = vector_normal(contactVector)

		if contactDistance > self.radius:
			return None

		return Intercept(distance = planeIntersect.distance,
						 point = planeIntersect.point,
						 normal = self.normal,
						 obj = self,
						 texcoords = None)


class AABB(Shape):

	def __init__(self, position, size, material):
		super().__init__(position, material)

		self.planes = []
		self.size = size

		leftPlane =    Plane(add_vector(self.position, (-size[0] / 2,0,0)), (-1,0,0), material)
		rightPlane =   Plane(add_vector(self.position, ( size[0] / 2,0,0)), ( 1,0,0), material)
					  
		bottomPlane =  Plane(add_vector(self.position, (0,-size[1] / 2,0)), (0,-1,0), material)
		topPlane = 	   Plane(add_vector(self.position, (0, size[1] / 2,0)), (0, 1,0), material)
					   
		backPlane =    Plane(add_vector(self.position, (0,0,-size[2] / 2)), (0,0,-1), material)
		frontPlane =   Plane(add_vector(self.position, (0,0, size[2] / 2)), (0,0, 1), material)

		self.planes.append(leftPlane)
		self.planes.append(rightPlane)
		self.planes.append(bottomPlane)
		self.planes.append(topPlane)
		self.planes.append(backPlane)
		self.planes.append(frontPlane)

		self.boundsMin = [0,0,0]
		self.boundsMax = [0,0,0]

		self.bias = 0.001

		for i in range(3):
			self.boundsMin[i] = self.position[i] - (self.bias + size[i]/2)
			self.boundsMax[i] = self.position[i] + (self.bias + size[i]/2)
		

	def ray_intersect(self, origin, direction):
		intersect = None
		t = float('inf')

		u = 0
		v = 0

		for plane in self.planes:
			planeIntersect = plane.ray_intersect(origin, direction)

			if planeIntersect is not None:
				
				planePoint = planeIntersect.point

				if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
					if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
						if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
							if planeIntersect.distance < t:
								t = planeIntersect.distance
								intersect = planeIntersect

								if abs(plane.normal[0]) > 0:
							
									u = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2)
									v = 1 - (planePoint[1] - self.boundsMin[1]) / (self.size[1] + self.bias * 2)
								
								elif abs(plane.normal[1]) > 0:
								
									u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + self.bias * 2) 
									v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2) 

								elif abs(plane.normal[2]) > 0:
								
									u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + self.bias * 2)
									v = 1 - (planePoint[1] - self.boundsMin[1]) / (self.size[1] + self.bias * 2)

		if intersect is None:
			return None

		return Intercept(distance = t,
						 point = intersect.point,
						 normal = intersect.normal,
						 obj = self,
						 texcoords = (u, v))
