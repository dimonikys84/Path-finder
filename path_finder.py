import math

# Тестовое чб изображение 5x6
test_arr = [[False,False,False,False,False],
           [False,False,True ,False,False],
           [False,False,True ,False,False],
           [True ,True ,True ,True ,True ],
           [True ,False,False,False,False],
           [False,False,False,False,False]]



def find_paths(array):

    X=len(array[0])
    Y=len(array)

    neighbors = lambda x, y : [[x2, y2] for x2 in range(x-1, x+2)
                                   for y2 in range(y-1, y+2)
                                   if (-1 < x <= X and
                                       -1 < y <= Y and
                                       (x != x2 or y != y2) and
                                       (0 <= x2 <= X) and
                                       (0 <= y2 <= Y))]

    arr = array
    lines = []
    used_pixels = []

    # Определение направления движения точки
    def check_vec_side(p1,p2):
        vec = [p2[0]-p1[0],p2[1]-p1[1]]
        side = 'r'

        if vec[0] == 1 and vec[1] == -1:
            side = 'l'
        elif vec[0] == 1 and vec[1] == 0:
            side = 'l'
        elif vec[0] == 1 and vec[1] == 1:
            side = 'l'
        elif vec [0] == 0 and vec[1] == 1:
            side = 'l'

        return side

    # Посик прринадлежности точки к линии
    def find_affiliation(point,inverted):
        # Перебираем каждую линию

        if len(lines) == 0:
            lines.append([point])
            used_pixels.append(point)
            return True

        lines_last_objects = [i[-1] for i in lines]
        nb = neighbors(point[0],point[1])
        indexes = []
        for n in nb:
            if n in lines_last_objects:
                indexes.append(lines_last_objects.index(n))

        for i in indexes:
            line = lines[i]
            #Определяем расстояние между последней/первой точкой линии
            dist_nd = math.sqrt(math.pow(line[-1][0]-point[0],2)+math.pow(line[-1][1]-point[1],2))
            #Определяем расстояние между начальной точкой линии
            dist_st = math.sqrt(math.pow(line[0][0]-point[0],2)+math.pow(line[0][1]-point[1],2))

            if inverted == False and 0 < dist_nd < 1.5:
                if check_vec_side(line[-1],point) == 'l':
                    line.append(point)
                    used_pixels.append(point)
                    return True
            elif inverted == True and 0 < dist_nd < 1.5:
                if check_vec_side(line[-1],point) == 'r':
                    line.append(point)
                    used_pixels.append(point)
                    return True
            elif inverted == True and 0 < dist_st < 1.5:
                if check_vec_side(line[-1],point) == 'r':
                    line + point
                    used_pixels.append(point)
                    return True

    # Перебираем массив изображения на поиск черных пикселей
    # Было бы круто сделать это в несколько потоков, но ума не приложу как
    for y,row in enumerate(arr):
        for x,item in enumerate(row):
            if item == True:
                point = [x,y]
                inUsed = point in used_pixels
                if inUsed == False:
                    find_affiliation(point,False)
        ind = len(row) - 1
        for x,item in enumerate(reversed(row)):
            if item == True:
                point = [ind,y]
                inUsed = point in used_pixels
                if inUsed == False:
                    find_affiliation(point,True)
            if item == True:
                point = [ind,y]
                in_used = point in used_pixels
                if in_used == False:
                    lines.append([point])
                    used_pixels.append([point])
            ind -= 1

    lines_last_objects = [i[-1] for i in lines]
    del lines_last_objects[0]
    lines_first_objects = [i[0] for i in lines]
    del lines_last_objects[0]

    # Поиск возможных соединений маршрутов (сильно замедляет процесс)
    def find_conections():
        conected = 0
        for i,item in enumerate(lines):
            nb = neighbors(item[-1][0],item[-1][1])
            print(nb)
            conections_last = [i for e in nb for i in lines_last_objects if e in i]
            conections_first = [i for e in nb for i in lines_first_objects if e in i]
            for n in nb:
                if [n[0],n[1]] in lines_last_objects:
                    ind = lines_last_objects.index([n[0],n[1]])
                    if ind != -1:
                        conected += 1
                        item.extend(lines[ind][::-1])
                        del lines[ind]
                        break
                elif [n[0],n[1]] in lines_first_objects:
                    ind = lines_first_objects.index([n[0],n[1]])
                    if ind != -1:
                        conected += 1
                        item.extend(lines[ind])
                        del lines[ind]
                        break
        print(conected)

    #find_conections()

    return lines
