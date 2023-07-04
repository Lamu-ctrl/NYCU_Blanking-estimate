import math
import numpy as np
import csv
import random

################## mixed sheet ###################

def produce_sheet(sheet_index):

    training_cir_rectshear_sheet = []
    training_cir_rectshear_sheet.append(["; SYSCONFIG"])
    training_cir_rectshear_sheet.append(["; version", "unit flag", "draw speed"])
    training_cir_rectshear_sheet.append(["; 2.1", "0(mks) 1(fbs)", "(%)"])
    training_cir_rectshear_sheet.append([201, 0, 5, 0, 0, 0, 0, 0, 0, 0,])
    training_cir_rectshear_sheet.append([";"])
    training_cir_rectshear_sheet.append(["; SYS INT DATA"])
    training_cir_rectshear_sheet.append(["; nibble", "nibble", "rect", "shear", "hit1", "hit2", "hit3", "not used"])
    training_cir_rectshear_sheet.append(["; arc", "line", "4side", "line", "one", "2nd", "3rd"])
    training_cir_rectshear_sheet.append([10, 10, 20, 40, 20, 15, 15, 0, 0, 0])
    training_cir_rectshear_sheet.append(["; screw", "tap", "louver", "form", "turret", "not used",])
    training_cir_rectshear_sheet.append(["; 1", "1", "1", "4", "rot 90",])
    training_cir_rectshear_sheet.append([600, 100, 200, 100, 500, 0, 0, 0, 0, 0])
    training_cir_rectshear_sheet.append([5, 10, 5, 10, 10, 20, 0, 0, 0, 0])
    training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_rectshear_sheet.append([";"])
    training_cir_rectshear_sheet.append(["; SYS DBL DATA"])
    training_cir_rectshear_sheet.append(["; operation time in sec", "distance in meter - unless specified otherwise"])
    training_cir_rectshear_sheet.append(["; Vx m/s", "Vy m/s", "Ax m/s2", "Ay m/s2, not used"])
    training_cir_rectshear_sheet.append([8, 10, 20, 30, 0., 0., 0., 0., 0., 0.])
    training_cir_rectshear_sheet.append(["; not used"])
    training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_rectshear_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_rectshear_sheet.append(["; gID", "gType", "loopID"])
    training_cir_rectshear_sheet.append([0, 0, 0])
    training_cir_rectshear_sheet.append(["; table off(x", "y)", "sheet size(x", "y)", "start(edge", "par)", "end(edge", "par)", "thickness"])
    training_cir_rectshear_sheet.append([0, 0, 4000, 2000, 4, 0.95, 2, 0.2, 0.062])
    training_cir_rectshear_sheet.append(["; "])
    
    rows = sheet_index % 3 + 2
    gID = 3 # gID begin from 3
    pass_num = 0
    
    columns = math.floor(sheet_index / 3) + 3
    if columns>8:
        columns = 8
    
    if rows>4:
        rows = 4
        
    for k1 in range(columns):
                
        for k2 in range(rows):
            
            x_pos = k1 * 450.0 + 325
            y_pos = k2 * 450.0 + 325
            
            shape_num = random.randint(1,5) # 20% --> this pos didn't have part
            if (shape_num == 2) | (shape_num == 3 ): # 40% --> create a circle part in this pos
                r = random.randint(160, 210)
                # CIRCLE2D
                training_cir_rectshear_sheet.append(["; CIRCLE2D"])
                training_cir_rectshear_sheet.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
                training_cir_rectshear_sheet.append([gID, 32, gID, 0, 1, 36, 0, 0, 1,])
                training_cir_rectshear_sheet.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                training_cir_rectshear_sheet.append([r, 0., x_pos, y_pos,])
                gID += 1
                training_cir_rectshear_sheet.append(["; "])
                
                # RECTANGLE2D IN GRID
                y_gap = random.randint(7, 10) + 8
                y_num = random.randint(5, 8)
                x_halfchord = pow(pow(r,2) - pow(y_num * y_gap, 2),0.5)
                x_gap = random.randint(5, 10) + 10
                x_halfnum = math.floor(x_halfchord / x_gap) - 1
                x_grid = x_pos - x_halfnum * x_gap
                y_grid = y_pos - y_gap * y_num
                training_cir_rectshear_sheet.append(["; RECTANGLE2D IN GRID"])
                training_cir_rectshear_sheet.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
                training_cir_rectshear_sheet.append([gID, 30, gID, gID-1, 0, 1, 18, 1,])
                training_cir_rectshear_sheet.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4",])
                training_cir_rectshear_sheet.append([x_grid-5.0, y_grid-5.0, x_grid+5.0, y_grid-5.0, x_grid+5.0, y_grid+5.0, x_grid-5.0, y_grid+5.0])
                training_cir_rectshear_sheet.append(["; x0",  "y0",  "X gap",   "# in X",  "Y gap", "# in Y", "style",])
                training_cir_rectshear_sheet.append([x_grid, y_grid,  x_gap, 2 * x_halfnum, y_gap,  y_num,     10,])
                #  where style = FirstEdge*10 + omit(1): no entity at origin omit(0): entity at origin
                #  first edge: bottom (1), right (2), top (3), left (4)
                
                gID += 1
                training_cir_rectshear_sheet.append(["; "])
                
                # circle ALONG A LINE
                y_gap = random.randint(3, 8) + 5
                y_num = random.randint(5, 10)
                x_halfchord = pow(pow(r,2) - pow(y_num * y_gap, 2), 0.5)
                x_gap = random.randint(5, 10) + 10
                x_halfnum = math.floor(x_halfchord / x_gap) - 1
                x_along = x_pos - x_halfnum * x_gap
                y_along = y_pos + 5
                pass_num = 0
                for k3 in range(y_num):
                    
                    if (random.randint(1,8) != 1): # 12.5% --> this pos didn't have holes
                        training_cir_rectshear_sheet.append(["; CIRCLE2D ALONG A LINE"])
                        training_cir_rectshear_sheet.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
                        training_cir_rectshear_sheet.append([   gID,   32,        gID,   gID-2-k3+pass_num, 1,   36,     1,       17,      1,])
                        training_cir_rectshear_sheet.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                        training_cir_rectshear_sheet.append([      2.5,     0., 		 x_along, y_along + y_gap * k3,])
                        training_cir_rectshear_sheet.append(["; x0",     "y0",             "entity gap", "line angle", "# of entity", "style",])
                        training_cir_rectshear_sheet.append([x_along, y_along + y_gap * k3,    x_gap,    0., 	2 * x_halfnum, 	0.,])
                        gID += 1
                        training_cir_rectshear_sheet.append(["; "])
                    else:
                        pass_num += 1
            # end if  ## circle
            
            elif (shape_num == 4) | (shape_num == 5): # 40% --> create a rect part in this pos
                
                rect_W = random.randint(320, 420) # width
                rect_H = random.randint(320, 420) # hight
                
                training_cir_rectshear_sheet.append(["; RECTANGLE2D"])
                training_cir_rectshear_sheet.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
                training_cir_rectshear_sheet.append([gID, 30, gID, 0, 0, 0, 0, 1,])
                training_cir_rectshear_sheet.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
                training_cir_rectshear_sheet.append([x_pos - rect_W/2, y_pos - rect_H/2,\
                                                     x_pos + rect_W/2, y_pos - rect_H/2,\
                                                     x_pos + rect_W/2, y_pos + rect_H/2,\
                                                     x_pos - rect_W/2, y_pos + rect_H/2])
                
                hole_W = random.randint(45, 90)
                hole_H = random.randint(45, 90)
                hole_Xgap = hole_W * 0.5 + random.randint(10, 15)
                hole_Ygap = hole_W * 0.72 + hole_H * 0.72 + random.randint(10, 20)
                hole_rotmiliDeg = 45000
                hole_Xnum = math.floor((rect_W - 0.72 * (hole_H + hole_Ygap)) / (hole_W + hole_Xgap))
                hole_Ynum = math.floor((rect_H ) / (0.71 * (hole_H + hole_W + hole_Ygap)))
                # print(hole_Ynum)
                hole_1st_X = x_pos - (hole_Xnum / 2 * hole_W + (hole_Xnum - 1)/2 * hole_Xgap) + (hole_H + hole_W) / (2*math.sqrt(2))
                hole_1st_Y = y_pos - (hole_Ynum / 2 * hole_H + (hole_Ynum - 1)/2 * hole_Ygap)
                sub_gID = 1   # the hole gID = (sub_gID + rect(gID))
                
                for j1 in range(hole_Ynum):
                    
                    if (True): # 12.5% --> this pos didn't have holes #random.randint(1,8) != 1
                        for j2 in range(hole_Xnum):
                            if (random.randint(1,10) != 1): # 10% --> this pos didn't have holes
                                training_cir_rectshear_sheet.append(["; RECTANGLE2D"])
                                training_cir_rectshear_sheet.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
                                training_cir_rectshear_sheet.append([sub_gID+gID, 30, sub_gID+gID, gID, hole_rotmiliDeg, 0, 0, 1,])
                                training_cir_rectshear_sheet.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
                                training_cir_rectshear_sheet.append([hole_1st_X + j2*(hole_W + hole_Xgap),          hole_1st_Y + j1*(hole_H*0 + hole_Ygap),\
                                                                     hole_1st_X + j2*(hole_W + hole_Xgap) + hole_W, hole_1st_Y + j1*(hole_H*0 + hole_Ygap),\
                                                                     hole_1st_X + j2*(hole_W + hole_Xgap) + hole_W, hole_1st_Y + j1*(hole_H*0 + hole_Ygap) + hole_H,\
                                                                     hole_1st_X + j2*(hole_W + hole_Xgap),          hole_1st_Y + j1*(hole_H*0 + hole_Ygap) + hole_H])
                                sub_gID += 1
                # for end
                gID += sub_gID
                                
                
    return training_cir_rectshear_sheet

################## mixed sheet end ###################


########################## main #########################

if __name__ == '__main__':


    print("Cir_RectShear_sheetC\n")
    
    
    sheet_num = 25
    for k in range(sheet_num):
    
        path = 'Cir_RectShear_Training_sheetC'
        training_cir_rectshear_sheet = produce_sheet(k)
        
        path = path + str(k) + ".txt"
        print(path)
        with open(path ,'w', newline='') as txtfile:
            writer = csv.writer(txtfile)
            writer.writerows(training_cir_rectshear_sheet)
    
######## main code end #######
