import random
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, LineString


class roundConer:
    def __init__(self, w=100, l=80, raidus=10, sheet_width=2000, sheet_height=4000, out=[]):
        self.w = w
        self.l = l
        self.raidus = raidus
        self.sides = out
        self.x1 = self.sides[0][0]
        self.y1 = self.sides[0][1]
        self.x2 = self.sides[1][0]
        self.y2 = self.sides[1][1]
        self.x3 = self.sides[2][0]
        self.y3 = self.sides[2][1]
        self.x4 = self.sides[3][0]
        self.y4 = self.sides[3][1]

    def __str__(self):
        return f"{self.w}: {self.l}, {self.raidus}"

    def output(self):

        return [self.w, self.video_counter, self.video, self.note_counter, self.note]

    def write_to_txt(self, gID):
        counter = 0
        path = f'./output.txt'
        f = open(path, 'a', encoding='UTF-8')

        print(f"; COMPOSITE2DLOOP ", file=f)
        print(f"; gID, gType, iUserSetID, parentID, numEdge, close, iAppRef, iCamAttr, iRevEngF, ", file=f)
        print(f"{gID}, 31, 7, 0, 8, 0, 0, 0, 1, ", file=f)

        # print(f"Trader Name: {traderName}", file=f)
        # 1:line
        print(f"; edgeID, gType,", file=f)
        print(f"{gID*10000+counter},12", file=f)
        print(f"; x1, y1, x2, y2, ", file=f)
        print(f"{round(self.x1+self.raidus,1)}, {round(self.y1,1)}, {round(self.x2-self.raidus,1)}, {round(self.y2,1)}, ", file=f)
        counter += 1
        # 2:arc
        print(f"; edgeID, gType, CCW, segCt,", file=f)
        print(f"{gID*10000+counter}, 14, 1, 15, ", file=f)
        print(f"; x1, y1, xc, yc, x2, y2, radius, degrees ", file=f)
        print(f"{round(self.x2-self.raidus,1)}, {round(self.y2,1)}, {round(self.x2-self.raidus,1)}, {round(self.y2 + self.raidus,1)}, {round(self.x2,1)}, {round(self.y2 + self.raidus,1)},  {round(self.raidus,1)},  90.", file=f)
        counter += 1

        # 3:line
        print(f"; edgeID, gType,", file=f)
        print(f"{gID*10000+counter},12", file=f)
        print(f"; x1, y1, x2, y2, ", file=f)
        print(f"{round(self.x2,1)}, {round(self.y2+self.raidus,1)}, {round(self.x3,1)}, {round(self.y3-self.raidus,1)}, ", file=f)
        counter += 1
        # 4:arc
        print(f"; edgeID, gType, CCW, segCt,", file=f)
        print(f"{gID*10000+counter}, 14, 1, 15, ", file=f)
        print(f"; x1, y1, xc, yc, x2, y2, radius, degrees ", file=f)
        print(f"{round(self.x3,1)}, {round(self.y3-self.raidus,1)}, {round(self.x3-self.raidus,1)}, {round(self.y3 - self.raidus,1)}, {round(self.x3-self.raidus,1)}, {round(self.y3 ,1)},  {round(self.raidus,1)},  90.", file=f)
        counter += 1

        # 5:line
        print(f"; edgeID, gType,", file=f)
        print(f"{gID*10000+counter},12", file=f)
        print(f"; x1, y1, x2, y2, ", file=f)
        print(f"{round(self.x3-self.raidus,1)}, {round(self.y3,1)}, {round(self.x4+self.raidus,1)}, {round(self.y4,1)}, ", file=f)
        counter += 1
        # 6:arc
        print(f"; edgeID, gType, CCW, segCt,", file=f)
        print(f"{gID*10000+counter}, 14, 1, 15, ", file=f)
        print(f"; x1, y1, xc, yc, x2, y2, radius, degrees ", file=f)
        print(f"{round(self.x4+self.raidus,1)}, {round(self.y4,1)}, {round(self.x4+self.raidus,1)}, {round(self.y4 - self.raidus,1)}, {round(self.x4,1)}, {round(self.y4 - self.raidus,1)},  {round(self.raidus,1)},  90.", file=f)
        counter += 1

        # 7:line
        print(f"; edgeID, gType,", file=f)
        print(f"{gID*10000+counter},12", file=f)
        print(f"; x1, y1, x2, y2, ", file=f)
        print(f"{round(self.x4,1)}, {round(self.y4 - self.raidus,1)}, {round(self.x1,1)}, {round(self.y1 + self.raidus,1)}, ", file=f)
        counter += 1
        # 8:arc
        print(f"; edgeID, gType, CCW, segCt,", file=f)
        print(f"{gID*10000+counter}, 14, 1, 15, ", file=f)
        print(f"; x1, y1, xc, yc, x2, y2, radius, degrees ", file=f)
        print(f"{round(self.x1,1)}, {round(self.y1 + self.raidus,1)}, {round(self.x1 + self.raidus,1)}, {round(self.y1 + self.raidus,1)}, {round(self.x1 + self.raidus,1)}, {round(self.y1 ,1)},  {round(self.raidus,1)},  90.", file=f)
        counter += 1


def plot_shapes(shapes, sheet_width, sheet_height):
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.set_xlim(0, sheet_width)
    ax.set_ylim(0, sheet_height)

    for shape in shapes:
        if isinstance(shape, Polygon):
            x, y = shape.exterior.xy
            ax.fill(x, y, alpha=0.5)
        elif isinstance(shape, LineString):
            x, y = shape.xy
            ax.plot(x, y, linewidth=3)
        else:
            print("Unsupported shape type")

    plt.show()


def generate_shapes(num_rectangles, sheet_width, sheet_height, max_rectangle_width, max_rectangle_height):
    shapes = []
    while len(shapes) < num_rectangles:
        new_shape = generate_random_rectangle(
            max_rectangle_width, max_rectangle_height, sheet_width, sheet_height)

        if not any(new_shape.intersects(shape) for shape in shapes):
            shapes.append(new_shape)

    return shapes


def generate_random_rectangle(max_width, max_height, sheet_width, sheet_height):
    width = random.randint(200, max_width)
    height = random.randint(200, max_height)
    x = random.randint(0, sheet_width - width)
    y = random.randint(0, sheet_height - height)
    return Polygon([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])


def generate_random_roundconer(sides):

    r = random.randint(
        5, int(min(abs(sides[0][0]-sides[1][0]), abs(sides[1][1]-sides[2][1]))/2))

    w = abs(sides[0][0]-sides[1][0])-2*r
    l = abs(sides[1][1]-sides[2][1])-2*r
    geo = roundConer(w=w, l=l, raidus=r, out=sides)
    return geo


# Example usage
sheet_width = 4000
sheet_height = 2000
# 矩形數量
num_rectangles = random.randint(5, 15)
max_rectangle_width = 1000
max_rectangle_height = 1000
gIDnow = 1
shapes = generate_shapes(num_rectangles, sheet_width,
                         sheet_height, max_rectangle_width, max_rectangle_height)

plot_shapes(shapes, sheet_width, sheet_height)


# print(shapes)
all_rounds = []
for s in shapes:
    # print(s)
    # print(type(s))
    p = list(s.exterior.coords)
    # print(type(p))
    # print(p[:4])
    # print(p[0][1])
    all_rounds.append(generate_random_roundconer(p))

for it in all_rounds:
    it.write_to_txt(gIDnow)
    gIDnow += 1
