def cross_product(o, a, b):
    """
    Oblicza iloczyn wektorowy dla trzech punktów na płaszczyźnie.
    
    Ta funkcja sprawdza, w którą stronę trzeba skręcić, aby przejść z punktu O 
    przez punkt A do punktu B. Wynik dodatni oznacza skręt w lewo, ujemny w prawo,
    a zero oznacza, że punkty leżą na jednej linii prostej.
    
    Parametry:
        o: Punkt początkowy (środkowy) [x, y]
        a: Pierwszy punkt [x, y]
        b: Drugi punkt [x, y]
    
    Zwraca:
        Liczbę dodatnią (skręt w lewo), ujemną (w prawo) lub zero (linia prosta)
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def get_convex_hull(points):
    """
    Znajduje otoczkę wypukłą - najmniejszy wielokąt otaczający wszystkie punkty.
    
    Wyobraź sobie, że wbijasz gwoździe w punkty na tablicy, a potem naciągasz 
    na nie gumkę - taki kształt to właśnie otoczka wypukła. Algorytm używa 
    metody "Monotone Chain" (Łańcuch Monotoniczny), która działa podobnie 
    jak rysowanie dolnego brzegu, a potem górnego brzegu tej gumki.
    
    Parametry:
        points: Lista punktów w formacie [[x1, y1], [x2, y2], ...]
    
    Zwraca:
        Lista punktów tworzących otoczkę wypukłą, ułożonych w kolejności
    """
    # Krok 1: Usuń punkty powtarzające się i uporządkuj od lewej do prawej
    # (najpierw po współrzędnej X, przy równych X - po współrzędnej Y)
    unique_points = sorted(list(set(tuple(p) for p in points)))

    # Jeśli mamy 2 punkty lub mniej, one już tworzą otoczkę
    if len(unique_points) <= 2:
        return [list(p) for p in unique_points]

    # Krok 2: Budujemy dolną część otoczki (od lewej do prawej strony)
    lower = []
    for p in unique_points:
        # Usuwamy punkty, które powodują skręt w prawo (nie są częścią otoczki)
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Krok 3: Budujemy górną część otoczki (od prawej do lewej strony)
    upper = []
    for p in reversed(unique_points):
        # Podobnie jak wyżej - usuwamy punkty powodujące skręt w prawo
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Krok 4: Łączymy dolną i górną część w jedną otoczkę
    # Usuwamy ostatni punkt z każdej części, bo są to te same punkty (skrajne)
    hull = lower[:-1] + upper[:-1]
    
    return [list(p) for p in hull]

def classify_shape(hull_points):
    """
    Rozpoznaje, jaki kształt geometryczny tworzy otoczka wypukła.
    
    Na podstawie liczby wierzchołków otoczki określa, czy otrzymaliśmy punkt,
    odcinek, trójkąt, czworokąt czy inny wielokąt. Dodatkowo podaje wyjaśnienie,
    co oznacza taki wynik.
    
    Parametry:
        hull_points: Lista punktów tworzących otoczkę wypukłą
    
    Zwraca:
        Krotkę (nazwa_kształtu, opis) - np. ("Trójkąt", "Jeden punkt leży...")
    """
    n = len(hull_points)
    
    # Brak punktów - pusta otoczka
    if n == 0:
        return "Pusty", "Brak punktów"
    
    # Jeden wierzchołek - wszystkie punkty wejściowe były w tym samym miejscu
    elif n == 1:
        return "Punkt", "Wszystkie punkty pokrywają się"
    
    # Dwa wierzchołki - wszystkie punkty leżą na jednej linii prostej
    elif n == 2:
        return "Odcinek", "Punkty są współliniowe (leżą na jednej prostej)"
    
    # Trzy wierzchołki - czwarty punkt znajduje się wewnątrz trójkąta lub na jego krawędzi
    elif n == 3:
        return "Trójkąt", "Jeden punkt leży wewnątrz trójkąta lub na krawędzi"
    
    # Cztery wierzchołki - wszystkie punkty tworzą otoczkę (żaden nie jest w środku)
    elif n == 4:
        return "Czworokąt", "Wszystkie punkty są wierzchołkami otoczki"
    
    # Więcej niż 4 wierzchołki - wielokąt o większej liczbie boków
    else:
        return f"Wielokąt ({n})", f"Otoczka ma {n} wierzchołków"
