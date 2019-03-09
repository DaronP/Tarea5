import struct
from collections import namedtuple
from random import randint

def char(c):
	return struct.pack("=c",c.encode('ascii'))
def word(c):
	return struct.pack("=h",c)
def dword(c):
	return struct.pack("=l",c)
def color(r,g,b):
	return bytes([r, g, b])
	
	
def bbox(A,B,C):
	xs = [A.x, B.x, C.x]
	ys = [A.y, B.y, C.y]
	
	return V2(xs[0], ys[0]), V2(xs[2], ys[2])

def barycentric(A,B,C,P):
	cx, cy, cz = cross(
		V3(B.x - A.x, C.x - A.x, A.x - P.x),
		V3(B.y - A.y, C.y - A.y, A.y - P.y)
	)
	
	if cz == 0:
		return -1, -1, -1
		
	U = cx/cz
	V = cy/cz
	W = 1 - (U+V)
	
	return W, V, U
	
	
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point3', ['x', 'y', 'z', 'color'])
	

			

def sum(v0, v1):
	return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)
	
def sub(v0, v1):
	return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)
	
def mul(v0, k):
	return V3(v0.x * k, v0.y * k, v0.z * k)
	
def dot(v0, v1):
	return v0.x * v1.x + v0.y * v1.y + v0.z * v0.z
	
def cross(v0, v1):
	return V3(
		v0.y * v1.z - v0.z * v1.y,
		v0.z * v1.x - v0.x * v1.z,
		v0.x * v1.y + v0.y + v1.x
		)

def length(v0):
	return(v0.x**2 + v0.y**2 + v0.z**2)**0.5
	
def norm(v0):
	v0length = length(v0)
	
	if not v0length:
	
		return V3(0,0,0)

	return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

class Bitmap(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.framebuffer = []
		self.sx = 0
		self.sy = 0
		self.viewwidth = 0
		self.viewheight = 0
		self.clear()

	def clear (self):
		self.framebuffer = [
			[
				color(0,0,0)
					for x in range(self.width)
			]
			for y in range(self.height)
		]

	def Crear(self, filename):
		f = open(filename, 'wb')

		#File Header 14
		f.write(char('B'))
		f.write(char('M'))
		f.write(dword(14 + 40 + an * al * 3))
		f.write(dword(0))
		f.write(dword(14+40))

		#image header 40
		f.write(dword(40))
		f.write(dword(an))
		f.write(dword(al))
		f.write(word(1))
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(an * al* 3))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
       
		for x in range(an):
			for y in range(al):
					f.write(self.framebuffer[x][y])
					#print(self.framebuffer[x][y])

		f.close()


	def point(self, x, y,color):
		self.framebuffer[x][y] = color


	def vertex(self,x,y):
		self.framebuffer[int(round(self.sy + y))][int(round(self.sx + x ))] = color(255,255,255)

	def clearColor(self, r,g,b):
		r = r*255
		g = g*255
		b = b*255

		self.freamebuffer = [
			[
				color(r, g, b)
					for x in range(self.width)
			]
			for y in range(self.height)
		]

	def ViewPort(self, x, y, largo, alto):
		self.sx = x+(largo/2)
		self.sy = y+(alto/2)
		self.viewwidth = largo/2
		self.viewheight = alto/2
	def Color(self, x,y,color):
		self.framebuffer[int(round(self.sy + y))][int(round(self.sx + x ))] = color
		
		
	def Linea(self,y0, x0, y1, x1):

		dx = abs(x1 - x0)
		dy = abs(y1 - y0)

		steep = dy > dx

		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1

		if x0 > x1:
			xi = x0
			yi = y0
			xf = x1
			yf = y1

			x0, x1 = xf, xi
			y0, y1 = yf, yi

		offset = 0
		threshold = 2*dx

		y = y0

		#Odio python por hacerme perder tiempo por estas dos variables

		#Pintado de la linea
		for x in range(x0, x1+1):
			if dy > dx: 
				glPoint(y, x)
				if y0 > y1:
					y -=1
				if y0 < y1:
					y += 1
				if x0 > x1:
					x -=1
				if x0 < x1:
					x += 1
			else:
				glPoint(x,y)
				if y0 > y1:
					y -=1
				if y0 < y1:
					y += 1
				if x0 > x1:
					x -=1
				if x0 < x1:
					x += 1
		
class Obj(object):
	def __init__(self, filename):
		self.materials = {}
		if("obj" in filename):
			with open(filename) as f:
				self.lines = f.read().splitlines()
		if("mtl" in filename):
			with open(filename) as m:
				self.lines = m.read().splitlines()

			current_material = None
			
			for line in self.lines:
				if line:
					prefix, value = line.split(' ', 1)
					if prefix == "newmtl":
						current_material = value
					if prefix == "Kd":
						kd = [value.split(' ')] #convertir value a color
						self.materials[current_material] = kd


		self.vertices = []
		self.tvertices = []
		self.vfaces = []
		self.read()
		self.zbuffer = []
		self.framebuffer = []
		self.clear()
		#self.celarz()
		self.sx = 0
		self.sy = 0
		self.viewwidth = 0
		self.viewheight = 0

		
	def ViewPort(self, x, y, largo, alto):
		self.sx = x+(largo/2)
		self.sy = y+(alto/2)
		self.viewwidth = largo/2
		self.viewheight = alto/2
		
	def clear (self):
		self.framebuffer = [
			[
				color(0,0,0)
					for x in range(an)
			]
			for y in range(al)
		]
	#def clearz(self):
		self.zbuffer = [
			[
				float('inf')*-1
					for x in range(an)
			]
			for y in range(al)
		]
		
	def Crear(self, filename):
		f = open(filename, 'wb')

		#File Header 14
		f.write(char('B'))
		f.write(char('M'))
		f.write(dword(14 + 40 + an * al * 3))
		f.write(dword(0))
		f.write(dword(14+40))

		#image header 40
		f.write(dword(40))
		f.write(dword(an))
		f.write(dword(al))
		f.write(word(1))
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(an * al* 3))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
       
		for x in range(an):
			for y in range(al):
					f.write(self.framebuffer[y][x])

		f.close()

	def Color(self, x,y,color):
		self.framebuffer[int(round(self.sy + y))][int(round(self.sx + x ))] = color

	def NormX(self, x0):
		return int(round(((x0*(self.viewwidth/2))+self.sx)))
		
	def NormY(self, y0):
		return int(round((y0*(self.viewheight/3))+self.sy))
		
	def transform(self, vertex):
		return V3(
			self.NormX(vertex[0]),
			self.NormY(vertex[1]),
			self.NormY(vertex[2])
		)
	
	def point(self, x, y, color):
		self.framebuffer[x][y] = color
			
	def triangle(self, A, B, C, color):
		bbox_min, bbox_max = bbox(A, B, C)
		
		
		for x in range(bbox_min.x, bbox_max.x + 1):
			for y in range(bbox_min.y, bbox_max.y + 1):
				w, v, u = barycentric(A, B, C, V2(x,y))
				
				if w < 0 or v < 0 or u < 0:
					continue
				
				z = A.z * w + B.z * v + C.z * u
				
					
				if z > self.zbuffer[x][y]:
					self.point(x,y, color)
					self.zbuffer[x][y] = z				
			

	def read(self):
		current_material = None
		for line in self.lines:
			if line:
			
				prefix, value = line.split(' ', 1)

				if prefix == 'v':
					self.vertices.append(list(map(float, value.split(' '))))
				
				elif prefix == "usemtl":
					current_material = value
				elif prefix == 'f':
					colrs = self.materials[current_material] 
					self.vfaces.append([list(map(try_int, face.split('/'))) for face in value.split(' ')].extend(colrs))
	
	
		
	def load(self, filename, translate=(0,0,0), scale=(1,1,1), texture = None):
		model = Obj(filename)
		light = V3(0,0,1)		
		
		for face in model.vfaces:
			vcount = len(face)

			if vcount == 3:
				face.pop(2)			

				colr1 = [face[0][0][0]]
				colr2 = [face[0][0][1]]
				colr3 = [face[0][0][2]]

				for i in range(0,1):
					colr1.pop(i)
					colr2.pop(i)
					colr3.pop(i)

				f1 = face[0][0] - 1
				f2 = face[1][0] - 1
				f3 = face[2][0] - 1

				
				

				colr = V3(colr1, colr2, colr3)

				a = V3(*model.vertices[f1])
				b = V3(*model.vertices[f2])
				c = V3(*model.vertices[f3])


				normal = norm(cross(sub(b,a), sub(c,a)))
				intensity = dot(normal, light)
				grey = round((255 * colr) * intensity)

				a = self.transform(a)
				b = self.transform(b)
				c = self.transform(c)

				if intensity<0:
					continue
				
				self.triangle(a, b, c, color(grey, grey, grey))


def glCreateWindow(ancho, alto):
        return Bitmap(ancho, alto)
def glViewPort(x,y,largo,alto):
	l = largo
	a = alto
	im.ViewPort(x,y,l,a)
def glClear(r,g,b):
        im.clearColor(r,g,b)
def glVertex(x,y):
        im.vertex(x,y)
#def glColor(r,g,b,x,y):
#        rvertex(x,y,ancho,alto,color(r*255,g*255,b*255))
def glFinish(name):
        r.Crear(name+".bmp")

def glColor(x,y,color):
	r.Color(x,y,color)
	
def glLine(x0,y0,x1,y1):
	im.Linea(x0,y0,x1,y1)
	
def glPoint(x,y):
	im.point(x,y)

	
def try_int(s, base=10, val=None):
	try:
		return int(s,base)
	except ValueError:
		return val
		


an = 1280
al = 1280


				
im = glCreateWindow(an, al)

r = Obj("Poopybutthole.obj")
r.ViewPort(0,0,800,600)
r.load("Poopybutthole.obj")
l = Obj("Poopybutthole.mtl")
glFinish('out')
				
				
