import math
import numpy as np
import csv
import random

################## produce_sheet_rect ###################

def produce_sheet_rect(sheet_index):

    rect_training_sheet = []
    rect_training_sheet.append(["; SYSCONFIG"])
    rect_training_sheet.append(["; version", "unit flag", "draw speed"])
    rect_training_sheet.append(["; 2.1", "0(mks) 1(fbs)", "(%)"])
    rect_training_sheet.append([201, 0, 100, 0, 0, 0, 0, 0, 0, 0,])
    rect_training_sheet.append([";"])
    rect_training_sheet.append(["; SYS INT DATA"])
    rect_training_sheet.append(["; nibble", "nibble", "rect", "shear", "hit1", "hit2", "hit3", "not used"])
    rect_training_sheet.append(["; arc", "line", "4side", "line", "one", "2nd", "3rd"])
    rect_training_sheet.append([10, 10, 20, 40, 20, 15, 15, 0, 0, 0])
    rect_training_sheet.append(["; screw", "tap", "louver", "form", "turret", "not used",])
    rect_training_sheet.append(["; 1", "1", "1", "4", "rot 90",])
    rect_training_sheet.append([600, 100, 200, 100, 500, 0, 0, 0, 0, 0])
    rect_training_sheet.append([5, 10, 5, 10, 10, 20, 0, 0, 0, 0])
    rect_training_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    rect_training_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    rect_training_sheet.append([";"])
    rect_training_sheet.append(["; SYS DBL DATA"])
    rect_training_sheet.append(["; operation time in sec", "distance in meter - unless specified otherwise"])
    rect_training_sheet.append(["; Vx m/s", "Vy m/s", "Ax m/s2", "Ay m/s2, not used"])
    rect_training_sheet.append([8, 10, 20, 30, 0., 0., 0., 0., 0., 0.])
    rect_training_sheet.append(["; not used"])
    rect_training_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    rect_training_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    rect_training_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    rect_training_sheet.append(["; gID", "gType", "loopID"])
    rect_training_sheet.append([0, 0, 0])
    rect_training_sheet.append(["; table off(x", "y)", "sheet size(x", "y)", "start(edge", "par)", "end(edge", "par)", "thickness"])
    rect_training_sheet.append([0, 0, 4000, 2000, 4, 0.95, 2, 0.2, 0.062])
    rect_training_sheet.append(["; "])
    gID = 3 # gID begin from 3
    
    rows = sheet_index % 3 + 2
    columns = math.floor(sheet_index / 4) + 2
    if columns>8:
        columns = 8
        
    if rows>4:
        rows = 4
    for k1 in range(columns):
                
        for k2 in range(rows):
            
            x_pos = (k1) * 450.0 + 325
            y_pos = (k2) * 450.0 + 325
                            
            if (random.randint(1,10) != 1): # 10% --> this pos didn't have part
                
                rect_W = random.randint(320, 420) # width
                rect_H = random.randint(320, 420) # hight
                
                rect_training_sheet.append(["; RECTANGLE2D"])
                rect_training_sheet.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
                rect_training_sheet.append([gID, 30, gID, 0, 0, 0, 0, 1,])
                rect_training_sheet.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
                rect_training_sheet.append([x_pos - rect_W/2, y_pos - rect_H/2,\
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
                    
                    if (True): #random.randint(1,8) != 1 # 12.5% --> this row didn't have holes 
                        for j2 in range(hole_Xnum):
                            if (random.randint(1,10) != 1): # 10% --> this pos didn't have holes
                                rect_training_sheet.append(["; RECTANGLE2D"])
                                rect_training_sheet.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
                                rect_training_sheet.append([sub_gID+gID, 30, sub_gID+gID, gID, hole_rotmiliDeg, 0, 0, 1,])
                                rect_training_sheet.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"])
                                rect_training_sheet.append([hole_1st_X + j2*(hole_W + hole_Xgap),          hole_1st_Y + j1*(hole_H*0 + hole_Ygap),\
                                                            hole_1st_X + j2*(hole_W + hole_Xgap) + hole_W, hole_1st_Y + j1*(hole_H*0 + hole_Ygap),\
                                                            hole_1st_X + j2*(hole_W + hole_Xgap) + hole_W, hole_1st_Y + j1*(hole_H*0 + hole_Ygap) + hole_H,\
                                                            hole_1st_X + j2*(hole_W + hole_Xgap),          hole_1st_Y + j1*(hole_H*0 + hole_Ygap) + hole_H])
                                sub_gID += 1
                # for end
                gID += sub_gID
                
    return rect_training_sheet

################## produce_sheet_rect end ###################



########################## main #########################

if __name__ == '__main__':


    print("Rect_Training_SheetC\n")
    
    sheet_num = 25
    for k in range(sheet_num):
    
        path = 'Rect_Training_SheetC'
        training_sheet = produce_sheet_rect(k)
        
        path = path + str(k) + ".txt"
        print(path)
        with open(path ,'w', newline='') as txtfile:
            writer = csv.writer(txtfile)
            writer.writerows(training_sheet)
    
######## main code end #######
