import random
import matplotlib.pyplot as plt
from shapely import affinity
from shapely.geometry import Polygon, Point, LineString
import numpy as np
import math
import csv
import time
import tqdm
from tqdm import trange
import os


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


class with_sheer_hole:
    def __init__(self, out=[]):
        self.sides = out
        self.x1 = self.sides[0][0]
        self.y1 = self.sides[0][1]
        self.x2 = self.sides[1][0]
        self.y2 = self.sides[1][1]
        self.x3 = self.sides[2][0]
        self.y3 = self.sides[2][1]
        self.x4 = self.sides[3][0]
        self.y4 = self.sides[3][1]
        num_shear = random.randint(2, 5)
        shapes, self.raw_xydata = generate_shear_in_rectangle(
            num_shear, self.x1, self.x2, self.y1, self.y3)
        # plt
        # plot_shapes(shapes, 4000, 4000)

    def __str__(self):
        return f"{self.w}: {self.l}"

    def output(self):

        return [self.w, self.video_counter, self.video, self.note_counter, self.note]

    def write_to_txt(self, gID, path):
        counter = 1
        f = open(path, 'a+', encoding='UTF-8')

        print(f"; rect part", file=f)
        print(f"; gID, gType, iUserSetID, parentID, rotmiliDeg, iAppRef, iCamAttr, iRevEngF,", file=f)
        print(
            f"{gID},     30,       19,        0,        0, 	   0,  	0, 	    1,", file=f)
        print(f"{self.x1}, {self.y1}, {self.x2},{self.y2},{self.x3},{self.y3},{self.x4},{self.y4}, ", file=f)

        for row in self.raw_xydata:
            print(f"; rect hole  {row[4]} deg", file=f)
            print(
                f"; gID, gType, iUserSetID, parentID, rotmiliDeg, iAppRef, iCamAttr, iRevEngF, ", file=f)
            print(
                f"{gID+counter}, 30, {gID+counter}, {gID}, {row[4]*1000}, 0, 0, 1, ", file=f)
            print(f";x1, y1, x2, y2, x3, y3, x4, y4,", file=f)
            print(
                f"{row[0][0]}, {row[0][1]}, {row[1][0]}, {row[1][1]}, {row[2][0]},  {row[2][1]}, {row[3][0]},  {row[3][1]}, ", file=f)
            counter += 1

        f.close()
        return gID+counter


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

    # plt.show()


def generate_shapes(num_rectangles, sheet_width, sheet_height, max_rectangle_width, max_rectangle_height):
    shapes = []

    while len(shapes) < num_rectangles:
        new_shape = generate_random_rectangle(
            max_rectangle_width, max_rectangle_height, sheet_width, sheet_height)

        if not any(new_shape.intersects(shape) for shape in shapes):
            shapes.append(new_shape)

    return shapes


def generate_random_rectangle(max_width, max_height, sheet_width, sheet_height):
    width = random.randint(300, max_width)
    height = random.randint(300, max_height)
    x = random.randint(50, sheet_width - width-50)
    y = random.randint(50, sheet_height - height-50)
    return Polygon([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])

# shear


def generate_shear_in_rectangle(num_shear_rectangles, xl, xr, yl, yr):
    shapes = []
    raw_xydata = []
    max_try = 200000
    counter = 0
    counter2 = 0
    # print("{xl}, {xr}, {yl}, {yr} ", xl, xr, yl, yr)
    while len(shapes) < num_shear_rectangles:
        counter += 1
        # # 隨機角度
        # new_shape, xydata = generate_random_rotated_rectangle(
        #     xl, xr, yl, yr, degree=random.randint(15, 75))

        # fix degreee
        new_shape, xydata = generate_random_rotated_rectangle(
            xl, xr, yl, yr, 45)

        if not any(new_shape.intersects(shape) for shape in shapes):
            if new_shape.within(Polygon([(xl, yl), (xr, yl), (xr, yr), (xl, yr)])):
                shapes.append(new_shape)
                raw_xydata.append(xydata)
        if counter >= max_try:

            if counter2 >= 10:
                break

            counter2 += 1
            print("clear ", counter2)
            shapes.clear()
            raw_xydata.clear()
            counter = 0

    return shapes, raw_xydata


def generate_random_rotated_rectangle(xl, xr, yl, yr, degree=30):
    # 生成出來的小正方形 長、寬
    width = random.randint(20, int(abs(xr-xl)/2))
    height = random.randint(20, int(abs(yr-yl)/2))
    # 不貼邊
    x = random.randint(xl+2, xr - width-50)
    y = random.randint(yl+2, yr - height-50)

    #旋轉: [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]

    # Define the rectangle as a list of points
    # 左下 又下 右上 左上
    rectangle_points = [[x, y], [x + width, y],
                        [x + width, y + height], [x, y + height]]
    rotated_rectangle_points = rotate(rectangle_points, 0, degree)
    rotated_rectangle = Polygon(rotated_rectangle_points)
    # rectangle.rotate(angle, center=center)

    # 判定角度
    # angle = angle_between_points(
    #     rotated_rectangle_points[0], rotated_rectangle_points[1], rotated_rectangle_points[2])
    # print(f"The angle between points A, B, and C is {angle} degrees.")

    # 加上角度
    rectangle_points.append(degree)

    # print("aft", rectangle)
    # time.sleep(5)
    return rotated_rectangle, rectangle_points


def rotate(points, origin_index, angle):
    """
    Rotate a rectangle counterclockwise by a given angle around a given origin point.

    The angle should be given in degrees.
    """
    ox, oy = points[origin_index]
    angle = np.radians(angle)  # 將角度轉換為弧度

    rotated_points = []
    for px, py in points:
        qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
        qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
        rotated_points.append([qx, qy])

    return rotated_points


def angle_between_points(a, b, c):
    """Calculate the angle between three points."""
    ba = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)


def generate_random_roundconer(sides):

    r = random.randint(
        5, int(min(abs(sides[0][0]-sides[1][0]), abs(sides[1][1]-sides[2][1]))/2))

    w = abs(sides[0][0]-sides[1][0])-2*r
    l = abs(sides[1][1]-sides[2][1])-2*r
    geo = roundConer(w=w, l=l, raidus=r, out=sides)
    return geo


def generate_random_shear_inside_rect(sides):

    geo = with_sheer_hole(out=sides)
    return geo


def run_many_times(times):
    if not (os.path.exists(f'./rectWithShear_generator/')):
        os.mkdir(f'./rectWithShear_generator/')

    for i in trange(times):

        # Example usage
        sheet_width = 4000
        sheet_height = 2000
        # 矩形數量
        num_rectangles = random.randint(2, 5)
        max_rectangle_width = 1000
        max_rectangle_height = 1000
        gIDnow = 1
        shapes = generate_shapes(num_rectangles, sheet_width,
                                 sheet_height, max_rectangle_width, max_rectangle_height)

        plot_shapes(shapes, sheet_width, sheet_height)

        # print(shapes)

        # INI
        training_cir_rectshear_sheet = []
        training_cir_rectshear_sheet.append(["; SYSCONFIG"])
        training_cir_rectshear_sheet.append(
            ["; version", "unit flag", "draw speed"])
        training_cir_rectshear_sheet.append(["; 2.1", "0(mks) 1(fbs)", "(%)"])
        training_cir_rectshear_sheet.append([201, 0, 5, 0, 0, 0, 0, 0, 0, 0,])
        training_cir_rectshear_sheet.append([";"])
        training_cir_rectshear_sheet.append(["; SYS INT DATA"])
        training_cir_rectshear_sheet.append(
            ["; nibble", "nibble", "rect", "shear", "hit1", "hit2", "hit3", "not used"])
        training_cir_rectshear_sheet.append(
            ["; arc", "line", "4side", "line", "one", "2nd", "3rd"])
        training_cir_rectshear_sheet.append(
            [10, 10, 20, 40, 20, 15, 15, 0, 0, 0])
        training_cir_rectshear_sheet.append(
            ["; screw", "tap", "louver", "form", "turret", "not used",])
        training_cir_rectshear_sheet.append(["; 1", "1", "1", "4", "rot 90",])
        training_cir_rectshear_sheet.append(
            [600, 100, 200, 100, 500, 0, 0, 0, 0, 0])
        training_cir_rectshear_sheet.append([5, 10, 5, 10, 10, 20, 0, 0, 0, 0])
        training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        training_cir_rectshear_sheet.append([";"])
        training_cir_rectshear_sheet.append(["; SYS DBL DATA"])
        training_cir_rectshear_sheet.append(
            ["; operation time in sec", "distance in meter - unless specified otherwise"])
        training_cir_rectshear_sheet.append(
            ["; Vx m/s", "Vy m/s", "Ax m/s2", "Ay m/s2, not used"])
        training_cir_rectshear_sheet.append(
            [8, 10, 20, 30, 0., 0., 0., 0., 0., 0.])
        training_cir_rectshear_sheet.append(["; not used"])
        training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        training_cir_rectshear_sheet.append(["; gID", "gType", "loopID"])
        training_cir_rectshear_sheet.append([0, 0, 0])
        training_cir_rectshear_sheet.append(
            ["; table off(x", "y)", "sheet size(x", "y)", "start(edge", "par)", "end(edge", "par)", "thickness"])
        training_cir_rectshear_sheet.append(
            [0, 0, 4000, 2000, 4, 0.95, 2, 0.2, 0.062])
        training_cir_rectshear_sheet.append(["; "])

        path = "./rectWithShear_generator/output" + str(i) + ".txt"

        with open(path, 'w', newline='') as txtfile:
            writer = csv.writer(txtfile)
            writer.writerows(training_cir_rectshear_sheet)

        all_rounds = []

        for s in shapes:

            p = list(s.exterior.coords)

            all_rounds.append(generate_random_shear_inside_rect(p))

        for it in all_rounds:
            lastgID = it.write_to_txt(gIDnow, path)
            gIDnow = lastgID+1


if __name__ == "__main__":
    run_many_times(100)
    # # Example usage
    # sheet_width = 4000
    # sheet_height = 2000
    # # 矩形數量
    # num_rectangles = random.randint(2, 5)
    # max_rectangle_width = 1000
    # max_rectangle_height = 1000
    # gIDnow = 1
    # shapes = generate_shapes(num_rectangles, sheet_width,
    #                          sheet_height, max_rectangle_width, max_rectangle_height)

    # plot_shapes(shapes, sheet_width, sheet_height)

    # # print(shapes)

    # # INI
    # training_cir_rectshear_sheet = []
    # training_cir_rectshear_sheet.append(["; SYSCONFIG"])
    # training_cir_rectshear_sheet.append(
    #     ["; version", "unit flag", "draw speed"])
    # training_cir_rectshear_sheet.append(["; 2.1", "0(mks) 1(fbs)", "(%)"])
    # training_cir_rectshear_sheet.append([201, 0, 5, 0, 0, 0, 0, 0, 0, 0,])
    # training_cir_rectshear_sheet.append([";"])
    # training_cir_rectshear_sheet.append(["; SYS INT DATA"])
    # training_cir_rectshear_sheet.append(
    #     ["; nibble", "nibble", "rect", "shear", "hit1", "hit2", "hit3", "not used"])
    # training_cir_rectshear_sheet.append(
    #     ["; arc", "line", "4side", "line", "one", "2nd", "3rd"])
    # training_cir_rectshear_sheet.append([10, 10, 20, 40, 20, 15, 15, 0, 0, 0])
    # training_cir_rectshear_sheet.append(
    #     ["; screw", "tap", "louver", "form", "turret", "not used",])
    # training_cir_rectshear_sheet.append(["; 1", "1", "1", "4", "rot 90",])
    # training_cir_rectshear_sheet.append(
    #     [600, 100, 200, 100, 500, 0, 0, 0, 0, 0])
    # training_cir_rectshear_sheet.append([5, 10, 5, 10, 10, 20, 0, 0, 0, 0])
    # training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # training_cir_rectshear_sheet.append([";"])
    # training_cir_rectshear_sheet.append(["; SYS DBL DATA"])
    # training_cir_rectshear_sheet.append(
    #     ["; operation time in sec", "distance in meter - unless specified otherwise"])
    # training_cir_rectshear_sheet.append(
    #     ["; Vx m/s", "Vy m/s", "Ax m/s2", "Ay m/s2, not used"])
    # training_cir_rectshear_sheet.append(
    #     [8, 10, 20, 30, 0., 0., 0., 0., 0., 0.])
    # training_cir_rectshear_sheet.append(["; not used"])
    # training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # training_cir_rectshear_sheet.append(["; gID", "gType", "loopID"])
    # training_cir_rectshear_sheet.append([0, 0, 0])
    # training_cir_rectshear_sheet.append(
    #     ["; table off(x", "y)", "sheet size(x", "y)", "start(edge", "par)", "end(edge", "par)", "thickness"])
    # training_cir_rectshear_sheet.append(
    #     [0, 0, 4000, 2000, 4, 0.95, 2, 0.2, 0.062])
    # training_cir_rectshear_sheet.append(["; "])

    # path = f'./output.txt'

    # with open(path, 'w', newline='') as txtfile:
    #     writer = csv.writer(txtfile)
    #     writer.writerows(training_cir_rectshear_sheet)

    # all_rounds = []
    # print("how many shapes", len(shapes))
    # for s in shapes:
    #     print("deal")
    #     p = list(s.exterior.coords)

    #     all_rounds.append(generate_random_shear_inside_rect(p))

    # for it in all_rounds:
    #     it.write_to_txt(gIDnow)
    #     gIDnow += 1
