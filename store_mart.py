from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.dates import MonthLocator

from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://sklepy:Przetwarzanie123@127.0.0.1/sklepy")


def get_store_revenue_chart(store_id: int):
    global engine
    fig, ax = plt.subplots(figsize=(5.4, 2), layout='constrained')
    dates = []
    revenue = []

    query = text(
        f"SELECT sum(Wartosc * Ilosc * ((100-Rabat)/100)), Data_faktu FROM fakty WHERE Lokalizacja_id={store_id} GROUP BY Data_faktu")
    with engine.connect() as conn:
        for row in conn.execute(query):
            dates.append(datetime.strptime(str(row[1]), "%Y%m%d").date())
            revenue.append(float(row[0]))

        shop = conn.execute(text(f"SELECT nazwa from lokalizacje WHERE id={store_id}")).first()[0]
    ax.bar(dates, revenue)

    ax.xaxis.set_major_locator(MonthLocator())
    ax.set_ylabel('Przychód (zł)')
    ax.set_xlabel('Data')

    ax.set_title(f'Przychód sklepu {shop}')
    plt.savefig(f"store-revenue-{store_id}-all.png")


if __name__ == "__main__":
    get_store_revenue_chart(2)
