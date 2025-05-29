from customtkinter import *
from CTkListbox import CTkListbox
from math import floor
from tkinter import filedialog



list_all_monkey = []



class Zoo: #Класс зоопарка
    def __init__(self):
        self.__name = 'Зоопарк'
        self.__listEnclosure = []
        self.__list_all_monkeys_main = []

    def append_new_monkeys_in_all_list(self, monkey):
        self.__list_all_monkeys_main.append(monkey)

    def sort_monkey(self, monkey): # Распределяет обезьян по вольерам
        for i in self.__listEnclosure:
            if i.test_fit(monkey):
                i.sort_monkey(monkey)
                break

    def display(self):
        for i in range(len(self.__listEnclosure)):
            print(f'Вольер {i + 1}, Животные', [j.get_name() for j in self.__listEnclosure[i].get_list()])

    def count_free_spots(self): # Подсчитывает количество свободных вольеров
        cnt_free_enclosure = 0
        for i in self.__listEnclosure:
            if i.get_places() > 0:
                cnt_free_enclosure += 1

        return cnt_free_enclosure

    def count_enclosure(self): # Количество вольеров
        return len(self.__listEnclosure)

    def add_new_enclosure(self, enclosure): # Добавляет новый вольер
        self.__listEnclosure.append(enclosure)

    def delete(self): # Удаляет последний вольер списка
        del self.__listEnclosure[len(self.__listEnclosure) - 1]

    def get_list_enclosure(self):
        return self.__listEnclosure

    def get_list_all_monkey(self): # Возвращает список всех обезьян во всех вольерах
        list_all_monkeys = []
        for i in self.__listEnclosure:
            list_all_monkeys.extend(i.get_list())
        if len(list_all_monkeys) == 0:
            return self.__list_all_monkeys_main
        return list_all_monkeys

    def sort_list_all_monkey_by_settings(self, flag): # для сортировки списка обезьян
        sorted_list_monkeys = []
        if flag == 'name':
            sorted_list_monkeys = sorted(list_all_monkey, key=lambda monkey: monkey.get_name())
        if flag == 'height':
            sorted_list_monkeys = sorted(list_all_monkey, key=lambda  monkey: monkey.get_height())
        if flag == 'weight':
            sorted_list_monkeys = sorted(list_all_monkey, key=lambda monkey: monkey.get_weight())
        if flag == 'family':
            sorted_list_monkeys = sorted(list_all_monkey, key=lambda monkey: monkey.get_family())
        if flag == 'tail':
            sorted_list_monkeys = sorted(list_all_monkey, key=lambda monkey: monkey.get_tail())
        if flag == 'aggressive':
            sorted_list_monkeys = sorted(list_all_monkey, key=lambda monkey: monkey.get_aggression())
        if flag == 'number':
            sorted_list_monkeys = sorted(list_all_monkey, key=lambda monkey: monkey.get_number_enclosure())
        return sorted_list_monkeys

    def sort_list_all_enclosure_by_settings(self, flag):
        sorted_list_enclosures = []
        if flag == 'volume':
            sorted_list_enclosures = sorted(self.__listEnclosure, key=lambda enclosure: enclosure.get_volume())
        if flag == 'pool':
            sorted_list_enclosures = sorted(self.__listEnclosure, key=lambda enclosure: enclosure.get_pool())
        if flag == 'count_monkeys':
            sorted_list_enclosures = sorted(self.__listEnclosure, key=lambda enclosure: enclosure.count_monkey())
        return sorted_list_enclosures

    def get_list_sort_family(self, flag):
        list_monkeys_family = []
        for i in self.__list_all_monkeys_main:
            if i.get_info_family().lower() == flag:
                list_monkeys_family.append(i)
        return list_monkeys_family



class Monkey: # Главный класс обезьян
    def __init__(self, name, height, weight, family, type_monkey, tail, aggression):
        self.__name = name
        self.__height = height
        self.__weight = weight
        self.__family = family
        self.__type = type_monkey
        self.__tail = tail
        self.__aggression = aggression

    def display(self):
        print(f'Имя {self.__name}, рост {self.__height}, вес {self.__weight}')

    def get_number_enclosure(self):
        for i in zoo.get_list_enclosure():
            if self in i.get_list():
                return i.get_number()
        return 0

    def get_aggression(self):
        return self.__aggression

    def get_name(self):
        return self.__name

    def get_height(self):
        return self.__height

    def get_weight(self):
        return self.__weight

    def get_family(self):
        return self.__family

    def get_type_monkey(self):
        return self.__type

    def get_tail(self): # Наличие хвоста
        return self.__tail



class BroadNosedMonkey(Monkey): # Класс наследник широконосые
    def __init__(self, name, height, weight, family, type_monkey, tail, aggression):
        super().__init__(name, height, weight, family, type_monkey, tail, aggression)
        self.__abilitySwim = False
        self.__place = False
        self.__family = 'Широконосые'

    def get_info_family(self):
        return self.__family

    def get_swim_ability(self):
        return self.__abilitySwim

    def get_more_place(self):
        return self.__place



class NarrowNosedMonkey(Monkey): # Класс наследник узконосые
    def __init__(self, name, height, weight, family, type_monkey, tail, aggression):
        super().__init__(name, height, weight, family, type_monkey, tail, aggression)
        self.__abilitySwim = True
        self.__place = False
        self.__family = 'Узконосые'

    def get_info_family(self):
        return self.__family

    def get_swim_ability(self):
        return self.__abilitySwim

    def get_more_place(self):
        return self.__place



class HumanoidMonkey(Monkey): # Класс наследник человекообразные
    def __init__(self, name, height, weight, family, type_monkey, tail, aggression):
        super().__init__(name, height, weight, family, type_monkey, tail, aggression)
        self.__abilitySwim = False
        self.__place = True
        self.__family = 'Человекоподобные'

    def get_info_family(self):
        return self.__family

    def get_swim_ability(self):
        return self.__abilitySwim

    def get_more_place(self):
        return self.__place



class Enclosure:
    def __init__(self, number_enclosure, volume, pool, aggressive):
        self.__number = number_enclosure
        self.__volume = volume
        self.__pool = pool
        self.__listMonkeys = []
        self.__aggressive = aggressive
        self.__places = volume / 30 # Места в вольере
        self.__places = floor(self.__places)

    def sort_monkey(self, monkey): # Добавляет обезьяну в вольер, если там имеется место
        if self.__places >= 1:
            if monkey.get_aggression() == self.__aggressive and monkey.get_swim_ability() == self.__pool:
                self.__listMonkeys.append(monkey)
            self.__places -= 1

    def info_places(self):
        if self.__places > 0:
            return f'Осталось мест {self.__places}'
        else:
            return f'Мест нет'

    def test_fit(self, monkey):
        if monkey.get_aggression() == self.__aggressive and monkey.get_swim_ability() == self.__pool and monkey not in self.__listMonkeys:
            return True
        else:
            return False

    def get_volume(self):
        return self.__volume

    def get_pool(self):
        return self.__pool

    def get_aggressive(self):
        return self.__aggressive

    def get_list(self):
        return self.__listMonkeys

    def count_monkey(self):
        return len(self.__listMonkeys)

    def get_places(self):
        return self.__places

    def get_number(self):
        if len(str(self.__number)) == 1:
            return '0' + str(self.__number)
        return self.__number

    def get_free_spots(self):
        return self.__places

    def count_monkeys(self):
        return len(self.__listMonkeys)



zoo = Zoo() # Основной класс зоопарка

""" Визуальная часть """

set_appearance_mode('dark')
set_default_color_theme('green')



class WindowSettings(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title('Конструктор вольера')
        self.geometry('300x200')
        self.parent = parent
        self.lift()
        self.grab_set()
        self.transient(parent)

        self.switch_aggression = CTkCheckBox(self, text='агрессивность', onvalue=True, offvalue=False)
        self.switch_pool = CTkCheckBox(self, text='Наличие бассейна', onvalue=True, offvalue=False)
        self.entry_value = CTkEntry(self, placeholder_text='Введите объем вольера...')
        self.switch_aggression.pack(pady=5, padx=5, expand=True)
        self.switch_pool.pack(pady=5, padx=5, expand=True)
        self.entry_value.pack(pady=5, padx=5, expand=True)
        self.add_new_enclosure_button_el = CTkButton(self, text='Добавить вольер', command=self.add_new_enclosure_el)
        self.add_new_enclosure_button_el.pack(pady=5, padx=5)

    def add_new_enclosure_el(self):
        try:
            volume = int(self.entry_value.get())
            pool = self.switch_pool.get()
            aggressive = self.switch_aggression.get()

            # Создаем новый вольер только когда нажата кнопка и значения получены
            new_enclosure = Enclosure(zoo.count_enclosure() + 1, volume, pool, aggressive)
            zoo.add_new_enclosure(new_enclosure)
            enclosure_info = (
                f'Номер вольера: {new_enclosure.get_number()} '
                f'Объем вольера: {new_enclosure.get_volume()} '
                f'бассейн: {'да' if new_enclosure.get_pool() else 'нет'} '
                f'агрессия: {'да' if new_enclosure.get_aggressive() else 'нет'} '
            )
            self.parent.enclosure_listbox.insert(END, enclosure_info)
            zoo.add_new_enclosure(new_enclosure)
        except ValueError:
            print("Ошибка: объем вольера должен быть числом")



class WindowSort(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title('Меню сортировки')
        self.geometry('500x600')
        self.parent = parent
        self.lift()
        self.grab_set()
        self.transient(parent)

        self.frame = CTkFrame(self, bg_color='transparent')
        self.frame.pack(pady=5, padx=5)
        self.value_sort_switches = StringVar(value='')
        self.sort_switches = {
            'Узконосые': CTkButton(self.frame, text='Узконосые', command=lambda: self.choice_monkeys('узконосые')),
            'Широконосые': CTkButton(self.frame, text='Широконосые', command=lambda: self.choice_monkeys('широконосые')),
            'Человекообразные': CTkButton(self.frame, text='Человекообразные', command=lambda: self.choice_monkeys('человекообразные')),
            'Живут в бассейне': CTkButton(self.frame, text='Живут в бассейне', command=lambda: self.sort_for_flag('pool', True)),
            'Не живут в бассейне': CTkButton(self.frame, text='Живут в бассейне', command=lambda: self.sort_for_flag('pool', False)),
            'Агрессивные': CTkButton(self.frame, text='Агрессивные', command=lambda: self.sort_for_flag('aggressive', True)),
            'Не агрессивные': CTkButton(self.frame, text='не агреccивнные', command=lambda: self.sort_for_flag('aggressive', False))
        }

        for i in self.sort_switches.values():
            i.pack(side=BOTTOM, fill=BOTH, expand=True, padx=0, pady=5)

        self.__sort_list = []

    def sort_for_flag(self, flag, flag2):
        sorted_list = []
        if flag == 'pool':
            for i in zoo.get_list_all_monkey():
                if i.get_swim_ability() == flag2:
                    sorted_list.append(i)
        LoadWindow(self.parent).start_loading()
        self.parent.update_listbox_more_sort_monkeys(sorted_list)
        if flag == 'aggressive':
            for i in zoo.get_list_all_monkey():
                if i.get_swim_ability() == flag2:
                    sorted_list.append(i)
        LoadWindow(self.parent).start_loading()
        self.parent.update_listbox_more_sort_monkeys(sorted_list)

    def choice_monkeys(self, flag):

        self.__sort_list = zoo.get_list_sort_family(flag)
        print(self.__sort_list)
        self.parent.update_listbox_more_sort_monkeys(self.__sort_list)



class LoadWindow(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('200x25')
        self.lift()
        self.transient(parent)
        self.grab_set()
        self._center_window()
        self.overrideredirect(True)
        self.progressbar = CTkProgressBar(
            self,
            orientation="horizontal",
            width=300,
            height=30,
            corner_radius=15,
            mode="indeterminate",
            indeterminate_speed=0.5
        )
        self.progressbar.pack(pady=5, padx=5, expand=True)

    def _center_window(self):
        """Центрирует окно относительно родительского или экрана."""
        self.update_idletasks()  # Обновляем геометрию окна
        width = self.winfo_width()
        height = self.winfo_height()

        # Получаем координаты родительского окна
        parent_x = self.master.winfo_rootx()
        parent_y = self.master.winfo_rooty()
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()

        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2

        self.geometry(f"+{x}+{y}")

    def start_loading(self):
        self.progressbar.start()
        self.after(10000, self.close)

    def close(self):
        self.grab_release()
        self.destroy()

class MonkeyApp(CTk):
    def __init__(self):
        super().__init__()

        # параметры окна
        self.title('Зоопарк')
        self.geometry('1280x720')
        self.resizable(False, False)

        # Список для хранения данных
        self.__list_monkey_in_enclosure = zoo.get_list_all_monkey()
        self.__list_all_monkey = list_all_monkey
        self.__list_enclosure = zoo.get_list_enclosure()

        # Список обезьян
        self.frame_list_monkey = CTkFrame(self, fg_color='transparent')
        self.frame_list_monkey.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=20)

        self.text_monkey = CTkLabel(self.frame_list_monkey, text=f'Список обезьян, общее количество обезьян: 0', font=('Arial', 16))
        self.info_count_monkeys()
        self.text_monkey.pack(side='top', expand=True, pady=0)

        self.monkey_listbox = CTkListbox(self.frame_list_monkey, width=300,
                                         height=1000,
                                         corner_radius=0,
                                         multiple_selection=False,
                                         scrollbar_button_color='green',
                                         scrollbar_button_hover_color='green',
                                         font=('Arial', 14))

        self.monkey_listbox.pack(side='bottom',
                                 fill='both',
                                 expand=True)
        self.monkey_listbox.bind("<Double-Button-1>", self.show_info_monkey_list)

        # Список вольеров
        self.frame_list_enclosure = CTkFrame(self, fg_color='transparent')
        self.frame_list_enclosure.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=20)

        self.text_enclosure = CTkLabel(self.frame_list_enclosure, text='Список вольеров', font=('arial', 16))
        self.text_enclosure.pack(side='top', expand=True, pady=0)

        self.enclosure_listbox = CTkListbox(self.frame_list_enclosure,
                                            width=300,
                                            height=1000,
                                            corner_radius=0,
                                            multiple_selection=False,
                                            scrollbar_button_color='green',
                                            scrollbar_button_hover_color='green',
                                            font=('Arial', 14))

        self.enclosure_listbox.pack(side='top',
                                    fill=BOTH,
                                    expand=True,
                                    padx=0,
                                    pady=0)
        self.enclosure_listbox.bind("<Double-Button-1>", self.show_info_enclosure_list)

        # Окно с кнопками
        self.frame = CTkFrame(self,
                              fg_color='transparent')

        self.frame.pack(padx=0,
                        pady=(43, 20))
        # Сортировка листа с вольерами

        self.sort_enclosures_text_var = StringVar(value='')

        self.sort_enclosures_switches = {
            'volume': CTkSwitch(self.frame, text='Объему', command=lambda: self.sort_list_enclosures('volume')),
            'pool': CTkSwitch(self.frame, text='Наличию бассейна', command=lambda: self.sort_list_enclosures('pool')),
            'count_monkeys': CTkSwitch(self.frame, text='Количеству обезьян', command=lambda: self.sort_list_enclosures('count_monkeys'))
        }

        for switch in self.sort_enclosures_switches.values():
            switch.pack(side=BOTTOM, fill=BOTH, expand=True, padx=0, pady=5)

        self.sort_enclosures_text = CTkLabel(self.frame, text='Сортировка вольеров по:')
        self.sort_enclosures_text.pack(side=BOTTOM, fill=BOTH, expand=True, padx=0, pady=5)

        # Кнопки сортировки листа с обезьянами

        self.sort_var = StringVar(value='')

        self.sort_switches = {
            'name': CTkSwitch(self.frame, text='имени', command=lambda: self.sorted_list('name')),
            'height': CTkSwitch(self.frame, text='росту', command=lambda: self.sorted_list('height')),
            'weight': CTkSwitch(self.frame, text='весу', command=lambda: self.sorted_list('weight')),
            'family': CTkSwitch(self.frame, text='семейству', command=lambda: self.sorted_list('family')),
            'tail': CTkSwitch(self.frame, text='хвосту', command=lambda: self.sorted_list('tail')),
            'aggressive': CTkSwitch(self.frame, text='драчливости', command=lambda: self.sorted_list('aggressive')),
            'number': CTkSwitch(self.frame, text='номеру вольера', command=lambda: self.sorted_list('number'))
        }

        for switch in self.sort_switches.values():
            switch.pack(side=BOTTOM, fill=BOTH, expand=True, padx=0, pady=5)

        self.sort_monkeys_text = CTkLabel(self.frame, text='Сортировка обезьян по:')
        self.sort_monkeys_text.pack(side=BOTTOM, fill=BOTH, expand=True, padx=0, pady=5)

        self.button_sort_monkeys_more = CTkButton(self.frame, text='доп. сортировка', command=self.open_sorted_window)
        self.button_sort_monkeys_more.pack(
            side=BOTTOM,
            fill=BOTH,
            expand=True,
            padx=0,
            pady=5
        )

        # Кнопка добавления вольера
        self.add_enclosure_button = CTkButton(self.frame,
                                              text='Добавить вольер',
                                              command=self.open_settings_window)
        self.add_enclosure_button.pack(side=BOTTOM,
                                       fill=BOTH,
                                       expand=True,
                                       padx=0,
                                       pady=5)


        # Кнопка распределения обезьян по вольерам
        self.sort_monkey_in_enclosure = CTkButton(self.frame,
                                                  text='Распределить обезьян по вольерам',
                                                  command=self.sort_monkey_in_enclosure)
        self.sort_monkey_in_enclosure.pack(side=BOTTOM,
                                           fill=BOTH,
                                           expand=True,
                                           padx=0,
                                           pady=5)

        # Кнопка для загрузки данных про обезьян из файла
        self.read_file_list_monkey = CTkButton(self.frame,
                                               text='Загрузить список обезьян',
                                               command=self.load_data_monkey)

        self.read_file_list_monkey.pack(side=BOTTOM,
                                        fill=BOTH,
                                        expand=True,
                                        padx=0,
                                        pady=5)

        # Кнопка загрузки данных с вольерами
        self.read_file_list_enclosure = CTkButton(self.frame,
                                                  text='Загрузить список вольеров',
                                                  command=self.load_data_enclosure)

        self.read_file_list_enclosure.pack(side=BOTTOM,
                                           fill=BOTH,
                                           expand=True,
                                           padx=0,
                                           pady=5)

        # Кнопка появления окна сортировки
        self.sort_button = CTkButton(self.frame, text='Выход', command=self.destroy)
        self.sort_button.pack(side=BOTTOM,
                              fill=BOTH,
                              expand=True,
                              padx=0,
                              pady=5)

    def open_sorted_window(self):
        WindowSort(self)

    def sorted_list(self, flag):
        self.sort_var.set(flag)
        # Деактивируем все другие switch
        for key, switch in self.sort_switches.items():
            if key != flag:
                switch.deselect()
        LoadWindow(self).start_loading()
        self.update_sorted_list()

    def info_count_monkeys(self):
        count_all_monkeys = len(zoo.get_list_all_monkey())
        self.text_monkey.configure(text=f'Список обезьян, общее количество обезьян: {count_all_monkeys}')

    def update_sorted_list(self):
        sort_type = self.sort_var.get()
        if sort_type:
            self.monkey_listbox.delete(0, END)
            sorted_monkeys = zoo.sort_list_all_monkey_by_settings(sort_type)
            for monkey in sorted_monkeys:
                monkey_info = (
                    f"Имя: {monkey.get_name()}\t"
                    f"Рост: {monkey.get_height()}\t"
                    f"Вес: {int(monkey.get_weight())}\t"
                    f"Агрессия: {'Да' if monkey.get_aggression() else 'Нет'}"
                )
                self.monkey_listbox.insert(END, monkey_info)
        self.info_count_monkeys()

    def sort_list_enclosures(self, flag):
        self.sort_enclosures_text_var.set(flag)
        for key, switch in self.sort_enclosures_switches.items():
            if key != flag:
                switch.deselect()
        LoadWindow(self).start_loading()
        self.update_sorted_list_enclosure()

    def update_sorted_list_enclosure(self):
        sort_type = self.sort_enclosures_text_var.get()
        if sort_type:
            self.enclosure_listbox.delete(0, END)
            sorted_enclosure = zoo.sort_list_all_enclosure_by_settings(sort_type)
            for enclosure in sorted_enclosure:
                enclosure_info = (
                    f"Номер: {enclosure.get_number()}\t"
                    f"Объем: {int(enclosure.get_volume())}\t"
                    f"Бассейн: {'Да' if enclosure.get_pool() else 'Нет'}\t"
                    f"обезьяны: {enclosure.count_monkey()}"
                )
                self.enclosure_listbox.insert(END, enclosure_info)

    def open_settings_window(self):
        WindowSettings(self)

    def update_listbox_more_sort_monkeys(self, array):
        list_sorted_monkeys = array
        self.monkey_listbox.delete(0, END)
        for monkey in list_sorted_monkeys:
            monkey_info = (
                f"Имя: {monkey.get_name()}\t"
                f"Рост: {monkey.get_height()}\t"
                f"Вес: {int(monkey.get_weight())}\t"
                f"Агрессия: {'Да' if monkey.get_aggression() else 'Нет'}"
            )
            self.monkey_listbox.insert(END, monkey_info)
        self.info_count_monkeys()

    def load_data_monkey(self):
        self.__list_all_monkey.clear()
        self.monkey_listbox.delete(0, 'end')
        filepath = filedialog.askopenfilename(title='Выберете файл')

        try:
            with open(filepath, encoding='utf-8') as f:
                for line in f:
                    if ',' in line:
                        parts = [p.strip() for p in line.strip().split(',')]
                        name, height, weight, family, type_monkey, tail, aggression = parts
                        if family.lower() == 'широконосые':
                            monkey = BroadNosedMonkey(name.strip(), float(height.strip()), float(weight.strip()), family.strip(), type_monkey.strip(), eval(tail.strip()), eval(aggression.strip()))
                            list_all_monkey.append(monkey)
                            self.__list_all_monkey.append(monkey)
                            zoo.append_new_monkeys_in_all_list(monkey)
                        if family.lower() == 'узконосые':
                            monkey = NarrowNosedMonkey(name.strip(), float(height.strip()), float(weight.strip()), family.strip(), type_monkey.strip(), eval(tail.strip()), eval(aggression.strip()))
                            list_all_monkey.append(monkey)
                            self.__list_all_monkey.append(monkey)
                            zoo.append_new_monkeys_in_all_list(monkey)
                        if family.lower() == 'человекообразные':
                            monkey = HumanoidMonkey(name.strip(), float(height.strip()), float(weight.strip()), family.strip(), type_monkey.strip(), eval(tail.strip()), eval(aggression.strip()))
                            list_all_monkey.append(monkey)
                            self.__list_all_monkey.append(monkey)
                            zoo.append_new_monkeys_in_all_list(monkey)

        except FileNotFoundError:
            print("Файл monkeys.txt не найден.")
            return
        LoadWindow(self).start_loading()
        for monkey in self.__list_all_monkey:
            # Создаем строку со всеми данными об обезьяне
            monkey_info = (
                f"Имя: {monkey.get_name()}\t"
                f"Рост: {monkey.get_height()}\t"
                f"Вес: {int(monkey.get_weight())}\t"
                f"Агрессия: {'Да' if monkey.get_aggression() else 'Нет'}"
            )
            self.monkey_listbox.insert(END, monkey_info)
        self.info_count_monkeys()

    def load_data_enclosure(self):
        self.__list_enclosure.clear()
        self.enclosure_listbox.delete(0, 'end')
        filepath = filedialog.askopenfilename(title='Выберете имя файла')

        try:
            with open(filepath, encoding='utf-8') as f:
                for line in f:
                    if ',' in line:
                        parts = [i for i in line.strip().split(',')]
                        number_enclosure, volume, pool, aggressive = parts
                        enclosure = Enclosure(number_enclosure, int(volume), eval(pool), eval(aggressive))
                        zoo.add_new_enclosure(enclosure)

        except FileNotFoundError:
            print("Файл enclosures.txt не найден.")
            return
        LoadWindow(self).start_loading()
        for enclosure in self.__list_enclosure:
            enclosure_info = (
                f'Номер вольера: {enclosure.get_number()} '
                f'Объем вольера: {enclosure.get_volume()} '
                f'бассейн: {'да' if enclosure.get_pool() else 'нет'} '
                f'агрессия: {'да' if enclosure.get_aggressive() else 'нет'} '
            )
            self.enclosure_listbox.insert(END, enclosure_info)

    def sort_monkey_in_enclosure(self):
        for i in self.__list_all_monkey:
            zoo.sort_monkey(i)
        print(f'Список вольеров {zoo.get_list_enclosure()}')
        print(f'Список всех обезьян {self.__list_all_monkey}')
        print('Обезьяны рассортированы')
        for i in zoo.get_list_enclosure():
            for k in i.get_list():
                print(f'{i, k.get_name()}')
            print('\n')
        self.info_count_monkeys()

    def show_info_monkey_list(self, even):
        selection = self.monkey_listbox.curselection()
        if selection:
            index = selection
            selected_monkey = self.__list_all_monkey[index]
            info_text = (
                f"Имя: {selected_monkey.get_name()}\n"
                f"Рост: {selected_monkey.get_height()}\n"
                f"Вес: {selected_monkey.get_weight()}\n"
                f"Семейство: {selected_monkey.get_family()}\n"
                f"Тип: {selected_monkey.get_type_monkey()}\n"
                f"Хвост: {'Да' if selected_monkey.get_tail() else 'Нет'}\n"
                f"Агрессия: {'Да' if selected_monkey.get_aggression() else 'Нет'}\n"
                f"Умеет плавать: {'Да' if selected_monkey.get_swim_ability() else 'Нет'}\n"
                f"Требует больше места: {'Да' if selected_monkey.get_more_place() else 'Нет'}"
            )
            info_window_monkey = CTkToplevel(self)
            info_window_monkey.title("Подробная информация")
            info_label = CTkLabel(info_window_monkey, text=info_text, justify=LEFT)
            info_label.pack(padx=20, pady=20)
            info_window_monkey.grab_set()
            info_window_monkey.transient(self)
            info_window_monkey.lift()

    def show_info_enclosure_list(self, even):
        selection = self.enclosure_listbox.curselection()
        if selection:
            index = selection
            selected_enclosure = self.__list_enclosure[index]
            str_monkeys = ''
            for i in selected_enclosure.get_list():
                    str_monkeys += f'{i.get_name()}\n'

            info_text = (
                f'Номер вольера: {selected_enclosure.get_number()}\n'
                f'Объем вольера: {selected_enclosure.get_volume()}\n'
                f'Наличие бассейна: {'Да' if selected_enclosure.get_pool() else 'Нет'}\n'
                f'Наличие агрессивности: {'Да' if selected_enclosure.get_aggressive() else 'Нет'}\n'
                f'Количество свободных мест: {selected_enclosure.get_free_spots()}\n'
                f'Количество обезьян в вольере: {selected_enclosure.count_monkeys()}\n'
                f'Список обезьян в вольере:\n{str_monkeys}'
            )
            info_window_enclosure = CTkToplevel(self)
            info_window_enclosure.title("Подробная информация")
            info_label = CTkLabel(info_window_enclosure, text=info_text, justify=LEFT)
            info_label.pack(padx=20, pady=20)
            info_window_enclosure.grab_set()
            info_window_enclosure.transient(self)
            info_window_enclosure.lift()



if __name__ == '__main__':
    MonkeyApp().mainloop()



