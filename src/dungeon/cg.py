import random

class tool:
  @staticmethod
  def line(x, y, x2, y2):
      """Brensenham line algorithm"""
      steep = 0
      coords = []
      dx = abs(x2 - x)
      if (x2 - x) > 0: sx = 1
      else: sx = -1
      dy = abs(y2 - y)
      if (y2 - y) > 0: sy = 1
      else: sy = -1
      if dy > dx:
	  steep = 1
	  x, y = y, x
	  dx, dy = dy, dx
	  sx, sy = sy, sx
      d = (2 * dy) - dx
      for i in range(0, dx):
	  if steep: coords.append((y, x))
	  else: coords.append((x, y))
	  while d >= 0:
	      y = y + sy
	      d = d - (2 * dx)
	  x = x + sx
	  d = d + (2 * dy)
      coords.append((x2, y2))
      return coords

class cave_gen:
    
    def __init__(self, WIDTH, HEIGHT, count=0):
        self.width = WIDTH
        self.height = HEIGHT
        
        A = []
        for i in range(self.height):
            A.append([0] * self.width)
            
        for y in range(self.height):
            for x in range(self.width):
                if random.randrange(100) <= 45:
                    tile = 1
                else:
                    tile = 0
                    
                A[y][x] = tile
        self.A = A
        
        if count > 1:
            self.apply_cell(count)    
    

    def polycut(self):
        x1 = random.randrange(0, self.width / 4)
        y1 = random.randrange(0, self.height / 4)
        
        x2 = random.randrange(self.width - self.width / 4, self.width)
        y2 = random.randrange(0, self.height / 4)
        
        x3 = random.randrange(0, self.width / 4)
        y3 = random.randrange(self.height - self.height / 4, self.height)
        
        x4 = random.randrange(self.width - self.width / 4, self.width)
        y4 = random.randrange(self.height - self.height / 4, self.height)
        
        l = []
        l.append(tool.line(x1, y1, x2, y2))
        l.append(tool.line(x2, y2, x3, y3))
        l.append(tool.line(x3, y3, x4, y4))
        l.append(tool.line(x4, y4, x1, y1))
        
        for line in l:
            for point in line:
                x, y = point
                self.A[y][x] = 0      
        
    def apply_cell(self, count):
        
        for n in range(count):
        
            A = self.A
            B = []
            for i in range(self.height):
                B.append([0] * self.width)

            
            for y in range(self.height):
                for x in range(self.width):
                    if self.checkn(y, x, 4) or self.checkopen(y, x):
                        B[y][x] = 1
            self.A = B
        
    def checkopen(self, y, x):
        A = self.A
        wn = 0
        for r_x in (-2, -1, 0, 1, 2):
            for r_y in (-2, -1, 0, 1, 2):
                b_x = x + r_x
                b_y = y + r_y
                try:
                    if A[b_y][b_x]:
                        wn += 1
                except:
                    pass
        if wn == 0:
            return 1
        else:
            return 0
                    
    def checkn(self, y, x, n):
        A = self.A
        wn = 0
        for r_x in (-1, 0, 1):
            for r_y in (-1, 0, 1):
                b_x = x + r_x
                b_y = y + r_y
                try:
                    if A[b_y][b_x]:
                        wn += 1
                except:
                    pass
        if wn > n:
            return 1
        else:
            return 0
                    
    def dprint(self):
    
        A = self.A
        z = ''
        i = []
        for y in range(self.height):
            for x in range(self.width):
                if A[y][x] == 1:
                    z += '#'
                elif A[y][x] == 3:    
                    z += '@'
                else:
                    z += '.'
                #z+=str(A[y][x])
            i.append(z)
            z = ''
        
        for y in range(self.height):
            print i[y]

    def fix(self):
        A = self.A
        N = []
        for y in range(self.height + 1):
            l = []
            for x in range(self.width + 1):
                l.append('.')
            N.append(l)
            
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                if y == 0 or x == 0 or y == self.height - 1 or x == self.width - 1:
                    N[y][x] = 1
                else:
                    N[y][x] = A[y - 1][x - 1]
        self.A = N
                    
    def dget(self):
       
        A = self.A
        z = ''
        i = []
        for y in range(self.height):
            for x in range(self.width):
                if A[y][x] == 1:
                    z += '#'
                else:
                    z += '.'
                #z+=str(A[y][x])
            i.append(z)
            z = ''
        
        return i
