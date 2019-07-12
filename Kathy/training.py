import numpy as np
import xlwt
np.set_printoptions(threshold=np.inf)

g_cellMap=[]
maxX = 0
maxY = 0
eNbcount = 0
g_mapstatus = []

def fillmatrix(tmpline):
    global eNbcount
    if len(tmpline):
        posdata = tmpline.split(",")
        #print(posdata)
        x = int(posdata[0])
        y = int(posdata[1])
        for i in range(0,eNbcount):
            g_cellMap[i][x][y] = float(posdata[i+2])
        
def getmaxXY():
    global maxX
    global maxY

    isfirstline = 1
    with open('train.csv', 'r') as f:
        for line in f.readlines():
            if isfirstline:
                isfirstline=0
            else:
                pos = line.strip().split(",",3)
                x = int(pos[0])
                y = int(pos[1])
                if x>maxX:
                   maxX= x
                if y>maxY:
                   maxY= y
        maxX+=1 #行号从0开始所以总数是excel的最大行号加一
        maxY+=1 
        

def buildstatusmap():
    global g_cellMap
    global maxX
    global maxY
    global g_mapstatus
    
    for p in range(0,maxX):
        for q in range(0,maxY):
            if(g_cellMap[0][p][q]!=0):
                g_mapstatus[p][q] = 9
            else:
                g_mapstatus[p][q] = 0
                    
    for q in range(1,maxY-1):
        if g_mapstatus[0][q] < 9:
            g_mapstatus[0][q] = 2+int(g_mapstatus[0][q-1]==9) + \
                                            int(g_mapstatus[0][q+1]==9) + \
                                            int(g_mapstatus[1][q-1]==9) + \
                                            int(g_mapstatus[1][q]==9) + \
                                            int(g_mapstatus[1][q+1]==9)
        if g_mapstatus[maxX-1][q] < 9:
            g_mapstatus[maxX-1][q] = 2+int(g_mapstatus[maxX-1][q-1]==9) + \
                                            int(g_mapstatus[maxX-1][q+1]==9) + \
                                            int(g_mapstatus[maxX-2][q-1]==9) + \
                                            int(g_mapstatus[maxX-2][q]==9) + \
                                            int(g_mapstatus[maxX-2][q+1]==9)
                    
    for p in range(1,maxX-1):
        if g_mapstatus[p][0] < 9:
            g_mapstatus[p][0] = 2+int(g_mapstatus[p-1][1]==9) + \
                                            int(g_mapstatus[p][1]==9) + \
                                            int(g_mapstatus[p+1][1]==9) + \
                                            int(g_mapstatus[p-1][0]==9) + \
                                            int(g_mapstatus[p+1][0]==9)
        if g_mapstatus[p][maxY-1] < 9:
            g_mapstatus[p][maxY-1] = 2+int(g_mapstatus[p-1][maxY-2]==9) + \
                                            int(g_mapstatus[p][maxY-2]==9) + \
                                            int(g_mapstatus[p+1][maxY-2]==9) + \
                                            int(g_mapstatus[p-1][maxY-1]==9) + \
                                            int(g_mapstatus[p+1][maxY-1]==9)
    for a in range(0,5):
        for p in range(1,maxX-1):
            for q in range(1,maxY-1):
                if(g_mapstatus[p][q] < 9):
                    g_mapstatus[p][q] = int(g_mapstatus[p-1][q-1]==9) + \
                                            int(g_mapstatus[p-1][q]==9) + \
                                            int(g_mapstatus[p-1][q+1]==9) + \
                                            int(g_mapstatus[p][q-1]==9) + \
                                            int(g_mapstatus[p][q+1]==9) + \
                                            int(g_mapstatus[p+1][q-1]==9) + \
                                            int(g_mapstatus[p+1][q]==9) + \
                                            int(g_mapstatus[p+1][q+1]==9)+ \
                                            (int((g_mapstatus[p-1][q-1]!=9)&(g_mapstatus[p-1][q-1]>=3)) + \
                                            int((g_mapstatus[p-1][q]!=9)&(g_mapstatus[p-1][q]>=3)) + \
                                            int((g_mapstatus[p-1][q+1]!=9)&(g_mapstatus[p-1][q+1]>=3)) + \
                                            int((g_mapstatus[p][q-1]!=9)&(g_mapstatus[p][q-1]>=3)) + \
                                            int((g_mapstatus[p][q+1]!=9)&(g_mapstatus[p][q+1]>=3)) + \
                                            int((g_mapstatus[p+1][q-1]!=9)&(g_mapstatus[p+1][q-1]>=3)) + \
                                            int((g_mapstatus[p+1][q]!=9)&(g_mapstatus[p+1][q]>=3)) + \
                                            int((g_mapstatus[p+1][q+1]!=9)&(g_mapstatus[p+1][q+1]>=3)))//2
   

def predictpower():
    global eNbcount
    global g_cellMap
    global maxX
    global maxY
    global g_mapstatus

 
    for p in range(1,maxX-1):
        for q in range(1,maxY-1):
            if (g_mapstatus[p][q] < 9) & (g_mapstatus[p][q] >= 4):
                if (g_mapstatus[p-1][q]>=9) &(g_mapstatus[p+1][q]>=9):
                    g_mapstatus[p][q] = 10 #>=9 meas already have init power or predictpower
                    for i in range(0,eNbcount):  
                        g_cellMap[i][p][q] = (g_cellMap[i][p-1][q]+g_cellMap[i][p+1][q])/2
                    
                if (g_mapstatus[p][q-1]>=9) & (g_mapstatus[p][q+1]>=9) :
                    g_mapstatus[p][q] = 10
                    for i in range(0,eNbcount): 
                        g_cellMap[i][p][q] = (g_cellMap[i][p][q-1]+g_cellMap[i][p][q+1])/2
                        if ((g_mapstatus[p-1][q]>=9) & (g_mapstatus[p+1][q]>=9)) & \
                            (abs(g_cellMap[i][p-1][q]- g_cellMap[i][p+1][q]) <= g_cellMap[i][p][q]): #have predictpower value already 
                            g_cellMap[i][p][q] = (g_cellMap[i][p-1][q]+g_cellMap[i][p+1][q])/2;
                            
                        
                    


def writepowermap():
    global g_cellMap
    global maxX
    global maxY
    global g_mapstatus
    
    style0 = xlwt.XFStyle()
    style = xlwt.easyxf('pattern: pattern solid, fore_colour red')
    style1 = xlwt.easyxf('pattern: pattern solid, fore_colour yellow')
    style2 = xlwt.easyxf('pattern: pattern solid, fore_colour blue')
    file_power = xlwt.Workbook()
    for j in range (0,eNbcount):
        sheet_name = 'sheet name'+str(j)
        table = file_power.add_sheet(sheet_name)
        for k in range(0,maxX):
            for n in range(0,maxY):
                if g_mapstatus[k][n]==9:
                    table.write(k,n,str(g_cellMap[j][k][n]),style0)
                elif g_mapstatus[k][n]==10:
                    table.write(k,n,str(g_cellMap[j][k][n]),style2)
                else:
                    if g_mapstatus[k][n] >= 4 :
                        table.write(k,n,str(g_mapstatus[k][n]),style1)
                    else:
                        table.write(k,n,str(g_mapstatus[k][n]),style)
    file_power.save("powermappercell.xls")     

def buildmap():
    linenum = 0
    global eNbcount
    global g_cellMap
    global maxX
    global maxY
    global g_mapstatus
    getmaxXY()
    g_mapstatus = np.zeros([maxX,maxY])
    with open('train.csv', 'r') as f:

        for line in f.readlines():
            if linenum == 0:
                firstline = line.strip()
                eNbcount = firstline.count(",")-1
                for i in range (0,eNbcount):
                    g_cellMap.append(np.zeros([maxX,maxY]))
            else:
                tmpline = line.strip()
                fillmatrix(tmpline)   
            linenum +=1
        buildstatusmap()
        for i in range(5):
            predictpower()
        writepowermap()

        

                    
                    
def buildtestmap():
    global g_cellMap
    global eNbcount
    global maxX
    global maxY
    defaultpower = 9999.0
    numtoselect1 = 4
    numtoselect2 = 8
    numtoselect3 = 12
    numtoselect4 = 16
    buildmap()
    
    with open('test.csv', 'r') as f:
        linenum = 0
        
        file = xlwt.Workbook()
        default_style = xlwt.XFStyle()
        nearest_style1 = xlwt.easyxf('pattern: pattern solid, fore_colour dark_blue')
        nearest_style2 = xlwt.easyxf('pattern: pattern solid, fore_colour aqua')
        nearest_style3 = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue')
        nearest_style4 = xlwt.easyxf('pattern: pattern solid, fore_colour gray25')
        unknow_style = xlwt.easyxf('pattern: pattern solid, fore_colour red')
        for line in f.readlines():
            if linenum != 0:
                tmpline = line.strip()
                posdata = tmpline.split(",")
                tmp= np.zeros([maxX,maxY]) #init
                power_total = 0
                sheet_name = 'sheet name'+str(linenum)
                table = file.add_sheet(sheet_name)
                
                for i in range(0,eNbcount):   
                    power_total += abs(float(posdata[i+2]))
                    tmp = tmp+np.abs(g_cellMap[i]-np.ones([maxX,maxY])*float(posdata[i+2]))
                    
                m = np.array(tmp)
                min_powers1 = np.argpartition(m.ravel(),numtoselect1-1)[numtoselect1-1]
                min_powers2 = np.argpartition(m.ravel(),numtoselect2-1)[numtoselect2-1]
                min_powers3 = np.argpartition(m.ravel(),numtoselect3-1)[numtoselect3-1]
                min_powers4 = np.argpartition(m.ravel(),numtoselect4-1)[numtoselect4-1]

                for k in range(0,maxX):
                    for n in range(0,maxY):
                        new_style = default_style 
                        if m[k][n] == power_total:
                            m[k][n]= defaultpower
                            new_style = unknow_style
                        if m[k][n] <= m.ravel()[min_powers4]:
                            new_style = nearest_style4
                        if m[k][n] <= m.ravel()[min_powers3]:
                            new_style = nearest_style3
                        if m[k][n] <= m.ravel()[min_powers2]:
                            new_style = nearest_style2
                        if m[k][n] <= m.ravel()[min_powers1]:
                            new_style = nearest_style1
                        table.write(k,n,str(m[k][n]),new_style)
                                  
            linenum+=1
        file.save("reportsheets.xls")
    return
         
