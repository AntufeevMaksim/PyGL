
from PIL import Image
from PIL import ImageOps, ImageDraw
from obj_parser import ObjParser
import random
import math
import geometry as geo
import numpy as np
import cv2

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

def draw_obj(obj, texture, image):
  z_buffer = np.full((IMAGE_HEIGHT, IMAGE_WIDTH), -np.inf)
  for face in obj.faces:
    v1 = obj.vertexes[face[0].v-1]  #subtract 1 because in the file the vertex numbering starts from 1 and in the list from 0
    v2 = obj.vertexes[face[1].v-1]
    v3 = obj.vertexes[face[2].v-1]

    vt1 = obj.vertexes_textures[face[0].vt-1]
    vt2 = obj.vertexes_textures[face[1].vt-1]
    vt3 = obj.vertexes_textures[face[2].vt-1]


    screen_v1 = geo.Vec3()
    screen_v2 = geo.Vec3()
    screen_v3 = geo.Vec3()

    screen_vt1 = geo.Vec3()
    screen_vt2 = geo.Vec3()
    screen_vt3 = geo.Vec3()

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


    texture_width = len(texture[0])/2
    texture_height = len(texture)/2
    screen_vt1.x = int((vt1.x+1) * texture_width)-1
    screen_vt1.y = int((vt1.y+1) * texture_height)-1


    screen_vt2.x = int((vt2.x+1) * texture_width)-1
    screen_vt2.y = int((vt2.y+1) * texture_height)-1


    screen_vt3.x = int((vt3.x+1) * texture_width)-1
    screen_vt3.y = int((vt3.y+1) * texture_height)-1

    vec1 = [v1.x - v2.x, v1.y - v2.y, v1.z - v2.z]
    vec2 = [v1.x - v3.x, v1.y - v3.y, v1.z - v3.z]


    normal = geo.vec_product(vec2, vec1)

    light_dir = geo.Vec3(0, 0, -1)
    intensity = geo.cos_2vec(normal, light_dir)

    if intensity > 0:
      triangle(screen_v1, screen_v2, screen_v3, screen_vt1, screen_vt2, screen_vt3, image, z_buffer, (int(255*intensity), int(255*intensity), int(255*intensity)), texture)

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

def triangle(v1, v2, v3, screen_vt1, screen_vt2, screen_vt3, image, z_buffer, color, texture):

  if (v3.y < v1.y):
    v1, v3 = v3, v1

  if (v2.y < v1.y):
    v2, v1 = v1, v2

  if (v3.y < v2.y):
    v2, v3 = v3, v2

  dy1_3 = v3.y - v1.y 
  dy1_2 = v2.y - v1.y
  dy2_3 = v3.y - v2.y

  dx1_3 = abs(v3.x - v1.x)
  dx1_2 = abs(v2.x - v1.x)
  dx2_3 = abs(v3.x - v2.x)

  if v3.x > v1.x:
    dir_alpha = 1
  else:
    dir_alpha = -1

  if v2.x > v1.x:
    dir_beta = 1
  else:
    dir_beta = -1

  d_err_alpha = dx1_3
  d_err_beta = dx1_2

  x_alpha = v1.x
  x_beta = v1.x

  err_alpha = 0
  err_beta = 0

  if v1.y == v2.y:
    horizontal_line(v1.x, v2.x, v1.y, v1.z, v2.z, image, z_buffer, color)
    x_beta = v2.x


  for y in range(v1.y+1, v2.y+1):
    err_alpha += d_err_alpha
    x_alpha, err_alpha = change_x(x_alpha, y, err_alpha, dy1_3, dir_alpha, image, color)

    err_beta += d_err_beta
    x_beta, err_beta = change_x(x_beta, y, err_beta, dy1_2, dir_beta, image, color)

    z_alpha = v1.z + ((v3.z - v1.z)*(y - v1.y))/(v3.y - v1.y)
    z_beta = v1.z + ((v2.z - v1.z)*(y - v1.y))/(v2.y - v1.y)

    horizontal_line(x_alpha, x_beta, y, z_alpha, z_beta, image, z_buffer, color)

  if v3.x > v2.x:
    dir_beta = 1
  else:
    dir_beta = -1
  d_err_beta = dx2_3

  if v2.y == v3.y:
    horizontal_line(v2.x, v3.x, v2.y, v2.z, v3.z, image, z_buffer, color)

  for y in range(v2.y+1, v3.y+1):

    err_alpha += d_err_alpha
    x_alpha, err_alpha = change_x(x_alpha, y, err_alpha, dy1_3, dir_alpha, image, color)

    err_beta += d_err_beta
    x_beta, err_beta = change_x(x_beta, y, err_beta, dy2_3, dir_beta, image, color)

    z_alpha = v1.z + ((v3.z - v1.z)*(y - v1.y))/(v3.y - v1.y)
    z_beta = v2.z + ((v3.z - v2.z)*(y - v2.y))/(v3.y - v2.y)

    horizontal_line(x_alpha, x_beta, y, z_alpha, z_beta, image, z_buffer, color)


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


IMAGE_HEIGHT = 1000
IMAGE_WIDTH = 1000

image = np.zeros( (IMAGE_WIDTH,IMAGE_HEIGHT,3), dtype=np.uint8 )
#texture = cv2.imread("african_head_diffuse.tga")
obj = ObjParser("african_head.obj")

texture = Image.open("african_head_diffuse.tga")
texture.load()
texture = np.asarray(texture, dtype="int32")

draw_obj(obj, texture, image)





image = Image.fromarray(image)
ImageOps.flip(image).save("output.tga")
