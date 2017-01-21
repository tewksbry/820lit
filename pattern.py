import random


class LED:
    """docstring for LED"""

    def __init__(self, R=0, G=0, B=0, W=0, tup=None, brightness=1):
        self.R = R
        self.G = G
        self.B = B
        self.W = W
        self.brightness = brightness
        if tup is not None:
            self.R, self.G, self.B = tup
            if len(tup) == 4:
                self.W = tup[3]

    def RGB(self):
        return map(int, (self.R * self.brightness, self.G * self.brightness, self.B * self.brightness))

    def RGBW(self):
        return map(int, (self.R * self.brightness, self.G * self.brightness, self.B * self.brightness, self.W * self.brightness))

    def setColor(self, RGB):
        if isinstance(RGB, LED):
            self.R, self.G, self.B, self.W = RGB.R, RGB.G, RGB.B, RGB.W
        else:
            self.R, self.G, self.B = RGB
            if len(RGB) == 4:
                self.W = RGB[3]

    def __mul__(self, other):
        return LED(self.R * other, self.G * other, self.B * other, self.W * other)

    __rmul__ = __mul__

    def __repr__(self):
        return "(%i, %i, %i, %i)*%f" % (self.R, self.G, self.B, self.W, self.brightness)


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

    def setBrightness(self, brightness=1):
        for LED in self.arr:
            LED.brightness = brightness

    def fade(self, fade):
        for LED in self.arr:
            LED.brightness *= fade

    def fillWithPalette(self, palette, start=0, end=-1, dir=None):
        if start >= end:
            return
        if end == -1:
            end = self.patternwidth
        size = (end - start)
        if start < 0:
            start = 0
        if end > self.patternwidth:
            end = self.patternwidth
        stretch_factor = float(len(palette)) / size

        if start != 0 and dir != "right":
            self.fillWithPalette(palette[::-1], start - size, start, dir="left")
        if end != self.patternwidth and dir != "left":
            self.fillWithPalette(palette[::-1], end, end + size, dir="right")

        if start == 0:
            for i in range(start, end):

                self.arr[end - i - 1].setColor(palette[int((size - i - 1) * stretch_factor)])
        else:
            for i in range(start, end):
                self.arr[i].setColor(palette[int((i - start) * stretch_factor)])

    def fillWithColor(self, color, start=0, end=-1):
        if end == -1:
            end = self.patternwidth
        for i in range(start, end):
            self.arr[i].setColor(color)


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
grayScale = [LED(i, i, i, i) for i in range(255, -1, -1)]
redToWhite = [LED(255, i, i, i) for i in range(256)]
blueToWhite = [LED(255, i, i, i) for i in range(256)]
greenToWhite = [LED(255, i, i, i) for i in range(256)]


RGB = [255, 0, 0]
for decCol in range(3):
    incCol = 0 if decCol == 2 else decCol + 1
    for _ in range(255):
        RGB[decCol] -= 1
        RGB[incCol] += 1
        raindowColors.append(LED(tup=RGB))

rotatedRainbow = list(raindowColors)


def rotateRainbow(volume, last_volume):
    if last_volume and volume > last_volume:
        volumeChange = volume - last_volume
        global rotatedRainbow
        rotatedRainbow = rotate(rotatedRainbow, int(len(rotatedRainbow) * (volumeChange**1.1) / (100**1.1 * 3)))


def rotate(l, n):
    return l[-n:] + l[: -n]


def defaultPatternSet():
    patternArr = [Pattern([LED(i, i, i, i)]) for i in range(256)]
    patternArr.extend([Pattern([LED(i, i, i, i)]) for i in range(254, -1, -1)])
    return PatternSet(patternSet=patternArr)


def rainbowPatternSet():
    patternArr = []
    for color in raindowColors:
        patternArr.append(Pattern([color]))
    return PatternSet(patternwidth=1, pattern=patternArr)


def sparkle(width=240):
    noVolumeBar = Pattern([LED()] * width)
    for i in range(10):
        ChosenOne = random.randint(0, 239)
        noVolumeBar.arr[ChosenOne] = LED(R=255, G=59)
    for i in range(10):
        ChosenOne = random.randint(0, 239)
        noVolumeBar.arr[ChosenOne] = LED(R=255, G=208)
    return noVolumeBar


def middleOut(volume, width=240, previous=None, fade=0, cutoff=1, color_palette=raindowColors, fill=False, last_volume=None):
    pattern = previous

    if not pattern:
        pattern = Pattern([LED() for _ in range(width)])

    elif fill:
        pattern.setBrightness(1)
    else:
        pattern.fade(fade)

    middle = width / 2

    range_size = int(middle * cutoff)
    active_range = int(range_size * volume / 100.0)

    rotateRainbow(volume, last_volume)

    pattern.fillWithPalette(color_palette, middle, middle + range_size)

    for i in range(active_range):
        pattern.arr[middle + i].brightness = 1
        pattern.arr[middle - 1 - i].brightness = 1

        if i >= middle * (2 * cutoff - 1):
            spillover = int(i - middle * (2 * cutoff - 1))
            pattern.arr[-spillover - 1].brightness = 1
            pattern.arr[spillover].brightness = 1
    if fill and cutoff == 1:
        pattern.fillWithColor(color_palette[active_range * len(color_palette) / range_size - 1], end=middle - active_range)
        pattern.fillWithColor(color_palette[active_range * len(color_palette) / range_size - 1], start=middle + active_range)
    return pattern
