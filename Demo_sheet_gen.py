import math
import numpy as np
import csv
import random

################## produce_sheet ###################

def produce_sheet():
    
    sheet_graph = []
    sheet_graph.append(["; SYSCONFIG"])
    sheet_graph.append(["; version", "unit flag", "draw speed"])
    sheet_graph.append(["; 2.1", "0(mks) 1(fbs)", "(%)"])
    sheet_graph.append([201, 0, 10, 0, 0, 0, 0, 0, 0, 0,])
    sheet_graph.append([";"])
    sheet_graph.append(["; SYS INT DATA"])
    sheet_graph.append(["; nibble", "nibble", "rect", "shear", "hit1", "hit2", "hit3", "not used"])
    sheet_graph.append(["; arc", "line", "4side", "line", "one", "2nd", "3rd"])
    sheet_graph.append([10, 10, 20, 40, 20, 15, 15, 0, 0, 0])
    sheet_graph.append(["; screw", "tap", "louver", "form", "turret", "not used",])
    sheet_graph.append(["; 1", "1", "1", "4", "rot 90",])
    sheet_graph.append([600, 100, 200, 100, 500, 0, 0, 0, 0, 0])
    sheet_graph.append([5, 10, 5, 10, 10, 20, 0, 0, 0, 0])
    sheet_graph.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    sheet_graph.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    sheet_graph.append([";"])
    sheet_graph.append(["; SYS DBL DATA"])
    sheet_graph.append(["; operation time in sec", "distance in meter - unless specified otherwise"])
    sheet_graph.append(["; Vx m/s", "Vy m/s", "Ax m/s2", "Ay m/s2, not used"])
    sheet_graph.append([8, 10, 20, 30, 0., 0., 0., 0., 0., 0.])
    sheet_graph.append(["; not used"])
    sheet_graph.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    sheet_graph.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    sheet_graph.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    sheet_graph.append(["; gID", "gType", "loopID"])
    sheet_graph.append([0, 0, 0])
    sheet_graph.append(["; table off(x", "y)", "sheet size(x", "y)", "start(edge", "par)", "end(edge", "par)", "thickness"])
    sheet_graph.append([0, 0, 4000, 2000, 4, 0.95, 2, 0.2, 0.062])
    sheet_graph.append(["; "])
    gID = 3 # gID begin from 3
    
    # Shape-B
    for B_idx in range(2):
        x_start = 100 + 1200
        y_start = 100 + B_idx * 450
        sheet_graph.append(["; ", "COMPOSITE2DLOOP"])
        sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "numEdge", "close", "iAppRef", "iCamAttr", "iRevEngF"])
        sheet_graph.append([gID, 31, gID, 0, 52, 0, 0, 0, 1])
        sheet_graph.append([gID*1000+1, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 1
        sheet_graph.append([x_start, y_start + 60, x_start + 20, y_start + 60])
        sheet_graph.append([gID*1000+2, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 2
        sheet_graph.append([x_start + 20, y_start + 60, x_start + 20, y_start + 50])
        sheet_graph.append([gID*1000+3, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 3
        sheet_graph.append([x_start + 20, y_start + 50, x_start + 100, y_start + 50])
        sheet_graph.append([gID*1000+4, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 4
        sheet_graph.append([x_start + 100, y_start + 50, x_start + 100, y_start])
        sheet_graph.append([gID*1000+5, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 5
        sheet_graph.append([x_start + 100, y_start, x_start + 165, y_start])
        sheet_graph.append([gID*1000+6, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 6
        sheet_graph.append([x_start + 165, y_start, x_start + 165, y_start + 50])
        sheet_graph.append([gID*1000+7, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 7
        sheet_graph.append([x_start + 165, y_start + 50, x_start + 170, y_start + 50])
        sheet_graph.append([gID*1000+8, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 8
        sheet_graph.append([x_start + 170, y_start + 50, x_start + 170, y_start])
        sheet_graph.append([gID*1000+9, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 9
        sheet_graph.append([x_start + 170, y_start, x_start + 240, y_start])
        sheet_graph.append([gID*1000+10, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 10
        sheet_graph.append([x_start + 240, y_start, x_start + 240, y_start + 50])
        sheet_graph.append([gID*1000+11, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 11
        sheet_graph.append([x_start + 240, y_start + 50, x_start + 260, y_start + 50])
        sheet_graph.append([gID*1000+12, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 12
        sheet_graph.append([x_start + 260, y_start + 50, x_start + 260, y_start])
        sheet_graph.append([gID*1000+13, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 13
        sheet_graph.append([x_start + 260, y_start, x_start + 330, y_start])
        sheet_graph.append([gID*1000+14, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 14
        sheet_graph.append([x_start + 330, y_start, x_start + 330, y_start + 50])
        sheet_graph.append([gID*1000+15, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 15
        sheet_graph.append([x_start + 330, y_start + 50, x_start + 335, y_start + 50])
        sheet_graph.append([gID*1000+16, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 16
        sheet_graph.append([x_start + 335, y_start + 50, x_start + 335, y_start])
        sheet_graph.append([gID*1000+17, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 17
        sheet_graph.append([x_start + 335, y_start, x_start + 400, y_start])
        sheet_graph.append([gID*1000+18, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 18
        sheet_graph.append([x_start + 400, y_start, x_start + 400, y_start + 50])
        sheet_graph.append([gID*1000+19, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 19
        sheet_graph.append([x_start + 400, y_start + 50, x_start + 480, y_start + 50])
        sheet_graph.append([gID*1000+20, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 20
        sheet_graph.append([x_start + 480, y_start + 50, x_start + 480, y_start + 60])
        sheet_graph.append([gID*1000+21, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 21
        sheet_graph.append([x_start + 480, y_start + 60, x_start + 500, y_start + 60])
        sheet_graph.append([gID*1000+22, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 22
        sheet_graph.append([x_start + 500, y_start + 60, x_start + 500, y_start + 140])
        sheet_graph.append([gID*1000+23, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 23
        sheet_graph.append([x_start + 500, y_start + 140, x_start + 450, y_start + 140])
        sheet_graph.append(["; edgeID", "gType", "CCW", "segCt"])
        sheet_graph.append([gID*1000+24, 14, 0, 15])        # 24
        sheet_graph.append(["; x1"," y1"," xc"," yc"," x2"," y2"," radius"," degrees"])
        sheet_graph.append([x_start + 450, y_start + 140, x_start + 450, y_start + 150, x_start + 450, y_start + 160, 10, -180])
        sheet_graph.append([gID*1000+25, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 25
        sheet_graph.append([x_start + 450, y_start + 160, x_start + 500, y_start + 160])
        sheet_graph.append([gID*1000+26, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 26
        sheet_graph.append([x_start + 500, y_start + 160, x_start + 500, y_start + 240])
        sheet_graph.append([gID*1000+27, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 27
        sheet_graph.append([x_start + 500, y_start + 240, x_start + 480, y_start + 240])
        sheet_graph.append([gID*1000+28, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 28
        sheet_graph.append([x_start + 480, y_start + 240, x_start + 480, y_start + 250])
        sheet_graph.append([gID*1000+29, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 29
        sheet_graph.append([x_start + 480, y_start + 250, x_start + 400, y_start + 250])
        sheet_graph.append([gID*1000+30, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 30
        sheet_graph.append([x_start + 400, y_start + 250, x_start + 400, y_start + 300])
        sheet_graph.append([gID*1000+31, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 31
        sheet_graph.append([x_start + 400, y_start + 300, x_start + 335, y_start + 300])
        sheet_graph.append([gID*1000+32, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 32
        sheet_graph.append([x_start + 335, y_start + 300, x_start + 335, y_start + 250])
        sheet_graph.append([gID*1000+33, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 33
        sheet_graph.append([x_start + 335, y_start + 250, x_start + 330, y_start + 250])
        sheet_graph.append([gID*1000+34, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 34
        sheet_graph.append([x_start + 330, y_start + 250, x_start + 330, y_start + 300])
        sheet_graph.append([gID*1000+35, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 35
        sheet_graph.append([x_start + 330, y_start + 300, x_start + 260, y_start + 300])
        sheet_graph.append([gID*1000+36, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 36
        sheet_graph.append([x_start + 260, y_start + 300, x_start + 260, y_start + 250])
        sheet_graph.append([gID*1000+37, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 37
        sheet_graph.append([x_start + 260, y_start + 250, x_start + 240, y_start + 250])
        sheet_graph.append([gID*1000+38, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 38
        sheet_graph.append([x_start + 240, y_start + 250, x_start + 240, y_start + 300])
        sheet_graph.append([gID*1000+39, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 39
        sheet_graph.append([x_start + 240, y_start + 300, x_start + 170, y_start + 300])
        sheet_graph.append([gID*1000+40, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 40
        sheet_graph.append([x_start + 170, y_start + 300, x_start + 170, y_start + 250])
        sheet_graph.append([gID*1000+41, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 41
        sheet_graph.append([x_start + 170, y_start + 250, x_start + 165, y_start + 250])
        sheet_graph.append([gID*1000+42, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 42
        sheet_graph.append([x_start + 165, y_start + 250, x_start + 165, y_start + 300])
        sheet_graph.append([gID*1000+43, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 43
        sheet_graph.append([x_start + 165, y_start + 300, x_start + 100, y_start + 300])
        sheet_graph.append([gID*1000+44, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 44
        sheet_graph.append([x_start + 100, y_start + 300, x_start + 100, y_start + 250])
        sheet_graph.append([gID*1000+45, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 45
        sheet_graph.append([x_start + 100, y_start + 250, x_start + 20, y_start + 250])
        sheet_graph.append([gID*1000+46, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 46
        sheet_graph.append([x_start + 20, y_start + 250, x_start + 20, y_start + 240])
        sheet_graph.append([gID*1000+47, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 47
        sheet_graph.append([x_start + 20, y_start + 240, x_start, y_start + 240])
        sheet_graph.append([gID*1000+48, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 48
        sheet_graph.append([x_start, y_start + 240, x_start, y_start + 160])
        sheet_graph.append([gID*1000+49, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 49
        sheet_graph.append([x_start, y_start + 160, x_start + 50, y_start + 160])
        sheet_graph.append(["; edgeID", "gType", "CCW", "segCt"])
        sheet_graph.append([gID*1000+50, 14, 0, 15])        # 50
        sheet_graph.append(["; x1"," y1"," xc"," yc"," x2"," y2"," radius"," degrees"])
        sheet_graph.append([x_start + 50, y_start + 160, x_start + 50, y_start + 150, x_start + 50, y_start + 140, 10, -180])
        sheet_graph.append([gID*1000+51, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 51
        sheet_graph.append([x_start + 50, y_start + 140, x_start, y_start + 140])
        sheet_graph.append([gID*1000+52, 12])
        sheet_graph.append(["; x1", " y1", " x2", " y2"])   # 52
        sheet_graph.append([x_start, y_start + 140, x_start, y_start + 60])
        sheet_graph.append(["; "])
        Hole_gID = gID + 1
        
        sheet_graph.append(["; CIRCLE2D ALONG A LINE"])
        sheet_graph.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
        sheet_graph.append([Hole_gID, 32, Hole_gID, gID, 1, 36, 1, 17, 1])
        sheet_graph.append(["; radius"," start_at_degrees"," centerX"," centerY"])
        sheet_graph.append([2.5, 0., x_start + 110.0, y_start + 67.5])
        sheet_graph.append(["; x0"," y0"," entity gap"," line angle"," # of entity"," style"])
        sheet_graph.append([x_start + 110.0, y_start + 67.5, 15.0, 90.0,   12,         0, ])
        sheet_graph.append(["; "])
        Hole_gID += 1
        
        sheet_graph.append(["; CIRCLE2D ALONG A LINE"])
        sheet_graph.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
        sheet_graph.append([Hole_gID, 32, Hole_gID, gID, 1, 36, 1, 17, 1])
        sheet_graph.append(["; radius"," start_at_degrees"," centerX"," centerY"])
        sheet_graph.append([2.5, 0.0, x_start + 390.0, y_start + 67.5])
        sheet_graph.append(["; x0"," y0"," entity gap"," line angle"," # of entity"," style"])
        sheet_graph.append([x_start + 390.0, y_start + 67.5, 15.0, 90.0,   12,         0, ])
        sheet_graph.append(["; "])
        Hole_gID += 1
        
        sheet_graph.append(["; ", "RECTANGLE2D IN GRID"])
        sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
        sheet_graph.append([Hole_gID, 30, Hole_gID, gID, 0, 1, 18, 1,])
        sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
        sheet_graph.append([x_start + 122.5, y_start + 65, x_start + 127.5, y_start + 65,\
                            x_start + 127.5, y_start + 70, x_start + 122.5, y_start + 70])
        sheet_graph.append(["; x0", "y0", "X gap", "# in X", "Y gap", "# in Y", "style"])
        sheet_graph.append([x_start + 122.5, y_start + 65, 15, 5, 165, 2, 10])
        sheet_graph.append(["; "])
        Hole_gID += 1
        
        sheet_graph.append(["; ", "RECTANGLE2D IN GRID"])
        sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
        sheet_graph.append([Hole_gID, 30, Hole_gID, gID, 0, 1, 18, 1,])
        sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
        sheet_graph.append([x_start + 312.5, y_start + 65, x_start + 317.5, y_start + 65,\
                            x_start + 317.5, y_start + 70, x_start + 312.5, y_start + 70])
        sheet_graph.append(["; x0", "y0", "X gap", "# in X", "Y gap", "# in Y", "style"])
        sheet_graph.append([x_start + 122.5, y_start + 65, 15, 5, 165, 2, 10])
        sheet_graph.append(["; "])
        Hole_gID += 1
        
        cir_cen = np.array([[x_start + 50, y_start + 100], [x_start + 50, y_start + 200],\
                            [x_start + 450, y_start + 100], [x_start + 450, y_start + 200]])
        for ix in range(4):
            sheet_graph.append(["; CIRCLE2D"])
            sheet_graph.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
            sheet_graph.append([Hole_gID, 32, Hole_gID, gID, 1, 36, 0, 0, 1,])
            sheet_graph.append(["; radius", "start_at_degrees", "centerX", "centerY",])
            sheet_graph.append([10, 0., cir_cen[ix, 0], cir_cen[ix, 1]])
            sheet_graph.append(["; "])
            Hole_gID += 1
        
        gID += 10
    
    
    # Shape-A
    Apos = np.array([[0, 0], [0, 450], [600, 0], [600, 450]])
    for A_idx in range(4):
        kk = 0
        x_start = 100 + Apos[A_idx, 0]
        y_start = 100 + Apos[A_idx, 1]
        
        # Part
        sheet_graph.append(["; RECTANGLE2D"])
        sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
        sheet_graph.append([gID, 30, gID, 0, 0, 0, 0, 1,])
        sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
        sheet_graph.append([x_start, y_start,\
                            x_start + 500, y_start,\
                            x_start + 500, y_start + 300,\
                            x_start, y_start + 300])
        sheet_graph.append(["; "])
        Hole_gID = gID + 1
        kk += 1
        
        # Hole
        ## 1st section
        first_row_start = [x_start + 50, y_start + 20]
        second_row_start = [x_start + 30, y_start + 30]
        rect_x = first_row_start[0]
        rect_y = first_row_start[1]
        sheet_graph.append(["; ", "RECTANGLE2D IN GRID"])
        sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
        sheet_graph.append([Hole_gID, 30, Hole_gID, gID, 0, 1, 18, 1,])
        sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
        sheet_graph.append([rect_x,      rect_y,     rect_x + 20, rect_y,\
                            rect_x + 20, rect_y + 4, rect_x,      rect_y + 4])
        sheet_graph.append(["; x0", "y0", "X gap", "# in X", "Y gap", "# in Y", "style"])
        sheet_graph.append([ rect_x, rect_y, 40,      5,        20,        5,      10])
        sheet_graph.append(["; "])
        Hole_gID += 1
        kk += 1
        
        rect_x = second_row_start[0]
        rect_y = second_row_start[1]
        sheet_graph.append(["; ", "RECTANGLE2D IN GRID"])
        sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
        sheet_graph.append([Hole_gID, 30, Hole_gID, gID, 0, 1, 18, 1,])
        sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
        sheet_graph.append([rect_x,      rect_y,     rect_x + 20, rect_y,\
                            rect_x + 20, rect_y + 4, rect_x,      rect_y + 4])
        sheet_graph.append(["; x0", "y0", "X gap", "# in X", "Y gap", "# in Y", "style"])
        sheet_graph.append([ rect_x, rect_y, 40,      6,        20,        4,      10])
        sheet_graph.append(["; "])
        Hole_gID += 1
        kk += 1
        
        ## 2nd section
        x_2nd = x_start + 30
        y_2nd = y_start + 120
        sheet_graph.append(["; RECTANGLE2D"])
        sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
        sheet_graph.append([Hole_gID, 30, Hole_gID, gID, 0, 0, 0, 1,])
        sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
        sheet_graph.append([x_2nd      , y_2nd,\
                            x_2nd + 220, y_2nd,\
                            x_2nd + 220, y_2nd + 84,\
                            x_2nd      , y_2nd + 84])
        sheet_graph.append(["; "])
        Hole_gID += 1
        kk += 1
        
        
        ## 3rd section
        x_3rd = x_start + 60
        y_3rd = y_start + 230
        sub_cir = np.array([[-10, -10], [10, -10], [10, 10], [-10, 10]])
        
        for k in range(2):
            Cir_x = x_3rd
            Cir_y = y_3rd + 40*k
            r = 10
            sub_r = 1.5
            
            for j in range(5):
                sheet_graph.append(["; CIRCLE2D"])
                sheet_graph.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
                sheet_graph.append([Hole_gID, 32, Hole_gID, gID, 1, 36, 0, 0, 1,])
                sheet_graph.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                sheet_graph.append([r, 0., Cir_x, Cir_y,])
                sheet_graph.append(["; "])
                Hole_gID += 1
                kk += 1
                
                for i in range(4):
                    sheet_graph.append(["; CIRCLE2D"])
                    sheet_graph.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
                    sheet_graph.append([Hole_gID, 32, Hole_gID, gID, 1, 36, 0, 0, 1,])
                    sheet_graph.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                    sheet_graph.append([sub_r, 0., Cir_x + sub_cir[i,0], Cir_y + sub_cir[i,1]])
                    sheet_graph.append(["; "])
                    Hole_gID += 1
                    kk += 1
                Cir_x += 40
        
        ## 4th section
        x_4th = x_start + 327.5 # Octagon cen
        y_4th = y_start + 62
        x_gap = 110
        for k in range(2):
            X_cen = x_4th + k * 110
            Y_cen = y_4th
            # Octagon vertex
            o_vtx = np.array([[X_cen - 17.5, Y_cen - 42.5], [X_cen + 17.5, Y_cen - 42.5],\
                              [X_cen + 42.5, Y_cen - 17.5], [X_cen + 42.5, Y_cen + 17.5],\
                              [X_cen + 17.5, Y_cen + 42.5], [X_cen - 17.5, Y_cen + 42.5],\
                              [X_cen - 42.5, Y_cen + 17.5], [X_cen - 42.5, Y_cen - 17.5]])
            sheet_graph.append(["; "," POLYGON2D_Octagon"])
            sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "nvtx", "iAppRef", "iCamAttr", "iRevEngF",])
            sheet_graph.append([Hole_gID, 34, Hole_gID, gID, 8, 0, 0, 1,])
            sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
            sheet_graph.append([o_vtx[0,0], o_vtx[0,1], o_vtx[1,0], o_vtx[1,1], o_vtx[2,0], o_vtx[2,1], o_vtx[3,0], o_vtx[3,1]])
            sheet_graph.append(["; x5", "y5", "x6", "y6", "x7", "y7", "x8", "y8"])
            sheet_graph.append([o_vtx[4,0], o_vtx[4,1], o_vtx[5,0], o_vtx[5,1], o_vtx[6,0], o_vtx[6,1], o_vtx[7,0], o_vtx[7,1]])
            sheet_graph.append(["; "])
            Hole_gID += 1
            kk += 1
            
            # small circle
            r = 2.5
            cir_cen = np.array([[X_cen - 42.5, Y_cen - 42.5],
                                [X_cen + 42.5, Y_cen - 42.5],
                                [X_cen + 42.5, Y_cen + 42.5],
                                [X_cen - 42.5, Y_cen + 42.5]])
            for j in range(4):
                sheet_graph.append(["; CIRCLE2D"])
                sheet_graph.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
                sheet_graph.append([Hole_gID, 32, Hole_gID, gID, 1, 36, 0, 0, 1,])
                sheet_graph.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                sheet_graph.append([r, 0., cir_cen[j,0], cir_cen[j,1]])
                sheet_graph.append(["; "])
                Hole_gID += 1
                kk += 1
            
        ## 5th section
        x_5th = x_start + 285 # Cir cen
        y_5th = y_start + 140
        r = 2.5
        for i in range(3):
            for j in range(5):
                x_cen = x_5th + j * 8
                y_cen = y_5th + i * 32
                sheet_graph.append(["; CIRCLE2D"])
                sheet_graph.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
                sheet_graph.append([Hole_gID, 32, Hole_gID, gID, 1, 36, 0, 0, 1,])
                sheet_graph.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                sheet_graph.append([r, 0., x_cen, y_cen])
                sheet_graph.append(["; "])
                Hole_gID += 1
                kk += 1
                
        rect_x = x_5th + 41
        rect_y = y_5th - 20
        for i in range(3):
            sheet_graph.append(["; RECTANGLE2D"])
            sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
            sheet_graph.append([Hole_gID, 30, Hole_gID, gID, 0, 0, 0, 1,])
            sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
            sheet_graph.append([rect_x     , rect_y,\
                                rect_x + 50, rect_y,\
                                rect_x + 50, rect_y + 20,\
                                rect_x     , rect_y + 20])
            sheet_graph.append(["; "])
            rect_y += 32
            Hole_gID += 1
            kk += 1
        
        rect_x = x_5th + 111
        rect_y = y_5th - 20
        sheet_graph.append(["; RECTANGLE2D"])
        sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
        sheet_graph.append([Hole_gID, 30, Hole_gID, gID, 0, 0, 0, 1,])
        sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
        sheet_graph.append([rect_x     , rect_y,\
                            rect_x + 84, rect_y,\
                            rect_x + 84, rect_y + 84,\
                            rect_x     , rect_y + 84])
        sheet_graph.append(["; "])
        Hole_gID += 1
        kk += 1
        
        ## 6th section
        x_5th = x_start + 285 # rect start
        y_5th = y_start + 225
        r = 2.5
        for i in range(3):
            rect_x = x_5th + i * 75
            rect_y = y_5th
            sheet_graph.append(["; RECTANGLE2D"])
            sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
            sheet_graph.append([Hole_gID, 30, Hole_gID, gID, 0, 0, 0, 1,])
            sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
            sheet_graph.append([rect_x     , rect_y,\
                                rect_x + 40, rect_y,\
                                rect_x + 40, rect_y + 15,\
                                rect_x     , rect_y + 15])
            sheet_graph.append(["; "])
            Hole_gID += 1
            kk += 1
            for j in range(2):
                x_cen = rect_x - 10 + 60 * j
                y_cen = rect_y + 7.5
                sheet_graph.append(["; CIRCLE2D"])
                sheet_graph.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
                sheet_graph.append([Hole_gID, 32, Hole_gID, gID, 1, 36, 0, 0, 1,])
                sheet_graph.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                sheet_graph.append([r, 0., x_cen, y_cen])
                sheet_graph.append(["; "])
                Hole_gID += 1
                kk += 1
                
        for i in range(2):
            rect_x = x_5th + 15 + i * 100
            rect_y = y_5th + 40
            sheet_graph.append(["; RECTANGLE2D"])
            sheet_graph.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
            sheet_graph.append([Hole_gID, 30, Hole_gID, gID, 0, 0, 0, 1,])
            sheet_graph.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
            sheet_graph.append([rect_x     , rect_y,\
                                rect_x + 60, rect_y,\
                                rect_x + 60, rect_y + 15,\
                                rect_x     , rect_y + 15])
            sheet_graph.append(["; "])
            Hole_gID += 1
            kk += 1
            for j in range(2):
                x_cen = rect_x - 10 + 80 * j
                y_cen = rect_y + 7.5
                sheet_graph.append(["; CIRCLE2D"])
                sheet_graph.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF"])
                sheet_graph.append([Hole_gID, 32, Hole_gID, gID, 1, 36, 0, 0, 1,])
                sheet_graph.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                sheet_graph.append([r, 0., x_cen, y_cen])
                sheet_graph.append(["; "])
                Hole_gID += 1
                kk += 1
        gID += kk
    
    
    
    
    
    return sheet_graph

################## produce_sheet end ###################



########################## main #########################

if __name__ == '__main__':


    print("Demo_Sheet\n")
    
    
    path = 'Demo_Sheet_graph'
    Demo_sheet = produce_sheet()
        
    path = path + ".txt"
    print(path)
    with open(path ,'w', newline='') as txtfile:
        writer = csv.writer(txtfile)
        writer.writerows(Demo_sheet)
    
######## main code end #######
