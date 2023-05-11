
from geometry import Vec3

class Face:
  v = int()
  vt = int()
  vn = int()

  def __init__(self, v, vt, vn=0) -> None:
    self.v = v
    self.vt = vt
    self.vn = vn


class ObjParser:

  vertexes = list()
  vertexes_textures = list()
  faces = list()


  def __init__(self, file_path) -> None:
    file = open(file_path)
    self._parse_vertexes(file)
    self._parse_vertexes_textures(file)
    self._parse_faces(file)
    
    


  def _parse_vertexes(self, file):
    while((line := file.readline())[0] == "v"):
      line = line[1:]
      vertex = list()
      for str_coord in line.split():
        vertex.append(float(str_coord))
      self.vertexes.append(Vec3(vertex[0], vertex[1], vertex[2]))


  def _parse_vertexes_textures(self, file):
    while ((line := file.readline())[0:2] != "vn"):

      if(line[0:2] == "vt"):
        line = line[2:]
        vt = list()
        for str_coord in line.split():
          vt.append(float(str_coord))
        self.vertexes_textures.append(Vec3(vt[0], vt[1], 0))


  def _parse_faces(self, file):
    while ((line := file.readline()) != ""):

      if(line[0] == "f"):
        line = line[1:]
        self.faces.append(list())
        for s in line.split():
          face = s.split("/")[0:2]
          face = Face(int(face[0]), int(face[1]))
          self.faces[-1].append(face)