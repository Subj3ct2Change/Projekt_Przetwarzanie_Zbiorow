import os

from sqlalchemy import create_engine, text

from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.dates import MonthLocator

from GetUserData import get_user_data

user, password, host, port, db_name = get_user_data()


wykresy_dir = "Wykresy"

# Proba generacji folderu
try:
    os.mkdir(wykresy_dir)
    print("Wygenerowano nowy folder")
except FileExistsError:
    print("Folder juz istnieje")


engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")


def get_payment_methods_chart(conn):
    labels = []
    sizes = []

    query = text("""
        SELECT p.Nazwa_Metody, COUNT(f.Platnosc_ID) 
        FROM factsprzedaze f 
        JOIN dimplatnosc p ON f.Platnosc_ID = p.Platnosc_ID
        GROUP BY p.Nazwa_Metody
    """)

    for row in conn.execute(query):
        labels.append(row[0])
        sizes.append(row[1])

    fig, ax = plt.subplots(figsize=(6, 6), layout='constrained')
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99'])
    ax.set_title('Popularność metod płatności')

    plt.savefig(f"{wykresy_dir}/Uzycie-Metod-Platnosci.png")
    print("Wygenerowano wykres płatności.")


def get_category_revenue_chart(conn):
    categories = []
    revenue = []

    query = text("""
        SELECT p.Kategoria, SUM(f.Wartosc) 
        FROM factsprzedaze f
        JOIN dimprodukt p ON f.Produkt_ID = p.Produkt_ID 
        GROUP BY p.Kategoria
        ORDER BY SUM(f.Wartosc) DESC
    """)

    for row in conn.execute(query):
        categories.append(row[0].replace("_", " "))
        revenue.append(float(row[1]))

    fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
    ax.barh(categories, revenue, color='skyblue')
    ax.set_xlabel('Przychód (zł)')
    ax.set_title('Całkowity przychód według kategorii produktów')
    ax.invert_yaxis()

    plt.savefig(f"{wykresy_dir}/Wykres-Kategorii-Przychod.png")
    print("Wygenerowano wykres kategorii.")


def get_discount_impact_chart(conn):
    discounts = []
    quantities = []

    query = text("""
        SELECT Rabat, Ilosc 
        FROM factsprzedaze f
        WHERE Rabat > 0
    """)

    for row in conn.execute(query):
        discounts.append(float(row[0]))
        quantities.append(int(row[1]))

    fig, ax = plt.subplots(figsize=(6, 4), layout='constrained')
    ax.scatter(discounts, quantities, alpha=0.3, color='purple')
    ax.set_xlabel('Wysokość rabatu (%)')
    ax.set_ylabel('Ilość kupionych sztuk')
    ax.set_title('Wpływ rabatu na ilość kupowanych produktów')

    plt.savefig(f"{wykresy_dir}/analytics-discounts.png")
    print("Wygenerowano wykres wpływu rabatów.")

def get_store_revenue_chart(store_id: int, conn):
    fig, ax = plt.subplots(figsize=(10.8, 4), layout='constrained')
    dates = []
    revenue = []

    query = text(
        f"SELECT sum(Wartosc), Data_ID FROM factsprzedaze WHERE Lokalizacja_id={store_id} GROUP BY Data_ID")

    for row in conn.execute(query):
        dates.append(datetime.strptime(str(row[1]), "%Y%m%d").date())
        revenue.append(float(row[0]))
        shop = conn.execute(text(f"SELECT Nazwa_Lokalizacji from dimlokalizacja WHERE lokalizacja_id={store_id}")).first()[0]
    ax.bar(dates, revenue)

    ax.xaxis.set_major_locator(MonthLocator())
    ax.set_ylabel('Przychód (zł)')
    ax.set_xlabel('Data')

    ax.set_title(f'Przychód sklepu {shop}')
    plt.savefig(f"{wykresy_dir}/Przychod-Sklepu-{store_id}.png")

def get_product_revenue_charts(id: int, conn, store_id=None):
    fig, ax = plt.subplots(figsize=(10.8, 4), layout='constrained')
    dates = []
    revenue = []
    if store_id != None:
        query = text(
            f"SELECT sum(Wartosc), Data_ID FROM factsprzedaze WHERE Produkt_ID={id} AND Lokalizacja_ID = {store_id} GROUP BY Data_ID")
    else:
        query = text(
            f"SELECT sum(Wartosc), Data_ID FROM factsprzedaze WHERE Produkt_ID={id} GROUP BY Data_ID")
    with engine.connect() as conn:
        for row in conn.execute(query):
            dates.append(datetime.strptime(str(row[1]), "%Y%m%d").date())
            revenue.append(float(row[0]))
        nazwa = conn.execute(text(f"SELECT Nazwa_Produktu from dimprodukt WHERE produkt_id={id}")).first()[0]
        if store_id != None:
            shop = conn.execute(text(f"SELECT Nazwa_Lokalizacji from dimlokalizacja WHERE id={store_id}")).first()[0]
    ax.bar(dates, revenue)

    ax.xaxis.set_major_locator(MonthLocator())
    ax.set_ylabel('Przychód (zł)')
    ax.set_xlabel('Data')
    if store_id != None:
        ax.set_title(f'Przychód sprzedaży produktu {nazwa} w {shop}')
        plt.savefig(f"{wykresy_dir}/Przychod-Produktu-{id}-{store_id}.png")
    else:
        ax.set_title(f'Przychód sprzedaży produktu {nazwa}')
        plt.savefig(f"{wykresy_dir}/Przychod-Produktu-{id}-wszystkie.png")

def get_product_sold_charts(id: int, conn, store_id=None):
    fig, ax = plt.subplots(figsize=(10.8, 4), layout='constrained')
    dates = []
    revenue = []
    if store_id != None:
        query = text(
            f"SELECT SUM(ilosc), Data_ID FROM factsprzedaze WHERE Produkt_ID={id} AND Lokalizacja_ID = {store_id} GROUP BY Data_id")
    else:
        query = text(
            f"SELECT SUM(ilosc), Data_ID FROM factsprzedaze WHERE Produkt_ID={id} GROUP BY data_ID")
    for row in conn.execute(query):
        dates.append(datetime.strptime(str(row[1]), "%Y%m%d").date())
        revenue.append(float(row[0]))
    nazwa = conn.execute(text(f"SELECT Nazwa_Produktu from dimprodukt WHERE produkt_id={id}")).first()[0]
    if store_id != None:
        shop = conn.execute(text(f"SELECT Nazwa_Lokalizacji from dimlokalizacja WHERE id={store_id}")).first()[0]
    ax.bar(dates, revenue)

    ax.xaxis.set_major_locator(MonthLocator())
    ax.set_ylabel('Ilość')
    ax.set_xlabel('Data')
    if store_id != None:
        ax.set_title(f'Ilość sprzedanego produktu {nazwa} w {shop}')
        plt.savefig(f"{wykresy_dir}/sprzedaze-produktow{id}-{store_id}.png")
    else:
        ax.set_title(f'Ilość sprzedanego produktu {nazwa}')
        plt.savefig(f"{wykresy_dir}/sprzedaze-produktow-{id}-wszystkie-sklepy.png")

def get_sales_with_discounts(conn):
    fig, ax = plt.subplots(figsize=(5, 5), layout='constrained', )
    query = text('SELECT COUNT(*) FROM factsprzedaze GROUP BY RABAT > 0 ORDER BY RABAT > 0 DESC;')
    values = []
    for row in conn.execute(query):
        values.append(row[0])
    ax.bar(["Rabat", "Brak Rabatu"], values)
    ax.set_title("Porownanie ilosci transakcj z rabatami i bez rabatow")
    ax.set_ylabel('Ilosc transakcji')
    plt.savefig(f"{wykresy_dir}/Porownanie-Ilosci-Z-Rabatami")

dni_tyg = ['Niedziela',
'Poniedzialek',
'Wtorek',
'Sroda',
'Czwartek',
'Piatek',
'Sobota']


def get_day_sales(conn, dni=(i for i in range(0, 7))):
    fig, ax = plt.subplots(figsize=(7, 7), layout='constrained', )
    wybrane_dni = []
    for i in range(len(dni_tyg)):
        if i in dni:
            wybrane_dni.append(dni_tyg[i])
    wybrane_dni = tuple(wybrane_dni)
    query = text(f"""
    SELECT d.DzienTygodnia, COUNT(*)
    FROM factsprzedaze f
    JOIN dimdata d ON f.data_id = d.data_id WHERE d.DzienTygodnia IN {wybrane_dni}
    GROUP BY d.DzienTygodnia;
    """)
    dni = []
    values = []
    for row in conn.execute(query):
        dni.append(row[0])
        values.append(row[1])
    print(dni, values)
    ax.bar(dni, values)
    ax.set_title("Ilosc sprzedazy w dniach tygodnia")
    ax.set_ylabel('Ilosc sprzedazy')
    ax.set_xlabel("Dzien Tygodnia")
    plt.savefig(f"{wykresy_dir}/Ilosc-Sprzedazy-Dni-Tygodnia")




with engine.connect() as conn:
    get_payment_methods_chart(conn)
    get_category_revenue_chart(conn)
    get_discount_impact_chart(conn)
    get_sales_with_discounts(conn)
    get_store_revenue_chart(1, conn)
    get_store_revenue_chart(1, conn)
    get_product_revenue_charts(1, conn)
    get_product_sold_charts(1, conn)
    get_day_sales(conn)

