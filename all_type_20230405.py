import math
import numpy as np
import csv
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

        if ((s3[0]) != ';'):
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
    k = 12
    while k < len(wholedata):
        onerow_data = wholedata[k]
        if (len(onerow_data) <= 0):
            break

        if len(onerow_data) < 8:
            k = k+1
        elif (onerow_data[1] == 30) & (len(onerow_data) == 8):  # rectangle 2D
            parentID = onerow_data[3]  # 取出parentID
            r_xy = wholedata[k+1]  # 抓取方形資料

            x_point = [r_xy[0], r_xy[2], r_xy[4], r_xy[6]]
            y_point = [r_xy[1], r_xy[3], r_xy[5], r_xy[7]]
            L = max(x_point) - min(x_point)
            H = max(y_point) - min(y_point)
            j = 0

            for k1 in range(4):
                if (x_point[k1] == min(x_point)) & (j == 0):
                    a = k1
                    j = 1
                elif (x_point[k1] == min(x_point)) & (j == 1):
                    if y_point[k1] > y_point[a]:
                        a = k1
                rect_start_p = [x_point[a], y_point[a]]

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
                        rect_var.append(
                            [L, H, rect_grid_xy, parentID, onerow_data[6]])
                        #print(f'[{rect_grid_x}, {rect_grid_y}], col:{col_arr}, row:{row_arr}')
                k = k+3  # 將下2行也跳過

            else:
                rect_var.append([L, H, rect_start_p, parentID, onerow_data[6]])
                k = k+2  # 將下一行也跳過

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

                circle_var.append(
                    [radius, s_deg, x_ix, y_ix, parentID, punch_type])  # 抓取圓形資料
            k = k+3  # 將下2行也跳過

        elif (onerow_data[7] == 0) & (onerow_data[1] == 32) & (len(onerow_data) == 9):  # circle圓
            parentID = onerow_data[3]  # 取出圓的parentID
            one_cir_var = wholedata[k+1]
            one_cir_var.append(parentID)
            one_cir_var.append(onerow_data[7])  # punch type

            circle_var.append(one_cir_var)  # 抓取圓形資料
            k = k+2  # 將下一行也跳過

        elif (onerow_data[6] == 0) & (onerow_data[1] == 34) & (len(onerow_data) == 8):  # polygon多邊

            nvtx = onerow_data[4]
            poly_rows = math.ceil(nvtx/4)
            x_point = []
            y_point = []

            parentID = onerow_data[3]  # 取出多邊形的parentID，先以外部輪廓為主

            for i in range(poly_rows):
                poly_xy = wholedata[k+(1+i)]  # 取出多邊形的點位資料

                for j in range(int(len(poly_xy)/2)):

                    x_point.append(poly_xy[2*j])
                    y_point.append(poly_xy[2*j + 1])

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

                line_var.append([current_x, current_y, dis, deg, parentID])

            k = k + poly_rows  # 將下n行也跳過(每行有四個點)

        elif (onerow_data[7] == 0) & (onerow_data[1] == 31) & (len(onerow_data) == 9):  # composite

            parentID = onerow_data[3]
            k = k+1

            for com_index in range(8):
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

                    line_var.append([current_x, current_y, dis, deg, parentID])

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

                    arc_var.append(
                        [cen_x, cen_y, radius, star_deg, working_deg, orientation, parentID])

                    k = k+2
        else:
            k = k+1

    return line_var, rect_var, circle_var, arc_var

################ data_to_function end ##############

################# choose tool ##############


def ch_tool(degree, tool, square):  # 選擇要用的刀具

    b = 0  # 一個是否已經有找到刀的指標

    if square == 1:
        for k1 in range(len(tool)):
            tool_L = tool[k1, 0]
            tool_W = tool[k1, 1]
            if tool_L == tool_W:
                a = k1
    else:
        for k1 in range(len(tool)):  # 利用迴圈找刀具庫中的刀

            tool_deg = tool[k1, 2]*math.pi/180

            if ((degree == (tool_deg+math.pi)) | (degree == tool_deg)) & (b == 0):
                a = k1
                b = 1
            elif ((degree == (tool_deg+math.pi)) | (degree == tool_deg)) & (b == 1):
                if tool[k1, 0] > tool[a, 0]:  # 如果有更適用的刀，就換過去
                    a = k1
            else:  # 如果沒有適合的方形刀，就用圓刀
                for k2 in range(len(tool)):
                    if (tool[k2, 2] == -1) & (b == 0):
                        a = k2
                        b = 1
                    elif (tool[k2, 2] == -1) & (b == 1):
                        if tool[k2, 0] > tool[a, 0]:
                            a = k2
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


def line(line_start_x, line_start_y, distance, line_deg, tool, offset_index):

    line_xy = []
    befortrans_line_xy = []
    line_h_track = 0
    line_track = 0
    line_v_track = 0
    line_h_shearbwn = 0
    line_v_shearbwn = 0

    h_line_hit = 0
    v_line_hit = 0
    line_single_hit = 0
    line_shear_hit = 0
    line_nib_hit = 0

    line_nib_overlap = 1

    hit_type = 0  # (33-水平垂直line hit)(34 line shear hit)(40 沿著線nib)

    tool_num = ch_tool(line_deg, tool, 0)

    if (tool[tool_num, 2] == -1):  # 圓刀nib
        r = tool[tool_num, 0]
        a = distance  # + line_nib_overlap    #line_nib_overlap預計過切的長度
        one_step = r*0.5

        if offset_index == 0:  # 由右向"左"加工
            orient = -1

        else:  # 由左向"右"加工
            orient = 1

        # + (line_nib_overlap/2) * math.cos(line_deg)
        x_offset = r * math.sin(line_deg)
        # - (line_nib_overlap/2) * math.sin(line_deg)
        y_offset = orient * r * math.cos(line_deg)

        hit_type = 40
        line_track = 0  # nib的直線運行不列入記錄

        line_xy.append(
            [line_start_x + x_offset, line_start_y + y_offset, tool_num, hit_type])

        while (a > 0):
            a_pre = a

            a = a - one_step  # 這次加工後剩餘的長度

            if a < 0:  # a剩餘長度最少為0
                a = 0

            last_line_xy = line_xy[len(line_xy)-1]
            line_x = last_line_xy[0] + one_step * \
                math.cos(line_deg)  # 記錄此時加工的點位
            line_y = last_line_xy[1] + one_step * math.sin(line_deg)

            line_xy.append([line_x, line_y, tool_num, hit_type])

    else:  # (line hit) or (line shear hit) 方刀
        L_tool = tool[tool_num, 0]
        W_tool = tool[tool_num, 1]
        a = distance - (L_tool-2)

        if offset_index == 0:  # 由右向"左"加工
            orient = -1

        else:  # 由左向"右"加工
            orient = 1

        x_offset = (L_tool/2)-1
        y_offset = W_tool/2 * orient

        if ((tool[tool_num, 2] != 0) & (tool[tool_num, 2] != 90)):
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

            line_track = line_track + (a_pre - a)  # 記錄水平路徑和；(a_pre - a)永遠為正

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

            line_xy.append([line_x, line_y, tool_num, hit_type])

    return line_xy, line_h_track, line_v_track, line_h_shearbwn, line_v_shearbwn, h_line_hit,\
        v_line_hit, line_single_hit, line_shear_hit, line_nib_hit

################# line end #################

################# circle ###################


def circle(r, start_deg, cen_x, cen_y, parentID, tool, punch_type):

    tool_num = ch_tool(-1, tool, 0)
    cir_xy = []
    h_track_cir = 0
    v_track_cir = 0
    cir_hpm = 0  # circle horizontal part move
    cir_vpm = 0  # circle vertical part move
    single_hit_cir = 0
    nib_hit_cir = 0
    pitch = 2

    if (parentID != 0):  # 除料範圍為圓內

        if r == tool[tool_num, 0]:       # 刀具等於洞的大小時
            single_hit_cir += 1
            cir_xy.append([cen_x, cen_y, tool_num, 17])  # punch_type先用17，模擬方便
            #cir_xy格式為 [x, y, 圓刀半徑, 打洞方式]
            # 圓刀打洞方式(16:single, 17:1_hit along a line, 39:nibbling-arc, 40:nibbling-line)

        elif r > tool[tool_num, 0]:     # nibbling hit

            r2 = r - tool[tool_num, 0]
            feeding_a = pitch / r2
            angle = 0
            while angle < (2*np.pi):
                x_point = math.cos(angle) * r2 + cen_x
                y_point = math.sin(angle) * r2 + cen_y
                nib_hit_cir += 1
                cir_xy.append([x_point, y_point, tool_num, 39])
                angle += feeding_a

    elif (parentID == 0):  # 除料範圍為圓外 # nibbling hit
        r2 = r + tool[tool_num, 0]
        feeding_a = pitch / r2
        angle = 0
        s_deg = (start_deg*np.pi)/180

        while angle < (2*np.pi):
            x_point = math.cos(angle + s_deg) * r2 + cen_x
            y_point = math.sin(angle + s_deg) * r2 + cen_y
            cir_xy.append([x_point, y_point, tool_num, 39])
            nib_hit_cir += 1
            angle += feeding_a

    return cir_xy, h_track_cir, v_track_cir, single_hit_cir, nib_hit_cir, cir_hpm, cir_vpm

################# circle end ###############

################# arc ###################


def arc(cen_x, cen_y, r, s_deg, working_deg, orientation, parentID, tool):

    tool_num = ch_tool(-1, tool, 0)
    arc_xy = []
    nib_hit_arc = 0
    pitch = 2

    if (parentID == 0) & (orientation == 1):  # 除料範圍為圓外 # nibbling hit
        r2 = r + tool[tool_num, 0]
    elif (parentID == 0) & (orientation == -1):
        r2 = r - tool[tool_num, 0]

    feeding_a = pitch / r2
    angle = 0

    while angle < working_deg:
        x_point = math.cos(angle*orientation + s_deg) * r2 + cen_x
        y_point = math.sin(angle*orientation + s_deg) * r2 + cen_y
        arc_xy.append([x_point, y_point, tool_num, 39])
        nib_hit_arc += 1
        angle += feeding_a

    return arc_xy, nib_hit_arc

################# arc end ###############

############### hole array rotate ###############


def hole_array_rotate(hole_xy, sp2, degree):

    theta = degree * np.pi / 180  # 將角度轉為徑度制

    trans_array = np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    # 旋轉矩陣

    all_hole_hit = len(hole_xy)

    for k1 in range(all_hole_hit):  # 將每一點都乘上旋轉矩陣，再加上第一個洞的原點

        k1_xy = hole_xy[k1]
        x_pre = k1_xy[0]
        y_pre = k1_xy[1]
        tool_num = k1_xy[2]
        xy_pre = np.array([[x_pre], [y_pre]])  # 取單點的座標(x,y)
        xy_trans = np.matmul(trans_array, xy_pre)  # 乘上旋轉矩陣

        x_abs = xy_trans[0, 0] + sp2[0]   # X 轉置後，加上原點座標，變成絕對座標
        y_abs = xy_trans[1, 0] + sp2[1]   # Y 轉置後，加上原點座標，變成絕對座標

        xy_data.append([x_abs, y_abs, tool_num])  # 將點位記錄在 xy_data 內

    return xy_data

############## hole array rotate end ############

############### hole array #################


def hole_array(column, row, x_gap, y_gap, L, H, hole_xy):

    one_hole_hit = len(hole_xy)  # 單一洞內點的數量，也就是打了多少次

    for k1 in range(int(column) - 1):  # 做單一 row 方向的陣列

        for k2 in range(one_hole_hit):

            k2_hole_xy = hole_xy[k2]
            x_hole = k2_hole_xy[0] + (x_gap + L) * (k1+1)
            y_hole = k2_hole_xy[1]
            tool_num = k2_hole_xy[2]

            hole_xy.append([x_hole, y_hole, tool_num])  # 將點位記錄在hole_xy內

    first_row_hole_hit = len(hole_xy)  # 陣列第一列中點的數量，也就是打了多少次

    for k3 in range(int(row) - 1):  # 將上面單一row的陣列做 column 方向的陣列

        for k4 in range(first_row_hole_hit):

            k4_hole_xy = hole_xy[k4]
            x_hole = k4_hole_xy[0]
            y_hole = k4_hole_xy[1] - (y_gap + H) * (k3+1)
            tool_num = k4_hole_xy[2]

            hole_xy.append([x_hole, y_hole, tool_num])

    return hole_xy

############### hole array end #############

################ rect hole #################


def rect_hole(L, H, degree, sp1, punch_type, station):  # 做法為：以單一矩形洞做全孔加工，剩下的陣列洞另外處理

    hole_xy_data = []
    tool_num = ch_tool(degree, station, 1)  # 選到適用的刀
    L_tool = station[tool_num, 0]
    w_tool = station[tool_num, 1]

    b = H - w_tool  # 洞內高度所要走的行程只有 H - w_tool
    c = 1  # 一個橫加工時的指標
    d = 0  # 垂直向的一個指標，用於垂直移動剛好讓剩餘長度為0時用
    h_track = 0  # 水平線加工時所走的路徑總和
    v_track = 0  # 垂直線加工時所走的路徑總和

    hole_xy = []      # 記錄洞內衝孔時的點位，洞口左上為暫時原點(0,0)

    if (L == L_tool) & (H == w_tool):

        hole_xy.append([L_tool/2, -w_tool/2, tool_num])

    else:
        # 第一點位置，記錄點的型式為[x, y , 刀編號]
        hole_xy.append([L_tool, -w_tool/2, tool_num])

        while True:  # 以橫向加工到底後垂直移動一些，再繼續橫向加工(b>0)

            a = L - L_tool  # 洞內水平長度所要走的行程只有 L - L_tool

            while a > 0:

                a_pre = a  # 記錄前一次加工程剩餘的長度(水平維度)
                a = a - (L_tool - 1)  # 這次加工後剩餘的長度

                if a < 0:  # a剩餘長度最少為0
                    a = 0

                h_track = h_track + (a_pre - a)  # 記錄水平路徑和；(a_pre - a)永遠為正

                last_hole_xy = hole_xy[len(hole_xy)-1]
                x_hole = last_hole_xy[0] + c * (a_pre - a)  # 記錄此時加工的點位
                y_hole = last_hole_xy[1]
                hole_xy.append([x_hole, y_hole, tool_num])  # 將點位記錄在hole_xy內

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

            v_track = v_track + (b_pre - b)

            last_hole_xy = hole_xy[len(hole_xy)-1]
            x_hole = last_hole_xy[0]
            y_hole = last_hole_xy[1] - (b_pre - b)  # 記錄此時加工的點位

            hole_xy.append([x_hole, y_hole, tool_num])

    theta = degree * np.pi / 180  # 將角度轉為徑度制
    trans_array = np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    # 旋轉矩陣

    all_hole_hit = len(hole_xy)

    for k1 in range(all_hole_hit):  # 將每一點都乘上旋轉矩陣，再加上第一個洞的原點

        k1_xy = hole_xy[k1]
        x_pre = k1_xy[0]
        y_pre = k1_xy[1]
        tool_num = k1_xy[2]
        xy_pre = np.array([[x_pre], [y_pre]])  # 取單點的座標(x,y)
        xy_trans = np.matmul(trans_array, xy_pre)  # 乘上旋轉矩陣

        x_abs = xy_trans[0, 0] + sp1[0]   # X 轉置後，加上原點座標，變成絕對座標
        y_abs = xy_trans[1, 0] + sp1[1]   # Y 轉置後，加上原點座標，變成絕對座標

        # 將點位記錄在 xy_data 內
        hole_xy_data.append([x_abs, y_abs, tool_num, punch_type])

    return hole_xy_data, h_track, v_track

################ rect hole end #############

############## outside edge ################


def rect_outside_edge(L, H, sp1, station):  # 做矩形外圍的加工

    rect_xy = []
    rect_punch_type = 34
    # 橫向
    tool_num = ch_tool(0, station, 0)  # 取刀具的資料
    L_tool = station[tool_num, 0]
    w_tool = station[tool_num, 1]

    x_start = sp1[0] + (L_tool/2 - 1)  # 啟始點
    y_start = sp1[1] + w_tool/2

    rect_xy.append([x_start, y_start, tool_num,
                   rect_punch_type])  # 外邊緣開始工作的第一點

    hpm_out = x_start  # outside part horizontal part move
    vpm_out = y_start  # outside part vertical part move

    c = -1  # 加工方向係數
    d = 1
    h_track_out = 0
    v_track_out = 0
    h_line_hit_out = 1
    v_line_hit_out = 1

    for k1 in range(2):

        a = L - (L_tool-2)

        while a > 0:
            a_pre = a  # 記錄前一次加工後剩餘的長度
            a = a - (L_tool - 1)  # 這次加工後剩餘的長度

            if a < 0:  # a剩餘長度最少為0
                a = 0

            h_track_out = h_track_out + (a_pre - a)  # 記錄水平路徑和；(a_pre - a)永遠為正

            h_line_hit_out = h_line_hit_out + 1  # 記錄水平打多少下

            last_xy_data = rect_xy[(len(rect_xy)-1)]
            x_out = last_xy_data[0] + (a_pre - a) * d  # 記錄此時加工的點位
            y_out = last_xy_data[1]

            rect_xy.append([x_out, y_out, tool_num, rect_punch_type])

        last_xy_data = rect_xy[(len(rect_xy)-1)]
        x_out = last_xy_data[0]
        y_out = last_xy_data[1] + (H + w_tool) * c
        c = c * -1
        d = d * -1

        rect_xy.append([x_out, y_out, tool_num, rect_punch_type])

    # 直向
    line_deg = 90 * math.pi / 180
    tool_num = ch_tool(line_deg, station, 0)  # 取刀具的資料
    L_tool = station[tool_num, 0]
    w_tool = station[tool_num, 1]

    x_start = sp1[0] - (w_tool/2)  # 啟始點
    y_start = sp1[1] - (L_tool/2 - 1)

    rect_xy.append([x_start, y_start, tool_num,
                   rect_punch_type])  # 外邊緣開始工作的第一點

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

            h_track_out = h_track_out + (b_pre - b)  # 記錄水平路徑和；(b_pre - b)永遠為正

            h_line_hit_out = h_line_hit_out + 1  # 記錄水平打多少下

            last_xy_data = rect_xy[(len(rect_xy)-1)]
            x_out = last_xy_data[0]  # 記錄此時加工的點位
            y_out = last_xy_data[1] + (b_pre - b) * d

            rect_xy.append([x_out, y_out, tool_num, rect_punch_type])

        last_xy_data = rect_xy[(len(rect_xy)-1)]
        x_out = last_xy_data[0] + (L + w_tool) * c
        y_out = last_xy_data[1]
        c = c * -1
        d = d * -1

        # 34為衝孔型式 punching with 1 tool along a line
        rect_xy.append([x_out, y_out, tool_num, rect_punch_type])

    return rect_xy, h_track_out, v_track_out, hpm_out, vpm_out, h_line_hit_out, v_line_hit_out

############ outside edge end ##############


################# hole Shear calc ##############
'''
def hole_shear(L_hole, H_hole, degree, sp2):
    
    hole_xy, h_track, v_track = hole(L_hole, H_hole, degree)                #hole
    
    #hole_xy = hole_array(column, row, x_gap, y_gap, L_hole, H_hole, hole_xy)#hole_array
    
    Rect_shear_xy = hole_array_rotate(hole_xy, sp2, degree)                 #hole_array_rotate
    
    theta = degree * np.pi /180
    
    #hit data
    h_line_hit = h_lhit_out
    v_line_hit = v_lhit_out
    single_hit = 0
    nibbling_hit = 0
    shear_hit = len(hole_xy)
    
    #part move
    hpm = hpm_out
    vpm = vpm_out
    
    #in between move
    h_inbtwn = h_t_out
    v_inbtwn = v_t_out
    
    #因洞有傾角，因此用另一個shear的特徵記錄
    h_shearbtwn = (h_track * abs(math.cos(theta)) + v_track * abs(math.sin(theta))) * column * row
    v_shearbtwn = (h_track * abs(math.sin(theta)) + v_track * abs(math.cos(theta))) * column * row
    
    data.append([case_in,h_line_hit,v_line_hit,single_hit,nibbling_hit,shear_hit,hpm,vpm,\
                 h_inbtwn,v_inbtwn,h_shearbtwn,v_shearbtwn,tool_change_deg])
    
    return data, hole_shear_xy
'''
############### hole Shear calc end ############

################### graph ######################


def graph(xy_data, tool, ):

    graph_data = []

    for j in range(len(wholedata)):
        graph_data.append(wholedata[j])

    '''
    graph_data = []
    graph_data.append(["; SYSCONFIG"])
    graph_data.append([";version", "unit flag", "draw speed"])
    graph_data.append([";2.1", "0(mks) 1(fbs)", "(%)"])
    graph_data.append([201, 0, 100])
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
    k3 = 50000
    k4 = 1000
    for k1 in range(num):

        single_p = xy_data[k1]
        tool_num = single_p[2]
        single_p_gra = []

        if tool[tool_num, 2] == -1:  # 圓刀
            if single_p[3] == 17:
                R = tool[tool_num, 0]  # - 0.1 #為了讓視覺有加工到的感覺，所以讓圓稍微小一點
            else:
                R = tool[tool_num, 0]

            #graph_data.append([";gID", "gType", "iUserSetID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF"])
            graph_data.append([k4, 32, k4, 0, 1, 36, 0, single_p[3], 1])
            k4 += 1
            single_p_gra = [R, 0, single_p[0], single_p[1]]

        else:  # 方刀

            punch_type = single_p[3]
            #graph_data.append([";gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF"])
            graph_data.append([k3, 30, k3, 0, 0, 0, punch_type, 1])
            k3 += 1
            tool_trans = tool_expend(tool, tool_num)

            for k2 in range(4):

                gra_x_point = single_p[0] + tool_trans[0][k2]
                gra_y_point = single_p[1] + tool_trans[1][k2]
                single_p_gra.append(gra_x_point)
                single_p_gra.append(gra_y_point)

        graph_data.append(single_p_gra)

    return graph_data

################## graph end ###################

########################## main #########################

# data = []
# data.append([" ","horizontal line hit","vertical line hit","single hit","nibbling hit",
#              "shear hit","horizontal part move","vertical part move","horizontal tool in-btwn move",
#              "vertical tool in-btwn move","horizontal tool shear in-btwn move",
#              "vertical tool shear in-btwn move","turret tool change deg"
#              ])


# print("All-type part\n")

# station = np.zeros([10,3])      #刀具規格[長, 寬, 角度]
# station[0, :] = [20, 4,  0]
# station[1, :] = [10, 2, 30]
# station[2, :] = [10, 2, 45]
# station[3, :] = [10, 2, 60]
# station[4, :] = [20, 4, 90]
# station[5, :] = [10, 2, 120]
# station[6, :] = [10, 2, 135]
# station[7, :] = [10, 2, 150]
# station[8, :] = [10, 10, 0]
# station[9, :] = [2.5, 0, -1]     #角度-1設為圓刀([半徑, 0, -1])

# wholedata, row_data = readfile("test_alltype.txt")

# line_var, rect_var, circle_var, arc_var = data_to_function(wholedata)

# xy_data = []

# ##rect
# all_rect = []

# for k1 in range(len(rect_var)):
#     one_rect_var = rect_var[k1]
#     L = one_rect_var[0]
#     H = one_rect_var[1]
#     sp1 = one_rect_var[2]
#     parentID = one_rect_var[3]
#     punch_type = one_rect_var[4]

#     degree = 0
#     if parentID==0:
#         rect_xy, h_t_out, v_t_out, hpm_out, vpm_out, h_lhit_out, v_lhit_out = rect_outside_edge(L, H, sp1, station)
#         for j1 in range(len(rect_xy)):
#             j2 = rect_xy[j1]
#             all_rect.append(j2)

#     else:
#         hole_xy_data, h_track, v_track = rect_hole(L, H, degree, sp1, punch_type, station)
#         for j1 in range(len(hole_xy_data)):
#             j2 = hole_xy_data[j1]
#             all_rect.append(j2)


# #對all_rect重新排列，以第row中的二號位為指標，目的為同一把刀先加工完
# all_rect.sort(key=lambda x:x[2])


# ##line
# all_line = []
# for k2 in range(len(line_var)):
#     one_line_var = line_var[k2]
#     line_start_x = one_line_var[0]
#     line_start_y = one_line_var[1]
#     distance = one_line_var[2]
#     line_deg = one_line_var[3]
#     offset_index = one_line_var[4] #parentID

#     line_xy, line_h_track, line_v_track, line_h_shearbwn, line_v_shearbwn, h_line_hit,\
#            v_line_hit, line_single_hit, line_shear_hit, line_nib_hit\
#            = line(line_start_x, line_start_y, distance, line_deg, station, offset_index)
#     for j1 in range(len(line_xy)):
#         j2 = line_xy[j1]
#         all_line.append(j2)
#     #line_var.append([one_x, one_y, dis, deg, parentID])
#     #line(line_start_x, line_start_y, distance, line_deg, tool, offset_index)
# all_line.sort(key=lambda x:x[2])


# ##circle
# all_cir = []

# for k3 in range(len(circle_var)):
#     one_circle_var = circle_var[k3]
#     r = one_circle_var[0]
#     start_deg = one_circle_var[1]
#     cen_x = one_circle_var[2]
#     cen_y = one_circle_var[3]
#     parentID = one_circle_var[4]
#     punch_type = one_circle_var[5]

#     cir_xy, h_track_cir, v_track_cir, single_hit_cir, nib_hit_cir, cir_hpm, cir_vpm\
#             = circle(r, start_deg, cen_x, cen_y, parentID, station, punch_type)
#     for j1 in range(len(cir_xy)):
#         j2 = cir_xy[j1]
#         all_cir.append(j2)


# ## arc
# all_arc = []

# for k4 in range(len(arc_var)):
#     one_arc_var = arc_var[k4]

#     cen_x = one_arc_var[0]
#     cen_y = one_arc_var[1]
#     radius = one_arc_var[2]
#     star_deg = one_arc_var[3]
#     working_deg = one_arc_var[4]
#     orientation = one_arc_var[5]
#     parentID = one_arc_var[6]

#     arc_xy, nib_hit_arc = arc(cen_x, cen_y, radius, star_deg, working_deg, orientation, parentID, station)

#     for j1 in range(len(arc_xy)):
#         j2 = arc_xy[j1]
#         all_arc.append(j2)


# for kk in range(len(all_line)):
#     xy_data.append(all_line[kk])


# for kk in range(len(all_rect)):
#     xy_data.append(all_rect[kk])


# for kk in range(len(all_cir)):
#     xy_data.append(all_cir[kk])

# for kk in range(len(all_arc)):
#     xy_data.append(all_arc[kk])

# xy_data.sort(key=lambda x:x[2])

# graphic_data = graph(xy_data, station)

# '''
# in_variable_rs = np.zeros([8,12])                       # input variable
# in_variable_rs[0, :] = [500,500,50,-50,25,25,1,1,75,-130,10,10]
# in_variable_rs[1, :] = [500,500,50,-50,25,25,1,3,75,-130,10,10]
# in_variable_rs[2, :] = [500,500,50,-50,25,50,1,1,75,-130,10,10]
# in_variable_rs[3, :] = [500,500,50,-50,25,50,1,3,75,-130,10,10]
# in_variable_rs[4, :] = [500,500,50,-50,25,50,2,3,75,-130,10,10]
# in_variable_rs[5, :] = [500,500,50,-50,100,75,1,2,130,-200,10,10]
# in_variable_rs[6, :] = [500,500,50,-50,100,75,2,2,130,-200,10,10]
# in_variable_rs[7, :] = [500,500,50,-50,100,75,2,4,75,-300,10,10]

# for k in range(len(in_variable_rs)):

#     xy_data = []
#     xy_data.append([0,0,-1])

#     L = in_variable_rs[k,0]
#     H = in_variable_rs[k,1]
#     L_hole = in_variable_rs[k,4]
#     H_hole = in_variable_rs[k,5]
#     degree = 30

#     row_hole = in_variable_rs[k,6]
#     column_hole = in_variable_rs[k,7]

#     x_gap = in_variable_rs[k,10]
#     y_gap = in_variable_rs[k,11]

#     sp1 = [in_variable_rs[k,2], in_variable_rs[k,3]]
#     sp2 = [in_variable_rs[k,8], in_variable_rs[k,9]]

#     overlap = 1

#     print(f'case{k+1} - {L:3.0f}x{H:3.0f} + {L_hole:3.0f}x{H_hole:2.0f}-{row_hole:1.0f}x{column_hole:1.0f}')

#     data, xy_data = Rect_shear(L,H,sp1,L_hole,H_hole,degree,column_hole,row_hole,x_gap,y_gap,sp2)

#     graphic_data = graph(xy_data, tool)

#     k_str = str(k+1)
#     path = 'sample' + k_str + '_xy.txt'
#     with open(path ,'w', newline='') as txtfile:
#         writer = csv.writer(txtfile)
#         writer.writerows(graphic_data)
# '''
# path = 'All_type_sample.txt'
# with open(path ,'w', newline='') as txtfile:
#     writer = csv.writer(txtfile)
#     writer.writerows(graphic_data)
# '''
# path = 'All_type_sample1.csv'
# with open(path ,'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(data)
# '''
# ######## main code end #######
