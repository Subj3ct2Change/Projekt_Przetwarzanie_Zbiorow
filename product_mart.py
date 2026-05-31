from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.dates import MonthLocator

from sqlalchemy import create_engine, text





def getProductCharts(id:int, store_id = None):
    engine = create_engine("mysql+pymysql://sklepy:Przetwarzanie123@127.0.0.1/sklepy")
    fig, ax = plt.subplots(figsize=(5.4, 2), layout='constrained')
    dates = []
    revenue = []
    if store_id != None:
        query = text(f"SELECT sum(Wartosc * Ilosc * ((100-Rabat)/100)), Data_faktu FROM fakty WHERE Produkt_ID={id} AND Lokalizacja_ID = {store_id} GROUP BY Data_faktu")
    else:
        query = text(
            f"SELECT sum(Wartosc * Ilosc * ((100-Rabat)/100)), Data_faktu FROM fakty WHERE Produkt_ID={id} GROUP BY Data_faktu")
    with engine.connect() as conn:
        for row in conn.execute(query):
            dates.append(datetime.strptime(str(row[1]), "%Y%m%d").date())
            revenue.append(float(row[0]))
        nazwa = conn.execute(text(f"SELECT Nazwa from produkty WHERE id={id}")).first()[0]
        if store_id != None:
            shop = conn.execute(text(f"SELECT nazwa from lokalizacje WHERE id={store_id}")).first()[0]
    ax.bar(dates, revenue)

    ax.xaxis.set_major_locator(MonthLocator())
    if store_id != None:
        ax.set_title(f'Sprzedaż produktu {nazwa} w {shop}')
        plt.savefig(f"product-sales-{id}-{store_id}.png")
    else:
        ax.set_title(f'Sprzedaż produktu {nazwa}')
        plt.savefig(f"product-sales-{id}-all.png")


if __name__ == "__main__":
    getProductCharts(12)
    getProductCharts(11,1)