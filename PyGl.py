
from PIL import Image
from PIL import ImageOps

def line(x0, y0, x1, y1, im, color):

  if (x0 > x1):
    x1, x0 = x0, x1

  if (y0 > y1):
    y1, y0 = y0, y1

  steep = False
  if(x1 - x0 < y1 - y0):
    x0, y0 = y0, x0
    x1, y1 = y1, x1
    steep = True

  dy = y1 - y0
  dx = x1 - x0

  x = x0
  y = y0

  error = 0
  d_error = dy
  while x <= x1:
    error += d_error
    if (error >= dx):
      y += 1
      error -= dx
    if (steep):
      im.putpixel((int(y), x), color)
    else:
      im.putpixel((x, int(y)), color)
    x += 1  

  # if (abs(x1 - x0) > abs(y1 - y0)):
  #   delta_x = x1 - x0
  #   while x < x1:
  #     t = (x - x0) / delta_x
  #     y = y0*(1-t) + y1*t
  #     im.putpixel((x, int(y)), color)    
  #     x += 1
  # else:
  #   delta_y = y1 - y0
  #   while y < y1:
  #     t = (y - y0) / delta_y
  #     x = x0*(1-t) + x1*t
  #     im.putpixel((int(x), y), color)    
  #     y += 1
  # im.putpixel((x0, y0), (0,255,0))
  # im.putpixel((x1, y1), (0,255,0)) 


im = Image.new("RGB", (100, 100))
#im = Image.open("output.tga")

x0 = 30
y0 = 70

x1 = 4
y1 = 4

line(13, 20, 80, 40, im, (255, 255, 255))
line(40, 13, 20, 80, im, (255, 0, 0))
line(80, 40, 13, 20, im, (255, 0, 0))

line(6, 3, 1, 1, im, (255, 0, 0))
#line(5, 1, 1, 11, im, (255, 0, 0))

im = ImageOps.flip(im)
im.save("output.tga")
 