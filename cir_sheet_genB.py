import math
import numpy as np
import csv
import random

################## produce_sheet_cir end ###################

def produce_sheet_cir(sheet_index):

    training_cir_sheet = []
    training_cir_sheet.append(["; SYSCONFIG"])
    training_cir_sheet.append(["; version", "unit flag", "draw speed"])
    training_cir_sheet.append(["; 2.1", "0(mks) 1(fbs)", "(%)"])
    training_cir_sheet.append([201, 0, 100, 0, 0, 0, 0, 0, 0, 0,])
    training_cir_sheet.append([";"])
    training_cir_sheet.append(["; SYS INT DATA"])
    training_cir_sheet.append(["; nibble", "nibble", "rect", "shear", "hit1", "hit2", "hit3", "not used"])
    training_cir_sheet.append(["; arc", "line", "4side", "line", "one", "2nd", "3rd"])
    training_cir_sheet.append([10, 10, 20, 40, 20, 15, 15, 0, 0, 0])
    training_cir_sheet.append(["; screw", "tap", "louver", "form", "turret", "not used",])
    training_cir_sheet.append(["; 1", "1", "1", "4", "rot 90",])
    training_cir_sheet.append([600, 100, 200, 100, 500, 0, 0, 0, 0, 0])
    training_cir_sheet.append([5, 10, 5, 10, 10, 20, 0, 0, 0, 0])
    training_cir_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_sheet.append([";"])
    training_cir_sheet.append(["; SYS DBL DATA"])
    training_cir_sheet.append(["; operation time in sec", "distance in meter - unless specified otherwise"])
    training_cir_sheet.append(["; Vx m/s", "Vy m/s", "Ax m/s2", "Ay m/s2, not used"])
    training_cir_sheet.append([8, 10, 20, 30, 0., 0., 0., 0., 0., 0.])
    training_cir_sheet.append(["; not used"])
    training_cir_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_sheet.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    training_cir_sheet.append(["; gID", "gType", "loopID"])
    training_cir_sheet.append([0, 0, 0])
    training_cir_sheet.append(["; table off(x", "y)", "sheet size(x", "y)", "start(edge", "par)", "end(edge", "par)", "thickness"])
    training_cir_sheet.append([0, 0, 4000, 2000, 4, 0.95, 2, 0.2, 0.062])
    training_cir_sheet.append(["; "])
    gID = 3 # gID begin from 3
    
    rows = sheet_index % 3 + 1
    columns = math.floor(sheet_index / 4) + 2
    if columns>6:
        columns = 6
    
    if rows>3:
        rows = 3
        
    for k1 in range(columns):
                
        for k2 in range(rows):
            
            x_pos = (k1) * 620.0 + 400
            y_pos = (k2) * 620.0 + 380
            r = random.randint(200, 300)
            
            if (random.randint(1,4) != 1): # 25% --> this pos didn't have part
                
                # CIRCLE2D
                training_cir_sheet.append(["; CIRCLE2D"])
                training_cir_sheet.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
                training_cir_sheet.append([gID, 32, gID, 0, 1, 54, 0, 0, 1,])
                training_cir_sheet.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                training_cir_sheet.append([r, 0., x_pos, y_pos,])
                gID += 1
                training_cir_sheet.append(["; "])
                
                # RECTANGLE2D IN GRID
                y_gap = random.randint(5, 10) + 10
                y_num = random.randint(4, 6)
                x_halfchord = pow(pow(r,2) - pow(y_num * y_gap, 2),0.5)
                x_gap = random.randint(5, 10) + 10
                x_halfnum = math.floor(x_halfchord / x_gap) - 1
                x_grid = x_pos - x_halfnum * x_gap
                y_grid = y_pos - y_gap * y_num
                training_cir_sheet.append(["; RECTANGLE2D IN GRID"])
                training_cir_sheet.append(["; gID", "gType", "iUserSetID", "parentID", "rotmiliDeg", "iAppRef", "iCamAttr", "iRevEngF",])
                training_cir_sheet.append([gID, 30, gID, gID-1, 0, 1, 18, 1,])
                training_cir_sheet.append(["; x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4",])
                training_cir_sheet.append([x_grid-5.0, y_grid-5.0, x_grid+5.0, y_grid-5.0, x_grid+5.0, y_grid+5.0, x_grid-5.0, y_grid+5.0])
                training_cir_sheet.append(["; x0",  "y0",  "X gap",   "# in X",  "Y gap", "# in Y", "style",])
                training_cir_sheet.append([x_grid, y_grid,  x_gap, 2 * x_halfnum, y_gap,  y_num,     10,])
                #  where style = FirstEdge*10 + omit(1): no entity at origin omit(0): entity at origin
                #  first edge: bottom (1), right (2), top (3), left (4)
                
                gID += 1
                training_cir_sheet.append(["; "])
                
                # circle ALONG A LINE
                y_gap = random.randint(4, 8) + 10
                y_num = random.randint(5, 10)
                x_halfchord = pow(pow(r,2) - pow(y_num * y_gap, 2), 0.5)
                x_gap = random.randint(5, 10) + 10
                x_halfnum = math.floor(x_halfchord / x_gap) - 1
                x_along = x_pos - x_halfnum * x_gap
                y_along = y_pos + 5
                pass_num = 0
                for k3 in range(y_num):
                    
                    if (random.randint(1,8) != 1): # 12.5% --> this pos didn't have holes
                        training_cir_sheet.append(["; CIRCLE2D ALONG A LINE"])
                        training_cir_sheet.append(["; gID", "gType", "loopID", "parentID", "ccw", "segCt", "iAppRef", "iCamAttr", "iRevEngF",])
                        training_cir_sheet.append([   gID,   32,        gID,   gID-2-k3+pass_num, 1,   36,     1,       17,      1,])
                        training_cir_sheet.append(["; radius", "start_at_degrees", "centerX", "centerY",])
                        training_cir_sheet.append([      2.5,     0., 		 x_along, y_along + y_gap * k3,])
                        training_cir_sheet.append(["; x0",     "y0",             "entity gap", "line angle", "# of entity", "style",])
                        training_cir_sheet.append([x_along, y_along + y_gap * k3,    x_gap,    0., 	2 * x_halfnum, 	0.,])
                        gID += 1
                        training_cir_sheet.append(["; "])
                    else:
                        pass_num +=1
    return training_cir_sheet

################## produce_sheet_cir end ###################



########################## main #########################

if __name__ == '__main__':


    print("Cir_Training_SheetB\n")
    
    sheet_num = 25
    for k in range(sheet_num):
    
        path = 'Cir_Training_SheetB'
        training_cir_sheet = produce_sheet_cir(k)
        
        path = path + str(k) + ".txt"
        print(path)
        with open(path ,'w', newline='') as txtfile:
            writer = csv.writer(txtfile)
            writer.writerows(training_cir_sheet)
    
######## main code end #######
