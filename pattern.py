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
                rainbowself.W = tup[3]

    def RGB(self):
        return (self.R, self.G, self.B)

    def __repr__(self):
        return "(%i, %i, %i, %i)" % (self.R, self.G, self.B, self.W)


class Pattern:
    """docstring for Pattern"""

    def __init__(self, patternwidth=240, filltype="repeat", pattern=[LED()]):
        self.patternwidth = patternwidth
        self.filltype = filltype
        self.pattern = pattern
        self.nextIndex = 0
        self.patternLength = len(pattern)

    def next(self, width=240):
        arr = []
        if self.filltype == "repeat":
            for _ in range(width / self.patternwidth + 1):
                arr.extend(self.pattern[self.nextIndex])
        else:
            arr = [LED()] * width
            arr[:self.patternLength] = self.pattern[nextIndex]

        arr = arr[:width]

        self.nextIndex += 1
        if self.nextIndex == self.patternLength:
            self.nextIndex = 0

        return arr


def defaultPattern():
    patternArr = [[LED(i, i, i, i)] for i in range(256)]
    patternArr.extend([[LED(i, i, i, i)] for i in range(254, -1, -1)])
    return Pattern(patternwidth=1, pattern=patternArr)


def rainbow():
    RGB = [255, 0, 0]
    patternArr = []
    for decCol in range(3):
        incCol = 0 if decCol == 2 else decCol + 1

        for _ in range(255):
            RGB[decCol] -= 1
            RGB[incCol] += 1
            patternArr.append([LED(tup=RGB)])
    print patternArr
    return Pattern(patternwidth=1, pattern=patternArr)
