from cProfile import label
from re import U
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import MultipleLocator
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages

import csv
import os
import sys
import math

from pyparsing import alphanums

mpl.use('Qt5Agg')
mpl.rcParams['font.sans-serif'] = ['Times New Roman']
mpl.rcParams['font.serif'] = ['Times New Roman']
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

class LineData:
    value = []
    def __init__(self):
        self.value = []

    def addinfo(self, value):
        if isinstance(value, str):
            self.value.append(float(value))
        else:
            self.value.append(value)

    def op(self, other, optype):
        temp = LineData()
        idx = 0
        if isinstance(other, float) or isinstance(other, int):
            while idx < len(self.value):
                if optype == "-":
                    val = self.value[idx] - other
                elif optype == "*":
                    val = self.value[idx] * other
                elif optype == "/":
                    val = 1.0 * self.value[idx] / other
                else:
                    val = self.value[idx] + other
                temp.addinfo(val)
                idx = idx + 1

        if isinstance(other, LineData):
            if len(other.value) != len(self.value):
                return temp
            while idx < len(self.value):
                if optype == "-":
                    val = self.value[idx] - other.value[idx]
                elif optype == "*":
                    val = self.value[idx] * other.value[idx]
                elif optype == "/":
                    val = 1.0 * self.value[idx] / other.value[idx]
                else:
                    val = self.value[idx] + other.value[idx]
                temp.addinfo(val)
                idx = idx + 1
        return temp

    # 重载加减乘除运算
    def __add__(self, other):
        return self.op(other, "+")

    def __sub__(self, other):
        return self.op(other, "-")

    def __mul__(self, other):
        return self.op(other, "*")

    def __truediv__(self, other):
        return self.op(other, "/")


def cal_correlation(val1, val2):
    if not(np.any(val2)) or not(np.any(val2)):
        return 0
    ab = np.array([val1, val2])
    cor_info = np.corrcoef(ab)
    return cor_info[0,1]


def readdata(filename):
    datas = {}
    f = open(filename, 'r')
    reader = csv.reader(f)
    for row in reader:
        temp = LineData()
        idx = 1
        while idx < len(row):
            if len(row[idx]) > 0:
                temp.addinfo(row[idx])
            idx = idx + 1
        # datas.append(temp)
        if len(row[0]) == 0:
            row[0] = "stage"
        datas[row[0]] = temp
    datas['User Level IPC'] = datas['user_ipc']
    datas['Mispredicted Branch Number'] = datas['com_misp_jalr']+datas['com_misp_br']
    datas['DCache To L2Cache Number'] = datas['dcache_to_L2']
    datas['Branch Misprediction Rate'] = datas['Mispredicted Branch Number'] / (datas['com_is_br']+datas['com_is_jalr'])
    datas['Mispredicted Branch Per Kilo-Instruction'] = datas['Mispredicted Branch Number'] / datas['insts'] * 1000
    datas['DCache To L2Cache Per Kilo-Instruction'] = datas['dcache_to_L2'] / datas['insts'] * 1000
    f.close()
    return datas



def setMaxMin(minvalue, maxvalue, nstep):
    step = (maxvalue - minvalue)/nstep
    t = math.pow(10, -1*math.floor(math.log10(step)))
    minval = int(minvalue*t)/t
    maxval = math.ceil(maxvalue*t)/t
    step = (maxval - minval)/nstep
    t = math.pow(10, -1*math.floor(math.log10(step)))
    newstep = round(step*t)
    if(newstep<step*t):
        step = newstep+0.5
    else:
        step = newstep
    step = step / t
    maxval = minval + step * nstep
    return minval, maxval, step
    
def sampledata(xvalue, yvalue, step):
    xvalue1 = []
    yvalue1 = []
    idx = 0
    while idx < len(xvalue):
        xvalue1.append(xvalue[idx])
        yvalue1.append(yvalue[idx])
        idx+=step
    return xvalue1, yvalue1

def draw_lines(datas, fig, ax, xvalue, lnames, rnames, xlabel, ylabel1, ylabel2, showLegend=False, sample = 1):    
    print("draw line: " + ylabel1 + " & " + ylabel2)
    ccolors = plt.get_cmap('Paired')(np.linspace(0.75, 0.3, len(lnames)+len(rnames)))

    ylocatorNum = 4
    cidx = 0
    maxvalue = 0.0
    minvalue = min(datas[lnames[0]].value)
    for line in lnames:
        maxvalue = max(maxvalue, max(datas[line].value))
        minvalue = min(minvalue, min(datas[line].value))
        xvalue1 = xvalue
        yvalue1 = datas[line].value
        if sample != 1:
            xvalue1, yvalue1 = sampledata(xvalue, datas[line].value, sample)
        ax.plot(xvalue1, yvalue1, '-', label=line, color=ccolors[cidx], lw = 1)
        cidx = cidx + 1
    
    print(minvalue, maxvalue)
    ax.xaxis.set_major_locator(MaxNLocator(8))
    ax.yaxis.set_major_locator(MaxNLocator(ylocatorNum))
    ax.tick_params(axis="x", which="major", length=4, labelrotation=45, pad = 0.2, labelsize = 10)
    ax.tick_params(axis="y", which="major", length=4, pad = 0.2, labelsize = 11)
    ax.set_xlabel(xlabel, fontsize = 12, labelpad = 1)
    ax.set_ylabel("IPC", fontdict={"family": "Times New Roman", "size": 11})
    
    ax.set_xlim([0, max(xvalue)])
    minvalue, maxvalue, step = setMaxMin(minvalue, maxvalue, ylocatorNum)
    ax.set_ylim([minvalue, maxvalue])
    ax.set_yticks(np.arange(minvalue, maxvalue+step, step)[0:ylocatorNum+1])
    ax.grid(axis='y', linestyle ='--', alpha = 0.5)

    if len(rnames) != 0:
        ax2 = ax.twinx() 
        maxvalue = max(datas[rnames[0]].value)
        minvalue = min(datas[rnames[0]].value)
        cidx = len(lnames)
        for line in rnames:
            maxvalue = max(maxvalue, max(datas[line].value))
            minvalue = min(minvalue, min(datas[line].value))
            xvalue1 = xvalue
            yvalue1 = datas[line].value
            if sample != 1:
                xvalue1, yvalue1 = sampledata(xvalue, datas[line].value, sample)
            ax2.plot(xvalue1, yvalue1, '-', label=line, color=ccolors[cidx], lw = 1)
            cidx = cidx + 1
        print(minvalue, maxvalue)
        # ax2.yaxis.set_major_formatter(ticker.FuncFormatter(make_label))
        ax2.tick_params(axis="y", which="major", length=4, pad = 0.2, labelsize = 11)
        # ax2.set_ylabel(ylabel2, fontdict={"family": "Times New Roman", "size": 12})
        ax2.yaxis.set_major_locator(MaxNLocator(ylocatorNum-1))
        minvalue, maxvalue, step = setMaxMin(minvalue, maxvalue, ylocatorNum)
        # print(minvalue, maxvalue)
        ax2.set_ylim([minvalue, maxvalue])
        ax2.set_yticks(np.arange(minvalue, maxvalue+step, step)[0:ylocatorNum+1])
    # 将图例置于当前坐标轴下
    if showLegend:
        fig.legend(loc='upper right', fontsize=11, bbox_to_anchor=(0.91, 0.955), frameon=False, bbox_transform=fig.transFigure, ncol=(len(lnames)+len(rnames)))
    

def drawsubplot(fig, ax, csvname, title, hasLegend=False):
    datas = readdata(csvname)
    xvalue = datas['stage'].value
    xlabel = "Instruction Interval (200M)"
    rightnames = ['Mispredicted Branch Number', 'DCache To L2Cache Number']
    draw_lines(datas, fig, ax, xvalue, ['User Level IPC'], rightnames, xlabel, "IPC", "", hasLegend, 2)
    ax.set_title(title)


def drawplot():
    figs = []
    # fig, axs = plt.subplots(1, 3, figsize=(18, 3.5))
    # drawsubplot(fig, axs[0], "../csv/int/bzip2_eventinfo_h.csv", "401.bzip2", True)
    # drawsubplot(fig, axs[1], "../csv/int/gcc166_counter_eventinfo_h.csv", "403.gcc")
    # drawsubplot(fig, axs[2], "../csv/int/astar_rivers_eventinfo_h.csv", "473.astar")
    # fig.subplots_adjust(hspace=0, wspace=0.25)

    fig, axs = plt.subplots(2, 3, figsize=(18, 7))
    drawsubplot(fig, axs[0, 0], "../csv/int/bzip2_eventinfo_h.csv", "401.bzip2", True)
    drawsubplot(fig, axs[0, 1], "../csv/int/gcc166_counter_eventinfo_h.csv", "403.gcc")
    drawsubplot(fig, axs[0, 2], "../csv/int/astar_rivers_eventinfo_h.csv", "473.astar")
    drawsubplot(fig, axs[1, 0], "../csv/float/bwaves_eventinfo_h.csv", "410.bwaves")
    drawsubplot(fig, axs[1, 1], "../csv/float/povray_eventinfo_h.csv", "453.povray")
    drawsubplot(fig, axs[1, 2], "../csv/float/calculix_hyper_eventinfo_h.csv", "454.calculix")
    fig.subplots_adjust(hspace=0.37, wspace=0.25)

    plt.show()

    figs.append(fig)
    pp = PdfPages("int_float.pdf")
    idx = 0
    for fig in figs:
        print("save "+str(idx)+","+str(len(figs)))
        pp.savefig(fig, bbox_inches='tight', dpi=200)
        idx = idx + 1
    pp.close()

drawplot()