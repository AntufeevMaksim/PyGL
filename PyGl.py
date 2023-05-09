
from PIL import Image
from PIL import ImageOps, ImageDraw
from obj_parser import ObjParser
import random
import math
import geometry as geo
import numpy as np


def line(x0, y0, x1, y1, image, color):

  steep = False
  if(abs(x1 - x0) < abs(y1 - y0)):
    x0, y0 = y0, x0
    x1, y1 = y1, x1
    steep = True

  if (x0 > x1):
    x1, x0 = x0, x1
    y1, y0 = y0, y1


  dy = abs(y1 - y0)
  dx = x1 - x0

  x = x0
  y = y0

  dir_x = 1
  if (y0 > y1):
    dir_x = -1

  error = 0
  d_error = dy
  while x <= x1:
    if (2*error > dx):
      y += dir_x
      error -= dx
    if (steep):
      image[x][y] = color
    else:
      image[y][x] = color
    error += d_error
    x += 1

def draw_obj(obj, image):
  z_buffer = np.full((IMAGE_HEIGHT, IMAGE_WIDTH), -np.inf)
  for face in obj.faces:
    v1 = obj.vertexes[face[0]-1]
    v2 = obj.vertexes[face[1]-1]
    v3 = obj.vertexes[face[2]-1]

    screen_v1 = geo.Vec3()
    screen_v2 = geo.Vec3()
    screen_v3 = geo.Vec3()

    width = IMAGE_WIDTH/2
    height = IMAGE_HEIGHT/2
    screen_v1.x = int((v1.x+1) * width)-1
    screen_v1.y = int((v1.y+1) * height)-1
    screen_v1.z = v1.z

    screen_v2.x = int((v2.x+1) * width)-1
    screen_v2.y = int((v2.y+1) * height)-1
    screen_v2.z = v2.z

    screen_v3.x = int((v3.x+1) * width)-1
    screen_v3.y = int((v3.y+1) * height)-1
    screen_v3.z = v3.z


    vec1 = [v1.x - v2.x, v1.y - v2.y, v1.z - v2.z]
    vec2 = [v1.x - v3.x, v1.y - v3.y, v1.z - v3.z]


    normal = geo.vec_product(vec2, vec1)

    light_dir = geo.Vec3(0, 0, -1)
    intensity = geo.cos_2vec(normal, light_dir)

    if intensity > 0:
      triangle(screen_v1, screen_v2, screen_v3, image, z_buffer, (int(255*intensity), int(255*intensity), int(255*intensity)))

def change_x(x, y, err, dy, dir, image, color):
  while 2*err > dy:
    x += dir
    err -= dy


  return x, err

def horizontal_line(x1, x2, y, z1, z2, image, z_buffer, color):
  if (x1 > x2):
    x1, x2 = x2, x1

  for x in range(x1, x2):
    z = z1 + ((z2 - z1)*(x-x1))/(x2-x1)
    if (z_buffer[y][x] < z):
      z_buffer[y][x] = z
      image[y][x] = color

def triangle(v1, v2, v3, image, z_buffer, color):
  x1, y1 = v1.x, v1.y
  x2, y2 = v2.x, v2.y
  x3, y3 = v3.x, v3.y

  if (y3 < y1):
    y1, y3 = y3, y1
    x1, x3 = x3, x1

  if (y2 < y1):
    y2, y1 = y1, y2
    x2, x1 = x1, x2

  if (y3 < y2):
    y2, y3 = y3, y2
    x2, x3 = x3, x2

  dy1_3 = y3 - y1 
  dy1_2 = y2 - y1
  dy2_3 = y3 - y2

  dx1_3 = abs(x3 - x1)
  dx1_2 = abs(x2 - x1)
  dx2_3 = abs(x3 - x2)

  if x3 > x1:
    dir_alpha = 1
  else:
    dir_alpha = -1

  if x2 > x1:
    dir_beta = 1
  else:
    dir_beta = -1

  d_err_alpha = dx1_3
  d_err_beta = dx1_2

  x_alpha = x1
  x_beta = x1

  err_alpha = 0
  err_beta = 0

  if y1 == y2:
    horizontal_line(x1, x2, y1, v1.z, v2.z, image, z_buffer, color)
    x_beta = x2


  for y in range(y1+1, y2+1):
    err_alpha += d_err_alpha
    x_alpha, err_alpha = change_x(x_alpha, y, err_alpha, dy1_3, dir_alpha, image, color)

    err_beta += d_err_beta
    x_beta, err_beta = change_x(x_beta, y, err_beta, dy1_2, dir_beta, image, color)

    z_alpha = v1.z + ((v3.z - v1.z)*(y - y1))/(y3 - y1)
    z_beta = v1.z + ((v2.z - v1.z)*(y - y1))/(y2 - y1)

    horizontal_line(x_alpha, x_beta, y, z_alpha, z_beta, image, z_buffer, color)

  if x3 > x2:
    dir_beta = 1
  else:
    dir_beta = -1
  d_err_beta = dx2_3

  if y2 == y3:
    horizontal_line(x2, x3, y2, v2.z, v3.z, image, z_buffer, color)

  for y in range(y2+1, y3+1):

    err_alpha += d_err_alpha
    x_alpha, err_alpha = change_x(x_alpha, y, err_alpha, dy1_3, dir_alpha, image, color)

    err_beta += d_err_beta
    x_beta, err_beta = change_x(x_beta, y, err_beta, dy2_3, dir_beta, image, color)

    z_alpha = v1.z + ((v3.z - v1.z)*(y - y1))/(y3 - y1)
    z_beta = v2.z + ((v3.z - v2.z)*(y - y2))/(y3 - y2)

    horizontal_line(x_alpha, x_beta, y, z_alpha, z_beta, image, z_buffer, color)


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


IMAGE_HEIGHT = 1000
IMAGE_WIDTH = 1000
image = np.zeros( (IMAGE_WIDTH,IMAGE_HEIGHT,3), dtype=np.uint8 )
obj = ObjParser("african_head.obj")


#render(image)
draw_obj(obj, image)




image = Image.fromarray(image)
ImageOps.flip(image).save("output.tga")
