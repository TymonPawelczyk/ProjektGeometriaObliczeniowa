def cross_product(o, a, b):
    """
    Oblicza iloczyn wektorowy (2D cross product) wektorów OA i OB.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def get_convex_hull(points):
    """
    Wyznacza otoczkę wypukłą dla zbioru punktów algorytmem Monotone Chain.
    Punkty wejściowe to lista list/krotek [x, y].
    """
    # Usuń duplikaty i posortuj (domyślnie po x, potem po y)
    # Konwertujemy na krotki, żeby można było użyć set()
    unique_points = sorted(list(set(tuple(p) for p in points)))

    if len(unique_points) <= 2:
        return [list(p) for p in unique_points]

    # Dolna otoczka
    lower = []
    for p in unique_points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Górna otoczka
    upper = []
    for p in reversed(unique_points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Łączenie (usuwamy ostatnie punkty bo się dublują)
    hull = lower[:-1] + upper[:-1]
    
    return [list(p) for p in hull]

def classify_shape(hull_points):
    """
    Klasyfikuje kształt otoczki.
    """
    n = len(hull_points)
    if n == 0:
        return "Pusty", "Brak punktów"
    elif n == 1:
        return "Punkt", "Wszystkie punkty pokrywają się"
    elif n == 2:
        return "Odcinek", "Punkty są współliniowe"
    elif n == 3:
        return "Trójkąt", "Jeden punkt leży wewnątrz trójkąta lub na krawędzi"
    elif n == 4:
        return "Czworokąt", "Wszystkie punkty są wierzchołkami otoczki"
    else:
        return f"Wielokąt ({n})", f"Otoczka ma {n} wierzchołków"
