
from PIL import Image
from PIL import ImageOps
from obj_parser import ObjParser
import random
import math
from geometry import Vec3

def line(x0, y0, x1, y1, im, color):

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
      im.putpixel((int(y), x), color)
    else:
      im.putpixel((x, int(y)), color)
    error += d_error
    x += 1

def vec_product(vec1, vec2):
  a = Vec3(vec1[0], vec1[1], vec1[2])
  b = Vec3(vec2[0], vec2[1], vec2[2])
  return [a.y * b.z - a.z * b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x]

def cos_2vec(vec1, vec2):
  return (vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2])/(math.sqrt(vec1[0]**2 + vec1[1]**2 + vec1[2]**2) * math.sqrt(vec2[0]**2 + vec2[1]**2 + vec2[2]**2))

def draw_obj(obj, image):
  for face in obj.faces:
    v1 = obj.vertexes[face[0]-1]
    v2 = obj.vertexes[face[1]-1]
    v3 = obj.vertexes[face[2]-1]

    copy_v1 =[0,0]
    copy_v2 =[0,0]
    copy_v3 =[0,0]

    copy_v1[0] = int((v1[0]+1) * IMAGE_WIDTH/2)-1
    copy_v1[1] = int((v1[1]+1) * IMAGE_HEIGHT/2)-1

    copy_v2[0] = int((v2[0]+1) * IMAGE_WIDTH/2)-1
    copy_v2[1] = int((v2[1]+1) * IMAGE_HEIGHT/2)-1

    copy_v3[0] = int((v3[0]+1) * IMAGE_WIDTH/2)-1
    copy_v3[1] = int((v3[1]+1) * IMAGE_HEIGHT/2)-1

    vec1 = [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]
    vec2 = [v1[0] - v3[0], v1[1] - v3[1], v1[2] - v3[2]]

    # if ((vec2[0] - vec1[0]) * (vec2[1] + vec1[1])):
    #   normal = vec_product(vec1, vec2)
    # else:
    #   normal = vec_product(vec2, vec1)

    normal = vec_product(vec2, vec1)

    light_dir = [0,0,10]
    intensity = cos_2vec(normal, light_dir)

    if (intensity > 0):
      triangle(copy_v1, copy_v2, copy_v3, image, (int(255*intensity), int(255*intensity), int(255*intensity)))
    

#    line(copy_v1[0], copy_v1[1], copy_v2[0], copy_v2[1], image, (255, 255, 255))
#    line(copy_v1[0], copy_v1[1], copy_v3[0], copy_v3[1], image, (255, 255, 255))
#    line(copy_v2[0], copy_v2[1], copy_v3[0], copy_v3[1], image, (255, 255, 255))  


def triangle(v1, v2, v3, image, color):
  x1, y1 = v1[0], v1[1]
  x2, y2 = v2[0], v2[1]
  x3, y3 = v3[0], v3[1]

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

  line(x_alpha, y1, x_beta, y1, image, color)
  for y in range(y1+1, y2+1):
    err_alpha += d_err_alpha
    while 2*err_alpha > dy1_3:
      x_alpha += dir_alpha
      err_alpha -= dy1_3
    image.putpixel((x_alpha, y), color)

    err_beta += d_err_beta
    while 2*err_beta >= dy1_2:
      x_beta += dir_beta
      err_beta -= dy1_2
    image.putpixel((x_beta, y), color)

    line(x_alpha, y, x_beta, y, image, color)

  if x3 > x2:
    dir_beta = 1
  else:
    dir_beta = -1
  d_err_beta = dx2_3
  line(x_alpha, y2+1, x_beta, y2+1, image, color)
  for y in range(y2+2, y3+1):

    err_alpha += d_err_alpha
    while 2*err_alpha > dy1_3:
      x_alpha += dir_alpha
      err_alpha -= dy1_3
    image.putpixel((x_alpha, y), color)

    err_beta += d_err_beta
    while 2*err_beta > dy2_3:
      x_beta += dir_beta
      err_beta -= dy2_3
    image.putpixel((x_beta, y), color)

    line(x_alpha, y, x_beta, y, image, color)
#  ImageOps.flip(image).save("output.tga")




  # array_x1 = line_triangle(x1, y1, x3, y3, image, color)

  # array_x2 = line_triangle(x1, y1, x2, y2, image, color)
  # array_x2 += line_triangle(x2, y2, x3, y3, image, color)

  # for i in range(len(array_x1)):
  #   line(array_x1[i], y1+i, array_x2[i], y1+i, image, color)



IMAGE_HEIGHT = 1000
IMAGE_WIDTH = 1000


image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

obj = ObjParser("african_head.obj")

draw_obj(obj, image)



#triangle((1, 1), (12,6), (6,18), image, (0,255,0))

#triangle((20, 20), (240,120), (120,360),   image, (0,255,0))

#line(1,1, 7,3, image, (255,255,255))

ImageOps.flip(image).save("output.tga")

#triangle((20, 20), (240,120), (120,360),   image, (0,255,0))