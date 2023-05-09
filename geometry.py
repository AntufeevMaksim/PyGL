import math


class Vec3:
  def __init__(self, x=0, y=0, z=0) -> None:
    self.x = x
    self.y = y
    self.z = z


def vec_product(vec1, vec2):
  a = Vec3(vec1[0], vec1[1], vec1[2])
  b = Vec3(vec2[0], vec2[1], vec2[2])
  return Vec3(a.y * b.z - a.z * b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x)

def cos_2vec(a, b):
  return (a.x*b.x + a.y*b.y + a.z*b.z)/(math.sqrt((a.x)**2 + (a.y)**2 + (a.z)**2) * math.sqrt((b.x)**2 + (b.y)**2 + (b.z)**2))