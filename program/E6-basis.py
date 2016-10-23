"""
P31 2.10 (include wind.迎面风阻)
"""
import pylab as pl
import math
pl.ion()

#计算轨迹
class cannon_shell:
    def __init__(self, init_v = 0, init_theta = 0, time_step = 0, target_altitude = 0, wind_speeed = 0):
        self.x = [0]
        self.y = [0]
        self.init_theta = init_theta
        self.vx = [init_v * math.cos(self.init_theta / 180 * math.pi) / 1000]
        self.vy = [init_v * math.sin(self.init_theta / 180 * math.pi) / 1000]
        self.v_wind = wind_speeed / 1000
        self.dt = time_step
        self.C = 0
        self.h = target_altitude
    def launch(self):
        i = 0
        j = 0
        loop = True
        global high_enough
        while(loop):
            self.C = 4E-2 * math.pow(1 - 6.5 * self.y[i] / 288.15, 2.5)
            self.x.append(self.x[i] + self.vx[i] * self.dt)
            self.y.append(self.y[i] + self.vy[i] * self.dt)
            self.vx.append(self.vx[i] - self.C * math.sqrt(self.vx[i] ** 2 + self.vy[i] ** 2 + self.v_wind ** 2 + 2 * self.vx[i] * self.v_wind) * abs(self.vx[i] - self.v_wind) * self.dt)
            self.vy.append(self.vy[i] - 9.8E-3 * self.dt - self.C * math.sqrt(self.vx[i] ** 2 + self.vy[i] ** 2 + self.v_wind ** 2 + 2 * self.vx[i] * self.v_wind) * self.dt)
            i += 1
            if (self.y[i] < self.y[i-1]) and (self.y[i-1] < self.h):
                high_enough = False
                loop = False
            if (self.y[i] > self.h) or j:
                j = 1
            if (self.y[i] < self.h) and j:
                loop = False
        if self.y[i-1] > self.h:
            self.x[i] = -(self.y[i-1] - self.h) * (self.x[i] - self.x[i-1]) / (self.y[i] - self.y[i-1]) + self.x[i-1]
            self.y[i] = self.h
            high_enough = True

#输出结果图像
class show_results:
    def show_results_1(self):
        pl.figure(1)
        pl.title('Cannon Shell')
        pl.xlabel('x / $km$')
        pl.ylabel('y / $km$')
        pl.grid()
        pl.show()
    def show_results_2(self):
        pl.figure(1)
        line = [self.h, self.h]
        line_range = [self.x[-1] - 0.5, self.x[-1] + 0.5]
        pl.plot(line_range, line, 'k')
        pl.plot(self.x, self.y, label = "%.1f °"%self.init_theta)
        pl.legend(loc = 6, ncol = 1, title = 'Angle:', bbox_to_anchor = (1, 0.5))
        pl.draw()
        print("\n初速度：", user_input.init_v, "m/s")
        print("计算间隔：", user_input.time_step, "s")
        print("发射角度：", self.init_theta, "°")
        print("落点距离：%.4f km"%self.x[-1], "\n")

#用户输入初始值
class user_input:
    num_str_in = input("请输入初速度（m/s),计算间隔dt（s）的值,靶点高度（km）,风速（m/s）并用空格隔开:\n")
    num = [float(n) for n in num_str_in.split()]
    init_v = num[0]
    time_step = num[1]
    target_altitude = num[2]
    wind_speeed = num[3]

#用户输入不同的初始角度值，并输出结果曲线
class user_output:
    start = cannon_shell()
    show_results.show_results_1(start)
    while(True):
        init_theta = float(input("--------------\n输入初始角度（角度制，0~180）（输入999结束计算）:\n"))
        if init_theta != 999:
            start = cannon_shell(user_input.init_v, init_theta, user_input.time_step, user_input.target_altitude, user_input.wind_speeed)
            start.launch()
            if not high_enough:
                print("\n该角度无法射到靶所在的高度\n")
            else:
                show_results.show_results_2(start)
        else:
            break

#运行程序
user_input()
user_output()
end = input("\n\n\n按下回车结束程序...")
