
class part:
    def __init__(self, geometry) -> None:
        self.contour = [geometry]
        self.gID = geometry.gID
        self.hole = []

        print("create Part _ with contour ",
              self.contour)

    def hole(self, geometry):
        self.hole.append(geometry)
        pass

    def toFuntion():
        pass

################## geometry class#


class RECTANGLE2D:
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

    def toFuntion():
        pass


class CIRCLE2D:

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

        print("create CIRCLE2D : ", "gID", self.gID,
              self.radius, self.centerX, self.centerY)

    def toFuntion(self):
        circle(self.radius, self.start_at_degrees,
               self.centerX, self.centerY, self.parentID, tool)
        print("Call CIRCLE FUNTION", self.gID)
        pass


class POLYGON2D:
    #     ; POLYGON2D
    # ; gID, gType, loopID, parentID, nvtx, iAppRef, iCamAttr, iRevEngF,
    # 5, 34, 5, 0, 6, 0, 39, 1,
    # ; x1, y1, x2, y2, x3, y3, x4, y4, ; 8 doubles per line
    # 500.0, 300.0, 550.0, 450.0, 500.0, 500.0, 350.0, 430.0,
    # ; x5, y5, x6, y6,
    # 200.0, 410.0, 330, 295.0,
    def __init__(self, row1, rows) -> None:
        # rows may contain many row depend on nvtx
        self.gID = row1[0]
        self.gType = row1[1]
        self.loopID = row1[2]
        self.parentID = row1[3]
        self.nvtx = row1[4]
        self.iAppRef = row1[5]
        self.iCamAttr = row1[6]
        self.iRevEngF = row1[7]

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

    def toFuntion(self):
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

        print("create TRIANGLE2D : ", "gID",
              self.gID, self.x_point, self.y_point)

    def toFuntion(self):
        print("Call TRIANGLE2D FUNTION", self.gID)
        pass


class COMPOSITE2DLOOP:

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

        self.subElemnt = []
        print("create COMPOSITE2DLOOP : ", "gID",
              self.gID)

    def toFuntion(self):
        # circle(self.radius, self.start_at_degrees,
        #        self.centerX, self.centerY, self.parentID, tool)
        print("Call COMPOSITE2DLOOP FUNTION", self.gID)
        pass


class RECTANGLE2D_IN_GRID:
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

        print("create RECTANGLE2D_IN_GRID : ", "gID",
              self.gID, self.x_point, self.y_point)

    def toFuntion():
        pass
