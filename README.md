# Projekt Zaliczeniowy: Otoczka Wypukła (Geometria Obliczeniowa)

Aplikacja służąca do wizualizacji i wyznaczania otoczki wypukłej dla zbioru czterech punktów na płaszczyźnie euklidesowej. Projekt został zrealizowany w ramach przedmiotu **Geometria Obliczeniowa (Semestr Zimowy 2025/26)**.

## 📌 Cel Projektu
Celem programu jest analiza geometryczna wzajemnego położenia czterech punktów $P_1, P_2, P_3, P_4$ i wyznaczenie ich otoczki wypukłej (ang. *Convex Hull*). 

Program odpowiada na pytania:
1.  Jaki kształt tworzy otoczka? (Czworokąt, Trójkąt, Odcinek lub Punkt).
2.  Jakie są współrzędne wierzchołków tej otoczki?
3.  Które punkty wejściowe stanowią wierzchołki otoczki?

## 🧮 Zastosowany Algorytm
W projekcie zaimplementowano **Algorytm Łańcuchów Monotonicznych (Monotone Chain Algorithm)**, znany również jako algorytm Andrew.

### Zasada działania:
1.  **Sortowanie:** Punkty wejściowe są sortowane leksykograficznie (według współrzędnej X, a w przypadku remisu – według Y).
2.  **Podział:** Konstrukcja otoczki jest dzielona na dwa etapy: wyznaczenie **łańcucha dolnego** (Lower Hull) oraz **łańcucha górnego** (Upper Hull).
3.  **Iloczyn wektorowy:** Dla każdej trójki punktów sprawdzany jest skręt (iloczyn wektorowy 2D). Jeśli utworzony kąt jest wklęsły (skręt w prawo), środkowy punkt jest usuwany z potencjalnej otoczki.
4.  **Złożoność:** Złożoność obliczeniowa wynosi $O(N \log N)$ ze względu na sortowanie. Dla stałej liczby punktów ($N=4$) czas działania jest pomijalnie mały.

## 🛠 Stack Technologiczny
Projekt wykorzystuje architekturę klient-serwer z wyraźnym podziałem na logikę biznesową i warstwę prezentacji.

*   **Backend (Logika):** Python 3.10
    *   Algorytm geometryczny zaimplementowany w czystym Pythonie (bez ciężkich zależności).
    *   Biblioteka standardowa (`math`) do operacji podstawowych.
*   **API / Serwer:** Flask
    *   Lekki framework webowy obsługujący żądania REST API.
    *   Blueprinty do organizacji endpointów.
*   **Frontend (Wizualizacja):** HTML5 + JavaScript (ES6)
    *   **Canvas API:** Rysowanie siatki, punktów i figur geometrycznych.
    *   **Fetch API:** Asynchroniczna komunikacja z serwerem.
    *   **CSS Flexbox:** Responsywny układ interfejsu.

## 📂 Struktura Plików
```text
otoczka_wypukla/
├── run.py                 # Punkt startowy aplikacji
├── config.py              # Konfiguracja środowiska (Dev/Prod)
├── core/                  # CZYSTA LOGIKA (niezależna od frameworka)
│   └── geometry.py        # Implementacja algorytmu Monotone Chain
├── web/                   # WARSTWA PREZENTACJI (Flask)
│   ├── routes.py          # Kontroler (Endpointy API)
│   ├── templates/         # Widoki HTML
│   └── static/            # Zasoby (CSS, JS)
└── requirements.txt       # Zależności Python
```

## 🚀 Instrukcja Uruchomienia

### Krok 1: Aktywacja środowiska
Upewnij się, że jesteś w głównym katalogu projektu, a następnie aktywuj wirtualne środowisko:

```bash
# Linux / MacOS
source otoczka_wypukla/venv/bin/activate
```

### Krok 2: Start serwera
Uruchom aplikację za pomocą skryptu startowego:

```bash
python otoczka_wypukla/run.py
```

### Krok 3: Obsługa
Otwórz przeglądarkę internetową i przejdź pod adres:
👉 **http://127.0.0.1:5000**

1.  **Dodawanie punktów:** Kliknij lewym przyciskiem myszy na siatce LUB wpisz współrzędne w panelu bocznym.
2.  **Obliczenia:** Po wprowadzeniu 4 punktów otoczka zostanie wyrysowana automatycznie.
3.  **Reset:** Użyj klawisza `R` lub przycisku "Reset", aby wyczyścić planszę.

## 📐 Układ Współrzędnych
Aplikacja mapuje piksele ekranu na matematyczny układ współrzędnych kartezjańskich:
*   **Zakres:** $X, Y \in [0, 100]$
*   **Początek układu (0,0):** Lewy dolny róg wykresu.
*   **Precyzja:** Obliczenia wykonywane są na zmiennoprzecinkowych liczbach rzeczywistych (float), a wyniki prezentowane z dokładnością do 2 miejsc po przecinku.

## 🧪 Testy
Aby uruchomić testy jednostkowe (sprawdzające m.in. przypadki punktów współliniowych):

```bash
python -m unittest discover otoczka_wypukla/tests
```