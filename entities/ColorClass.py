class ColorClass:

    def __init__(self, vertices, color):
        self._color = color
        self._vertices = vertices
        self._size = len(vertices)

    def getColor(self):
        return self._color

    def getVertices(self):
        return self._vertices

    def setVertices(self, vertices):
        self._vertices = vertices
        self._size = len(vertices)

    def addVertex(self, vertex):
        self._vertices.append(vertex)
        self._size += 1

    def removeVertex(self, vertex):
        self._vertices.remove(vertex)
        self._size -= 1

    def __lt__(self, other):
        return self._size < len(other)

    def __eq__(self, other):
        return self._color == other.getColor()

    def __len__(self):
        return self._size
