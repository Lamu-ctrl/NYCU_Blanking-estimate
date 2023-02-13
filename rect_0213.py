import math
import numpy as np
import csv

################# choose tool ##############


def ch_tool(degree, tool):  # 選擇要用的刀具

    b = 0  # 一個是否已經有找到刀的指標
    for k1 in range(len(tool)):  # 利用迴圈找刀具庫中的刀

        # for k2 in range(7):  # 垂直於邊的也一併找進
        #     degree2 = degree + (k2 - 3)*90

        #     if (degree2 == tool[k1, 2]) & (b == 0):  # 第一次找到適合的刀
        #         a = k1
        #         b = 1
        #     elif (degree2 == tool[k1, 2]) & (b == 1):  # 已經有到適合的刀，進行比較

        #         if tool[k1, 0] > tool[a, 0]:  # 如果有更適用的刀，就換過去
        #             a = k1
        #             b = 1
        if (degree == tool[k1, 2]) & (b == 0):  # 第一次找到適合的刀
            a = k1
            b = 1
        elif (degree == tool[k1, 2]) & (b == 1):  # 已經有到適合的刀，進行比較

            if tool[k1, 0] > tool[a, 0]:  # 如果有更適用的刀，就換過去
                a = k1
                b = 1

    return a


################# choose tool end ##########

################# graph _ tool expend ##############

def tool_expension(tool, tool_expend):
    # tool = np.zeros([4, 3])
    # tool[0, :] = [10, 2, 0]
    # tool[2, :] = [10, 2, 90]
    # tool[1, :] = [10, 2, 30]
    for i in range(len(tool)):
        tool_s_0deg = np.zeros([2, 4])
        # rotate part
        theta = tool[i][2] * np.pi / 180
        trans_array = np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        # rotate part end
        tool_s_0deg[0] = [- tool[i][0], tool[i][0], tool[i][0], -tool[i][0]]
        tool_s_0deg[1] = [- tool[i][1], -tool[i][1], tool[i][1], tool[i][1]]
        # tool_b[0] = [-10, 10, 10, -10]
        # tool_b[1] = [-2, -2, 2, 2]
        tool_expend[i] = np.matmul(trans_array, tool_s_0deg)

    print(tool_expend)
    return tool_expend

################# graph _ tool expend ##############
##################### hole #################


def hole(L, H, degree):  # 做法為：以單一矩形洞做全孔加工，剩下的陣列洞另外處理

    tool_num = ch_tool(degree, tool)  # 選到適用的刀
    L_tool = tool[tool_num, 0]
    w_tool = tool[tool_num, 1]

    b = H - w_tool  # 洞內高度所要走的行程只有 H - w_tool
    c = 1  # 一個橫加工時的指標

    hole_xy = []      # 記錄洞內衝孔時的點位，洞口左上為暫時原點(0,0)
    hole_xy.append([L_tool, -w_tool/2, tool_num])  # 第一點位置，記錄點的型式為[x, y , 刀編號]

    h_track = 0  # 水平線加工時所走的路徑總和
    v_track = 0  # 垂直線加工時所走的路徑總和

    d = 0  # 垂直向的一個指標，用於垂直移動剛好讓剩餘長度為0時用

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
            # print('d=1')
            d = 1

        v_track = v_track + (b_pre - b)

        last_hole_xy = hole_xy[len(hole_xy)-1]
        x_hole = last_hole_xy[0]
        y_hole = last_hole_xy[1] - (b_pre - b)  # 記錄此時加工的點位

        hole_xy.append([x_hole, y_hole, tool_num])

    return hole_xy, h_track, v_track

##################### hole end #############

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

############# hole array rotate ############


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

########### hole array rotate end ##########

############## outside edge ################


def outside_edge(L, H, sp1, row_rect, column_rect):  # 做矩形外圍的加工

    tool_num = ch_tool(0, tool)  # 取刀具的資料
    L_tool = tool[tool_num, 0]
    w_tool = tool[tool_num, 1]
    print(L_tool, w_tool)
    x_start = (L_tool/2 - 1) + sp1[0]  # 啟始點
    y_start = w_tool/2 + sp1[1]

    # xy_data.append([x_start, y_start, tool_num])  # 外邊緣開始工作的第一點

    start_offset = np.zeros([3, 2])  # 在角落時的移動
    start_offset[0, :] = [(L_tool-1), -(w_tool-1)]
    start_offset[1, :] = [-(L_tool-1), -(w_tool-1)]
    start_offset[2, :] = [-(L_tool-1), (w_tool-1)]

    hpm_out = x_start  # outside part horizontal part move
    vpm_out = y_start  # outside part vertical part move
    for i in range(len(start_offset)):
        hpm_out = hpm_out + abs(start_offset[i, 0])
        vpm_out = vpm_out + abs(start_offset[i, 1])

    wd = np.zeros([4, 2])  # work direction [x,y]分別為四個邊在工作時增量係數
    wd[0, :] = [1, 0]
    wd[1, :] = [0, -1]
    wd[2, :] = [-1, 0]
    wd[3, :] = [0, 1]

    k2 = 0
    h_track_out = 0
    v_track_out = 0
    h_line_hit_out = 0
    v_line_hit_out = 0
    #print(str(L_tool) + ", " + str(w_tool))
    # for k1 in range(2):

    #     a = L - (L_tool-2)
    #     b = H - (w_tool-2)

    #     while a > 0:
    #         a_pre = a  # 記錄前一次加工程剩餘的長度
    #         a = a - (L_tool - 1)  # 這次加工後剩餘的長度

    #         if a < 0:  # a剩餘長度最少為0
    #             a = 0

    #         h_track_out = h_track_out + (a_pre - a)  # 記錄水平路徑和；(a_pre - a)永遠為正

    #         h_line_hit_out = h_line_hit_out + 1  # 記錄水平打多少下

    #         last_xy_data = xy_data[(len(xy_data)-1)]
    #         x_out = last_xy_data[0] + wd[k2, 0] * (a_pre - a)  # 記錄此時加工的點位
    #         y_out = last_xy_data[1]

    #         xy_data.append([x_out, y_out, tool_num])

    #     xy_data.append([x_out+start_offset[k2, 0], y_out +
    #                    start_offset[k2, 1], tool_num])

    #     k2 = k2 + 1

    #     while b > 0:  # 長跟高不一定一樣，所以分兩個迴圈做
    #         b_pre = b  # 記錄前一次加工程剩餘的長度
    #         b = b - (w_tool - 1)  # 這次加工後剩餘的長度

    #         if b < 0:  # a剩餘長度最少為0
    #             b = 0

    #         v_track_out = v_track_out + (b_pre - b)  # 記錄水平路徑和；(b_pre - b)永遠為正

    #         v_line_hit_out = v_line_hit_out + 1  # 記錄水平打多少下

    #         last_xy_data = xy_data[(len(xy_data)-1)]
    #         x_out = last_xy_data[0]  # 記錄此時加工的點位
    #         y_out = last_xy_data[1] + wd[k2, 1] * (b_pre - b)
    #         xy_data.append([x_out, y_out, tool_num])

    #     if k2 == 1:
    #         xy_data.append([x_out+start_offset[k2, 0], y_out +
    #                        start_offset[k2, 1], tool_num])

    #     k2 = k2 + 1
    ################### -----------改寫#################
   # x-dir part
    partgap = 200
    for y in range(int(column_rect)*2):

        x_start = (L_tool/2 - 1) + sp1[0]  # 啟始點
        y_start = w_tool/2 + sp1[1]-y/2*(H+partgap)-y % 2*(H)
        for i in range(int(row_rect)):

            x_start = x_start+partgap
            xy_data.append([x_start, y_start, tool_num])  # 外邊緣開始工作的第一點

            a = L - (L_tool-2)
            b = H - (w_tool-2)

            while a > 0:
                a_pre = a  # 記錄前一次加工程剩餘的長度
                a = a - (L_tool - 1)  # 這次加工後剩餘的長度

                if a < 0:  # a剩餘長度最少為0
                    a = 0

                # 記錄水平路徑和；(a_pre - a)永遠為正
                h_track_out = h_track_out + (a_pre - a)

                h_line_hit_out = h_line_hit_out + 1  # 記錄水平打多少下

                last_xy_data = xy_data[(len(xy_data)-1)]
                x_out = last_xy_data[0] + wd[k2, 0] * (a_pre - a)  # 記錄此時加工的點位
                y_out = last_xy_data[1]

                xy_data.append([x_out, y_out, tool_num])

    # # y-dir part
    # tool_num = ch_tool(90, tool)  # 取刀具的資料
    # L_tool = tool[tool_num, 0]
    # w_tool = tool[tool_num, 1]
    # print(L_tool, w_tool)
    # x_start = (L_tool/2 - 1) + sp1[0]  # 啟始點
    # y_start = w_tool/2 + sp1[1]

    # for i in range(int(row_rect)*2):
    #     x_start = (L_tool/2 - 1) + sp1[0]+i/2*(L+partgap)+i % 2*(L)  # 啟始點
    #     y_start = w_tool/2 + sp1[1]

    #     for y in range(int(column_rect)-1):
    #         y_start = y_start-partgap
    #         xy_data.append([x_start, y_start, tool_num])  # 外邊緣開始工作的第一點

    #         a = L - (L_tool-2)
    #         b = H - (w_tool-2)

    #         while b > 0:  # 長跟高不一定一樣，所以分兩個迴圈做
    #             b_pre = b  # 記錄前一次加工程剩餘的長度
    #             b = b - (w_tool - 1)  # 這次加工後剩餘的長度

    #             if b < 0:  # a剩餘長度最少為0
    #                 b = 0

    #             # 記錄水平路徑和；(b_pre - b)永遠為正
    #             v_track_out = v_track_out + (b_pre - b)

    #             v_line_hit_out = v_line_hit_out + 1  # 記錄水平打多少下

    #             last_xy_data = xy_data[(len(xy_data)-1)]
    #             x_out = last_xy_data[0]  # 記錄此時加工的點位
    #             y_out = last_xy_data[1] + wd[1, 1] * (b_pre - b)
    #             xy_data.append([x_out, y_out, tool_num])

    return xy_data, h_track_out, v_track_out, hpm_out, vpm_out, h_line_hit_out, v_line_hit_out

############ outside edge end ##############

################# Rect+Shear calc ##############


def Rect(L, H, sp1, L_hole, H_hole, degree, column, row, x_gap, y_gap, sp2, row_rect, column_rect):

    # hole_xy, h_track, v_track = hole(L_hole, H_hole, degree)  # hole

    # hole_xy = hole_array(column, row, x_gap, y_gap, L_hole,
    #                      H_hole, hole_xy)  # hole_array

    # xy_data = hole_array_rotate(hole_xy, sp2, degree)  # hole_array_rotate

    # h_t_out=h_track_out || v_t_out=v_track_out
    xy_data, h_t_out, v_t_out, hpm_out, vpm_out, h_lhit_out, v_lhit_out = outside_edge(
        L, H, sp1, row_rect, column_rect)  # outside_edge

    num = str(int(column * row))
    case_in = "Rect+shear-"+str(int(L))+"x"+str(int(H)) + \
        "-"+str(int(L_hole))+"x"+str(int(H_hole))+","+num
    theta = degree * np.pi / 180

    # hit data
    h_line_hit = h_lhit_out
    v_line_hit = v_lhit_out
    single_hit = 0
    nibbling_hit = 0
    #shear_hit = len(hole_xy)
    shear_hit = 0

    # part move
    hpm = hpm_out
    vpm = vpm_out

    # in between move
    h_inbtwn = h_t_out
    v_inbtwn = v_t_out
    # h_shearbtwn = (h_track * abs(math.cos(theta)) + v_track *
    #                abs(math.sin(theta))) * column * row
    # v_shearbtwn = (h_track * abs(math.sin(theta)) + v_track *
    #                abs(math.cos(theta))) * column * row
    h_shearbtwn = 0
    v_shearbtwn = 0
    # 假設刀盤可裝36把刀(每把間隔10度)，Rect+Shear只需要兩把刀即可完成
    tool_change_deg = (len(tool)-1) * 10

    data.append([case_in, h_line_hit, v_line_hit, single_hit, nibbling_hit, shear_hit, hpm, vpm,
                 h_inbtwn, v_inbtwn, h_shearbtwn, v_shearbtwn, tool_change_deg
                 ])
    return data, xy_data

############### Rect+Shear calc end ############

################### graph ######################


def graph(xy_data):

    num = len(xy_data)  # 刀具總共停留在多少個地方

    graph_data = []
    graph_data.append([2, 0, 0, 0, num, 0, 0])
    # version1, version2, # circle, # triangle, # rectangle, # polygon, # loop,
    graph_data.append([0, 0, 0])
    #gID, gType, loopID
    graph_data.append([0, 0, 1200, 800, 4, 0.95, 2, 0.2, 0.062])
    # table off(x,y), sheet-size(x, y), start(edge,par), end(edge,par), thickness

    for k1 in range(num):

        graph_data.append([";gID", "gType", "iUserSetID", "parentID",
                          "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF"])
        graph_data.append([k1, 30, k1, 0, 0, 0, 1, 1])

        single_p = xy_data[k1]
        theta = 30 * np.pi / 180
        trans_array = np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        # 旋轉矩陣

        theta = 30 * np.pi / 180  # 將角度轉為徑度制
        tool_s_0deg = np.zeros([2, 4])  # 較小的刀
        tool_s_0deg[0] = [-5, 5, 5, -5]
        tool_s_0deg[1] = [-1, -1, 1, 1]

        tool_30trans = np.matmul(trans_array, tool_s_0deg)  # 乘上旋轉矩陣

        tool_b = np.zeros([2, 4])
        tool_b[0] = [-10, 10, 10, -10]
        tool_b[1] = [-2, -2, 2, 2]

        if str(single_p[2]) == '1':

            single_p_gra = []

            for k2 in range(4):

                x_point = single_p[0] + tool_30trans[0][k2] + 600
                y_point = single_p[1] + tool_30trans[1][k2] + 700
                single_p_gra.append(x_point)
                single_p_gra.append(y_point)

            graph_data.append(single_p_gra)
        else:
            single_p_gra = []

            for k2 in range(4):
                x_point = single_p[0] + tool_b[0][k2] + 600
                y_point = single_p[1] + tool_b[1][k2] + 700
                single_p_gra.append(x_point)
                single_p_gra.append(y_point)
            graph_data.append(single_p_gra)

    return graph_data

################## graph end ###################

########################## main #########################


data = []
data.append([" ", "horizontal line hit", "vertical line hit", "single hit", "nibbling hit",
             "shear hit", "horizontal part move", "vertical part move", "horizontal tool in-btwn move",
             "vertical tool in-btwn move", "horizontal tool shear in-btwn move",
             "vertical tool shear in-btwn move", "turret tool change deg"
             ])

######## Rect+Shear #######

print("Rect + Shear part\n")

tool = np.zeros([4, 3])
tool[0, :] = [10, 2, 0]
tool[2, :] = [10, 2, 90]
tool[1, :] = [10, 2, 30]
tool_expend = np.zeros(([len(tool), 2, 4]))
tool_expend = tool_expension(tool, tool_expend)

in_variable_rs = np.zeros([1, 14])                       # input variable
in_variable_rs[0, :] = [50, 30, 50, -50, 25, 25, 1, 1, 75, -130, 10, 10, 2, 2]
# in_variable_rs[1, :] = [500, 500, 50, -50, 25, 25, 1, 3, 75, -130, 10, 10]
# in_variable_rs[2, :] = [500, 500, 50, -50, 25, 50, 1, 1, 75, -130, 10, 10]
# in_variable_rs[3, :] = [500, 500, 50, -50, 25, 50, 1, 3, 75, -130, 10, 10]
# in_variable_rs[4, :] = [500, 500, 50, -50, 25, 50, 2, 3, 75, -130, 10, 10]
# in_variable_rs[5, :] = [500, 500, 50, -50, 100, 75, 1, 2, 130, -200, 10, 10]
# in_variable_rs[6, :] = [500, 500, 50, -50, 100, 75, 2, 2, 130, -200, 10, 10]
# in_variable_rs[7, :] = [500, 500, 50, -50, 100, 75, 2, 4, 75, -300, 10, 10]


for k in range(len(in_variable_rs)):

    xy_data = []
    xy_data.append([0, 0, -1])

    L = in_variable_rs[k, 0]
    H = in_variable_rs[k, 1]
    L_hole = in_variable_rs[k, 4]
    H_hole = in_variable_rs[k, 5]
    degree = 30

    row_hole = in_variable_rs[k, 6]
    column_hole = in_variable_rs[k, 7]

    row_rect = in_variable_rs[k, 12]
    column_rect = in_variable_rs[k, 13]
    x_gap = in_variable_rs[k, 10]
    y_gap = in_variable_rs[k, 11]

    sp1 = [in_variable_rs[k, 2], in_variable_rs[k, 3]]
    sp2 = [in_variable_rs[k, 8], in_variable_rs[k, 9]]

    overlap = 1

    print(f'case{k+1} - {L:3.0f}x{H:3.0f} + {L_hole:3.0f}x{H_hole:2.0f}-{row_hole:1.0f}x{column_hole:1.0f}')

    data, xy_data = Rect(
        L, H, sp1, L_hole, H_hole, degree, column_hole, row_hole, x_gap, y_gap, sp2, row_rect, column_rect)

    graphic_data = graph(xy_data)

    k_str = str(k+1)
    path = 'sample' + k_str + '_xy.txt'
    with open(path, 'w', newline='') as txtfile:
        writer = csv.writer(txtfile)
        writer.writerows(graphic_data)

######## Rect+Shear end #######

path = 'sample1.csv'
with open(path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

'''
path = 'sample1_xy.csv'
with open(path ,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(xy_data)
'''
