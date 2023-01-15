import math
import csv


def circle(radius, nibblingSide, circledeg, tool_list, x_num, y_num, x_startpos, y_startpos, partgap, overlap, turret_extime, turret_deg):
    # Inizilize
    horizontalLineHit = 0
    verticalLineHit = 0
    singleHit = 0
    nibblinghit = 0
    shearHit = 0
    horizontalPartMove = 0
    verticalPartMove = 0  # only when x_dir change line
    horizontalInbtwnMove = 0
    verticalInbtwnMove = 0
    turrettoolchange = 0
    horizontalShearInbtwnMove = 0
    verticalShearInbtwnMove = 0
    # tool
    rectToolMaxLen = 0
    circleToolMaxLen = 0

    for tool in tool_list:
        if (tool[1] == "circle"):
            circleToolMaxLen = max(circleToolMaxLen, tool[1])

    # move to start POS
    horizontalPartMove += x_startpos
    verticalPartMove += y_startpos

    # x dir

    horizontalPartMove += ((radius*2+partgap)*(x_num-1))*(y_num*2)
    verticalPartMove += (radius*2+partgap)*(y_num-1)*2
    nibblinghit = x_num*y_num * \
        nibblingcircle(radius, tool_list, circledeg, nibblingSide)

    return [horizontalLineHit, verticalLineHit, singleHit, nibblinghit, shearHit, horizontalPartMove,
            verticalPartMove, horizontalInbtwnMove, verticalInbtwnMove, horizontalShearInbtwnMove, verticalShearInbtwnMove, turrettoolchange]


def nibblingcircle(radius, tool_list, circledeg, nibblingSide):

    pinch = float(radius)/3

    nibblinghit = 0
    circumference = 2*math.pi*radius
    hits = circumference*(circledeg/360)/pinch

    return math.ceil(hits)


if __name__ == "__main__":
    # rect(x_part, y_part, tool_list, x_num, y_num, x_startpos, y_startpos, partgap, overlap, turret_extime, turret_deg)
    data = []
    x_part = 150
    y_part = 60
    # tool_list = [[3, "r"]]
    tool_list = [["circle", 3]]
    x_num = 5
    y_num = 5
    x_startpos = 50
    y_startpos = 50
    partgap = 10
    overlap = 1
    turret_extime = 5
    turret_deg = 90
    radius = 50
    nibblingSide = -1  # 外側
    circledeg = 360

    for r in [50, 125]:
        for num in [[2, 2], [3, 4], [5, 5], [3, 6]]:
            data.append(circle(r, -1, circledeg, tool_list, num[0],
                               num[1], x_startpos, y_startpos, partgap, overlap, turret_extime, turret_deg))

    # for da in data:
    #     print(da)

    with open('output.csv', 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        # 寫入一列資料
        writer.writerow(["horizontalLineHit", "verticalLineHit", "singleHit", "nibblinghit", "shearHit", "horizontalPartMove",
                        "verticalPartMove", "horizontalInbtwnMove", "verticalInbtwnMove", "horizontalShearInbtwnMove", "verticalShearInbtwnMove", "turrettoolchange"])
        # 寫入另外幾列資料
        for row in data:
            writer.writerow(row)
