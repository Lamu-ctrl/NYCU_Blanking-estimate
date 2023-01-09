import math
import csv


def rect(x_part, y_part, tool_list, x_num, y_num, x_startpos, y_startpos, partgap, overlap, turret_extime, turret_deg):
    print(" . ")
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
    horizontalShearInbtwnMove = 0
    verticalShearInbtwnMove = 0
    turrettoolchange = 0

    rectToolMaxLen = 0
    for tool in tool_list:
        if (tool[2] == "rect"):
            rectToolMaxLen = max(rectToolMaxLen, max(tool[0], tool[1]))

    # move to start POS
    horizontalPartMove += x_startpos
    verticalPartMove += y_startpos
    # x dir--橫刀
    horizontalPartMove += (x_num*x_part+(x_num-1) *
                           partgap)*(y_num*2)  # x方向總長*邊數
    verticalPartMove += (y_num*y_part+(y_num-1)*partgap) * \
        2  # 移動到底部的距離+回到startpos

    horizontalLineHit_single = math.ceil(x_part/(rectToolMaxLen-overlap))
    horizontalLineHit += horizontalLineHit_single*x_num*y_num*2

    hibm = (rectToolMaxLen-overlap)*(horizontalLineHit_single-1) - \
        ((rectToolMaxLen-overlap)*horizontalLineHit_single-x_part-2*overlap)
    horizontalInbtwnMove += hibm*x_num*y_num
    # 換刀
    turrettoolchange += turret_deg
    # y dir--直刀

    horizontalPartMove += (x_num*x_part+(x_num-1) *
                           partgap) * 2  # 移動到底部的距離+回到startpos
    verticalPartMove += (y_num*y_part+(y_num-1) *
                         partgap)*(x_num*2)  # x方向總長*邊數

    verticalLineHit_single = math.ceil(y_part/(rectToolMaxLen-overlap))
    verticalLineHit += verticalLineHit_single*x_num*y_num*2

    vibm = (rectToolMaxLen-overlap)*(verticalLineHit_single-1) - \
        ((rectToolMaxLen-overlap)*verticalLineHit_single-y_part-2*overlap)
    verticalInbtwnMove += vibm*x_num*y_num
    return [horizontalLineHit, verticalLineHit, singleHit, nibblinghit, shearHit, horizontalPartMove,
            verticalPartMove, horizontalInbtwnMove, verticalInbtwnMove, horizontalShearInbtwnMove, verticalShearInbtwnMove, turrettoolchange]


if __name__ == "__main__":
    data = []
    #rect(x_part, y_part, tool_list, x_num, y_num, x_startpos, y_startpos, partgap, overlap, turret_extime, turret_deg)
    x_part = 150
    y_part = 60
    #tool_list = [[10, 2, "rect"], [2, 10, "rect"]]
    tool_list = [[15, 2, "rect"], [2, 15, "rect"]]
    x_num = 5
    y_num = 5
    x_startpos = 50
    y_startpos = 50
    partgap = 6
    overlap = 1
    turret_extime = 5
    turret_deg = 90
#(x_part, y_part, tool_list, x_num, y_num, x_startpos,y_startpos, partgap, overlap, turret_extime, turret_deg)
    data.append(rect(50, 30, [[10, 2, "rect"], [2, 10, "rect"]], 2, 2, x_startpos,
                     y_startpos, partgap, overlap, turret_extime, turret_deg))
    data.append(rect(50, 30, [[10, 2, "rect"], [2, 10, "rect"]], 3, 4, x_startpos,
                     y_startpos, partgap, overlap, turret_extime, turret_deg))
    data.append(rect(50, 30, [[10, 2, "rect"], [2, 10, "rect"]], 5, 5, x_startpos,
                     y_startpos, partgap, overlap, turret_extime, turret_deg))
    data.append(rect(50, 30, [[10, 2, "rect"], [2, 10, "rect"]], 3, 6, x_startpos,
                     y_startpos, partgap, overlap, turret_extime, turret_deg))

    data.append(rect(150, 60, [[15, 2, "rect"], [2, 15, "rect"]], 2, 2, x_startpos,
                     y_startpos, partgap, overlap, turret_extime, turret_deg))
    data.append(rect(150, 60, [[15, 2, "rect"], [2, 15, "rect"]], 3, 4, x_startpos,
                     y_startpos, partgap, overlap, turret_extime, turret_deg))
    data.append(rect(150, 60, [[15, 2, "rect"], [2, 15, "rect"]], 5, 5, x_startpos,
                     y_startpos, partgap, overlap, turret_extime, turret_deg))
    data.append(rect(150, 60, [[15, 2, "rect"], [2, 15, "rect"]], 3, 6, x_startpos,
                     y_startpos, partgap, overlap, turret_extime, turret_deg))

    # output
    with open('output.csv', 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        # 寫入一列資料
        writer.writerow(["horizontalLineHit", "verticalLineHit", "singleHit", "nibblinghit", "shearHit", "horizontalPartMove",
                        "verticalPartMove", "horizontalInbtwnMove", "verticalInbtwnMove", "horizontalShearInbtwnMove", "verticalShearInbtwnMove", "turrettoolchange"])
        # 寫入另外幾列資料
        for row in data:
            writer.writerow(row)
