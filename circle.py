''' Animation of circles bouncing in a box '''

from time import sleep
from random import randint, uniform
from graphics import Circle, GraphWin, Point
from multiprocessing import Process

class NewCircle(Circle):
    def __init__(self, center, radius, velocity):
        Circle.__init__(self, center, radius)
        self.vel = velocity
        self.left = self.vel[0] < 0
        self.down = self.vel[1] < 0
        self.setFill("white")

def main():
    width, height = 1920, 1080
    window = GraphWin("Ball", width, height)
    window.setBackground("black")
    circles = make_circles(10, window)
    bounce(window, circles)

def make_circles(num, window):
    circles = []
    width, height = window.getWidth(), window.getHeight()
    for _ in range(num):
        center = Point(randint(0, width), randint(0, height))
        radius = randint(10, 30)
        velocity = [uniform(5, 10), uniform(5, 10)]
        circle = NewCircle(center, radius, velocity)
        circle.draw(window)
        circles += [circle]
    return circles

def bounce(window, circles):
    width = window.getWidth()
    height = window.getHeight()
    while True:
        for c in circles:
            move_circle(c, width, height)

def move_circle(circle, width, height):
    p1, p2 = circle.getP1(), circle.getP2()
    dx, dy = circle.vel[0], circle.vel[1]
    left, down = dx > 0, dy > 0
    if (down and p2.getY()+dy >= height) or ((not down) and p1.getY()-dy <= 0):
        circle.vel[1] = -dy
        down = not down
    if (left and p2.getX()+dx >= width) or ((not left) and p1.getX()-dx <= 0):
        circle.vel[0] = -dx
        left = not left
    circle.move(circle.vel[0], circle.vel[1])

if __name__ == "__main__":
    main()
