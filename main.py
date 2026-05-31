# Import bibliotek
from datetime import date
from enum import Enum
import numpy as np
import csv

# Ustawienie seeda
np.random.seed(69)

### USTAWIENIE PARAMETRÓW

ilosc_danych = 1000
min_rok = 2026
max_rok = 2026
min_miesiac = 3
max_miesiac = 4
rabat_szansa = 0.25

############ Funkcjonalność

assert min_rok <= max_rok
if min_rok == max_rok:
    assert min_miesiac <= max_miesiac

# Definicja klasy produktu oraz listy produktów
Products = []


class Product:
    def __init__(self, name, subcategory, value):
        self.name = name
        self.subcategory = subcategory
        self.value = value
        Products.append(self)


# Definicja subkaterogii
class SubCategory(Enum):
    # Jedzenie
    Produkty_Mleczne = 1
    Slodycze = 2
    Pieczywo = 3
    Napoje = 4
    Przekaski = 5
    Mieso = 6
    Owoce = 7
    Warzywa = 8
    # Higieniczne
    Toaleta = 9
    Higiena_Ciala = 10
    # Sprzatajace
    Chemia = 11
    Czyszczenie = 12
    # Zabawki
    Metalowe = 13
    Plastikowe = 14
    # Elektronika
    Komputer = 15
    Transport = 16


# Definicja metod płatnosci
class Metody(Enum):
    GOTOWKA = 1
    KARTA = 2
    BLIK = 3


# Definicja lokalizacji
class Lokalizacje(Enum):
    Warszawa = 1
    Wroclaw = 2
    Krakow = 3
    Bydgoszcz = 4
    Zielona_Gora = 5


# Definicja kategorii
class Category(Enum):
    Produkty_Spozywcze = 1
    Produkty_Higieniczne = 2
    Produkty_Sprzatajace = 3
    Zabawki = 4
    Elektronika = 5


'''Stan na 03.13 dane cenowe z dlahandlu.pl dla sklepów Aldi, odnotowane 19.04.2026 dla następujących produktów: Mleko, Chleb 500g, 
Bulka Kajzerka, Czekolada Mleczna 100g, Woda Niegazowana 2L, Cukier 1kg, Ser Gouda 200g, Sok Pomaranczowy 1L, Szynka wiejska 450g, 
Dzem 280g, Banany 1kg, Jablka 1kg, Cytryny 1kg, Pomarancze 1kg, Poledwica sopocka 450g, Parowki 250g, Kielbasa 1kg, Kurczak 1kg, 
Ziemniaki 1kg, Pomidory 1kg, Papryka 1kg, Pieczarki 1kg, Papier Toaletowy op. 8 rolek, Proszek do prania 400g, Plyn do zmywania naczyn 1L,
 Pasta do zebow 125 ml, Mydlo kostka 100g, Plyn do czyszczenia toalet 750 ml, Szampon 250ml, Recznik papierowy op. 2 rolki, 

Google search dla następujących produktów Przepychacz, Chusteczki nawilzane 72 szt., Chipsy 110g, Samochod zabawkowy, 
Tor samochodowy, Pociag zabawkowy, Figurka Dinozaura, Lalka, Hulajnoga elektrycza,

Dane produktów Myszka i klawiatura: sklep x-kom, stan na 19.04.2026 
'''

# Definicja produktów
Mleko = Product("Mleko", SubCategory.Produkty_Mleczne, 4.49)
Chleb = Product("Chleb 500g", SubCategory.Pieczywo, 2.29)
Bulka = Product("Bulka Kajzerka", SubCategory.Pieczywo, 0.31)
Czekolada = Product("Czekolada Mleczna 100g", SubCategory.Slodycze, 8.88)
Woda = Product("Woda Niegazowana 2L", SubCategory.Napoje, 3.85)
Cukier = Product("Cukier 1kg", SubCategory.Slodycze, 2.69)
Ser = Product("Ser Gouda 200g", SubCategory.Produkty_Mleczne, 4.80)
Sok = Product("Sok Pomaranczowy 1L", SubCategory.Napoje, 7.99)
Szynka = Product("Szynka wiejska 450g", SubCategory.Mieso, 15.73)
Dzem = Product("Dzem 280g", SubCategory.Slodycze, 7.49)
Banany = Product("Banany 1kg", SubCategory.Owoce, 6.99)
Jablka = Product("Jablka 1kg", SubCategory.Owoce, 3.49)
Cytryny = Product("Cytryny 1kg", SubCategory.Owoce, 7.99)
Pomarancze = Product("Pomarancze 1kg", SubCategory.Owoce, 4.99)
Poledwica = Product("Poledwica sopocka 450g", SubCategory.Mieso, 17.97)
Parowki = Product("Parowki 250g", SubCategory.Mieso, 5.55)
Kielbasa = Product("Kielbasa 1kg", SubCategory.Mieso, 23.80)
Kurczak = Product("Kurczak 1kg", SubCategory.Mieso, 9.49)
Ziemniaki = Product("Ziemniaki 1kg", SubCategory.Warzywa, 2.99)
Pomidory = Product("Pomidory 1kg", SubCategory.Warzywa, 5.55)
Papryka = Product("Papryka 1kg", SubCategory.Warzywa, 18.99)
Pieczarki = Product("Pieczarki 1kg", SubCategory.Warzywa, 15.98)
Papier = Product("Papier Toaletowy op. 8 rolek", SubCategory.Toaleta, 4.99)
Proszek = Product("Proszek do prania 400g", SubCategory.Chemia, 10.91)
Plyn = Product("Plyn do zmywania naczyn 1L", SubCategory.Chemia, 9.99)
Pasta = Product("Pasta do zebow 125 ml", SubCategory.Higiena_Ciala, 12.99)
Mydlo = Product("Mydlo kostka 100g", SubCategory.Higiena_Ciala, 6.43)
Domestos = Product("Plyn do czyszczenia toalet 750 ml", SubCategory.Chemia, 11.24)
Szampon = Product("Szampon 250ml", SubCategory.Higiena_Ciala, 8.74)
Recznik = Product("Recznik papierowy op. 2 rolki", SubCategory.Czyszczenie, 4.99)
Przepychaczka = Product("Przepychacz", SubCategory.Czyszczenie, 16.39)
Chusteczki = Product("Chusteczki nawilzane 72 szt.", SubCategory.Toaleta, 5.39)
Chipsy = Product("Chipsy 110g", SubCategory.Przekaski, 6.79)
Samochod = Product("Samochod zabawkowy", SubCategory.Metalowe, 12.99)
Tor = Product("Tor samochodowy", SubCategory.Plastikowe, 72.57)
Pociag = Product("Pociag zabawkowy", SubCategory.Metalowe, 111.00)
Figurka = Product("Figurka Dinozaura", SubCategory.Plastikowe, 49.99)
Hulajnoga = Product("Hulajnoga elektrycza", SubCategory.Transport, 749.00)
Myszka = Product("Myszka komputerowa", SubCategory.Komputer, 139.00)
Klawiatura = Product("Klawiatura komputerowa", SubCategory.Komputer, 219.00)

# Przypisanie id podkategorii do kategorii
kategorie2 = {k: Category.Produkty_Spozywcze for k in range(1, 9)}
kategorie2.update({z: Category.Produkty_Higieniczne for z in range(9, 11)})
kategorie2.update({z: Category.Produkty_Sprzatajace for z in range(11, 13)})
kategorie2.update({z: Category.Zabawki for z in range(13, 15)})
kategorie2.update({z: Category.Elektronika for z in range(15, 17)})

# Przypisanie produktów do ich kategorii
Produkty_Kategoryzowane = [[], [], [], [], []]
for produkt in Products:
    Produkty_Kategoryzowane[kategorie2[produkt.subcategory.value].value - 1].append(produkt)

# Zdefiniowanie prawdopodobieństw
Platnosci = [Metody.GOTOWKA, Metody.KARTA, Metody.BLIK]
Platnosci_Weights = [0.7, 0.2, 0.1]

kategorie = [Category.Produkty_Spozywcze, Category.Produkty_Higieniczne, Category.Produkty_Sprzatajace,
             Category.Zabawki, Category.Elektronika]
kategorie_weights = [0.5, 0.19, 0.2, 0.1, 0.01]

lokalizacje = [Lokalizacje.Wroclaw, Lokalizacje.Zielona_Gora, Lokalizacje.Warszawa, Lokalizacje.Bydgoszcz,
               Lokalizacje.Krakow]
lokalizacje_weights = [0.3, 0.1, 0.2, 0.15, 0.25]


# Wygenerowania przedziałów generowanych dat
def generacja_przedzialu(minimum, maximum):
    return [i for i in range(minimum, maximum + 1)]


lata = generacja_przedzialu(min_rok, max_rok)
dnie = generacja_przedzialu(1, 31)


# Sprawdzenie roku przestępnego:
def czy_przestepny(rok):
    return rok % 4 == 0 and (rok % 100 != 0 or rok % 400 == 0)


miesiace_30dni = [4, 6, 9, 11]

# Zdefiniowanie rabatów oraz ich prawdopodobieństw
rabaty = [0.05, 0.10, 0.15, 0.20, 0.25]
rabaty_weights = [0.6, 0.2, 0.1, 0.08, 0.02]

# Maksymalne ilości dla każdej kategorii
maks_ilosci = [4, 2, 2, 1, 1]

# Zapisywanie dat oraz faktów
daty = []
fakty = []


# Funkcja generowania losowego
def generuj_losowy(przedzial, prawdopodobienstwa=None):
    return np.random.choice(przedzial, p=prawdopodobienstwa) if prawdopodobienstwa else np.random.choice(przedzial)


# Funkcja generowania losowego dnia
def generuj_dzien(miesiac, rok):
    if miesiac == 2:
        if czy_przestepny(rok):
            dzien = generuj_losowy(dnie[:-2])
        else:
            dzien = generuj_losowy(dnie[:-3])
    elif miesiac in miesiace_30dni:
        dzien = generuj_losowy(dnie[:-1])
    else:
        dzien = generuj_losowy(dnie)
    return dzien


def dodaj_0(argument):
    argument = str(argument)
    return "0" + argument if len(argument) == 1 else argument


# Generowanie faktów
for i in range(ilosc_danych):
    fakty.append([])

    kategoria = generuj_losowy(kategorie, kategorie_weights)
    produkt = generuj_losowy(Produkty_Kategoryzowane[kategoria.value - 1])
    platnosc = generuj_losowy(Platnosci, Platnosci_Weights)
    lokalizacja = generuj_losowy(lokalizacje, lokalizacje_weights)

    # Generacja daty
    rok = generuj_losowy(lata)

    # Ustalenie zakresu miesięcy w zależności od roku
    if min_rok == max_rok:
        dostepne_miesiace = generacja_przedzialu(min_miesiac, max_miesiac)
    elif rok == min_rok:
        dostepne_miesiace = generacja_przedzialu(min_miesiac, 12)
    elif rok == max_rok:
        dostepne_miesiace = generacja_przedzialu(1, max_miesiac)
    else:
        dostepne_miesiace = generacja_przedzialu(1, 12)

    miesiac = generuj_losowy(dostepne_miesiace)
    dzien = generuj_dzien(miesiac, rok)

    miesiac_str = dodaj_0(miesiac)
    dzien_str = dodaj_0(dzien)
    data_ = int(f"{rok}{miesiac_str}{dzien_str}")

    czy_rabat = np.random.choice([0, 1], p=[1 - rabat_szansa, rabat_szansa])
    rabat = np.random.choice(rabaty, p=rabaty_weights) if czy_rabat else 0

    maks_ilosc = maks_ilosci[kategoria.value - 1]
    if maks_ilosc > 1:
        if maks_ilosc == 4:
            ilosc_weights = [0.7, 0.2, 0.08, 0.02]
        else:
            ilosc_weights = [0.8, 0.2]
        ilosc = generuj_losowy([i for i in range(1, maks_ilosc + 1)], ilosc_weights)
    else:
        ilosc = 1

    ilosc = int(ilosc)

    # Bezpieczna kalkulacja ceny
    total_cena = round(float(produkt.value * ilosc - produkt.value * ilosc * rabat), 2)

    fakty[i].append(Products.index(produkt) + 1)
    fakty[i].append(lokalizacja.value)
    fakty[i].append(data_)

    if data_ not in daty:
        daty.append(data_)

    fakty[i].append(platnosc.value)
    fakty[i].append(f"{total_cena:.2f}")
    fakty[i].append(ilosc)
    fakty[i].append(f"{rabat:.2f}")  # Zmiana na int, by unikać zapisów typu "5.0%"

fakty.sort(key=lambda x: x[2])
daty.sort()

# Zapis do plików CSV (Dodano kodowanie UTF-8)
fakty_labels = ["Produkt_ID", "Lokalizacja_ID", "Data", "Platnosc_ID", "Wartosc", "Ilosc", "Rabat"]
with open('Fakty.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(fakty_labels)
    writer.writerows(fakty)

produkty_row = ["ID", "Nazwa", "Podkategoria", "Kategoria", "Cena Bazowa"]
produkty = []
for i, product in enumerate(Products):
    produkty.append(
        [i + 1, product.name, product.subcategory.name, kategorie2[product.subcategory.value].name, product.value])

with open('Produkty.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(produkty_row)
    writer.writerows(produkty)

lokalizacje_row = ["ID", "Nazwa"]
lokalizacje_tabela = [[loc.value, loc.name.replace("_", " ")] for loc in
                      [Lokalizacje.Warszawa, Lokalizacje.Wroclaw, Lokalizacje.Krakow, Lokalizacje.Bydgoszcz,
                       Lokalizacje.Zielona_Gora]]

with open('Lokalizacje.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(lokalizacje_row)
    writer.writerows(lokalizacje_tabela)

platnosci_row = ["ID", "Nazwa"]
platnosci_tabela = [[p.value, p.name] for p in Platnosci]

with open('Platnosci.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(platnosci_row)
    writer.writerows(platnosci_tabela)

daty_row = ["ID_Daty", "Data", "Rok", "Miesiac", "Dzien", "Dzien Tygodnia"]
daty_tabela = []
dnie_tyg = {0: "Poniedzialek", 1: "Wtorek", 2: "Sroda", 3: "Czwartek", 4: "Piatek", 5: "Sobota", 6: "Niedziela"}


def dzien_tygodnia(rok, miesiac, dzien):
    return dnie_tyg[date.weekday(date(int(rok), int(miesiac), int(dzien)))]


for i, data_val in enumerate(daty):
    data_converted = str(data_val)
    data_s = data_converted[:4] + "-" + data_converted[4:6] + "-" + data_converted[6:]
    rok, miesiac, dzien = data_s.split("-")
    daty_tabela.append([data_val, data_s, rok, miesiac, dzien, dzien_tygodnia(rok, miesiac, dzien)])

with open('daty.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(daty_row)
    writer.writerows(daty_tabela)

product_count = {}
subcategory_count = {}
category_count = {}


def updatedictionary(dictionary, key):
    dictionary[key] = dictionary.get(key, 0) + 1


for fakt in fakty:
    produkt = Products[fakt[0] - 1]
    updatedictionary(product_count, produkt.name)
    updatedictionary(subcategory_count, produkt.subcategory.name)
    updatedictionary(category_count, kategorie2[produkt.subcategory.value].name)

dane_wygenerowane = []
dane_rows = ["Dana", "Ilosc"]
dane_wygenerowane.extend([[k, v] for k, v in product_count.items()])
dane_wygenerowane.extend([[k, v] for k, v in subcategory_count.items()])
dane_wygenerowane.extend([[k, v] for k, v in category_count.items()])

with open('dane.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(dane_rows)
    writer.writerows(dane_wygenerowane)
