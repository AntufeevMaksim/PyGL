
from geometry import Vec3

class ObjParser:

  vertexes = list()
  faces = list()


  def __init__(self, file_path) -> None:
    file = open(file_path)
    self._parse_vertexes(file)
    self._parse_faces(file)
    
    


  def _parse_vertexes(self, file):
    while((line := file.readline())[0] == "v"):
      line = line[1:]
      vertex = list(map(float, line.split()))
      self.vertexes.append(Vec3(vertex[0], vertex[1], vertex[2]))

  def _parse_faces(self, file):
    while ((line := file.readline()) != ""):

      if(line[0] == "f"):
        line = line[1:]
        self.faces.append(list())
        for s in line.split():
          self.faces[-1].append(int(s.split("/")[0]))