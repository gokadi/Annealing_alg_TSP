from tkinter.messagebox import *
from tkinter import ttk
#from tkinter import Tk
from tkinter import *
from func import *
import ctypes # чтобы иконка была в трее
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageTk


class form(ttk.Frame):
    """The adders gui and functions."""

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def on_quit(self):
        """Exits program."""
        self.quit()

    def calculate(self):
        global tmax,tmin,n,flag,route0,energy0,dist0,num_it
        tmax,tmin,flag,n,pack = 0,0,0,0,0
        # считываем, запоминаем температуру
        try:
            tmin = round(float(self.num1_entry.get()), 2)
            tmax = round(float(self.num2_entry.get()), 2)
            if tmax <= tmin:
                showerror("Температура", 'Введите корректные значения(tmax>tmin)!')
                # очищаем поля для ввода
                self.num1_entry.delete('0',END)
                self.num2_entry.delete('0',END)
                tmax, tmin,flag = 0,0,0 # на тот случай, если решение повторно ищут, сброс
            else:
                flag=1 # флаг чтобы матрица строилась только после всех правильных вводов. События
                        # onChange или подобного не нашел, поэтому считывание значений с полей Entry
                        # осуществляется по нажатию кнопки
        except ValueError:
            showerror("Температура", 'Неправильный формат ввода!')
            flag=0 # на тот случай, если решение повторно ищут, сброс
            # очищаем поля для ввода. больше часа искал эти свойства :(
            self.num1_entry.delete('0', END)
            self.num2_entry.delete('0', END)
        # если температура считана, то считываем число ПК
        if flag == 1:
            try:
                n=int(self.numb_pc.get())
                if n<=1:
                    showerror("Число ПК", 'Введите целое число ПК в сети >1!')
                    self.numb_pc.delete('0',END)
                    n=0
                    flag=1 # на тот случай, если решение повторно ищут, сброс
                else:
                    flag=2
            except ValueError:
                showerror("Число ПК", 'Неправильный формат ввода!')
                flag=1 # на тот случай, если решение повторно ищут, сброс
                self.numb_pc.delete('0', END)
        # если число ПК считано, то считываем объем входящего пакета
        if flag == 2:
            try:
                pack=round(float(self.package.get()),2)
                if pack<=0:
                    showerror("Объем пакета", 'Введите объем входящего пакета >0!')
                    self.package.delete('0',END)
                    pack=0
                    flag=2 # на тот случай, если решение повторно ищут, сброс
                else:
                    flag=3
            except ValueError:
                showerror("Объем пакета", 'Неправильный формат ввода!')
                flag=2 # на тот случай, если решение повторно ищут, сброс
                self.package.delete('0', END)
        # если все входные данные считаны правильно, то создаем первое состояние системы,
        # а именно, рандомную матрицу стоимостей, начальный маршрут 1..n, считаем начальную энергию и
        # отображаем их в label'ах
        if flag == 3:
            route0, energy0, dist0=makeS1(n,pack)
            #route0
            self.route0['text']=route0
            #energy0
            self.energy0['text']=energy0
            flag = 4
            # график матрицы стоимостей до решения
            # plt.imshow(dist0, cmap='Blues')
            plt.axis([0,dist0.shape[0], dist0.shape[0],0])
            plt.pcolor(dist0)
            plt.colorbar()
            plt.clim(0,np.max(dist0))
            fig1 = plt.gcf()  # возвращает фигуру
            fig1.set_size_inches(7.7, 5.2)
            plt.savefig('D:\\sprite.png', format='png', dpi=50)
            plt.clf()
            # img2 = PhotoImage(file='D:\\sprite.png')#почему-то это не работает,хотя в случае с графиком энергии все ОК
            self.img2 = ImageTk.PhotoImage(Image.open('D:\\sprite.png'))
            self.distance0.create_image(0, 0, image=self.img2, anchor='nw')


    def solution(self):
        global tmax,tmin,n,flag,route0,dist0,energy0,energy_hist,img,num_it#если убрать img, то не будет графика для энергии
        #self.choose()
        #print(mode)
        mode=1
        if self.switch.get()==u'Линейный':
            mode=1
        if self.switch.get()==u'Коши':
            mode=2
        if self.switch.get()==u'Тушение':
            mode=3
        if self.switch.get()==u'Закон Больцмана':
            mode=4
        if self.switch.get()==u'Экспоненциальный':
            mode=5


        # try:
        #     mode_tmp=copy.deepcopy(mode)
        # except NameError:
        #     mode_tmp=1
        print(mode)
        print(self.switch.get())
        try:
            if flag ==4:# если все входные данные правильно введены и произведено решение
                # сам алгоритм решения
                #self.choose()
                #print(mode)
                # чтобы не нужно было пересчитывать матрицу стоимостей
                tmin = round(float(self.num1_entry.get()), 2)
                tmax = round(float(self.num2_entry.get()), 2)
                n = int(self.numb_pc.get())
                pack = round(float(self.package.get()), 2)

                route, energy,num_it,energy_hist=make_new_state(tmin,tmax,n,route0,dist0,energy0,mode)
                self.route_end['text']=route
                self.energy_end['text']=energy
                self.number_iteration['text']=num_it

                dist_end = copy.deepcopy(dist0)
                for i in range(dist0.shape[0]):
                    for j in range(dist0.shape[1]):
                        dist_end[i][j] = dist0[route[i] - 1][route[j] - 1]
                # цикл ниже делает на графике узнаваемым конечный маршрут
                shta=0
                for i in range(n - 1):
                    dist_end[route[i] - 1][route[i + 1] - 1] = 2000*n-1000*shta
                    shta=shta+1

                # Строим диаграмму
                x = np.array([x for x in range(num_it+1)])
                #x[0]=0
                # print(x)
                plt.plot(x, energy_hist, 'r-')# ro- с точками
                # Задаем интервалы значений по осям X и Y
                plt.axis([0, num_it, min(energy_hist) - 20, max(energy_hist) + 20])
                # Задаем заголовок диаграммы
                plt.title(u'Energy (iteration)')
                # Задаем подписи к осям X и Y
                plt.xlabel(u'Number of iteration')
                plt.ylabel(u'Energy')
                # Включаем сетку
                plt.grid()
                fig = plt.gcf()
                fig.set_size_inches(7.7, 5.2)
                plt.savefig('D:\\spirit.png', format='png', dpi=50)
                plt.clf()
                #img = PhotoImage(file='D:\\spirit.png')#вообще,в этом графике и так работает,но чтобы было одинаково...
                self.img1=ImageTk.PhotoImage(Image.open('D:\\spirit.png'))
                self.energy.create_image(0, 0, image=self.img1, anchor='nw')

                # график матрицы стоимостей после решения
                #plt.imshow(dist0, cmap='Blues')
                plt.axis([0,dist0.shape[0],  dist0.shape[0],0])
                plt.pcolor(dist_end)
                plt.colorbar()
                plt.clim(0, np.max(dist_end))
                fig1 = plt.gcf()  # возвращает фигуру
                fig1.set_size_inches(7.7, 5.2)
                plt.savefig('D:\\sprite2.png', format='png', dpi=50)
                plt.clf()
                # img2 = PhotoImage(file='D:\\sprite.png')#почему-то это не работает,хотя в случае с графиком энергии все ОК
                self.img3 = ImageTk.PhotoImage(Image.open('D:\\sprite2.png'))
                self.distance1.create_image(0, 0, image=self.img3, anchor='nw')

            else:
                showerror('Решение','Сначала введите начальные значение и постройте матрицу!')
        except NameError:
            showerror('Решение', 'Сначала введите начальные значение и постройте матрицу!')
        # выбор закона температуры
    def choose(self):
        global mode
        if self.switch.get=='Линейный':
            mode=1
        if self.switch.get=='Коши':
            mode=2
        if self.switch.get=='Тушение':
            mode=3
        if self.switch.get=='Закон Больцмана':
            mode=4
        if self.switch.get=='Экспоненциальный':
            mode=5

    def init_gui(self):
        """Builds GUI."""
        global num_it,energy_hist

        # title формы
        self.root.title('Решение задачи маршрутизации методом имитации отжига')
        # задание сетки для формы
        self.grid(column=0, row=0, sticky='nsew')

        # фрейм ввода температуры
        self.answer_frame = ttk.LabelFrame(self, text='Ввод температуры',height=300)
        self.answer_frame.grid(column=0, row=0, columnspan=4,rowspan=1, sticky='nesw')
            # напдись tmin
        ttk.Label(self.answer_frame, text='Введите минимальную температуру: ').grid(column=0, row=0,sticky='w')
            # ввод tmin
        self.num1_entry = ttk.Entry(self.answer_frame, width=45)
        self.num1_entry.grid(column=0, row=1, sticky='wesn')
            # надпись tmax
        ttk.Label(self.answer_frame, text='Введите максимальную температуру: ').grid(column=0, row=2,sticky='w')
            # ввод tmax
        self.num2_entry = ttk.Entry(self.answer_frame, width=45)
        self.num2_entry.grid(column=0, row=3, sticky='wesn')
            # надпись выбора закона изменения температуры
        ttk.Label(self.answer_frame,text='Выберите закон изменения: ').grid(column=0,row=4,sticky='w')
            # выбор закона
        list1=[u'Линейный',u'Коши',u'Тушение',u'Закон Больцмана',u'Экспоненциальный']
        self.switch=ttk.Combobox(self.answer_frame,values=list1,state='readonly')
        self.switch.grid(column=0,row=5,sticky='we')
        self.switch.set(u'Линейный')
        self.switch.bind('<<ComboboxSelected>>', self.choose())

        # фрейм задания нач. значений (число ПК+объем входящего пакета)
        self.settings_frame=ttk.LabelFrame(self,text='Настройки сети',height=300)
        self.settings_frame.grid(column=0,row=1,columnspan=4,sticky='nesw')
            # напдись numb_pc
        ttk.Label(self.settings_frame, text='Число ПК: ').grid(column=0, row=0,columnspan=4, sticky='w')
            # ввод числа пк
        self.numb_pc = ttk.Entry(self.settings_frame, width=45)
        self.numb_pc.grid(column=0, row=1,columnspan=4, sticky='wesn')
            # надпись package
        ttk.Label(self.settings_frame, text='Объем пакета: ').grid(column=0, row=2, columnspan=4,sticky='w')
            # ввод размера входящего пакета
        self.package = ttk.Entry(self.settings_frame, width=45)
        self.package.grid(column=0, row=3, columnspan=4,sticky='wesn')

        # правила для ввода
        self.help_frame=ttk.LabelFrame(self,text='Справка',height=300)
        self.help_frame.grid(column=0,row=2,columnspan=4,sticky='wesn')
        ttk.Label(self.help_frame, text='Темпаратура max должна быть больше min.\n'
                             'Число ПК в сети должно быть целым и больше 1.\n'
                             'Объем пакета должен быть больше 0').grid(column=0, row=0, columnspan=4)

        # линия разделителя
        ttk.Separator(self, orient='horizontal').grid(column=0,row=3, columnspan=4, sticky='ew')

        # кнопка рассчета матрицы стоимостей (рандом)
        self.calc_button = ttk.Button(self, text='Матрица стоимостей',command=self.calculate)
        self.calc_button.grid(column=0, row=4, columnspan=4)

        # фрейм начального маршрута и энергии
        self.start_frame = ttk.LabelFrame(self, text='Начальные значения', width=150,height=300)
        self.start_frame.grid(column=0, row=5, columnspan=4, sticky='nesw')
            # заголовок энергии
        ttk.Label(self.start_frame, text='Начальная энергия: ').grid(column=0, row=0, sticky='w')
            # вывод начальной энергии
        self.energy0=ttk.Label(self.start_frame, text='')
        self.energy0.grid(column=0, row=1, sticky='w')
            # заголовок маршрута
        ttk.Label(self.start_frame, text='Начальный маршрут: ').grid(column=0, row=2, sticky='w')
            # вывод начального маршрута
        self.route0=ttk.Label(self.start_frame, text='')
        self.route0.grid(column=0, row=3, sticky='w')

        # фрейм для графиков матрицы стоимостей
        self.dist_graph_frame=ttk.LabelFrame(self,text='Графики стоимостных матриц',width=300)
        self.dist_graph_frame.grid(column=5,row=0,columnspan=7,rowspan=6,sticky='nesw')
            # вывод canvas для графика 1
        self.distance0 = Canvas(self.dist_graph_frame, bg='white')
        self.distance0.grid(column=0, row=0, sticky='wesn')
            # вывод canvas для графика 2
        self.distance1 = Canvas(self.dist_graph_frame, bg='white')
        self.distance1.grid(column=0, row=1, sticky='wesn')

        # фрейм "Решение"
        self.solu_frame=ttk.Labelframe(self,text='Решение')
        self.solu_frame.grid(column=12,row=0,sticky='nwse')
            # кнопка "Решение"
        self.solu_button = ttk.Button(self.solu_frame, text='Решение задачи',command=self.solution)
        self.solu_button.grid(column=0, row=0,sticky='we',padx=100)
            # вывод надписи "Число итераци"
        ttk.Label(self.solu_frame, text='Число итераций: ').grid(column=0, row=1, sticky='w')
            # вывод поля для числа итераций
        self.number_iteration = ttk.Label(self.solu_frame, text='')
        self.number_iteration.grid(column=0, row=2, sticky='w')

        # фрейм с графиком энергии по итерациям
        self.en_graph_frame=ttk.LabelFrame(self,width=300,text='Энергия по итерациям')
        self.en_graph_frame.grid(column=12,row=1,rowspan=4,sticky='wesn')
            # вывод canvas для графика
        self.energy=Canvas(self.en_graph_frame,bg='white')
        self.energy.grid(column=0,row=0,sticky='wesn')

        # фрейм для конечных энергии и маршрута
        self.final_frame = ttk.LabelFrame(self, text='Конечные значения', width=300)
        self.final_frame.grid(column=12, row=5, columnspan=4, sticky='nesw')
            # вывод надписи "Конечная энергия"
        self.energy_end = ttk.Label(self.final_frame, text='Конечная энергия:')
        self.energy_end.grid(column=0, row=0, sticky='w')
            # вывод поля для конечной энергии
        self.energy_end = ttk.Label(self.final_frame, text='')
        self.energy_end.grid(column=0, row=1, sticky='w')
            # вывод надписи "Конечный маршрут"
        self.route_end=ttk.Label(self.final_frame,text='Конечный маршрут:')
        self.route_end.grid(column=0,row=2,sticky='w')
            # вывод поля для конечного маршрута
        self.route_end = ttk.Label(self.final_frame, text='')
        self.route_end.grid(column=0, row=3, sticky='w')

        # эта штука делает вокруг дочерних фреймов отступы вокруг, шоб красиво
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


def main():
    # без понятия, что это, но нужно, чтоб в трее иконка тоже менялась, объявить надо в самом начале
    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # инициализируем окно Tkinter
    root = Tk()
    # из-за того,что все начал делать через grid, при изменении размера окна ничего не масштабируется.
    # поэтому стоит запрет за изменение размеров
    root.resizable(FALSE, FALSE)
    # иконка для красоты
    icon_main='D:\\icon.ico'
    root.iconbitmap(icon_main)
    # вывод окна в центре экрана. почему 200 и 100 - непонятно, это координаты, но в чем они измеряются - неясно
    # координаты 20*10,это не в % - наверное, в пикселях. Разрешение опытным путем
    root.geometry('+200+100')
    # вставляем в окно Tkinter созданную форму
    myframe = form(root)
    # чтобы не закрывалось через миллисекунду
    myframe.mainloop()

if __name__ == '__main__':
    main()

