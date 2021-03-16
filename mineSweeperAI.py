# https://yandex.ru/games/play/97011
# разрабатывался для 40*33 - при 1920*1080 и панели сбоку - прокручиваем сайт вниз до упора
# прекратить выполнение досрочно - увести мышку за экран (лево-верх)
# https://pyautogui.readthedocs.io/en/latest/screenshot.html документация по pyautogui
import pyautogui
import time
from random import randint
import sys



def start_click(game_field):  # на доделку будем сюда передвать матрицу
    """ просто рандомный клик по площади \n
    переделать. сделать анализ веса \n
    и клик по наименее вероятной бомбе \n """
    i = randint(0, cells_x-1)
    j = randint(0, cells_y-1)
    open_in_game_field(game_field, i, j)
    # x = game_coords[0] + i*cell_width + 15
    # y = game_coords[1] + j*cell_width + 15
    # pyautogui.click(x=x, y=y)


def screenshot_to_matrix(game_field, img=None):
    """ -1  = закрытая клетка \n
    0-8 = число в клетке - сколько бомб граничит \n
    9  = флаг \n
    переделать через getpixel - Тормозило жутко :D, стало лучше \n
    не встречал цифры 8 - её не добавил в распознание \n
    game_field = матрица \n"""
    if img == None:
        # pyautogui.moveTo(20, 20)
        img = pyautogui.screenshot('1.png', region=game_coords)

    # (213, 213, 213) = 0 на +14 +18
    # (52, 152, 219) = 1
    # (46, 204, 113) = 2
    # (229, 130, 159) = 3
    # (190, 140, 182) = 4
    # (239, 199, 150) = 5
    # (56, 190, 169) = 6
    # (203, 160, 125) = 7 на +13 +10
    # (204, 75, 76) = флаг на +13 +10
    for j in range(len(game_field[0])):
        for i in range(len(game_field)):
            # для 0..5
            x_get_pix = (i*26)+14
            y_get_pix = (j*26)+18
            pix = img.getpixel((x_get_pix, y_get_pix))
            if pix == (213, 213, 213):
                game_field[i][j] = 0
            elif pix == (52, 152, 219):
                game_field[i][j] = 1
            elif pix == (46, 204, 113):
                game_field[i][j] = 2
            elif pix == (229, 130, 159):
                game_field[i][j] = 3
            elif pix == (190, 140, 182):
                game_field[i][j] = 4
            elif pix == (239, 199, 150):
                game_field[i][j] = 5
            elif pix == (56, 190, 169):
                game_field[i][j] = 6

            elif pix == (204, 75, 76):
                # для флага
                x_get_pix = (i*26)+13
                y_get_pix = (j*26)+10
                pix = img.getpixel((x_get_pix, y_get_pix))
                if pix == (204, 75, 76):
                    game_field[i][j] = 9
                elif pix == (203, 160, 125):
                    game_field[i][j] = 7


def print_matrix(matrix):
    """ распечатаем матрицу из чисел \n
    (макс 2 значные положительные и однозначные отрицательные) \n
    game_field = матрица \n """
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            if matrix[i][j] == 0:
                print('\033[30m%2s\033[0m' % (' '), end='')
            elif matrix[i][j] == -1:
                print('\033[37m%2s\033[0m' % ('▓'), end='')
            elif matrix[i][j] in range(1, 8):
                print('\033[32m%2s\033[0m' % (matrix[i][j]), end='')
            elif matrix[i][j] == 9:
                print('\033[31m%2s\033[0m' % ('▓'), end='')
            else:
                print('\033[33m%2s\033[0m' % ('▓'), end='')
                pass
        print()


def count_secret_around(game_field, x, y):
    """ считаем сколько закрытых клеток окружает запрошенную позицию \n
    возвращаем число  \n
    x и y по координатам матрицы \n
    game_field = матрица \n
    x y - позиция в матрице \n """
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x+i < 0 or y+j < 0 or x+i > len(game_field)-1 or y+j > len(game_field[0])-1:
                continue
            if game_field[x+i][y+j] == -1:
                count += 1
    return count


def count_bomb_around(game_field, x, y):
    """ считаем сколько бомб окружает запрошенную позицию  \n
    возвращаем число  \n
    x и y по координатам матрицы \n
    game_field = матрица \n
    x y - позиция в матрице \n """
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x+i < 0 or y+j < 0 or x+i > len(game_field)-1 or y+j > len(game_field[0])-1:
                continue
            if game_field[x+i][y+j] == 9:
                count += 1
    return count


def mark_bomb_in_game_field(game_field, x, y):
    if game_field[x][y] != 9:
        game_field[x][y] = 9
    x_mark = game_coords[0] + (x)*cell_width + 15
    y_mark = game_coords[1] + (y)*cell_width + 15
    pyautogui.click(button='right', x=x_mark, y=y_mark)


def open_in_game_field(game_field, x, y):
    """ откываем клетку по указанным координатам матрицы """
    if game_field[x][y] == -1:
        x_mark = game_coords[0] + (x)*cell_width + 15
        y_mark = game_coords[1] + (y)*cell_width + 15
        pyautogui.click(x=x_mark, y=y_mark)
        # подождём, пока всё откроется
        time.sleep(1.05)
        # по идее надо перескинировать матрицу
        screenshot_to_matrix(game_field)


def mark_bomb_around(game_field, x, y):
    """ вокруг заданной клетки помечаем все закрытые бомбами \n
    game_field = матрица \n
    x y - позиция в матрице \n """
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x+i < 0 or y+j < 0 or x+i > len(game_field)-1 or y+j > len(game_field[0])-1:
                continue
            if game_field[x+i][y+j] == -1:
                game_field[x+i][y+j] = 9
                mark_bomb_in_game_field(game_field, x+i, y+j)


def open_secret_around(game_field, x, y):
    """ вокруг заданной позиции открываем все закрытые
    game_field = матрица \n
    x y - позиция в матрице \n  """
    for i in range(-1, 2):
        for j in range(-1, 2):
            # если выходим за пределы матрицы, то пропускаем
            if x+i < 0 or y+j < 0 or x+i > len(game_field)-1 or y+j > len(game_field[0])-1:
                continue
            if game_field[x+i][y+j] == -1:
                open_in_game_field(game_field, x+i, y+j)


def rule1(game_field):
    """ Если число закртытых клеток + отмеченных бомб вокруг клетки = числу в клетке \n
    помечаем всё вокруг бомбами \n
    после действия можно не обновлять поле с экрана \n"""
    count_action = 0  # потом для приоритета алгоритмов.. пока есть простые действия 'count_action <> 0' делаем их
    # перебор матрицы
    for j in range(len(game_field[0])):
        for i in range(len(game_field)):
            if game_field[i][j] > 0 and game_field[i][j] < 9:
                count_sa = count_secret_around(game_field, i, j)
                count_ba = count_bomb_around(game_field, i, j)
                if count_sa > 0 and game_field[i][j] == count_sa + count_ba:
                    mark_bomb_around(game_field, i, j)
                    count_action += 1
    return count_action


def rule2(game_field):
    """ если число в клетке равняется числу бобм вокруг - открываем все закртытые вокруг \n
    после пробега - обновляем поле с экрана \n """
    count_action = 0  # потом для приоритета алгоритмов.. пока есть простые действия 'count_action <> 0' делаем их
    # перебор матрицы
    for j in range(len(game_field[0])):
        for i in range(len(game_field)):
            if game_field[i][j] > 0 and game_field[i][j] < 9:
                count_sa = count_secret_around(game_field, i, j)
                count_ba = count_bomb_around(game_field, i, j)
                if game_field[i][j] == count_ba and count_sa > 0:
                    open_secret_around(game_field, i, j)
                    count_action += 1
    return count_action


def make_field_set(game_field, x, y):  # для правила 3
    """ по статейке с хабра - попробуем анализировать где могут быть бомбы, а где нет \n
    бегаем вокруг заданной клетки \n
    формирует пары возможностей \n
    a.add((frozenset(((i,j), (ik,jk))), 1)) \n
    где i..ik индекс X секретной клетки \n
    где j..jk индекс Y секретной клетки \n
    1 = количество бомб в клетках \n """
    bomb_around = 0  # собственно кол-во бомб вокруг клетки
    list_coords = []  # здесь будем сохранять координаты для пар возможностей
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x+i < 0 or y+j < 0 or x+i > len(game_field)-1 or y+j > len(game_field[0])-1:
                continue
            if game_field[x+i][y+j] == 9:
                bomb_around += 1
            if game_field[x+i][y+j] == -1:
                # тут сохраним координаты
                list_coords.append((x+i, y+j))
    a = set()
    # формируем frozenset с координатами закртытых ячеек
    c = frozenset(list_coords)
    if len(c) > 0:
        num_bomb = game_field[x][y] - bomb_around
        a.add((c, num_bomb))
    return a


def make_finde_set(a):  # для правила 3 - тут может быть косяк, но я не нашёл такого варианта
    """ замороченный алгоритм, смысл в том, что обрабатываем веса и вероятность \n
    a.add((frozenset((1, 2)), 1)) \n
    a.add((frozenset((1, 2, 3)), 2)) \n
    выдаст {(frozenset({координаты}), количество бомб), (frozenset({(0,0)}), 1), (frozenset({(5,2), (6,3)}), 2)} \n
    возвращаем однозначные бомбы \n
    или однозначые "нет бомб" \n
    тут может быть косяк, но лень перебирать все варианты - пока не находил ошибок \n """
    c = set()
    # создадим копию множества
    b = a.copy()
    # # пересечения множеств
    for i in a:
        # создадим копию множества без элемента
        b.remove(i)
        # переберём получившееся множество
        for j in b:
            # print(i, j)
            # если кол-во мин больше
            if i[1] > j[1]:
                # если клетки входят - разобьём множество
                if len(j[0].intersection(i[0])) != 0:
                    c.add((frozenset(i[0]-j[0]), i[1]-j[1]))

            # если в множестввах кол-во бомб одинаково - попробуем выделить подмножество без бомб
            elif i[1] == j[1]:
                if j[0].issubset(i[0]):
                    c.add((frozenset(i[0]-j[0]), 0))
                elif i[0].issubset(j[0]):
                    c.add((frozenset(j[0]-i[0]), 0))
            else:  # если кол-во мин меньше
                if len(i[0].intersection(j[0])) != 0:
                    c.add((frozenset(j[0]-i[0]), j[1]-i[1]))
    a = a.union(c)
    c = set()
    # однозначные результаты
    for element in a:
        if len(element[0]) == element[1] or element[1] == 0:
            c.add(element)
    return c


def make_action_with_field_set(game_field, need_action):
    """  обрабатываем результаты make_finde_set \n
    у нас есть массив формата a == ((frozenset(((i,j), (ik,jk))), N)) \n
    либо расставим бомбы в количестве N \n
    либо, если N 0 - откроем пустые \n """
    for item in need_action:
        # если бомб быть не может - просто откроем
        if item[1] > 0:
            for coords in item[0]:
                mark_bomb_in_game_field(game_field, coords[0], coords[1])
        else:
            for coords in item[0]:
                open_in_game_field(game_field, coords[0], coords[1])


def rule3(game_field):
    """ хабро алгоритм - создаём множества вероятностей бомб и высчитываем их пересечение
    фиг знает как это объяснить.. помоему %!%№ поймёшь
    тут где-то есть ошибка, но лень вычислять...
    скорее всего в intersection - там с пересечениями полей... недоработанный алгоритм
    можно просто выключить правило, тогда работает без подрывов и останавливается
    когда не может однозначно вычислить бомбы"""
    count_action = 0
    a = set()
    for j in range(len(game_field[0])):
        for i in range(len(game_field)):
            if game_field[i][j] > 0 and game_field[i][j] < 9:
                # если вокруг клетки есть закртые, то
                if count_secret_around(game_field, i, j) > 0:
                    # попробуем собрать вероятности
                    b = make_field_set(game_field, i, j)
                    if len(b) > 0:
                        a = a.union(b)
    if len(a) > 0:
        # здесь увеличим экшен и промаркируем бомбы \ откроем пустые
        # короче обработаем массив а
        need_action = make_finde_set(a)
        if len(need_action) > 0:
            count_action += 1
            make_action_with_field_set(game_field, need_action)
    return count_action


""" погнали саму прогу """
if __name__ == "__main__":
    # тут ищем конец игры (переделать, искать по всему экрану)
    game_over_region = (595, 180, 625, 216)
    # тут ищем новую игру (переделать, искать по всему экрану)
    new_game_region = (82, 95, 885, 130)
    # здесь координаты игрового поля (сделать авто распознование)
    game_coords = (396, 215, 1443-395, 1070-205)
    bombs = 999  # количество бомб - переделать - сделать скан с игры
    cells_x = 40  # количество клеток по X (сделать скан с поля)
    cells_y = 33  # количество клето по Y (сделать скан с поля)


    cell_width = 26  # ширина клеток (справедливо для яндекс сапёра)
    # генерируем матрицу поля, значение -1 это закрытая клетка
    game_field = [[-1] * cells_y for _ in range(cells_x)]


    # pyautogui.PAUSE = 0.1 # выставляет пазу между действиями через pyautogui
    # переключаемся альт табом в окно с сапёром
    pyautogui.hotkey('alt', 'tab')
    # поспим, на всякий случай чтоб сильно быстро не переключаться
    time.sleep(0.5)

    # нажмём новую игру
    pyautogui.click('./img/new_game.png')
    time.sleep(1)
    # воткнём случайный клик
    start_click(game_field)
    # time.sleep(2)
    print_matrix(game_field)
    # sys.exit()


    # погнали крутить цикл
    runing = True
    while runing:
        # win = pyautogui.locateOnScreen('./img/win.png', grayscale=True) - через эту шляпу пипец долго.. лучше через getpixel
        img = pyautogui.screenshot()
        x_get_pix = 608
        y_get_pix = 210
        # (0, 128, 0) = цвет победы :)
        # (255, 0, 0) = цвет поражения :(
        pix = img.getpixel((x_get_pix, y_get_pix))

        # win = pyautogui.locateOnScreen('./img/win.png', grayscale=True)
        # pyautogui.hotkey('alt', 'tab')
        
        if pix == (0, 128, 0):
            print('Ура победа!!!!, заново, победим опять!')
            pyautogui.click('./img/new_game.png')
            time.sleep(1)
            game_field = [[-1] * cells_y for _ in range(cells_x)]
            start_click(game_field)        
            # runing = False
            continue
        else:
            # pyautogui.hotkey('alt', 'tab')
            # loose = pyautogui.locateOnScreen('./img/game_over.png', grayscale=True)
            # pyautogui.hotkey('alt', 'tab')
            if pix == (255, 0, 0):
                print('Заново, проиграли :(')
                pyautogui.click('./img/new_game.png')
                time.sleep(1)
                game_field = [[-1] * cells_y for _ in range(cells_x)]
                start_click(game_field)

        count_action = 0
        count_action = rule1(game_field)
        count_action += rule2(game_field)
        # if count_action == 0:
        #     count_action += rule3(game_field)
        #     if count_action == 0:
        #         start_click(game_field)
        #         continue



    pyautogui.hotkey('alt', 'tab')
    print_matrix(game_field)
