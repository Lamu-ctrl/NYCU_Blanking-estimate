import all_type_20230405 as main
import numpy as np
import math

station = np.zeros([10, 3])  # 刀具規格[長, 寬, 角度]
station[0, :] = [20, 4,  0]
station[1, :] = [10, 2, 30]
station[2, :] = [10, 2, 45]
station[3, :] = [10, 2, 60]
station[4, :] = [20, 4, 90]
station[5, :] = [10, 2, 120]
station[6, :] = [10, 2, 135]
station[7, :] = [10, 2, 150]
station[8, :] = [10, 10, 0]
station[9, :] = [2.5, 0, -1]  # 角度-1設為圓刀([半徑, 0, -1])


class part:
    Data = []

    def __init__(self, geometry) -> None:
        self.gID = geometry.gID
        self.contour = [geometry]
        self.hole = []
        self.data = []
        print("create Part _ with contour ",
              self.contour)

    def add_hole(self, geometry):
        self.hole.append(geometry)
        print("add hole _ in part ", geometry)

    def toFuntion(self):
        print("inside class Part to funtion")
        # contour
        for ele in self.contour:
            print("contour")
            self.data.extend(ele.toFuntion(0))

        # hole

        for ele in self.hole:
            print("hole")
            if ele != None:
                self.data.extend(ele.toFuntion(1))

        # 記錄到class part.Data
        self.Data.extend(self.data)
        pass

################## geometry class#


class RECTANGLE2D:
    Data = []

    def __init__(self, row1, row2) -> None:
        self.gID = row1[0]
        self.gType = row1[1]
        self.iUserSetID = row1[2]
        self.parentID = row1[3]
        self.rotmiliDeg = row1[4]
        self.iAppRef = row1[5]
        self.iCamAttr = row1[6]
        self.iRevEngF = row1[7]
        self.x1 = row2[0]
        self.y1 = row2[1]
        self.x2 = row2[2]
        self.y2 = row2[3]
        self.x3 = row2[4]
        self.y3 = row2[5]
        self.x4 = row2[6]
        self.y4 = row2[7]
        self.x_point = [row2[0], row2[2], row2[4], row2[6]]
        self.y_point = [row2[1], row2[3], row2[5], row2[7]]
        self.data = []
        j = 0
        for k1 in range(4):
            if (self.x_point[k1] == min(self.x_point)) & (j == 0):
                a = k1
                j = 1
            elif (self.x_point[k1] == min(self.x_point)) & (j == 1):
                if self.y_point[k1] > self.y_point[a]:
                    a = k1
            self.start_p = [self.x_point[a], self.y_point[a]]

            self.L = max(self.x_point) - min(self.x_point)
            self.H = max(self.y_point) - min(self.y_point)
            # row_arr = 1
            # col_arr = 1
        print("create Rectangel : ", "gID",
              self.gID, self.x_point, self.y_point)

    def toFuntion(self, ishole):
        print("Call Rect2D FUNTION", self.gID)
        res = []
        #rect_var.append([L, H, rect_start_p, parentID, onerow_data[6]])
        degree = 0
        if ishole == 0:
            rect_xy, h_t_out, v_t_out, hpm_out, vpm_out, h_lhit_out, v_lhit_out = main.rect_outside_edge(
                self.L, self.H, self.start_p, station)
            for j1 in range(len(rect_xy)):
                j2 = rect_xy[j1]
                res.append(j2)

        else:
            hole_xy_data, h_track, v_track = main.rect_hole(
                self.L, self.H, degree, self.start_p, self.iCamAttr)
            for j1 in range(len(hole_xy_data)):
                j2 = hole_xy_data[j1]
                res.append(j2)
        # print(res)
        self.data.extend(res)
        self.Data.extend(self.data)
        return res


class CIRCLE2D:
    Data = []

    def __init__(self, row1, row2) -> None:
        self.gID = row1[0]
        self.gType = row1[1]
        self.loopID = row1[2]
        self.parentID = row1[3]
        self.ccw = row1[4]
        self.segCt = row1[5]
        self.iAppRef = row1[6]
        self.iCamAttr = row1[7]
        self.iRevEngF = row1[8]
        self.radius = row2[0]
        self.start_at_degrees = row2[1]
        self.centerX = row2[2]
        self.centerY = row2[3]
        self.data = []

        print("create CIRCLE2D : ", "gID", self.gID,
              self.radius, self.centerX, self.centerY)

    def toFuntion(self, ishole):
        # ; radius, start_at_degrees, centerX, centerY, parentID , icamattr
        # 50.0, 0., 100.0, 100.0,
        res = []
        cir_xy, h_track_cir, v_track_cir, single_hit_cir, nib_hit_cir, cir_hpm, cir_vpm = main.circle(
            self.radius, self.start_at_degrees, self.centerX, self.centerY, self.parentID, station, self.iCamAttr)
        for j1 in range(len(cir_xy)):
            j2 = cir_xy[j1]
            res.append(j2)
        # circle(self.radius, self.start_at_degrees,self.centerX, self.centerY, self.parentID, tool)
        print("Call CIRCLE FUNTION", self.gID)
        print(len(res))

        self.data.extend(res)
        self.Data.extend(self.data)
        # print("data", len(self.data))
        return res


class POLYGON2D:
    #     ; POLYGON2D
    # ; gID, gType, loopID, parentID, nvtx, iAppRef, iCamAttr, iRevEngF,
    # 5, 34, 5, 0, 6, 0, 39, 1,
    # ; x1, y1, x2, y2, x3, y3, x4, y4, ; 8 doubles per line
    # 500.0, 300.0, 550.0, 450.0, 500.0, 500.0, 350.0, 430.0,
    # ; x5, y5, x6, y6,
    # 200.0, 410.0, 330, 295.0,
    Data = []

    def __init__(self, row1, rows) -> None:
        # rows may contain many row depend on nvtx
        self.subElemnt = []
        self.gID = row1[0]
        self.gType = row1[1]
        self.loopID = row1[2]
        self.parentID = row1[3]
        self.nvtx = row1[4]
        self.iAppRef = row1[5]
        self.iCamAttr = row1[6]
        self.iRevEngF = row1[7]
        self.data = []
        self.x_points = []
        self.y_points = []
        for row in rows:
            counter = 0
            for ele in row:
                if counter % 2 == 0:
                    self.x_points.append(float(ele))
                else:
                    self.y_points.append(float(ele))

                counter += 1

        print("create POLYGON2D : ", "gID",
              self.gID, self.x_point, self.y_point)

    def toFuntion(self, ishole):
        # circle(self.radius, self.start_at_degrees,
        #        self.centerX, self.centerY, self.parentID, tool)
        print("Call POLYGON2D FUNTION", self.gID)
        pass


class TRIANGLE2D:
    # ; TRIANGLE2D
    # ; gID, gType, iUserSetID, parentID, rotmiliDeg, iAppRef, iCamAttr, iRevEngF,
    # 6, 29, 6, 0, 0, 0, 16, 1,
    # ; x1, y1, x2, y2, x3, y3,
    # 700.0, 150.0, 850.0, 120.0, 600.0, 300.0,
    Data = []

    def __init__(self, row1, row2) -> None:
        self.gID = row1[0]
        self.gType = row1[1]
        self.loopiUserSetID = row1[2]
        self.parentID = row1[3]
        self.rotmiliDeg = row1[4]
        self.iAppRef = row1[5]
        self.iCamAttr = row1[6]
        self.iRevEngF = row1[7]
        self.x_point = [row2[0], row2[2], row2[4]]
        self.y_point = [row2[1], row2[3], row2[5]]
        self.data = []
        print("create TRIANGLE2D : ", "gID",
              self.gID, self.x_point, self.y_point)

    def toFuntion(self, ishole):
        print("Call TRIANGLE2D FUNTION", self.gID)
        pass


class COMPOSITE2DLOOP:
    Data = []

    def __init__(self, row1, rows) -> None:
        # rows may contain many row depend on nvtx
        self.gID = row1[0]
        self.gType = row1[1]
        self.iUserSetID = row1[2]
        self.parentID = row1[3]
        self.numEdge = row1[4]
        self.close = row1[5]
        self.iAppRef = row1[6]
        self.iCamAttr = row1[7]
        self.iRevEngF = row1[8]
        self.data = []
        self.subElemnt = []
        for i in range(len(rows)):
            if rows[i][1] == 12:  # line
                ele = LINE(rows[i], rows[i+1])
                self.subElemnt.append(ele)
            elif rows[i][1] == 14:  # arc
                ele = ARC(rows[i], rows[i+1])
                self.subElemnt.append(ele)
            i += 2
        print("create COMPOSITE2DLOOP : ", "gID",
              self.gID)
        print("self.subElemnt", self.subElemnt)

    def toFuntion(self, ishole):
        # circle(self.radius, self.start_at_degrees,
        #        self.centerX, self.centerY, self.parentID, tool)
        print("Call COMPOSITE2DLOOP FUNTION", self.gID)
        for ele in self.subElemnt:
            self.data.extend(ele.toFuntion(ishole))
        return self.data


class RECTANGLE2D_IN_GRID:
    Data = []

    def __init__(self, row1, row2, row3) -> None:
        self.gID = row1[0]
        self.gType = row1[1]
        self.iUserSetID = row1[2]
        self.parentID = row1[3]
        self.rotmiliDeg = row1[4]
        self.iAppRef = row1[5]
        self.iCamAttr = row1[6]
        self.iRevEngF = row1[7]
        self.x1 = float(row2[0])
        self.y1 = row2[1]
        self.x2 = row2[2]
        self.y2 = row2[3]
        self.x3 = row2[4]
        self.y3 = row2[5]
        self.x4 = row2[6]
        self.y4 = row2[7]
        self.x_point = [row2[0], row2[2], row2[4], row2[6]]
        self.y_point = [row2[1], row2[3], row2[5], row2[7]]
        self.x0 = row3[0]
        self.y0 = row3[1]
        self.xGap = row3[2]
        self.numInX = row3[3]
        self.yGap = row3[4]
        self.numInY = row3[5]
        self.style = row3[6]
        self.data = []
        print("create RECTANGLE2D_IN_GRID : ", "gID",
              self.gID, self.x_point, self.y_point)

    def toFuntion(self, ishole):
        #rect_var.append([L, H, rect_grid_xy, parentID, onerow_data[6]])
        pass


class LINE:
    Data = []

    def __init__(self, row1, row2) -> None:
        # rows may contain many row depend on nvtx
        self.gID = row1[0]
        self.gType = row1[1]
        # self.loopID = row1[2]
        # poly不會帶parentId
        self.parentID = 0
        # self.nvtx = row1[4]
        # self.iAppRef = row1[5]
        # self.iCamAttr = row1[6]
        # self.iRevEngF = row1[7]
        self.x1 = row2[0]
        self.y1 = row2[1]
        self.x2 = row2[2]
        self.y2 = row2[3]
        self.dis = math.sqrt((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)
        self.data = []
        self.deg = None
        # if (self.x2 != self.x1):
        #     # 用math.atan反三角正切取到角度值
        #     self.deg = math.atan((self.y2 - self.y1) /
        #                          (self.x2 - self.x1))
        #     if self.deg < 0:
        #         self.deg = self.deg + 2*math.pi  # tan的定義域在-0.5pi~0.5pi，而我想得到的是 0~2pi，剩餘的下面判別
        #     elif (self.deg == 0) & ((self.x1 - self.x2) > 0):
        #         self.deg = math.pi
        if (self.x2 - self.x1) == 0:
            self.deg = 0
        else:
            self.deg = math.atan((self.y2 - self.y1) /
                                 (self.x2 - self.x1))
        if self.deg < 0:
            self.deg = self.deg + 2*math.pi  # tan的定義域在-0.5pi~0.5pi，而我想得到的是 0~2pi，剩餘的下面判別
        elif (self.deg == 0) & ((self.x1 - self.x2) > 0):
            self.deg = math.pi

        print("create LINE : ", "gID",
              self.gID)

    def toFuntion(self, ishole):
        print("Call Line FUNTION", self.gID)
        #line(line_start_x, line_start_y, distance, line_deg, tool, offset_index)

        # all_line = []
        # for k2 in range(len(line_var)):
        #     one_line_var = line_var[k2]
        #     line_start_x = one_line_var[0]
        #     line_start_y = one_line_var[1]
        #     distance = one_line_var[2]
        #     line_deg = one_line_var[3]
        #     offset_index = one_line_var[4] #parentID
        res = []
        line_xy, line_h_track, line_v_track, line_h_shearbwn, line_v_shearbwn, h_line_hit,\
            v_line_hit, line_single_hit, line_shear_hit, line_nib_hit\
            = main.line(self.x1, self.y1, self.dis, self.deg, station, self.parentID)

        for j1 in range(len(line_xy)):
            j2 = line_xy[j1]
            res.append(j2)

        self.data.extend(res)
        self.Data.extend(self.data)
        return self.data
        pass


class ARC:
    Data = []
    #     ; POLYGON2D
    # ; gID, gType, loopID, parentID, nvtx, iAppRef, iCamAttr, iRevEngF,
    # 5, 34, 5, 0, 6, 0, 39, 1,
    # ; x1, y1, x2, y2, x3, y3, x4, y4, ; 8 doubles per line
    # 500.0, 300.0, 550.0, 450.0, 500.0, 500.0, 350.0, 430.0,
    # ; x5, y5, x6, y6,
    # 200.0, 410.0, 330, 295.0,

    def __init__(self, row1, row2) -> None:
        # rows may contain many row depend on nvtx
        self.gID = row1[0]
        self.gType = row1[1]
        self.CCW = row1[2]
        self.segCt = row1[3]
        # self.loopID = row1[2]
        self.parentID = 0
        # self.nvtx = row1[4]
        # self.iAppRef = row1[5]
        # self.iCamAttr = row1[6]
        # self.iRevEngF = row1[7]
        self.data = []
        self.x1 = row2[0]
        self.y1 = row2[1]
        self.xc = row2[2]
        self.yc = row2[3]
        self.x2 = row2[4]
        self.y2 = row2[5]
        self.radius = row2[6]
        self.degrees = row2[7]*math.pi/180
        self.star_deg = None
        self.orientation = (self.CCW*2-1)  # 將方向變成 1代表ccw, -1代表cw
        if (self.xc != self.x1):
            self.star_deg = math.atan(
                (self.y1 - self.yc) / (self.x1 - self.xc))
            if (self.y1 == self.yc):  # 起點在正x軸
                if self.x1 > self.xc:
                    self.star_deg = 0
                else:  # 起點在負x軸
                    self.star_deg = math.pi

            elif (self.y1 > self.yc) & (self.star_deg < 0):  # 起點在第二象限
                self.star_deg = self.star_deg + math.pi

            elif (self.y1 < self.yc) & (self.star_deg > 0):  # 起點在第三象限
                self.star_deg = self.star_deg + math.pi

            elif (self.y1 < self.yc) & (self.star_deg < 0):  # 起點在第四象限
                self.star_deg = self.star_deg + math.pi*2

        elif (self.y1 > self.yc):  # 起點在正y軸
            self.star_deg = math.pi/2
        else:  # 起點在負y軸
            self.star_deg = math.pi*3/2

        print("create ARC : ", "gID",
              self.gID)

    def toFuntion(self, ishole):
        print("Call ARC FUNTION", self.gID)
        # for k4 in range(len(arc_var)):
        #     one_arc_var = arc_var[k4]

        #     cen_x = one_arc_var[0]
        #     cen_y = one_arc_var[1]
        #     radius = one_arc_var[2]
        #     star_deg = one_arc_var[3]
        #     working_deg = one_arc_var[4]
        #     orientation = one_arc_var[5]
        #     parentID = one_arc_var[6]

        #     for j1 in range(len(arc_xy)):
        #         j2 = arc_xy[j1]
        #         all_arc.append(j2)
        res = []
        arc_xy, nib_hit_arc = main.arc(
            self.xc, self.yc, self.radius, self.star_deg, self.degrees, self.orientation, self.parentID, station)
        for j1 in range(len(arc_xy)):
            j2 = arc_xy[j1]
            res.append(j2)

        self.data.extend(res)
        self.Data.extend(self.data)

        return self.data
        pass
