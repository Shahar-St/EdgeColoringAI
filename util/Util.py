import random


def getValidIndexes(vecSize):
    index1 = random.randint(0, vecSize - 1)
    index2 = random.choice([i for i in range(vecSize) if i != index1])

    # make sure index1 < index2
    if index1 > index2:
        temp = index1
        index1 = index2
        index2 = temp

    return index1, index2
