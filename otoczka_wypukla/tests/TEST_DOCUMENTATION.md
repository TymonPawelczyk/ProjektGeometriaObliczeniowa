# Dokumentacja Testów - Geometria Obliczeniowa

Dokument ten opisuje zestaw testów jednostkowych dla modułu geometrii (`core/geometry.py`) w projekcie "Otoczka Wypukła". Testy znajdują się w pliku `tests/test_geometry.py`.

## Zakres Testów

Testy pokrywają kluczowe funkcje geometryczne:
1.  **`cross_product`**: Obliczanie iloczynu wektorowego.
2.  **`get_convex_hull`**: Algorytm wyznaczania otoczki wypukłej (Monotone Chain).
3.  **`classify_shape`**: Klasyfikacja wynikowego kształtu otoczki.

## Przypadki Testowe

### 1. Iloczyn Wektorowy (`test_cross_product`)
Sprawdza poprawność określania relacji skrętności trzech punktów (O, A, B):
*   **Skręt w lewo**: Wynik dodatni.
*   **Skręt w prawo**: Wynik ujemny.
*   **Współliniowość**: Wynik zero.

### 2. Wyznaczanie Otoczki Wypukłej (`get_convex_hull`)

| Nazwa Testu | Opis Przypadku | Oczekiwany Wynik |
| :--- | :--- | :--- |
| `test_get_convex_hull_triangle` | 3 punkty tworzące trójkąt. | Otoczka składa się z 3 punktów (wierzchołków trójkąta). |
| `test_get_convex_hull_square` | 4 punkty tworzące kwadrat. | Otoczka składa się z 4 punktów (wierzchołków kwadratu). |
| `test_get_convex_hull_point_inside` | Trójkąt z jednym punktem wewnątrz. | Otoczka ma 3 wierzchołki; punkt wewnętrzny jest pomijany. |
| `test_get_convex_hull_collinear` | 3 punkty współliniowe. | Otoczka zredukowana do 2 punktów końcowych (odcinek). |
| `test_get_convex_hull_collinear_4_points` | 4 punkty współliniowe. | Otoczka zredukowana do 2 punktów końcowych (odcinek). Pośrednie punkty usunięte. |
| `test_get_convex_hull_duplicates` | Zduplikowane punkty na wejściu. | Duplikaty są usuwane przed obliczeniami; wynik zależy od unikalnych punktów. |
| `test_get_convex_hull_horizontal_line` | Punkty leżące na poziomej linii. | Otoczka to 2 skrajne punkty (lewy i prawy). |
| `test_get_convex_hull_vertical_line` | Punkty leżące na pionowej linii. | Otoczka to 2 skrajne punkty (dolny i górny). |
| `test_get_convex_hull_diamond_shape` | "Romb" (obrócony kwadrat) z punktem w środku. | Otoczka to 4 zewnętrzne wierzchołki; punkt środkowy usunięty. |
| `test_get_convex_hull_negative_coordinates` | Punkty o współrzędnych ujemnych. | Algorytm działa poprawnie niezależnie od ćwiartki układu współrzędnych. |
| `test_get_convex_hull_float_precision` | Współrzędne zmiennoprzecinkowe (float). | Algorytm poprawnie przetwarza wartości niecałkowite. |
| `test_get_convex_hull_all_identical` | 4 identyczne punkty. | Otoczka zredukowana do pojedynczego punktu. |

### 3. Klasyfikacja Kształtu (`test_classify_shape`)
Weryfikuje, czy funkcja poprawnie nazywa kształty na podstawie liczby wierzchołków otoczki:
*   0 punktów -> "Pusty"
*   1 punkt -> "Punkt"
*   2 punkty -> "Odcinek"
*   3 punkty -> "Trójkąt"
*   4 punkty -> "Czworokąt"
*   >4 punkty -> "Wielokąt (n)"

## Uruchamianie Testów

Aby uruchomić wszystkie testy, należy wykonać poniższe polecenie z głównego katalogu projektu:

```bash
python -m unittest discover otoczka_wypukla/tests
```
lub uruchamiając plik bezpośrednio:
```bash
python otoczka_wypukla/tests/test_geometry.py
```
