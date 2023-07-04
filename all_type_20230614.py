import math
import numpy as np
import csv
import random
from operator import itemgetter, attrgetter  # sort 排序時用


################## readfile ########################

def readfile(path):

    wholedata = []
    row_data = []
    a = 0
    s1 = open(path, 'r')

    while True:
        s4 = []
        s2 = s1.readline()  # s2 one line data
        s2 = s2.strip()
        # remove s2's space, comma, and split it
        s3 = s2.replace(',', ' ').split()
        if (len(s3) <= 0):
            break

        if ((s3[0] != ';') & (s3[0] != ';x1')):
            for k in range(len(s3)):
                s4.append(float(s3[k]))
            wholedata.append(s4)  # become 2D list
        row_data.append([s2])
        # print(s2)
    s1.close()  # close file

    return wholedata, row_data

################## readfile end ####################

################ data_to_function ##################


def data_to_function(wholedata):

    line_var = []
    rect_var = []
    circle_var = []
    arc_var = []
    polygon_var = []

    k = 12
    while k < len(wholedata):
        onerow_data = wholedata[k]
        if (onerow_data[3] == 0):
            print(f"Part gID : {onerow_data[0]:5}, gType: {onerow_data[1]}")
        if (len(onerow_data) <= 0):
            break

        if len(onerow_data) < 8:
            k = k+1

        #######################
        # rectangle 2D
        #######################
        elif (onerow_data[1] == 30) & (len(onerow_data) == 8):
            parentID = onerow_data[3]  # 取出parentID
            r_xy = wholedata[k+1]  # 抓取方形資料
            roDeg = (onerow_data[4] / 1000) * (math.pi / 180)  # 取旋轉角轉成弳度制

            x_point = [r_xy[0], r_xy[2], r_xy[4], r_xy[6]]
            y_point = [r_xy[1], r_xy[3], r_xy[5], r_xy[7]]
            L = max(x_point) - min(x_point)
            H = max(y_point) - min(y_point)
            j = 0

            for k1 in range(4):  # 要取到左下角點位值
                if (x_point[k1] == min(x_point)) & (j == 0):
                    a = k1  # 取x值小的點
                    j = 1
                elif (x_point[k1] == min(x_point)) & (j == 1):
                    if y_point[k1] < y_point[a]:  # 取y值小的點
                        a = k1
                rect_start_p = [x_point[a], y_point[a]]

            #######################
            ## rectangle - grid
            #######################
            if (onerow_data[6] == 18):  # 判斷是不是grid

                grid_rect_data = wholedata[k+2]
                x_gap = grid_rect_data[2]
                y_gap = grid_rect_data[4]

                col_arr = int(grid_rect_data[3])
                row_arr = int(grid_rect_data[5])
                quantity = col_arr * row_arr

                for ix in range(row_arr):
                    for iy in range(col_arr):
                        rect_grid_x = rect_start_p[0] + x_gap * iy
                        rect_grid_y = rect_start_p[1] + y_gap * ix
                        rect_grid_xy = [rect_grid_x, rect_grid_y]
                        # [L, H, rect_grid_xy, parentID, punch type,     roDeg,      gID      , (ix + iy + 1)]
                        rect_var.append(
                            [L, H, rect_grid_xy, parentID, onerow_data[6], roDeg, onerow_data[0], (ix + iy + 1)])
                        #print(f'[{rect_grid_x}, {rect_grid_y}], col:{col_arr}, row:{row_arr}')
                k = k+3  # 將下2行也跳過

            #######################
            ## rectangle - normal
            #######################
            else:  # 不是grid的情況
                # sub_serial_num 先以 0 代表
                # [L, H, star point,   parentID,   punch_type,   roDeg, serial_num, sub_serial_num]
                rect_var.append([L, H, rect_start_p, parentID,
                                onerow_data[6], roDeg, onerow_data[0], 0])
                k = k+2  # 將下一行也跳過

        #######################
        # alone a line-circle
        #######################
        # alone a line-circle
        elif (onerow_data[7] == 17) & (onerow_data[1] == 32) & (len(onerow_data) == 9):

            parentID = onerow_data[3]  # 取出圓的parentID
            punch_type = onerow_data[7]
            first_p = wholedata[k+1]
            radius = first_p[0]
            s_deg = first_p[1] * math.pi / 180
            x_alone = first_p[2]
            y_alone = first_p[3]

            alone_data = wholedata[k+2]
            gap = alone_data[2]
            line_angle = alone_data[3] * math.pi / 180
            quantity = int(alone_data[4])

            for ix in range(quantity):
                x_ix = x_alone + gap * ix * \
                    math.cos(line_angle)  # 這邊的gap 是指中心點的差距
                y_ix = y_alone + gap * ix * math.sin(line_angle)

                circle_var.append([radius, s_deg, x_ix, y_ix, parentID,
                                  punch_type, onerow_data[0], quantity+1])  # 抓取圓形資料
            k = k+3  # 將下2行也跳過

        #######################
        # circle
        #######################
        elif (onerow_data[7] == 0) & (onerow_data[1] == 32) & (len(onerow_data) == 9):  # circle圓
            parentID = onerow_data[3]  # 取出圓的parentID
            one_cir_var = wholedata[k+1]
            one_cir_var.append(parentID)  # one_cir_var[4] = parentID
            one_cir_var.append(onerow_data[7])  # punch type
            one_cir_var.append(onerow_data[0])  # gID
            one_cir_var.append(0)

            # one_cir_var = [radius, start_at_degrees, centerX, centerY, parentID, punch type, gID, sub_serial_num = 0]
            circle_var.append(one_cir_var)  # 抓取圓形資料
            k = k+2  # 將下一行也跳過

        #######################
        # polygon
        #######################
        elif (onerow_data[6] == 0) & (onerow_data[1] == 34) & (len(onerow_data) == 8):  # polygon多邊

            nvtx = onerow_data[4]
            poly_rows = math.ceil(nvtx/4)
            x_point = []
            y_point = []

            parentID = onerow_data[3]  # 取出多邊形的parentID，先以外部輪廓為主
            poly_gID = onerow_data[0]

            for i in range(poly_rows):
                poly_xy = wholedata[k+(1+i)]  # 取出多邊形的點位資料

                for j in range(int(len(poly_xy)/2)):  # 此行長度除以2
                    x_point.append(poly_xy[2*j])
                    y_point.append(poly_xy[2*j + 1])

            if (parentID == 0):  # contour
                for h in range(len(x_point)):
                    current_x = x_point[h-1]
                    current_y = y_point[h-1]
                    next_x = x_point[h]
                    next_y = y_point[h]

                    # distance  # x**2代表x的二次方
                    dis = math.sqrt((current_x - next_x)**2 +
                                    (current_y - next_y)**2)
                    # print(f'{current_x},{next_x},{current_y},{next_y},{dis}')
                    # degree
                    if (next_x != current_x):
                        # 用math.atan反三角正切取到角度值
                        deg = math.atan((next_y - current_y) /
                                        (next_x - current_x))

                        # tan的定義域在-0.5pi~0.5pi，而我想得到的是 0~2pi，剩餘的下面判別
                        if (deg > 0) & ((next_y - current_y) < 0):
                            deg = deg + math.pi

                        elif (deg < 0) & (next_y > current_y):
                            deg = deg + math.pi

                        elif (deg < 0) & (next_y < current_y):
                            deg = deg + 2 * math.pi

                        elif (next_y == current_y) & ((next_x - current_x) < 0):  # 如果是水平，然後下個點在左邊，角度為pi
                            deg = math.pi

                    elif (next_y > current_y):  # 垂直，下個點在正上方
                        deg = math.pi/2
                    else:  # 垂直，下個點在正下方
                        deg = math.pi*3/2

                    # sub_serial_num 是指在同一個圖案中，個別的線段編號
                    ############### [current_x, current_y, dis, deg, parentID, poly_gID, sub_serial_num]
                    line_var.append(
                        [current_x, current_y, dis, deg, parentID, poly_gID,    h+1])
            # if  contour end
            elif (parentID != 0) & (nvtx == 8):
                L = max(x_point) - min(x_point)
                H = max(y_point) - min(y_point)
                j = 0
                a = 0
                for k1 in range(8):                         # 取最下面的點再取左邊的點
                    if (y_point[k1] == min(y_point)) & (j == 0):
                        a = k1  # 取y值小的點
                        j = 1
                    elif (y_point[k1] == min(y_point)) & (j == 1):  # 相同小的y值時
                        if (x_point[k1] < x_point[a]):  # 取x值小的點
                            a = k1

                Octagon_pts = []
                Octagon_pts.append([x_point[a], y_point[a]]
                                   )     # Octagon_pts[0]
                # Octagon_pts[1]
                Octagon_pts.append([x_point[a-7], y_point[a-7]])
                # Octagon_pts[2]
                Octagon_pts.append([x_point[a-6], y_point[a-6]])
                # Octagon_pts[3]
                Octagon_pts.append([x_point[a-5], y_point[a-5]])
                # Octagon_pts[4]
                Octagon_pts.append([x_point[a-4], y_point[a-4]])
                # Octagon_pts[5]
                Octagon_pts.append([x_point[a-3], y_point[a-3]])
                # Octagon_pts[6]
                Octagon_pts.append([x_point[a-2], y_point[a-2]])
                # Octagon_pts[7]
                Octagon_pts.append([x_point[a-1], y_point[a-1]])

                polygon_var.append([Octagon_pts, parentID, poly_gID])

            k = k + poly_rows  # 將下n行也跳過(每行有四個點)

        #######################
        # composite
        #######################
        elif (onerow_data[7] == 0) & (onerow_data[1] == 31) & (len(onerow_data) == 9):  # composite

            parentID = onerow_data[3]
            com_gID = onerow_data[0]
            numEdge = onerow_data[4]
            k = k+1

            line_subserialnum = 0
            arc_subserialnum = 0

            for com_index in range(int(numEdge)):
                one_comdata = wholedata[k]

                if len(one_comdata) == 2:

                    com_line_xy = wholedata[k+1]  # composite的line(線段)
                    current_x = com_line_xy[0]
                    current_y = com_line_xy[1]
                    next_x = com_line_xy[2]
                    next_y = com_line_xy[3]
                    # distance  # x**2代表x的二次方
                    dis = math.sqrt((current_x - next_x)**2 +
                                    (current_y - next_y)**2)
                    # print(f'{current_x},{next_x},{current_y},{next_y},{dis}')
                    # degree

                    if (next_x != current_x):
                        # 用math.atan反三角正切取到角度值
                        deg = math.atan((next_y - current_y) /
                                        (next_x - current_x))
                        if deg < 0:
                            deg = deg + 2*math.pi  # tan的定義域在-0.5pi~0.5pi，而我想得到的是 0~2pi，剩餘的下面判別
                        elif (deg == 0) & ((current_x - next_x) > 0):
                            deg = math.pi

                    elif (next_y > current_y):  # 垂直，下個點在正上方
                        deg = math.pi/2
                    else:  # 垂直，下個點在正下方
                        deg = math.pi*3/2

                    line_subserialnum += 1
                    line_var.append(
                        [current_x, current_y, dis, deg, parentID, com_gID, line_subserialnum])

                    k = k+2

                elif (len(one_comdata) == 4):  # composite的arc

                    orientation = (one_comdata[2]*2-1)  # 將方向變成 1代表ccw, -1代表cw
                    # print(one_comdata[1])
                    com_arc_data = wholedata[k+1]
                    # print(com_arc_data)
                    current_x = com_arc_data[0]
                    current_y = com_arc_data[1]
                    cen_x = com_arc_data[2]
                    cen_y = com_arc_data[3]
                    radius = com_arc_data[6]
                    working_deg = com_arc_data[7]*math.pi/180

                    if (cen_x != current_x):
                        star_deg = math.atan(
                            (current_y - cen_y) / (current_x - cen_x))
                        if (current_y == cen_y):  # 起點在正x軸
                            if current_x > cen_x:
                                star_deg = 0
                            else:  # 起點在負x軸
                                star_deg = math.pi

                        elif (current_y > cen_y) & (star_deg < 0):  # 起點在第二象限
                            star_deg = star_deg + math.pi

                        elif (current_y < cen_y) & (star_deg > 0):  # 起點在第三象限
                            star_deg = star_deg + math.pi

                        elif (current_y < cen_y) & (star_deg < 0):  # 起點在第四象限
                            star_deg = star_deg + math.pi*2

                    elif (current_y > cen_y):  # 起點在正y軸
                        star_deg = math.pi/2
                    else:  # 起點在負y軸
                        star_deg = math.pi*3/2

                    arc_subserialnum += 1
                    arc_var.append([cen_x, cen_y, radius, star_deg, working_deg,
                                   orientation, parentID, com_gID, arc_subserialnum])

                    k = k+2
        else:
            k = k+1

    return line_var, rect_var, circle_var, arc_var, polygon_var

################ data_to_function end ##############

################# choose tool ##############


def ch_tool(degree, station, tool_shape, required_dim):
    # 選擇要用的刀具, tool_shape：選用刀型態, required_dim [1st dim, 2nd dim]
    # tool_shape 0 rectangle
    # tool_shape 1 square
    # tool_shape 2 round

    # degree 是弳度制
    a = -1
    b = 0       # 是否已經有找到刀的指標

    if (tool_shape == 1):  # square

        for k1 in range(len(station)):
            tool_deg = station[k1, 2]*math.pi/180
            if (required_dim[0] == 0) & (degree == tool_deg):  # "沒"有指定刀的尺寸
                tool_L = station[k1, 0]
                tool_W = station[k1, 1]
                if tool_L == tool_W:
                    a = k1
                    break
            else:  # 有指定刀的尺寸
                tool_L = station[k1, 0]
                tool_W = station[k1, 1]
                if (tool_L == tool_W) & (degree == tool_deg):
                    if tool_L == required_dim[0]:
                        a = k1
                        break

    elif (tool_shape == 2):  # round

        for k2 in range(len(station)):
            if required_dim[0] == 0:  # "沒"有指定刀的尺寸
                if (station[k2, 2] == -1) & (b == 0):
                    a = k2
                    b = 1
                elif (station[k2, 2] == -1) & (b == 1):  # 預設選半徑較大的刀
                    if station[k2, 0] > station[a, 0]:
                        a = k2
            else:  # 有指定刀的尺寸
                if (station[k2, 0] == required_dim[0]) & (station[k2, 2] == -1):
                    # print(k2)
                    a = k2
                    break
        if (a == -1):
            for k1 in range(len(station)):
                if (station[k1, 2] == -1) & (b == 0):
                    a = k1
                    b = 1
                elif (station[k1, 2] == -1) & (b == 1):  # 預設選半徑較大的刀
                    if station[k1, 0] > station[a, 0]:
                        a = k1
    else:   # = 0 # rectangle
        for k1 in range(len(station)):     # 找刀具庫中的所有刀
            tool_deg = station[k1, 2]*math.pi/180

            if (required_dim[0] == 0) & (required_dim[1] == 0):  # "沒"有指定刀的尺寸
                #print((degree==tool_deg) & (b==0))
                if (((degree == (tool_deg + math.pi)) | (degree == tool_deg)) & (b == 0)):
                    a = k1
                    b = 1
                    # print('abc')
                elif ((degree == (tool_deg + math.pi)) | (degree == tool_deg)) & (b == 1):
                    if station[k1, 0] > station[a, 0]:  # 如果有更適用的刀，就換過去
                        a = k1
                elif (k1 == (len(station)-1)):  # 如果沒有適合的方形刀，就用圓刀

                    for k2 in range(len(station)):
                        if (station[k2, 2] == -1) & (b == 0):
                            a = k2
                            b = 1
                        elif (station[k2, 2] == -1) & (b == 1):
                            if station[k2, 0] > station[a, 0]:
                                a = k2
                #print(f'{type(degree)}; {type(tool_deg)}')
                #print(f'{degree}; {tool_deg}; {required_dim}; {a}; {k1}; {b}; {tool_shape}')
            else:
                if (required_dim[0] != 0) & (required_dim[1] != 0):  # 有指定刀的長度 & 寬度
                    if ((degree == (tool_deg + math.pi)) | (degree == tool_deg)) & (station[k1, 0] == required_dim[0]) &\
                       (station[k1, 1] == required_dim[1]):
                        a = k1
                        break
                if (required_dim[0] != 0) & (required_dim[1] == 0):  # 有指定刀的長度
                    if ((degree == (tool_deg + math.pi)) | (degree == tool_deg)) & (station[k1, 0] == required_dim[0]):
                        a = k1
                        break
                if (required_dim[0] == 0) & (required_dim[1] != 0):  # 有指定刀的寬度
                    if ((degree == (tool_deg + math.pi)) | (degree == tool_deg)) & (station[k1, 1] == required_dim[1]):
                        a = k1
                        break
    return a

################# choose tool end ##########

################# tool expend ##############


def tool_expend(tool, tool_num):

    if tool[tool_num, 2] == -1:
        radius = tool[tool_num, 0]
        tool_trans = [radius, 0]
    else:
        theta = tool[tool_num, 2] * np.pi / 180  # 將角度轉為徑度制
        trans_array = np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        # 旋轉矩陣

        tool_graph = np.zeros([2, 4])  # 刀四個方位點
        x_offset = tool[tool_num, 0]/2
        y_offset = tool[tool_num, 1]/2

        tool_graph[0] = [-x_offset, x_offset, x_offset, -x_offset]
        tool_graph[1] = [-y_offset, -y_offset, y_offset, y_offset]
        tool_trans = np.matmul(trans_array, tool_graph)  # 乘上旋轉矩陣

    return tool_trans

################# tool expend end ##########

################# line #####################


def line(line_start_x, line_start_y, distance, line_deg, station, offset_index, line_serial_num, sub_serial_num, overlap):

    line_xy = []
    befortrans_line_xy = []
    hit_type = 0  # (33-水平垂直line hit)(34 line shear hit)(40 沿著線nib)
    ishole = 0
    if (distance < 10.5):
        tool_num = ch_tool(line_deg, station, 0, [distance, 0])
        #print(line_deg, distance, tool_num)
    else:
        tool_num = ch_tool(line_deg, station, 0, [0, 0])

    if (station[tool_num, 2] == -1):  # 圓刀nib ########
        r = station[tool_num, 0]
        a = distance  # + overlap    # overlap預計過切的長度
        one_step = r*0.5

        if offset_index == 0:  # 由右向"左"加工
            orient = -1

        else:  # 由左向"右"加工
            orient = 1

        x_offset = r * math.sin(line_deg)  # + (overlap/2) * math.cos(line_deg)
        # - (overlap/2) * math.sin(line_deg)
        y_offset = orient * r * math.cos(line_deg)

        hit_type = 40

        line_xy.append([line_start_x + x_offset, line_start_y + y_offset, tool_num,
                        hit_type, line_serial_num, sub_serial_num, ishole])

        while (a > 0):
            a_pre = a

            a = a - one_step  # 這次加工後剩餘的長度

            if a < 0:  # a剩餘長度最少為0
                a = 0

            last_line_xy = line_xy[len(line_xy)-1]
            line_x = last_line_xy[0] + one_step * \
                math.cos(line_deg)  # 記錄此時加工的點位
            line_y = last_line_xy[1] + one_step * math.sin(line_deg)

            line_xy.append([line_x, line_y, tool_num, hit_type,
                           line_serial_num, sub_serial_num, ishole])

    else:  # (line hit) or (line shear hit) 矩形刀 ########
        L_tool = station[tool_num, 0]
        W_tool = station[tool_num, 1]
        a = distance - (L_tool - 2 * overlap)

        if offset_index == 0:  # 由右向"左"加工
            orient = -1

        else:  # 由左向"右"加工
            orient = 1

        x_offset = (L_tool/2)-overlap
        y_offset = W_tool/2 * orient

        if ((station[tool_num, 2] == 0) | (station[tool_num, 2] == 90)):
            hit_type = 33
        else:
            hit_type = 34

        befortrans_line_xy.append([x_offset, y_offset])
        # 旋轉矩陣
        trans_array = np.array(
            [[np.cos(line_deg), -np.sin(line_deg)], [np.sin(line_deg), np.cos(line_deg)]])

        while (a > 0):  # 先以水平加工計算，再將點位剩上轉置矩陣
            a_pre = a
            a = a - (L_tool - 1)  # 這次加工後剩餘的長度

            if a < 0:  # a剩餘長度最少為0
                a = 0

            last_line_xy = befortrans_line_xy[len(befortrans_line_xy)-1]
            line_x = last_line_xy[0] + (a_pre - a)  # 記錄此時加工的點位
            line_y = last_line_xy[1]

            befortrans_line_xy.append([line_x, line_y])

        for g in range(len(befortrans_line_xy)):
            oneb_line_xy = befortrans_line_xy[g]
            line_trans_xy = np.array([[oneb_line_xy[0]], [oneb_line_xy[1]]])

            line_trans_xy = np.matmul(trans_array, line_trans_xy)
            line_x = (line_trans_xy[0][0]) + line_start_x
            line_y = (line_trans_xy[1][0]) + line_start_y

            line_xy.append([line_x, line_y, tool_num, hit_type,
                           line_serial_num, sub_serial_num, ishole])

    return line_xy

################# line end #################

################# circle ###################


def circle(r, start_deg, cen_x, cen_y, parentID, station, punch_type, cir_serial_num):

    tool_num = ch_tool(-1, station, 2, [r, 0])
    cir_xy = []

    if (parentID != 0):  # 除料範圍為圓內
        ishole = 1
        if r == station[tool_num, 0]:       # 刀具等於洞的大小時
            # punch_type先用17，模擬方便
            cir_xy.append([cen_x, cen_y, tool_num, 17,
                          cir_serial_num, 1, ishole])
            #cir_xy格式為 [x, y, 圓刀半徑, 打洞方式]
            # 圓刀打洞方式(16:single, 17:1_hit along a line, 39:nibbling-arc, 40:nibbling-line)

        elif r > tool[tool_num, 0]:     # nibbling hit

            r2 = r - tool[tool_num, 0]
            feeding_a = pitch / r2
            angle = 0
            while angle < (2*np.pi):
                x_point = math.cos(angle) * r2 + cen_x
                y_point = math.sin(angle) * r2 + cen_y
                cir_xy.append([x_point, y_point, tool_num,
                              39, cir_serial_num, 1, ishole])
                angle += feeding_a

    elif (parentID == 0):  # 除料範圍為圓外 # nibbling hit
        ishole = 0
        r2 = r + station[tool_num, 0]
        angle = 0
        s_deg = (start_deg*np.pi)/180

        while angle < (2*np.pi):
            if (station[tool_num, 0] >= 10):
                pitch = random.uniform(3, 5)
            else:
                pitch = 1 * random.uniform(0.90, 1.10)  # random.randint(1, 2)
            feeding_a = pitch / r2

            x_point = math.cos(angle + s_deg) * r2 + cen_x
            y_point = math.sin(angle + s_deg) * r2 + cen_y
            cir_xy.append([x_point, y_point, tool_num,
                          39, cir_serial_num, 1, ishole])
            angle += feeding_a

    return cir_xy

################# circle end ###############

################# arc ###################


def arc(cen_x, cen_y, r, s_deg, working_deg, orientation, parentID, station, line_serial_num, sub_serial_num):
    if r < 30:
        tool_num = ch_tool(-1, station, 2, [2.5, 0])  # choose small tool
    else:
        tool_num = ch_tool(-1, station, 2, [0, 0])  # choose large tool
    arc_xy = []
    nib_hit_arc = 0
    ishole = 0
    # print(cen_x, cen_y, tool_num, parentID, station[tool_num, 0], s_deg, working_deg, orientation)
    if (parentID == 0) & (orientation == 1):  # 除料範圍為圓外 # nibbling hit
        r2 = r + station[tool_num, 0]
    elif (parentID == 0) & (orientation == -1):
        r2 = r - station[tool_num, 0]

    angle = 0

    while angle < abs(working_deg):
        if (station[tool_num, 0] >= 10):
            pitch = random.uniform(3, 5)
        else:
            pitch = 1 * random.uniform(0.90, 1.10)  # random.randint(1, 2)
        feeding_a = pitch / r2

        x_point = math.cos(angle*orientation + s_deg) * r2 + cen_x
        y_point = math.sin(angle*orientation + s_deg) * r2 + cen_y
        arc_xy.append([x_point, y_point, tool_num, 39, line_serial_num,
                      sub_serial_num, ishole])  # arc的punch type 只會是39
        nib_hit_arc += 1
        angle += feeding_a

    return arc_xy, nib_hit_arc

################# arc end ###############

############### hole array rotate ###############


def xy_data_rotate(befor_rota_xy, sp2, degree):
    ##  input(洞的所有點位資訊, 旋轉點, 旋轉角度)
    # 角度為徑度制

    af_rota_xy = []

    trans_array = np.array(
        [[np.cos(degree), -np.sin(degree)], [np.sin(degree), np.cos(degree)]])
    # 旋轉矩陣

    pts_num = len(befor_rota_xy)

    for k1 in range(pts_num):  # 將每一點都乘上旋轉矩陣，再加上第一個洞的原點

        k1_xy = befor_rota_xy[k1]
        x_pre = k1_xy[0] - sp2[0]
        y_pre = k1_xy[1] - sp2[1]
        tool_num = k1_xy[2]
        punch_type = k1_xy[3]
        rect_serial_num = k1_xy[4]
        rect_subserial_num = k1_xy[5]
        ishole = k1_xy[6]

        xy_pre = np.array([[x_pre], [y_pre]])  # 取單點的座標(x,y)
        xy_trans = np.matmul(trans_array, xy_pre)  # 乘上旋轉矩陣

        x_abs = xy_trans[0, 0] + sp2[0]   # X 轉置後，加上原點座標，變成絕對座標
        y_abs = xy_trans[1, 0] + sp2[1]   # Y 轉置後，加上原點座標，變成絕對座標

        af_rota_xy.append([x_abs, y_abs, tool_num, punch_type,
                          rect_serial_num, rect_subserial_num, ishole])
        # 將點位記錄在 xy_data 內

    return af_rota_xy

############## hole array rotate end ############

################ rect hole #################


def rect_hole(L, H, sp1, punch_type, station, hole_roDeg, rect_serial_num, rect_subserial_num):  # 做法為：以單一矩形洞做全孔加工，剩下的陣列洞另外處理

    hole_xy_data = []
    ishole = 1

    # ch_tool 3rd parameter:
    # tool_shape 0 rectangle
    # tool_shape 1 square
    # tool_shape 2 round

    if punch_type == 18:  # grid
        tool_num = ch_tool(roDeg, station, 0, [L, H])  # 選到適用的刀
        # 第三個參數"1"表示要選"正方形"刀

    else:
        if roDeg == 0:    # along 4 sides of a rectangle
            punch_type = 33
        else:           # 1 tool along a line (shear)
            punch_type = 34

        tool_num = ch_tool(hole_roDeg, station, 1, [0, 0])  # 先選方刀

        if tool_num == -1:
            tool_num = ch_tool(hole_roDeg, station, 0, [0, 0])  # 沒有適合方刀,再選長方刀

    L_tool = station[tool_num, 0]
    w_tool = station[tool_num, 1]

    b = H - w_tool  # 洞內高度所要走的行程只有 H - w_tool
    c = 1  # 一個橫加工時的指標
    d = 0  # 垂直向的一個指標，用於垂直移動剛好讓剩餘長度為0時用

    hole_xy = []      # 記錄洞內衝孔時的點位，洞口左上為暫時原點(0,0)

    if (L == L_tool) & (H == w_tool):  # single hit

        hole_xy.append([L_tool/2, H-w_tool/2, tool_num, punch_type, rect_serial_num,
                        rect_subserial_num, ishole])

    else:
        hole_xy.append([L_tool/2, H-w_tool/2, tool_num, punch_type, rect_serial_num,
                        rect_subserial_num, ishole])  # 第一點位置，記錄點的型式為[x, y , 刀編號]

        while True:  # 以橫向加工到底後垂直移動一些，再繼續橫向加工(b>0)

            a = L - L_tool  # 洞內水平長度所要走的行程只有 L - L_tool

            while a > 0:

                a_pre = a  # 記錄前一次加工程剩餘的長度(水平維度)
                a = a - (L_tool - 1)  # 這次加工後剩餘的長度

                if a < 0:  # a剩餘長度最少為0
                    a = 0

                last_hole_xy = hole_xy[len(hole_xy)-1]
                x_hole = last_hole_xy[0] + c * (a_pre - a)  # 記錄此時加工的點位
                y_hole = last_hole_xy[1]
                hole_xy.append([x_hole, y_hole, tool_num, punch_type, rect_serial_num,
                                rect_subserial_num, ishole])  # 將點位記錄在hole_xy內

            c = c*-1

            if d == 1:  # 已經在垂直剩餘長度為 0 加工完橫軸了
                # print('break')
                break

            b_pre = b  # 記錄前一次加工程剩餘的長度(垂直維度)
            b = b - (w_tool - 1)  # 這次加工後剩餘的長度
            if b < 0:  # b剩餘長度最少為0
                b = 0

            if (b == 0) & (d == 0):  # 第一次移動到讓剩餘量為0，讓指標為1
                d = 1

            last_hole_xy = hole_xy[len(hole_xy)-1]
            x_hole = last_hole_xy[0]
            y_hole = last_hole_xy[1] - (b_pre - b)  # 記錄此時加工的點位

            hole_xy.append([x_hole, y_hole, tool_num, punch_type, rect_serial_num,
                            rect_subserial_num, ishole])

    trans_array = np.array(
        [[np.cos(hole_roDeg), -np.sin(hole_roDeg)], [np.sin(hole_roDeg), np.cos(hole_roDeg)]])
    # 旋轉矩陣

    all_hole_hit = len(hole_xy)

    for k1 in range(all_hole_hit):  # 將每一點都乘上旋轉矩陣，再加上第一個洞的原點

        k1_xy = hole_xy[k1]
        x_pre = k1_xy[0]
        y_pre = k1_xy[1]
        tool_num = k1_xy[2]
        punch_type = k1_xy[3]
        rect_serial_num = k1_xy[4]
        rect_subserial_num = k1_xy[5]
        ishole = k1_xy[6]
        xy_pre = np.array([[x_pre], [y_pre]])  # 取單點的座標(x,y)
        xy_trans = np.matmul(trans_array, xy_pre)  # 乘上旋轉矩陣

        x_abs = xy_trans[0, 0] + sp1[0]   # X 轉置後，加上原點座標，變成絕對座標
        y_abs = xy_trans[1, 0] + sp1[1]   # Y 轉置後，加上原點座標，變成絕對座標

        hole_xy_data.append([x_abs, y_abs, tool_num, punch_type, rect_serial_num,
                             rect_subserial_num, ishole])  # 將點位記錄在 xy_data 內

    # if hole_roDeg!=0:    ## 加入旋轉
    #     hole_xy_data = xy_data_rotate(hole_xy_data, sp1, roDeg)
        # rotate  (befor_rota_xy, fixed point, degree)

    return hole_xy_data

################ rect hole end #############

############## outside edge ################


def rect_outside_edge(L, H, sp1, station, roDeg, rect_serial_num):  # 做矩形外圍的加工 ## roDeg是弳度制

    rect_xy = []
    rect_punch_type = 33
    ishole = 0

    # 橫向
    tool_num = ch_tool(roDeg, station, 0, [0, 0])  # 取刀具的資料
    L_tool = station[tool_num, 0]
    w_tool = station[tool_num, 1]

    x_start = sp1[0] + (L_tool/2 - 1)  # 啟始點
    y_start = sp1[1] + H + w_tool/2

    rect_xy.append([x_start, y_start, tool_num, rect_punch_type,
                   rect_serial_num, 1, ishole])  # 外邊緣開始工作的第一點

    hpm_out = x_start  # outside part horizontal part move
    vpm_out = y_start  # outside part vertical part move

    c = -1  # y方向加工係數
    d = 1  # x方向加工係數

    for k1 in range(2):

        a = L - (L_tool-2)

        while a > 0:
            a_pre = a  # 記錄前一次加工後剩餘的長度
            a = a - (L_tool - 1)  # 這次加工後剩餘的長度

            if a < 0:  # a剩餘長度最少為0
                a = 0

            last_xy_data = rect_xy[(len(rect_xy)-1)]
            x_out = last_xy_data[0] + (a_pre - a) * d  # 記錄此時加工的點位
            # 1.由左下加工到右下   ## 2.由右上加工到左上
            y_out = last_xy_data[1]

            # k1+1 視為sub serial num 在取特徵時用到，sub serial num 範圍是 1 ~ 4
            rect_xy.append(
                [x_out, y_out, tool_num, rect_punch_type, rect_serial_num, k1+1, ishole])

        last_xy_data = rect_xy[(len(rect_xy)-1)]
        x_out = last_xy_data[0]
        y_out = last_xy_data[1] + (H + w_tool) * c  # 右下結束第一條線加工，轉到右上準備開始第二條線加工
        c = c * -1
        d = d * -1

        rect_xy.append([x_out, y_out, tool_num, rect_punch_type,
                       rect_serial_num, 2, ishole])

    # 直向
    line_deg = roDeg + 90 * math.pi / 180
    tool_num = ch_tool(line_deg, station, 0, [0, 0])  # 取刀具的資料
    L_tool = station[tool_num, 0]
    w_tool = station[tool_num, 1]

    x_start = sp1[0] - (w_tool/2)  # 啟始點
    y_start = sp1[1] - (L_tool/2 - 1) + H

    rect_xy.append([x_start, y_start, tool_num, rect_punch_type,
                   rect_serial_num, 3, ishole])  # 外邊緣開始工作的第一點

    hpm_out = hpm_out + x_start  # outside part horizontal part move
    vpm_out = vpm_out + y_start  # outside part vertical part move

    c = 1  # 加工方向係數
    d = -1

    for k1 in range(2):

        b = H - (L_tool-2)

        while b > 0:
            b_pre = b  # 記錄前一次加工後剩餘的長度
            b = b - (L_tool - 1)  # 這次加工後剩餘的長度

            if b < 0:  # a剩餘長度最少為0
                b = 0

            last_xy_data = rect_xy[(len(rect_xy)-1)]
            x_out = last_xy_data[0]  # 記錄此時加工的點位
            y_out = last_xy_data[1] + (b_pre - b) * d

            rect_xy.append(
                [x_out, y_out, tool_num, rect_punch_type, rect_serial_num, k1+3, ishole])

        last_xy_data = rect_xy[(len(rect_xy)-1)]
        x_out = last_xy_data[0] + (L + w_tool) * c
        y_out = last_xy_data[1]
        c = c * -1
        d = d * -1

        rect_xy.append([x_out, y_out, tool_num, rect_punch_type,
                       rect_serial_num, 4, ishole])
        # 34為衝孔型式 punching with 1 tool along a line

    if roDeg != 0:  # 加入旋轉
        rect_xy = xy_data_rotate(rect_xy, sp1, roDeg)
        # rotate  (befor_rota_xy, fixed point, degree)

    return rect_xy

############ outside edge end ##############

################ polygon hole (Octagon) #################


def Octagon_hole(Octagon_pts, station, gID, parentID):
    Octagon_pts = np.array(Octagon_pts)
    # print(Octagon_pts)
    H1 = Octagon_pts[2, 1] - Octagon_pts[0, 1]  # 把八角形分三段高
    H2 = Octagon_pts[3, 1] - Octagon_pts[2, 1]
    H3 = Octagon_pts[4, 1] - Octagon_pts[3, 1]
    D1 = Octagon_pts[0, 0] - Octagon_pts[7, 0]  # 把水平也分段
    D2 = Octagon_pts[1, 0] - Octagon_pts[0, 0]
    D3 = Octagon_pts[2, 0] - Octagon_pts[1, 0]
    # print(H1, H2, H3)
    slope1 = -D1 / H1
    slope2 = D3 / H1
    slope3 = D1 / H3
    slope4 = -D3 / H3

    hole_xy = []
    ishole = 2  # priority
    H = 0
    L = 0

    # 1st section
    poly_subserial_num = 1
    punch_type = 33         # along 4 sides of a rectangle
    tool_num = ch_tool(0, station, 0, [0, 0])  # 選長方形刀
    L_tool = station[tool_num, 0]
    w_tool = station[tool_num, 1]

    hole_xy.append([Octagon_pts[0, 0] + L_tool/2, Octagon_pts[0, 1] + w_tool/2, tool_num, punch_type, gID,
                    poly_subserial_num, ishole])

    b = H1 - w_tool  # 第一階段加工
    c = 1  # 水平加工的方向指標
    d = 0  # 移動到 H1 剩餘量為0 的指標
    while True:
        a = (D2 - L_tool) - (H1-b-w_tool) * \
            slope1 + (H1-b-w_tool)*slope2    # 水平行程

        while a > 0:
            e = 0
            a_pre = a  # 記錄前一次加工程剩餘的長度(水平維度)
            a = a - (L_tool - 1)  # 這次加工後剩餘的長度

            last_hole_xy = hole_xy[len(hole_xy)-1]

            if (a < 0) & (last_hole_xy[1] == (Octagon_pts[0, 1] + w_tool/2)):  # a剩餘長度最少為0
                a = 0
            elif a < 2:
                a = 2
                e = 1

            x_hole = last_hole_xy[0] + c * (a_pre - a)  # 記錄此時加工的點位
            y_hole = last_hole_xy[1]
            hole_xy.append([x_hole, y_hole, tool_num, punch_type, gID,
                            poly_subserial_num, ishole])  # 將點位記錄在hole_xy內
            if e == 1:
                a = 0
        c = c*-1

        if d == 1:  # 已經在垂直剩餘長度為 0 加工完橫軸了
            # print('break')
            break

            # break while

        b_pre = b  # 記錄前一次加工程剩餘的長度(垂直維度)
        b = b - (w_tool - 1)  # 這次加工後剩餘的長度
        if b < -1:  # b剩餘長度最少為01
            b = -1
            d = 1

        last_hole_xy = hole_xy[len(hole_xy)-1]
        if (last_hole_xy[1] == Octagon_pts[0, 1] + w_tool/2):
            if c == -1:
                x_hole = last_hole_xy[0] + (b_pre - b)*slope2 - 1
            else:
                x_hole = last_hole_xy[0] + (b_pre - b)*slope1 + 1
        else:
            if c == -1:
                x_hole = last_hole_xy[0] + (b_pre - b)*slope2
            else:
                x_hole = last_hole_xy[0] + (b_pre - b)*slope1
        y_hole = last_hole_xy[1] + (b_pre - b)  # 記錄此時加工的點位

        hole_xy.append([x_hole, y_hole, tool_num, punch_type, rect_serial_num,
                        rect_subserial_num, ishole])

    # 2nd section
    if c == -1:
        x_hole = Octagon_pts[2, 0] - L_tool/2
    else:
        x_hole = Octagon_pts[7, 0] + L_tool/2
    y_hole = H1 + Octagon_pts[0, 1] + w_tool/2

    hole_xy.append([x_hole, y_hole, tool_num, punch_type, gID,
                    poly_subserial_num, ishole])
    b = H2 - w_tool  # 第二階段加工
    d = 0
    while True:
        a = D1 + D2 + D3 - L_tool   # 水平行程

        while a > 0:
            a_pre = a  # 記錄前一次加工程剩餘的長度(水平維度)
            a = a - (L_tool - 1)  # 這次加工後剩餘的長度

            last_hole_xy = hole_xy[len(hole_xy)-1]

            if (a < 0):  # a剩餘長度最少為0
                a = 0
            x_hole = last_hole_xy[0] + c * (a_pre - a)  # 記錄此時加工的點位
            y_hole = last_hole_xy[1]
            hole_xy.append([x_hole, y_hole, tool_num, punch_type, gID,
                            poly_subserial_num, ishole])  # 將點位記錄在hole_xy內
        c = c*-1

        if d == 1:  # 已經在垂直剩餘長度為 0 加工完橫軸了
            # print('break')
            break

            # break while

        b_pre = b  # 記錄前一次加工程剩餘的長度(垂直維度)
        b = b - (w_tool - 1)  # 這次加工後剩餘的長度
        if b < 0:  # b剩餘長度最少為01
            b = 0
        if (b == 0) & (d == 0):
            d = 1

        last_hole_xy = hole_xy[len(hole_xy)-1]
        x_hole = last_hole_xy[0]
        y_hole = last_hole_xy[1] + (b_pre - b)  # 記錄此時加工的點位

        hole_xy.append([x_hole, y_hole, tool_num, punch_type, rect_serial_num,
                        rect_subserial_num, ishole])

    # 3rd section
    last_hole_xy = hole_xy[len(hole_xy)-1]
    if c == -1:
        x_hole = Octagon_pts[2, 0] - L_tool/2 + 3*slope4 - 1
    else:
        x_hole = Octagon_pts[7, 0] + L_tool/2 + 3*slope3 + 1
    y_hole = H1 + H2 + Octagon_pts[0, 1] + w_tool/2 - 1

    hole_xy.append([x_hole, y_hole, tool_num, punch_type, gID,
                    poly_subserial_num, ishole])

    b = H3 - w_tool + 1  # 第 3 階段加工
    d = 0  # 移動到 H1 剩餘量為0 的指標
    while True:
        a = (D2 - L_tool) + b*slope3 - b*slope4    # 水平行程

        while a > 0:
            e = 0
            a_pre = a  # 記錄前一次加工程剩餘的長度(水平維度)
            a = a - (L_tool - 1)  # 這次加工後剩餘的長度

            last_hole_xy = hole_xy[len(hole_xy)-1]

            if (a < 0) & (last_hole_xy[1] == (Octagon_pts[4, 1] - w_tool/2)):  # a剩餘長度最少為0
                a = 0
            elif a < 2:
                a = 2
                e = 1

            x_hole = last_hole_xy[0] + c * (a_pre - a)  # 記錄此時加工的點位
            y_hole = last_hole_xy[1]
            hole_xy.append([x_hole, y_hole, tool_num, punch_type, gID,
                            poly_subserial_num, ishole])  # 將點位記錄在hole_xy內
            if e == 1:
                a = 0
        c = c*-1

        if d == 1:  # 已經在垂直剩餘長度為 0 加工完橫軸了
            # print('break')
            break

            # break while

        b_pre = b  # 記錄前一次加工程剩餘的長度(垂直維度)
        b = b - (w_tool - 1)  # 這次加工後剩餘的長度
        if b < 0:  # b剩餘長度最少為0
            b = 0
            d = 1

        last_hole_xy = hole_xy[len(hole_xy)-1]
        y_hole = last_hole_xy[1] + (b_pre - b)  # 記錄此時加工的點位
        if (y_hole == Octagon_pts[4, 1] - w_tool/2):
            if c == -1:
                x_hole = Octagon_pts[4, 0] - L_tool/2
            else:
                x_hole = Octagon_pts[5, 0] + L_tool/2
        else:
            if c == -1:
                x_hole = last_hole_xy[0] + (b_pre - b)*slope4
            else:
                x_hole = last_hole_xy[0] + (b_pre - b)*slope3

        hole_xy.append([x_hole, y_hole, tool_num, punch_type, rect_serial_num,
                        rect_subserial_num, ishole])

    # 4th section
    # line 1
    edge_deg = 135 * math.pi / 180
    distance = math.sqrt(
        (Octagon_pts[7, 0]-Octagon_pts[0, 0])**2 + (Octagon_pts[7, 1]-Octagon_pts[0, 1])**2)
    overlap = 0
    offset_index = 0  # 由右向"左"加工
    edge_xy = line(Octagon_pts[0, 0], Octagon_pts[0, 1], distance, edge_deg, station, offset_index,
                   gID, 2, overlap)  # sub_serial_num : 2
    for ix in edge_xy:
        ix[6] = 1
        hole_xy.append(ix)

    # line 2
    edge_deg = 45 * math.pi / 180
    distance = math.sqrt(
        (Octagon_pts[1, 0]-Octagon_pts[2, 0])**2 + (Octagon_pts[1, 1]-Octagon_pts[2, 1])**2)
    overlap = 0
    offset_index = 1  # 由左向"右"加工
    edge_xy = line(Octagon_pts[1, 0], Octagon_pts[1, 1], distance, edge_deg, station, offset_index,
                   gID, 2, overlap)
    for ix in edge_xy:
        ix[6] = 1
        hole_xy.append(ix)

    # line 3
    edge_deg = 135 * math.pi / 180
    distance = math.sqrt(
        (Octagon_pts[3, 0]-Octagon_pts[4, 0])**2 + (Octagon_pts[3, 1]-Octagon_pts[4, 1])**2)
    overlap = 0
    offset_index = 1  # 由左向"右"加工
    edge_xy = line(Octagon_pts[3, 0], Octagon_pts[3, 1], distance, edge_deg, station, offset_index,
                   gID, 2, overlap)
    for ix in edge_xy:
        ix[6] = 1
        hole_xy.append(ix)

    # line 4
    edge_deg = 45 * math.pi / 180
    distance = math.sqrt(
        (Octagon_pts[6, 0]-Octagon_pts[5, 0])**2 + (Octagon_pts[6, 1]-Octagon_pts[5, 1])**2)
    overlap = 0
    offset_index = 0  # 由右向"左"加工
    edge_xy = line(Octagon_pts[6, 0], Octagon_pts[6, 1], distance, edge_deg, station, offset_index,
                   gID, 2, overlap)
    for ix in edge_xy:
        ix[6] = 1   # is hole
        hole_xy.append(ix)
    # line(line_start_x, line_start_y, distance, line_deg, tool, offset_index, line_serial_num, sub_serial_num)
    # line_xy.append([line_x, line_y, tool_num, hit_type, line_serial_num, sub_serial_num, ishole])
    return hole_xy

################ polygon hole (Octagon) end #############

################### graph ######################


def graph(xy_data, station):

    graph_data = []

    for j in range(len(wholedata)):
        graph_data.append(wholedata[j])

    '''
    graph_data = []
    graph_data.append(["; SYSCONFIG"])
    graph_data.append([";version", "unit flag", "draw speed"])
    graph_data.append([";2.1", "0(mks) 1(fbs)", "(%)"])
    graph_data.append([201, 0, 20, 0, 0, 0, 0, 0, 0, 0,])
    graph_data.append([";"])
    graph_data.append(["; SYS INT DATA"])
    graph_data.append([";nibble", "nibble", "rect", "shear", "hit1", "hit2", "hit3", "not used"])
    graph_data.append([";arc", "line", "4side", "line", "one", "2nd", "3rd"])
    graph_data.append([10, 10, 20, 40, 20, 15, 15, 0, 0, 0])
    graph_data.append([";form", "form", "form", "form", "not used"])
    graph_data.append([";1", "2", "3", "4"])
    graph_data.append([10, 10, 10, 10, 0, 0, 0, 0, 0, 0])
    graph_data.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    graph_data.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    graph_data.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    graph_data.append([";"])
    graph_data.append(["; SYS DBL DATA"])
    graph_data.append([";Vx m/s", "Vy m/s", "Ax m/s2", "Ay m/s2"])
    graph_data.append([8, 10, 0.2, 0.3])
    graph_data.append([";not used"])
    graph_data.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    graph_data.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    graph_data.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #gID, gType, loopID
    graph_data.append([";gID", "gType", "loopID"])
    graph_data.append([0, 0, 0])
    graph_data.append([";table off(x", "y)", "sheet size(x", "y)", "start(edge", "par)", "end(edge", "par)", "thickness"])
    graph_data.append([0, 0, 1200, 800, 4, 0.95, 2, 0.2, 0.062])
    '''

    num = len(xy_data)  # 刀具總共停留在多少個地方
    k3 = 10000
    # k4 = 100000
    for k1 in range(num):

        single_p = xy_data[k1]
        tool_num = single_p[2]
        single_p_gra = []

        if station[tool_num, 2] == -1:  # 圓刀
            if single_p[3] == 17:
                R = station[tool_num, 0]  # single
            else:
                R = station[tool_num, 0]

            #graph_data.append([";gID", "gType", "iUserSetID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF"])
            graph_data.append([k3, 32, k3, 0, 1, 36, 0, single_p[3], 1])
            k3 += 1
            single_p_gra = [R, 0, single_p[0], single_p[1]]

        else:  # 方刀

            punch_type = single_p[3]
            #graph_data.append([";gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF"])
            graph_data.append([k3, 30, k3, 0, 0, 0, punch_type, 1])
            k3 += 1
            tool_trans = tool_expend(station, tool_num)

            for k2 in range(4):

                gra_x_point = single_p[0] + tool_trans[0][k2]
                gra_y_point = single_p[1] + tool_trans[1][k2]
                single_p_gra.append(gra_x_point)
                single_p_gra.append(gra_y_point)

        graph_data.append(single_p_gra)

    return graph_data

################## graph end ###################

################## punch_time #######################


def punch_time(punch_type, tool_num):

    # 0: single hit             5%
    # 1: nibbling_hit           5%
    # 2: horizontal_line_hit    10%
    # 3: vertical_line_hit      10%
    # 4: shear_hit              10%
    # 5: turret rotate 90 deg   5%

    # station[0, :] = [20, 4,  0]  20%
    # station[1, :] = [20, 4, 90]  20%
    # station[2, :] = [10, 2, 30]  10%
    # station[3, :] = [10, 2, 45]  10%
    # station[4, :] = [10, 2, 60]  10%
    # station[5, :] = [10, 2, 120] 10%
    # station[6, :] = [10, 2, 135] 10%
    # station[7, :] = [10, 2, 150] 10%
    # station[8, :] = [10, 10, 0]  20%
    # station[9, :] = [1.5, 0, -1]   5%
    # station[10, :] = [2.5, 0, -1]  5%
    # station[11, :] = [10, 0, -1]  20%
    # station[12, :] = [10, 10, 45] 20%

    if punch_type == 0:
        random_num = random.uniform(0.95, 1.05)
        using_time = random_num * 0.02

    elif punch_type == 1:
        random_num = random.uniform(0.95, 1.05)
        using_time = random_num * 0.01

    elif punch_type == 2:
        random_num = random.uniform(0.90, 1.10)
        using_time = random_num * 0.02

    elif punch_type == 3:
        random_num = random.uniform(0.90, 1.10)
        using_time = random_num * 0.02

    elif punch_type == 4:
        random_num = random.uniform(0.90, 1.10)
        using_time = random_num * 0.04

    elif punch_type == 5:
        random_num = random.uniform(0.95, 1.05)
        using_time = random_num * 0.5
    # print(f'punch type : {punch_type}; time : {using_time}')

    if (tool_num == 0) | (tool_num == 1) | (tool_num == 8) | (tool_num == 11) | (tool_num == 12):
        random_num = random.uniform(0.8, 1.2)  # 20%
        using_time = using_time * random_num

    elif (tool_num == 2) | (tool_num == 3) | (tool_num == 4) | (tool_num == 5) | (tool_num == 6) | (tool_num == 7):
        random_num = random.uniform(0.9, 1.1)  # 10%
        using_time = using_time * random_num

    elif (tool_num == 9) | (tool_num == 10):
        random_num = random.uniform(0.95, 1.05)  # 5%
        using_time = using_time * random_num

    return using_time

################## punch_time end ###################

################## moving_time #######################


def moving_time(moving_type, movement):

    # 0: horizontal_part_move               20%
    # 1: vertical_part_move                 20%
    # 2: horizontal_tool_in_btwn_move       10%
    # 3: vertical_tool_in_btwn_move         10%
    # 4: horizontal_tool_shear_in_btwn_move 10%
    # 5: vertical_tool_shear_in_btwn_move   10%

    # nibbling time no need to count

    random_num = random.uniform(0.85, 1.15)
    Vx_max = 8  # m/s
    Vy_max = 10  # m/s
    Ax = 20     # m/s^2
    Ay = 30     # m/s^2

    reach_Vx_max_dis = 2 * (Vx_max / Ax) * Vx_max / 2
    reach_Vy_max_dis = 2 * (Vy_max / Ay) * Vy_max / 2
    movement = movement / 1000

    if moving_type == 0:        # 0: horizontal_part_move (20%)
        t = 0.0
        if movement > reach_Vx_max_dis:
            t = (2 * Vx_max / Ax) + (movement - reach_Vx_max_dis) / Vx_max
        else:
            t = 2 * pow(movement/Ax, 0.5)
        random_num = random.uniform(0.80, 1.20)
        using_time = random_num * t

    elif moving_type == 1:      # 1: vertical_part_move  (20%)
        t = 0.0
        if movement > reach_Vx_max_dis:
            t = (2 * Vy_max / Ay) + (movement - reach_Vy_max_dis) / Vy_max
        else:
            t = 2 * pow(movement/Ay, 0.5)
        random_num = random.uniform(0.80, 1.20)
        using_time = random_num * t

    elif moving_type == 2:      # 2: horizontal_tool_in_btwn_move  (10%)
        t = 2 * pow(movement/Ax, 0.5)
        random_num = random.uniform(0.90, 1.10)
        using_time = random_num * t

    elif moving_type == 3:      # 3: vertical_tool_in_btwn_move  (10%)
        t = 2 * pow(movement/Ay, 0.5)
        random_num = random.uniform(0.90, 1.10)
        using_time = random_num * t

    elif moving_type == 4:      # 4: horizontal_tool_shear_in_btwn_move (10%)
        t = 2 * pow(movement/Ax, 0.5)
        random_num = random.uniform(0.90, 1.10)
        using_time = random_num * t

    elif moving_type == 5:      # 5: vertical_tool_shear_in_btwn_move  (10%)
        t = 2 * pow(movement/Ay, 0.5)
        random_num = random.uniform(0.90, 1.10)
        using_time = random_num * t
    #print(f'move type : {moving_type}; movement: {movement}; time : {using_time}')
    return using_time

################## moving_time end ###################

################## feature_calc #######################


def feature_calc(xy_data, path):
    time1 = 0  # record punch time
    time2 = 0  # record moving time

    single_hit = 0
    nibbling_hit = 0
    horizontal_line_hit = 0
    vertical_line_hit = 0
    shear_hit = 0
    turret_tool_change = 0  # (deg)

    horizontal_part_move = 0
    vertical_part_move = 0
    horizontal_tool_in_btwn_move = 0
    vertical_tool_in_btwn_move = 0
    horizontal_tool_shear_in_btwn_move = 0
    vertical_tool_shear_in_btwn_move = 0

    Ax = 20
    Ay = 30

    feature_data = []
    '''
    feature_data.append([" ","horizontal line hit","vertical line hit","single hit","nibbling hit",
             "shear hit","horizontal part move","vertical part move","horizontal tool in-btwn move",
             "vertical tool in-btwn move","horizontal tool shear in-btwn move",
             "vertical tool shear in-btwn move","turret tool change deg", "total time"
             ])
    '''
    pre_pt = [0, 0, 0, 0, 0, 0]
    for ix in range(len(xy_data)):

        ## [x, y, tool_num, hit_type, serial_num, sub_serial_num]
        one_xy_data = xy_data[ix]
        tool_num = one_xy_data[2]
        x_move = abs(one_xy_data[0] - pre_pt[0])  # x向移動
        y_move = abs(one_xy_data[1] - pre_pt[1])  # y向移動

        if (ix < (len(xy_data) - 1)):  # 取下把刀資訊
            next_xy_data = xy_data[ix+1]
        # print(pre_pt)
        # print(one_xy_data)

        if pre_pt[4] != one_xy_data[4]:  # 同把刀換新線段

            # move
            if ((x_move * Ay/Ax) >= y_move):  # time
                time2 += moving_time(0, x_move)
                horizontal_part_move += x_move
            else:
                time2 += moving_time(1, y_move)
                vertical_part_move += y_move

            # punch
            if one_xy_data[3] == 16:  # 16-> single hit
                single_hit += 1
                time1 += punch_time(0, tool_num)

            elif one_xy_data[3] == 17:  # 17-> along a line hit
                single_hit += 1
                time1 += punch_time(0, tool_num)

            elif one_xy_data[3] == 18:  # 18-> grid
                single_hit += 1
                time1 += punch_time(0, tool_num)

            elif one_xy_data[3] == 20:  # 20-> arc
                nibbling_hit += 1
                time1 += punch_time(1, tool_num)

            elif one_xy_data[3] == 33:  # 33-> along 4 sides using a square tool
                if next_xy_data[0] == one_xy_data[0]:  # 打垂直方向時
                    vertical_line_hit += 1
                    time1 += punch_time(3, tool_num)

                elif next_xy_data[1] == one_xy_data[1]:  # 打水平方向時
                    horizontal_line_hit += 1
                    time1 += punch_time(2, tool_num)

            elif one_xy_data[3] == 34:  # 34-> along a line (shear)
                if one_xy_data[2] == -1:  # round tool
                    nibbling_hit += 1
                    time1 += punch_time(1, tool_num)
                else:       # rect tool
                    shear_hit += 1
                    time1 += punch_time(4, tool_num)

            elif one_xy_data[3] == 39:  # 39-> arc
                nibbling_hit += 1
                time1 += punch_time(1, tool_num)

        else:  # 同把刀、同線段，持續加工
            if one_xy_data[3] == 16:  # 16-> single hit
                single_hit += 1
                time1 += punch_time(0, tool_num)

                if ((x_move * Ay / Ax) >= y_move):  # time
                    time2 += moving_time(0, x_move)
                    horizontal_part_move += x_move
                else:
                    time2 += moving_time(1, y_move)
                    vertical_part_move += y_move

            elif one_xy_data[3] == 17:  # 17-> along a line hit
                single_hit += 1
                time1 += punch_time(0, tool_num)

                if ((x_move * Ay / Ax) >= y_move):  # time
                    time2 += moving_time(0, x_move)
                    horizontal_part_move += x_move
                else:
                    time2 += moving_time(1, y_move)
                    vertical_part_move += y_move

            elif one_xy_data[3] == 18:  # 18-> grid
                single_hit += 1
                time1 += punch_time(0, tool_num)

                if ((x_move * Ay / Ax) >= y_move):  # time
                    time2 += moving_time(0, x_move)
                    horizontal_part_move += x_move
                else:
                    time2 += moving_time(1, y_move)
                    vertical_part_move += y_move

            elif one_xy_data[3] == 20:  # arc
                nibbling_hit += 1
                time1 += punch_time(1, tool_num)

            elif one_xy_data[3] == 33:  # along 4 sides using a square tool
                if x_move == 0:  # 打垂直方向時
                    vertical_line_hit += 1
                    time1 += punch_time(3, tool_num)

                    vertical_tool_in_btwn_move += y_move
                    time2 += moving_time(3, y_move)

                elif y_move == 0:  # 打水平方向時
                    horizontal_line_hit += 1
                    time1 += punch_time(2, tool_num)

                    horizontal_tool_in_btwn_move += x_move
                    time2 += moving_time(2, x_move)

            elif one_xy_data[3] == 34:  # along a line (shear)
                if one_xy_data[2] == -1:  # round tool
                    nibbling_hit += 1
                    time1 += punch_time(1, tool_num)
                else:  # rect tool
                    shear_hit += 1
                    time1 += punch_time(4, tool_num)

                    if ((x_move * Ay/Ax) >= y_move):  # time
                        time2 += moving_time(4, x_move)
                        horizontal_tool_shear_in_btwn_move += x_move
                    else:
                        time2 += moving_time(5, y_move)
                        vertical_tool_shear_in_btwn_move += y_move

            elif one_xy_data[3] == 39:  # arc
                nibbling_hit += 1
                time1 += punch_time(1, tool_num)

            elif one_xy_data[3] == 40:  # single * 2
                for i in range(2):
                    single_hit += 1
                    time1 += punch_time(0, tool_num)*2

            elif one_xy_data[3] == 50:  # single * 3
                for i in range(3):
                    single_hit += 1
                    time1 += punch_time(0, tool_num)*3

        if (ix != (len(xy_data) - 1)):    # 當不是最後一點時，進入迴圈
            # 下把刀要換刀時，會先把點為歸零；沒有換刀就將pre_pt改成現在的點
            # any(pre_pt) 指pre_pt中的元素只要有一個不為0，就會回傳True
            if (one_xy_data[2] != next_xy_data[2]) & (any(pre_pt)):  # 換刀時，前一點必為原點
                pre_pt = [0, 0, 0, 0, 0, 0]
                turret_tool_change += 90
                time1 += punch_time(5, tool_num)
                # 預設每次換刀turret轉90度
            else:
                pre_pt = one_xy_data

        # END ##for ix in range(len(xy_data))
    print(f'punch time : {time1}')
    print(f'moving time : {time2}')
    total_time = time1 + time2
    feature_data = [path, horizontal_line_hit, vertical_line_hit, single_hit, nibbling_hit, shear_hit,
                    horizontal_part_move, vertical_part_move, horizontal_tool_in_btwn_move,
                    vertical_tool_in_btwn_move, horizontal_tool_shear_in_btwn_move, vertical_tool_shear_in_btwn_move,
                    turret_tool_change, total_time]
    return feature_data
    '''
    total_time = time1 + time2
    feature_data.append([path , horizontal_line_hit, vertical_line_hit, single_hit, nibbling_hit, shear_hit,\
                         horizontal_part_move, vertical_part_move, horizontal_tool_in_btwn_move,\
                         vertical_tool_in_btwn_move, horizontal_tool_shear_in_btwn_move, vertical_tool_shear_in_btwn_move,\
                         turret_tool_change, total_time])
    
    fea_path = path + "_fea.csv"
    with open(fea_path ,'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(feature_data)
    return 0
    '''

################## feature_calc end ###################

########################## main #########################


if __name__ == '__main__':

    feature = []
    feature.append([" ", "horizontal line hit", "vertical line hit", "single hit", "nibbling hit",
                    "shear hit", "horizontal part move", "vertical part move", "horizontal tool in-btwn move",
                    "vertical tool in-btwn move", "horizontal tool shear in-btwn move",
                    "vertical tool shear in-btwn move", "turret tool change deg", "total time"])

    path = 'Cir_Training_SheetA'
    sheet_num = 25

    for sn in range(sheet_num):

        print("input : " + path + str(sn) + ".txt\n")
        wholedata, row_data = readfile(path + str(sn) + ".txt")
        # wholedata, row_data = readfile(path + ".txt")
        line_var, rect_var, circle_var, arc_var, polygon_var = data_to_function(
            wholedata)

        station = np.zeros([13, 3])  # 刀具規格[長, 寬, 角度]
        station[0, :] = [20, 4,  0]
        station[1, :] = [20, 4, 90]
        station[2, :] = [10, 2, 30]
        station[3, :] = [10, 2, 45]
        station[4, :] = [10, 2, 60]
        station[5, :] = [10, 2, 120]
        station[6, :] = [10, 2, 135]
        station[7, :] = [10, 2, 150]
        station[8, :] = [10, 10, 0]
        station[9, :] = [1.5, 0, -1]
        station[10, :] = [2.5, 0, -1]  # 角度-1設為圓刀([半徑, 0, -1])
        station[11, :] = [10, 0, -1]
        station[12, :] = [10, 10, 45]

        xy_data = []

        # rect
        all_rect = []

        for k1 in range(len(rect_var)):

            one_rect_var = rect_var[k1]
            L = one_rect_var[0]
            H = one_rect_var[1]
            sp1 = one_rect_var[2]
            parentID = one_rect_var[3]
            punch_type = one_rect_var[4]
            roDeg = one_rect_var[5]
            rect_serial_num = one_rect_var[6]
            rect_subserial_num = one_rect_var[7]

            if parentID == 0:  # rect_outside_edge
                rect_xy = rect_outside_edge(
                    L, H, sp1, station, roDeg, rect_serial_num)
                for j1 in range(len(rect_xy)):
                    j2 = rect_xy[j1]
                    all_rect.append(j2)

            else:  # hole
                hole_xy_data = rect_hole(
                    L, H, sp1, punch_type, station, roDeg, rect_serial_num, rect_subserial_num)
                for j1 in range(len(hole_xy_data)):
                    j2 = hole_xy_data[j1]
                    all_rect.append(j2)
        # rect_var->[L, H, star point,   parentID,   punch_type,   roDeg, serial_num, sub_serial_num]

        # line
        all_line = []
        for k2 in range(len(line_var)):

            one_line_var = line_var[k2]
            line_start_x = one_line_var[0]
            line_start_y = one_line_var[1]
            distance = one_line_var[2]
            line_deg = one_line_var[3]
            offset_index = one_line_var[4]  # parentID
            line_serial_num = one_line_var[5]
            line_sub_serial_num = one_line_var[6]
            overlap = 1

            line_xy = line(line_start_x, line_start_y, distance, line_deg, station, offset_index,
                           line_serial_num, line_sub_serial_num, overlap)

            for j1 in range(len(line_xy)):
                j2 = line_xy[j1]
                all_line.append(j2)

        # line_var->[current_x, current_y, dis, deg, parentID, poly_gID, sub_serial_num]
        # line(line_start_x, line_start_y, distance, line_deg, station, offset_index,\
        #                  line_serial_num, line_sub_serial_num, overlap)

        # circle
        all_cir = []

        for k3 in range(len(circle_var)):
            cir_serial_num = k3
            one_circle_var = circle_var[k3]
            r = one_circle_var[0]
            start_deg = one_circle_var[1]
            cen_x = one_circle_var[2]
            cen_y = one_circle_var[3]
            parentID = one_circle_var[4]
            punch_type = one_circle_var[5]

            cir_xy = circle(r, start_deg, cen_x, cen_y, parentID,
                            station, punch_type, cir_serial_num)
            for j1 in range(len(cir_xy)):
                j2 = cir_xy[j1]
                all_cir.append(j2)

        # arc
        all_arc = []

        for k4 in range(len(arc_var)):

            one_arc_var = arc_var[k4]
            cen_x = one_arc_var[0]
            cen_y = one_arc_var[1]
            radius = one_arc_var[2]
            star_deg = one_arc_var[3]
            working_deg = one_arc_var[4]
            orientation = one_arc_var[5]
            parentID = one_arc_var[6]
            arc_serial_num = one_arc_var[7]
            arc_sub_serial_num = one_arc_var[8]

            arc_xy, nib_hit_arc = arc(cen_x, cen_y, radius, star_deg, working_deg, orientation, parentID,
                                      station, arc_serial_num, arc_sub_serial_num)
            for j1 in range(len(arc_xy)):
                j2 = arc_xy[j1]
                all_arc.append(j2)

        # Octagon hole
        all_Octagon = []

        for k1 in polygon_var:
            Octagon_pts = k1[0]
            parentID = k1[1]
            poly_gID = k1[2]
            # hole # polygon_var.append([Octagon_pts, parentID, poly_gID])
            hole_xy_data = Octagon_hole(
                Octagon_pts, station, poly_gID, parentID)
            for j1 in (hole_xy_data):
                all_Octagon.append(j1)
        # Octagon hole END

        for kk in range(len(all_line)):
            xy_data.append(all_line[kk])

        for kk in range(len(all_rect)):
            xy_data.append(all_rect[kk])

        for kk in range(len(all_cir)):
            xy_data.append(all_cir[kk])

        for kk in range(len(all_arc)):
            xy_data.append(all_arc[kk])

        for kk in (all_Octagon):
            # print(kk)
            xy_data.append(kk)

        # xy_data.sort(key=lambda x:x[2]) ### 重新排列，以第row中的二號位為指標，目的為同一把刀先加工完
        xy_data = sorted(xy_data, key=itemgetter(
            6, 2), reverse=True)  # 重新排列，以6、2 的位置排

        graphic_data = graph(xy_data, station)
        feature_data = feature_calc(xy_data, path + str(sn))
        feature.append(feature_data)

        txt_path = path + str(sn) + "_result.txt"
        # txt_path = "rect_shear" + str(sn) + "_result.txt"
        with open(txt_path, 'w', newline='') as txtfile:
            writer = csv.writer(txtfile)
            writer.writerows(graphic_data)

    # for end

    fea_path = path + "_fea.csv"
    with open(fea_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(feature)

######## main code end #######
