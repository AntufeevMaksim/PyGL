
from PIL import Image
from PIL import ImageOps
from obj_parser import ObjParser
import random

def line(x0, y0, x1, y1, im, color):

  steep = False
  if(abs(x1 - x0) < abs(y1 - y0)):
    x0, y0 = y0, x0
    x1, y1 = y1, x1
    steep = True

  if (x0 > x1):
    x1, x0 = x0, x1
    y1, y0 = y0, y1


  dy = abs(y1 - y0) + 1
  dx = x1 - x0 + 1

  x = x0
  y = y0

  dir_x = 1
  if (y0 > y1):
    dir_x = -1

  error = 0
  d_error = dy
  while x <= x1:
    error += d_error
    if (error > dx):
      y += dir_x
      error -= dx
    if (steep):
      im.putpixel((int(y), x), color)
    else:
      im.putpixel((x, int(y)), color)
    x += 1  


def draw_obj(obj, image):
  for face in obj.faces:
    v1 = obj.vertexes[face[0]-1]
    v2 = obj.vertexes[face[1]-1]
    v3 = obj.vertexes[face[2]-1]

    copy_v1 =[0,0]
    copy_v2 =[0,0]
    copy_v3 =[0,0]

    copy_v1[0], copy_v1[1] = int((v1[0]+1) * IMAGE_WIDTH/2)-1, int((v1[1]+1) * IMAGE_HEIGHT/2)-1
    copy_v2[0], copy_v2[1] = int((v2[0]+1) * IMAGE_WIDTH/2)-1, int((v2[1]+1) * IMAGE_HEIGHT/2)-1
    copy_v3[0], copy_v3[1] = int((v3[0]+1) * IMAGE_WIDTH/2)-1, int((v3[1]+1) * IMAGE_HEIGHT/2)-1

    triangle(copy_v1, copy_v2, copy_v3, image, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))

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

  dy1_3 = y3 - y1 + 1
  dy1_2 = y2 - y1 + 1
  dy2_3 = y3 - y2 + 1

  dx1_3 = abs(x3 - x1) + 1
  dx1_2 = abs(x2 - x1) + 1
  dx2_3 = abs(x3 - x2) + 1

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

  for y in range(y1, y2+1):
    image.putpixel((x_alpha, y), color)
    err_alpha += d_err_alpha
    while err_alpha > 0:
      x_alpha += dir_alpha
      err_alpha -= dy1_3

    err_beta += d_err_beta
    while err_beta > 0:
      x_beta += dir_beta
      err_beta -= dy1_2
    image.putpixel((x_beta, y), color)

    line(x_alpha, y, x_beta, y, image, color)

  if x3 > x2:
    dir_beta = 1
  else:
    dir_beta = -1
  d_err_beta = dx2_3
  for y in range(y2+1, y3+1):
    err_alpha += d_err_alpha
    while err_alpha > 0:
      x_alpha += dir_alpha
      err_alpha -= dy1_3
    image.putpixel((x_alpha, y), color)

    err_beta += d_err_beta
    while err_beta > 0:
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

#image = Image.new("RGB", (500, 500))


#triangle((1, 1), (12,6), (6,18), image, (0,255,0))

#triangle((20, 20), (240,120), (120,360),   image, (0,255,0))

image = ImageOps.flip(image)
image.save("output.tga")


#triangle((20, 20), (240,120), (120,360),   image, (0,255,0))