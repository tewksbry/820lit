import random
import itertools
from visualizer import Visualizer
import pattern


def main():
    visualizer = Visualizer(pattern=pattern.rainbow())
    visualizer.play(delay=0)

main()
