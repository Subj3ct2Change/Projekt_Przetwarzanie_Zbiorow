
# Import bibliotek

from datetime import date
from enum import Enum
import numpy as np
import csv

#Ustawienie seeda
np.random.seed(67)

### USTAWIENIE PARAMETRÓW

#Ilość faktów do wygenerowania:
ilosc_danych=1000

#Przedziały dat:
min_rok = 2026
max_rok = 2026
min_miesiac = 3
max_miesiac = 4

#Szansa na rabat
rabat_szansa = 0.2


############ Funkcjonalność

assert min_rok <= max_rok
assert min_miesiac <= max_miesiac


# Definicja klasy produktu oraz listy produktów

Products = []

class Product:
    def __init__(self, name, subcategory, value):
        self.id = id
        self.name = name
        self.subcategory = subcategory
        self.value = value
        Products.append(self)


#Definicja subkaterogii
class SubCategory(Enum):

    #Jedzenie
    Produkty_Mleczne = 1
    Slodycze = 2
    Pieczywo = 3
    Napoje = 4
    Przekaski = 5
    Mieso = 6
    Owoce = 7
    Warzywa = 8

    #Higieniczne
    Toaleta = 9
    Higiena_Ciala = 10

    #Sprzatajace
    Chemia = 11
    Czyszczenie = 12

    #zabawki
    Metalowe = 13
    Plastikowe = 14

    #Elektronika
    Komputer = 15
    Transport = 16

#Definicja metod płatnosci

class Metody(Enum):
    GOTOWKA = 1
    KARTA = 2
    BLIK = 3

#Definicja lokalizacji

class Lokalizacje(Enum):
    Warszawa = 1
    Wroclaw = 2
    Krakow = 3
    Bydgoszcz = 4
    Zielona_Gora = 5


#Definicja kategorii

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

#Definicja produktów
Mleko = Product("Mleko", SubCategory.Produkty_Mleczne,  4.49)
Chleb = Product("Chleb 500g", SubCategory.Pieczywo, 2.29)
Bulka = Product("Bulka Kajzerka", SubCategory.Pieczywo, 0.31)
Czekolada = Product("Czekolada Mleczna 100g", SubCategory.Slodycze, 8.88)
Wooda = Product("Woda Niegazowana 2L", SubCategory.Napoje, 3.85)
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
Myszka= Product("Myszka komputerowa", SubCategory.Komputer, 139.00)
Klawiatura=Product("Klawiatura komputerowa", SubCategory.Komputer, 219.00)


#Przypisanie id podkategorii do kategorii
#Kategoria produktów spozywczych
kategorie2 = {k: Category.Produkty_Spozywcze for k in range(1, 9)}

#Kategoria produktów higienicznych
kategorie2.update({z: Category.Produkty_Higieniczne for z in range(9, 11)})

#Kategoria produktów sprzątających
kategorie2.update({z: Category.Produkty_Sprzatajace for z in range(11, 13)})

#Kategoria zabawek
kategorie2.update({z: Category.Zabawki for z in range(13, 15)})

#Kategoria elektroniki
kategorie2.update({z: Category.Elektronika for z in range(15, 17)})


#Przypisanie produktów do ich kategorii
Produkty_Kategoryzowane=[[], [], [], [], []]

for produkt in Products:
    Produkty_Kategoryzowane[kategorie2[produkt.subcategory.value].value-1].append(produkt)

#Zdefiniowanie prawdopodobieństw metod płatności
Platnosci = [Metody.GOTOWKA, Metody.KARTA, Metody.BLIK]
Platnosci_Weights = [0.7, 0.2, 0.1]

#Zdefiniowanie prawdopodobieństw każdej z kategorii
kategorie = [Category.Produkty_Spozywcze, Category.Produkty_Higieniczne, Category.Produkty_Sprzatajace, Category.Zabawki, Category.Elektronika]
kategorie_weights = [0.5, 0.19, 0.2, 0.1, 0.01]

#Zdefiniowanie prawdopodobieństw każdej z lokalizacjii
lokalizajce = [Lokalizacje.Wroclaw, Lokalizacje.Zielona_Gora, Lokalizacje.Warszawa, Lokalizacje.Bydgoszcz, Lokalizacje.Krakow]
lokalizacje_weights = [0.3, 0.1, 0.2, 0.15, 0.25]




#Wygenerowania przedziałów generowanych dat
def generacja_przedzialu(minimum, maximum):
    return [i for i in range(minimum, maximum + 1)]

lata=generacja_przedzialu(min_rok, max_rok)
miesiace=generacja_przedzialu(min_miesiac, max_miesiac)
dnie=generacja_przedzialu(1, 31)
godziny=generacja_przedzialu(8, 20)
minuty_sekundy=generacja_przedzialu(0, 60)

#Sprawdzenie roku przestępnego:
def czy_przestepny(rok):
    przestepny = False
    if rok%4==0:
        if rok%100==0:
            if rok%400==0:
                przestepny = True
        else:
            przestepny = True
    return przestepny

#Zdefiniowanie poszczególnych miesięcy
miesiace_30dni = [4, 6, 9, 11]


#Zdefiniowanie rabatów oraz ich prawdopodobieństw
rabaty = [0.05, 0.10, 0.15, 0.20, 0.25]
rabaty_weights = [0.8, 0.1, 0.05, 0.04, 0.01]


#Maksymalne ilości dla każdej kategorii
maks_ilosci = [4, 2, 2, 1, 1]

#Zapisywanie dat oraz faktów
daty = []
fakty = []

#Funkcja generowania losowego
def generuj_losowy(przedzial, prawdopodobienstwa=None):
    return np.random.choice(przedzial, p=prawdopodobienstwa) if prawdopodobienstwa else np.random.choice(przedzial)

#Funkcja generowania losowego dnia

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
    argument=str(argument)
    return "0"+argument if len(argument)==1 else argument
#Gene

for i in range(ilosc_danych):
    fakty.append([])
    #Wylosowanie kategorii
    kategoria = generuj_losowy(kategorie, kategorie_weights)

    #Wylosowanie produktu
    produkt = generuj_losowy(Produkty_Kategoryzowane[kategoria.value-1])

    #Wylosowanie metody płatności
    platnosc = generuj_losowy(Platnosci, Platnosci_Weights)

    #Wylosowanie lokalizacji
    lokalizacja = generuj_losowy(lokalizajce, lokalizacje_weights)

    # Generacja daty
    rok = generuj_losowy(lata)
    miesiac= generuj_losowy(miesiace)
    dzien = generuj_dzien(miesiac, rok)
    miesiac=dodaj_0(miesiac)
    dzien=dodaj_0(dzien)
    data_=int(f"{rok}{miesiac}{dzien}")

    #Losowanie rabatu
    czy_rabat = np.random.choice([0, 1], p=[1-rabat_szansa, rabat_szansa])
    if czy_rabat:
        rabat = np.random.choice(rabaty, p=rabaty_weights)
    else: rabat = 0

    #Losowanie ilości
    maks_ilosc = maks_ilosci[kategoria.value-1]
    zbior_ilosc = [i for i in range(maks_ilosc+1)]
    if maks_ilosc>1:
        if maks_ilosc==4:
            ilosc_weights=[0.7, 0.2, 0.08, 0.02]
        else: ilosc_weights=[0.8, 0.2]
        ilosc = generuj_losowy([i for i in range(1, maks_ilosc+1)], ilosc_weights)
    else: ilosc = 1
    ilosc = int(ilosc)

    #Kalkulacja ceny
    total_cena = float(produkt.value*ilosc - produkt.value*ilosc*rabat)

    #Dodanie id produktu do tabeli
    fakty[i].append((Products.index(produkt))+1)

    #Dodanie lokalizacji do tabeli
    fakty[i].append(lokalizacja.value)

    #Dodanie daty do tabeli faktów
    fakty[i].append(data_)

    #Dodanie daty do tabeli dat
    if data_ not in daty:
        daty.append(data_)

    #Dodanie metody płatności do tabeli
    fakty[i].append(platnosc.value)

    #Dodanie ceny końcowej do tabeli
    fakty[i].append(f"{total_cena:.2f}")

    #Dodanie ilości do tabeli
    fakty[i].append(ilosc)

    #Dodanie rabatu do tabeli
    fakty[i].append(f"{rabat*100}%")


#Sortowanie tabeli faktów według dat
fakty.sort(key=lambda x: x[2])

#Sortowanie tabeli dat
daty.sort()


#Zapisywanie danych do tabeli faktów
fakty_labels = ["Produkt_ID", "Lokalizacja_ID", "Data", "Platnosc_ID", "Wartosc", "Ilosc", "Rabat"]

with open('Fakty.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fakty_labels)
    writer.writerows(fakty)


#Zapisywanie danych do tabeli produktów

produkty_row = ["ID", "Nazwa", "Podkategoria", "Kategoria", "Cena Bazowa"]
produkty = []
for i, product in enumerate(Products):
    produkty.append([])
    produkty[i].append(i+1)
    produkty[i].append(product.name)
    produkty[i].append(product.subcategory.name)
    produkty[i].append(kategorie2[product.subcategory.value].name)
    produkty[i].append(product.value)


with open('Produkty.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(produkty_row)
    writer.writerows(produkty)

#Zapisywanie danych do tabeli lokalizacji

lokalizacje_row = ["ID", "Nazwa"]
lokalizacje = [Lokalizacje.Warszawa, Lokalizacje.Wroclaw, Lokalizacje.Krakow, Lokalizacje.Bydgoszcz, Lokalizacje.Zielona_Gora]
lokalizacje_tabela = []

for i, lokalizacja in enumerate(lokalizacje):
    lokalizacje_tabela.append([])
    lokalizacje_tabela[i].append(lokalizacja.value)
    lokalizacje_tabela[i].append(lokalizacja.name.replace("_", " "))


with open('Lokalizacje.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(lokalizacje_row)
    writer.writerows(lokalizacje_tabela)


#Zapisywanie danych do tabeli metod płatności

platnosci = [Metody.GOTOWKA, Metody.KARTA, Metody.BLIK]
platnosci_row = ["ID", "Nazwa"]
platnosci_tabela = []

for i, platnosci in enumerate(platnosci):
    platnosci_tabela.append([])
    platnosci_tabela[i].append(platnosci.value)
    platnosci_tabela[i].append(platnosci.name)

with open('Platnosci.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(platnosci_row)
    writer.writerows(platnosci_tabela)



#Zapisywanie danych do tabeli dat

daty_row = ["ID_Daty", "Data", "Rok", "Miesiac", "Dzien", "Dzien Tygodnia"]
daty_tabela = []

dnie = {
    0: "Poniedzialek",
    1: "Wtorek",
    2: "Sroda",
    3: "Czwartek",
    4: "Piatek",
    5: "Sobota",
    6: "Niedziela"
}

#Kalkulowanie dnia tygodnia

def dzien_tygodnia(rok, miesiac, dzien):
    return dnie[date.weekday(date(int(rok), int(miesiac), int(dzien)))]

for i, _ in enumerate(daty):
    daty_tabela.append([])
    data_converted = str(_)
    data_s = data_converted[:4]+"-"+data_converted[4:6]+"-"+data_converted[6:]
    daty_tabela[i].append(_)
    daty_tabela[i].append(data_s)
    rok, miesiac, dzien = data_s.split("-")
    daty_tabela[i].append(rok)
    daty_tabela[i].append(miesiac)
    daty_tabela[i].append(dzien)
    daty_tabela[i].append(dzien_tygodnia(rok, miesiac, dzien))

with open('daty.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(daty_row)
    writer.writerows(daty_tabela)


#Przeliczenie wygenerowanych danych produktów
product_count = {}
subcategory_count = {}
category_count = {}

#Funkcja na przeliczanie produktów w formie słownika
def updatedictionary(dictionary, key):
    if dictionary.get(key):
        dictionary[key]+=1
    else: dictionary[key]=1


for fakt in fakty:
    produkt = Products[fakt[0]-1]
    updatedictionary(product_count, produkt.name)
    updatedictionary(subcategory_count, produkt.subcategory.name)
    updatedictionary(category_count, kategorie2[produkt.subcategory.value].name)

#Wyświetlenie ilości produktów
'''
dane_wygenerowane=[]
dane_rows = ["Dana", "Ilosc"]
for k, v in product_count.items():
    dane_wygenerowane.append([k, v])
for k, v in subcategory_count.items():
    dane_wygenerowane.append([k, v])
for k, v in category_count.items():
    dane_wygenerowane.append([k, v])

with open('dane.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(dane_rows)
    writer.writerows(dane_wygenerowane)

'''