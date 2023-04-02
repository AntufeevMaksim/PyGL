
class ObjParser:

  vertexes = list(list())
  faces = list(list())


  def __init__(self, file_path) -> None:
    file = open(file_path)
    self._parse_vertexes(file)
    self._parse_faces(file)
    
    


  def _parse_vertexes(self, file):
    while((line := file.readline())[0] == "v"):
      line = line[1:]
      self.vertexes.append(list(map(float, line.split())))

  def _parse_faces(self, file):
    while ((line := file.readline()) != ""):

      if(line[0] == "f"):
        line = line[1:]
        self.faces.append(list())
        for s in line.split():
          self.faces[-1].append(int(s.split("/")[0]))