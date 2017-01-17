class LED:
    """docstring for LED"""

    def __init__(self, R=0, G=0, B=0, W=0, tup=None):
        self.R = R
        self.G = G
        self.B = B
        self.W = W
        if tup is not None:
            self.R, self.G, self.B = tup
            if len(tup) == 4:
                self.W = tup[3]

    def RGB(self):
        return (self.R, self.G, self.B)

    def fade(self, old):
        mindiff = min(old.R - self.R, old.G - self.G,
                      old.B - self.B)
        if mindiff > 0:
            self.R += mindiff / 2
            self.G += mindiff / 2
            self.B += mindiff / 2
            self.W += mindiff / 2

    def __mul__(self, other):
        return LED(self.R * other, self.G * other, self.B * other, self.W * other)

    __rmul__ = __mul__

    def __repr__(self):
        return "(%i, %i, %i, %i)" % (self.R, self.G, self.B, self.W)


class Pattern:
    """docstring for Pattern"""

    def __init__(self, arr=[LED()] * 240):
        self.arr = arr
        self.patternwidth = len(arr)

    def extend(self, pattern):
        self.arr.extend(pattern.arr)
        self.patternwidth = len(self.arr)

    def trim(self, size):
        self.arr = self.arr[:size]

    def fade(self, old):
        for i in range(self.patternwidth):
            if i == old.patternwidth:
                break
            self.arr[i].fade(old.arr[i])


class PatternSet:
    """docstring for PatternSet"""

    def __init__(self, patternSet=[Pattern()], filltype="repeat"):
        self.filltype = filltype
        self.patternSet = patternSet
        self.nextIndex = 0

    def next(self, width=240):
        nextPattern = Pattern([LED()] * width)
        if self.filltype == "repeat":
            pattern = self.patternSet[self.nextIndex]
            for _ in range(width / pattern.patternwidth + 1):
                nextPattern.extend(pattern)
        else:
            nextPattern.arr[:len(self.patternSet)] = self.patternSet[
                self.nextIndex].arr

        nextPattern.trim(width)

        self.nextIndex += 1
        if self.nextIndex == self.patternLength:
            self.nextIndex = 0

        return nextPattern


raindowColors = []
RGB = [255, 0, 0]
for decCol in range(3):
    incCol = 0 if decCol == 2 else decCol + 1
    for _ in range(255):
        RGB[decCol] -= 1
        RGB[incCol] += 1
        raindowColors.append(LED(tup=RGB))


def defaultPatternSet():
    patternArr = [Pattern([LED(i, i, i, i)]) for i in range(256)]
    patternArr.extend([Pattern([LED(i, i, i, i)]) for i in range(254, -1, -1)])
    return PatternSet(patternSet=patternArr)


def rainbowPatternSet():
    patternArr = []
    for color in raindowColors:
        patternArr.append(Pattern([color]))
    return PatternSet(patternwidth=1, pattern=patternArr)


def leftPatternFromVolume(volume, width=240):
    volumeBar = Pattern([LED()] * width)
    for i in range(int(width * volume / 100.0)):
        volumeBar.arr[i] = LED(R=255)
    return volumeBar


def middleOutPatternFromVolume(volume, width=240):
    volumeBar = Pattern([LED()] * width)
    middle = width / 2
    for i in range(int(middle * volume / 100.0)):
        volumeBar.arr[middle + i] = LED(R=255)
        volumeBar.arr[middle - 1 - i] = LED(R=255)
    return volumeBar


def middleOutRainbowPatternFromVolume(volume, width=240, previous=None, fade=0.9):
    volumeBar = previous
    if not volumeBar:
        volumeBar = Pattern([LED()] * width)
    else:
        volumeBar.arr = map(lambda x: fade * x, volumeBar.arr)
    middle = width / 2
    for i in range(int(middle * volume / 100.0)):
        volumeBar.arr[middle + i] = raindowColors[i *
                                                  len(raindowColors) / middle]
        volumeBar.arr[middle - 1 - i] = raindowColors[i *
                                                      len(raindowColors) / middle]
    return volumeBar


def middleOutRainbowWithFillPatternFromVolume(volume, width=240):
    volumeBar = Pattern([LED()] * width)
    middle = width / 2
    lastIndex = int(middle * volume / 100.0)
    for i in range(lastIndex):
        volumeBar.arr[middle + i] = raindowColors[i *
                                                  len(raindowColors) / middle]
        volumeBar.arr[middle - i - 1] = raindowColors[i *
                                                      len(raindowColors) / middle]
    volumeBar.arr[:middle - lastIndex] = [raindowColors[lastIndex * len(raindowColors) / middle]] * (middle - lastIndex)
    volumeBar.arr[middle + lastIndex:] = [raindowColors[lastIndex * len(raindowColors) / middle]] * (middle - lastIndex)
    return volumeBar


def middleOutWithEndsRainbowPatternFromVolume(volume, width=240, previous=None, fade=0.9, ending=0.75):

    volumeBar = previous
    if not volumeBar:
        volumeBar = Pattern([LED()] * width)
    else:
        volumeBar.arr = map(lambda x: fade * x, volumeBar.arr)
    middle = width / 2
    range_size = int(middle * ending)
    for i in range(int(range_size * volume / 100.0)):
        volumeBar.arr[middle + i] = raindowColors[i * len(raindowColors) / range_size]
        volumeBar.arr[middle - 1 - i] = raindowColors[i * len(raindowColors) / range_size]
        if i >= middle * (2 * ending - 1):
            spillover = int(i - middle * (2 * ending - 1))
            volumeBar.arr[-spillover - 1] = raindowColors[i * len(raindowColors) / range_size]
            volumeBar.arr[spillover] = raindowColors[i * len(raindowColors) / range_size]
    return volumeBar
