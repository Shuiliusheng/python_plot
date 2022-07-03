### python-matplotlib绘图
1. 需要包含的包
    ```python
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import numpy as np
        mpl.use('Qt5Agg')  #用于在本地显示图片(windows)
        #sans-serif 表示字体中的无衬线体, SimHe 是 黑体
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        #设置正常显示字符
        mpl.rcParams['axes.unicode_minus'] = False
    ```
2. 绘制一个简单的多子图
    ```python
        #绘制一个2*2的具有四个子图的大图，sharex sharey用于指明子图之间是否需要共享x轴或者y轴
        #sharex='row' 'col' True 分别代表列上的子图共享/行上的子图共享/全部共享
        #返回的第二个值axs是子图的集合，根据子图的个数和排列一样，是一个矩阵
        fig, axs = plt.subplots(2, 2, sharex=True)
        #第一个子图绘制数据, plot(x, y)是绘制折线图
        axs[0, 0].plot(datas['stage'].value, datas['user_ipc'].value)
        #设置子图标题
        axs[0, 0].set_title('user_ipc')
        #设置x轴显示数据的范围
        axs[0, 0].set_xlim(0, max(datas['stage'].value))
        #设置子图的网格线
        axs[0, 0].grid(color = 'b', linestyle = '--', linewidth = 0.5)
        axs[0, 0].set_xlabel("x - label") #设置横纵坐标轴的标题
        axs[0, 0].set_ylabel("y - label")

        axs[0, 1].plot(datas['stage'].value, datas['user_ipc'].value)
        axs[0, 1].set_title('user_ipc1')

        axs[1, 0].plot(datas['stage'].value, datas['icache_miss_rate'].value)
        axs[1, 0].set_title('icache_miss_rate')

        #设置整体标题
        plt.suptitle("SPEC INFORATION")
        #显示结果
        plt.show()
    ```

3. rcParams设置
    - pylot使用rc配置文件来自定义图形的各种默认属性，称之为rc配置或rc参数
    - 通过rc参数可以修改默认的属性，包括窗体大小、每英寸的点数、线条宽度、颜色、样式、坐标轴、坐标和网络属性、文本、字体等
    - 
    ```python
        #plt.rcParams.keys()

        matplotlib.rcParams['figure.figsize']	#图片像素
        matplotlib.rcParams['savefig.dpi']		#分辨率
        plt.savefig('plot123_2.png', dpi=200)	#指定分辨率
        plt.rcParams['savefig.dpi'] = 300 #图片像素
        plt.rcParams['figure.dpi'] = 300 #分辨率
        # 默认的像素：[6.0,4.0]，分辨率为100，图片尺寸为 600&400
        # 指定dpi=200，图片尺寸为 1200*800
        # 指定dpi=300，图片尺寸为 1800*1200
        # 设置figsize可以在不改变分辨率情况下改变比例
        plt.rcParams['figure.figsize'] = (5.0, 4.0)     # 显示图像的最大范围
        plt.rcParams['image.interpolation'] = 'nearest' # 差值方式，设置 interpolation style
        plt.rcParams['image.cmap'] = 'gray'             # 灰度空间

        #设置rc参数显示中文标题
        #设置字体为SimHei显示中文
        plt.rcParams['font.sans-serif'] = 'SimHei'
        #设置正常显示字符
        plt.rcParams['axes.unicode_minus'] = False

        #设置线条样式
        plt.rcParams['lines.linestyle'] = '-.'
        #设置线条宽度
        plt.rcParams['lines.linewidth'] = 3
        plt.rcParams['lines.color'] = 'blue'	#线条颜色
        plt.rcParams['lines.marker'] = None	    #默认标记
        plt.rcParams['lines.markersize'] = 6	#标记大小
        plt.rcParams['lines.markeredgewidth'] = 0.5	#标记附近的线宽

        #横、纵轴：xtick、ytick
        plt.rcParams['xtick.labelsize']	    #横轴字体大小
        plt.rcParams['ytick.labelsize']	    #纵轴字体大小
        plt.rcParams['xtick.major.size']	#x轴最大刻度
        plt.rcParams['ytick.major.size']	#y轴最大刻度

        #figure中的子图：axes
        plt.rcParams['axes.titlesize']	#子图的标题大小
        plt.rcParams['axes.labelsize']	#子图的标签大小

        #设置legend大小
        plt.rc('legend', fontsize=16)
        plt.rc('legend', fontsize='medium')

        #设置字体大小的方法set_size
        axes.title.set_size(20)
        axes.xaxis.label.set_size(16)
        axes.yaxis.label.set_size(16)


        #恢复默认参数
        matplotlib.rcdefaults()
        #更新参数
        matplotlib.rcParams.update( matplotlib.rc_params() )
    ```

4. 设置图像信息及保存
    ```python
        #设置图像大小，单位为英寸
        #figsize 参数的默认值为 [6.4, 4.8]
        plt.figure(figsize=(6,4))
        plt.rcParams["figure.figsize"] = (8, 6)
        fig.set_figheight(6)
        fig.set_figwidth(8)
        fig.set_size_inches(5, 5)

        #优化坐标轴范围显示
        plt.autoscale(enable=True, axis="both", tight=True) 

        #获取axes对象
        ax = plt.gca()
        plt.sca(ax) #切换到某个子图

        #设置子图之间的间隔
        fig.subplots_adjust(hspace=0, wspace=0)
        #设置整体图像的位置
        plt.subplots_adjust(bottom =0.15, left=0.06, right = 0.95) 

        #多个图保存到一个pdf中
        from matplotlib.backends.backend_pdf import PdfPages
        pp = PdfPages('Save multiple plots as PDF.pdf')
        pp.savefig(fig1, dpi=200)
        pp.savefig(fig2)
        pp.close()
    ```


5. 多个子图的大小和位置等设置
    - 设置位置及大小
        ```python
            #gridspec.GridSpec(nrows, ncols, height_ratios=None, width_ratios=None)
            from matplotlib import gridspec
            fig = plt.figure()
            #设置一个一行两列，列宽比为2：1的网格，根据网格来绘制子图
            spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[2, 1])
            ax0 = fig.add_subplot(spec[0])
            ax0.plot(range(5), range(5, 10))
            ax1 = fig.add_subplot(spec[1])
            ax1.plot(range(5), range(5, 10))

            #在plt.subplots中使用gridspec_kw属性设置子图比例
            fig, ax = plt.subplots(2, 2, gridspec_kw={'width_ratios': [2, 1], 'height_ratios': [1, 2]})

            #使用plt.subplot2grid规定子图的大小和位置
            #subplot2grid(shape, loc, rowspan=1, colspan=1, fig=None, **kwargs)
            fig = plt.figure()
            #生成1行五列的网格，第一个子图从(0,0)开始，占据三列，第二个也是
            #两者的shape可以不一样
            ax0 = plt.subplot2grid((1, 5), (0, 0), colspan=3)
            ax1 = plt.subplot2grid((1, 5), (0, 3), colspan=2)
        ```
    - 设置子图边界线：ax.spines['left'].set_visible(False)
    - 子图之间的间距设置
        ```python
            #自动保持子图之间的正确间距
            tight_layout(pad, w_pad, h_pad)

            plt.subplots_adjust(left, right, top, bottom, wspace = 0.01, hspace = 0.01)
            #left, right, top, bottom控制上下左右距离边界的位置，是图形的宽度和高度的比例
            #wspace, hspace控制相邻子图之间的间隔，分别是轴的宽度和高度的分数
           
            #constrained_layout 会自动调整子图和装饰，使其尽可能地适合图中
            plt.subplots(2,2, constrained_layout=True)

            #设置子图之间的间隔
            fig.subplots_adjust(hspace=0, wspace=0)
        ```
    - 包含子图：在一个图中绘制另一个子图
        ```python
            #[bottom, left, width, height]（底坐标、左坐标、宽度、高度）数值的取值范围是左下角（原点）为 0，右上角为 1
            fig=plt.figure()          #新建画板
            ax1=plt.axes()            #默认坐标系
            ax2=plt.axes([0.65,0.65,0.2,0.2])
            #Add an axes to the current figure and make it the current axes.
        ```
    - 多个子图之间的顺序，主要用于twinx
        ```python
            ax.set_zorder(2)
            ax2.set_zorder(1)
        ```

6. 子图内具体信息设置
    - 设置标题
        ```python
            ax.set_title(label, loc, fontdict)
            #loc: 'center', 'left', 'right' 或者position=(0.5, 0.9)
            #fontdict：设置子图等参数，也可以直接使用fontsize等参数设置
                # 'family': 'serif'
                # 'color' : 'darkblue'
                # 'weight': 'bold',
                # 'size': 18
        ```
    - 设置坐标轴
        - 设置轴线（上下左右）和坐标轴中心
            ```python
                #设置左侧轴线不显示
                ax.spines['left'].set_visible(False)
                ax.spines['left'].set_color('none')
                
                #将左侧和低侧移动到数据中的0值处
                ax.spines['left'].set_position(('data', 0))
                ax.spines['bottom'].set_position(('data', 0))
                
                #关闭所有坐标轴
                ax.get_xaxis().set_visible(False)
                ax.set_axis_off()
            ```
        - 设置坐标轴尺度、比例、是否反转
            ```python
                #比例尺
                plt.xscale("log",basey=2)
                #xy轴长相等
                ax.set_aspect('equal', adjustable='box')#当两个轴的范围设置为相同时，为正方形
                ax.set_aspect(1./ax.get_data_ratio(), adjustable='box')
                #反转轴
                ax.invert_xaxis()   #利用slim设置范围：plt.xlim(max(x),min(x))
                ax.set_ylim([max(y),min(y)])
            ```
        - 设置坐标轴刻度
            ```python
                #开启次要坐标刻度，采用默认配置
                ax.minorticks_on()

                #利用major/minor单独设置每个周的主要和次要坐标刻度显示
                plt.tick_params(axis="x", which="minor", length=10, color="r", labelrotation=45.0)
                plt.tick_params(axis="x", which="major", length=10)
                #direction='in'

                #Matplotlib.ticker.MaxNLocator类定义了一个名为nbins的参数，代表最大的bins数量
                from matplotlib.ticker import MaxNLocator
                axes.yaxis.set_major_locator(MaxNLocator(5)) #设置最大的ticks数是6

                #利用axes.xaxis.get_ticklabels()设置某些刻度不显示
                for i, tick in enumerate(axes.xaxis.get_ticklabels()):
                    if i % 2 != 0:
                        tick.set_visible(False)

                #利用set_xticks来设置刻度的间隔 
                ax.xaxis.set_ticks([0,1,3,4,5,6])
                ax.set_xticks([1, 10, 30])

                #单独设置刻度对应的标签
                ax.set_xticks([1, 10, 30])
                ax.set_xticklabels(['name1', 'name2', 'name3'], , rotation=45, ha="right")         

                #设置坐标轴刻度范围
                ax.set_xlim(0, max)       
            ```
        - 设置坐标轴字体、标签、标题等
            ```python
                #利用plt统一设置
                plt.xticks(fontname="Times New Roman", fontsize=25)
                plt.yticks(fontname="Times New Roman", fontsize=25)
                #利用sca单独设置某一个子图
                plt.sca(ax)
                plt.xticks(fontname="Times New Roman", fontsize=10, rotation=45)


                #设置横纵坐标轴的标题
                ax.set_xlabel("xlabel", fontdict={"family": "Times New Roman", "size": 25}) 
                plt.xlabel()
                    # family='serif'
                    # color, size 
                    # weight: ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']
                    # labelpad = 6: 标签和 x 轴之间的间距


                #设置坐标轴标签
                ax.set_xticks(datas['stage'].value[::5])
                xlabels = ax.get_xticklabels()
                ax.set_xticklabels(xlabels, rotation=45, ha='right', fontsize=12) #需要搭配set_xticks使用
                    #可以使用新的标签替代当前的字符串标签列表
                    #ha='right' 将标签文本的右端与刻度对齐
                    #ha='left' 将标签文本的左端与刻度对齐
                    #ha='center' 使标签文本的中心与刻度线对齐
                #利用tick_params设置参数
                ax.tick_params(axis='x', labelrotation=45)
                    #labelration, labelsize, labelcolor
                    #length, width, pad:Distance in points between tick and label.
                for label in ax.get_xticklabels():
                    label.set_rotation(55)

                #set_方法
                ax.title.set_size(20)
                ax.xaxis.label.set_size(16)
                ax.yaxis.label.set_size(16)

                #设置坐标轴label的特殊格式
                import matplotlib.ticker as ticker
                def make_label(value, pos):
                    return '%0.0f%%' % (100. * value)
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(make_label))
            ```

    - 设置图例 legend
        ```python
            #统计设置属性
            plt.rc('legend', fontsize=16)
            plt.rc('legend', fontsize='medium')

            #设置内容等信息
            plt.legend(["ave", "csd"], loc = 0, ncol=2, prop={"family": "Times New Roman", "size": 20})
            #将多个line（plot的返回对象）的图例放在一起显示
            ax.legend([line1[0], line2[0]], [line1[0].get_label(), line2[0].get_label()], ncol = 2)

            #更复杂的位置摆放
            fig.legend(loc=1, bbox_to_anchor=(1,1), bbox_transform=ax.transAxes)
                # bbox_to_anchor用于设置图例在图中绝对位置，loc则是用于表示方向，即(0,0)坐标为图例的哪一个角
                # bbox_transform用于设置bbox_to_anchor是根据哪个坐标系设置的
                    # bbox_transform=plt.gcf().transFigure获取整个图像的坐标系
                    # 用户级的data坐标系ax.transData
                    # Axes坐标系ax.transAxes
                    # Figure坐标系fig.transFigure

            #loc的位置
               # 0: 'best'
               # 1: 'upper right'
               # 2: 'upper left'
               # 3: 'lower left'
               # 4: 'lower right'
               # 5: 'right'
               # 6: 'center left'
               # 7: 'center right'
               # 8: 'lower center'
               # 9: 'upper center'
               # 10: 'center'
        ```

7. plot的一些属性
    - color: b蓝色 | g绿色 | r红色 | c青色 | m品红 | y黄色 | k黑色 | w白
        - color = (0.9569, 0.2588, 0.3891)
        - color = "#f44265"
    - label: 标签，用于绘制图例
    - linestyle: ['solid’'dashed’, 'dashdot’, 'dotted’(offset, on-off-dash-seq)'-']
        - ['-', '--', ':', '-.']
    - linewidth: 线宽，以 points 为单位
    - matplotlib.axes.Axes.set_prop_cycle() / plt.gca().set_prop_cycle(color=colors)可以统计设置每条线的颜色
    - 带点的折线图：plt.plot(x,y,linestyle='solid',color='blue')
    - zorder：多个图的绘制顺序，以数字表示
        ```python
            plt.plot(x,y,color='b',zorder=1)
            plt.plot(x,y,color='b',zorder=2)

            #多个子图之间的顺序，主要用于twinx
            ax.set_zorder(2)
            ax2.set_zorder(1)
        ```
    - ax.get_lines()[0].set_color('g')：从图中获取线的对象

8. 柱状图ax.bar(x, height, width, bottom, align)
    - x: 一个标量序列，代表柱状图的x坐标，默认x取值是每个柱状图所在的中点位置，或者也可以是柱状图左侧边缘位置。
    - height: 一个标量或者是标量序列，代表柱状图的高度。
    - width: 可选参数，标量或类数组，柱状图的默认宽度值为 0.8。
    - bottom: 可选参数，标量或类数组，柱状图的y坐标默认为None, 
        - 该参数可以指定柱状图开始堆叠的起始值，一般从底部柱状图的最大值开始，依次类推
    - algin: 有两个可选项 {"center","edge"}，默认为 'center'，该参数决定 x 值位于柱状图的位置。
    - 示例1：多条柱状图
        ```python
            ax.bar(X + 0.00, data[0], color = 'b', width = 0.25)
            ax.bar(X + 0.25, data[1], color = 'g', width = 0.25)
            ax.bar(X + 0.50, data[2], color = 'r', width = 0.25)
        ```
    - 示例2：堆叠柱状图
        ```python
            countries = ['USA', 'India', 'China', 'Russia', 'Germany'] 
            bronzes = np.array([38, 17, 26, 19, 15]) 
            silvers = np.array([37, 23, 18, 18, 10]) 
            golds = np.array([46, 27, 26, 19, 17]) 
            # 此处的 _ 下划线表示将循环取到的值放弃，只得到[0,1,2,3,4]
            ind = [x for x, _ in enumerate(countries)] 
            #绘制堆叠图
            plt.bar(ind, golds, width=0.5, label='golds', color='gold', bottom=silvers+bronzes) 
            plt.bar(ind, silvers, width=0.5, label='silvers', color='silver', bottom=bronzes) 
            plt.bar(ind, bronzes, width=0.5, label='bronzes', color='#CD853F') 
            #设置坐标轴
            plt.xticks(ind, countries) 
            plt.ylabel("Medals") 
            plt.xlabel("Countries") 
            plt.legend(loc="upper right") 
        ```

9. hist直方图的属性: 直方图用于统计数据分布
    - data : (n,) n维数组或者n维数组序列，多维数组长度不要求一致
    - bins: 需要分割的精度， 柱状图条数
    - range : 元组，可选bins的边界，如果bins是一个序列则无效如果没有则是(x.min(), x.max())
    - density : boolean, 如果为真返回第一个值是每个区间的百分比，默认是个数
    - cumulative: True/False/-1, 绘制时是否从左往右/从右向左逐步递增，累加之前的结果
    - alpha: [0, 1]设置透明度，在绘制多个重叠直方图时有用
    - shrink = 0.5,各条柱之间呈现一定间距，默认为1，为无间距
    - stat = "probability",y轴以概率显示
    - color: 'red'
        - 设置更高数量的bin时，颜色会被边界掩盖，因此可以选择设置边框颜色ec='red'或者设置无边框lw=0


10. 多个图保存到一个pdf中
    ```python
        from matplotlib.backends.backend_pdf import PdfPages
        pp = PdfPages('Save multiple plots as PDF.pdf')
        pp.savefig(fig1)
        pp.savefig(fig2)
        pp.close()
    ```