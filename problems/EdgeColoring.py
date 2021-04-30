import os

import numpy as np


class EdgeColoring:

    def __init__(self, fileName):
        filePath = os.getcwd() + '\\util\\instances\\' + fileName
        inputFile = open(filePath, 'r')
        lines = [line[2:-1] for line in inputFile.readlines() if not line.startswith('c')]
        edgesAndVertices = lines[0].split(' ')[1:]
        numOfVertices = int(edgesAndVertices[0])
        numOfEdges = int(edgesAndVertices[1])
        graphMatrix = np.full((numOfEdges, numOfEdges), False)
        for edge in lines[1:]:
            vertices = edge.split(' ')
            graphMatrix[int(vertices[0]) - 1][int(vertices[1]) - 1] = True
            graphMatrix[int(vertices[1]) - 1][int(vertices[0]) - 1] = True

        print('Input File:' + fileName)
        print(f'# of edges: {numOfEdges}, # of vertices: {numOfVertices}')
        print(f'Graph density: {((2 * numOfEdges) / (numOfVertices * (numOfVertices - 1))):.6f}')

        self._graphMatrix = graphMatrix
        self._numOfEdges = numOfEdges
        self._numOfVertices = numOfVertices


    def generateRandomVec(self):
        raise NotImplementedError

    def calculateFitness(self, vec):
        raise NotImplementedError

    def translateVec(self, vec):
        raise NotImplementedError
