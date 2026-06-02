import os
import pandas as pd
from sqlalchemy.types import INTEGER, DECIMAL, VARCHAR

from GetUserData import get_user_data
from sqlalchemy import create_engine, text

folder_dir = "WygenerowaneDane"
files = os.listdir(folder_dir)

fakty = "Fakty.csv"
produkty = "Produkty.csv"
lokalizacje = "Lokalizacje.csv"
daty = "daty.csv"
platnosci = "Platnosci.csv"

required = [fakty, produkty, lokalizacje, daty, platnosci]

for file in required:
    if file not in files:
        raise Exception(f"Dane do zaladowania nie zostaly znalezione: {file}")

user, password, host, port, db_name = get_user_data()

server_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/")

drop_query = text(f"DROP DATABASE IF EXISTS {db_name}")
create_query = text(f"CREATE DATABASE {db_name}")


with server_engine.connect() as conn:
    conn.execute(drop_query)
    conn.execute(create_query)

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")

fakty_df = pd.read_csv(f"{folder_dir}/{fakty}")

fakty_typy = {
    "Produkt_ID": INTEGER,
    "Lokalizacje_ID": INTEGER,
    "Data": INTEGER,
    "Platnosci_ID": INTEGER,
    "Wartosc": DECIMAL(10,2),
    "Ilosc": INTEGER,
    "Rabat": DECIMAL(10,2)
}

produkty_df = pd.read_csv(f"{folder_dir}/{produkty}")

produkty_typy = {
    "Produkt_ID": INTEGER,
    "Nazwa_Produktu": VARCHAR(48),
    "Podkategoria":  VARCHAR(48),
    "Kategoria": VARCHAR(48),
    "CenaBazowa": DECIMAL(10,2)
}

lokalizacje_df = pd.read_csv(f"{folder_dir}/{lokalizacje}")

lokalizacje_typy = {
    "Lokalizacja_ID": INTEGER,
    "Nazwa_Lokalizacji": VARCHAR(48),
}

platnosci_df = pd.read_csv(f"{folder_dir}/{platnosci}")

platnosci_typy = {
    "Platnosci_ID": INTEGER,
    "Nazwa_Metody": VARCHAR(48),
}

daty_df = pd.read_csv(f"{folder_dir}/{daty}")
daty_typy = {
    "Data_ID": INTEGER,
    "Data": VARCHAR(10),
    "Rok": INTEGER,
    "Miesiac": INTEGER,
    "Dzien": INTEGER,
    "DzienTygodnia": VARCHAR(15)
}



with engine.connect() as conn:
    fakty_df.to_sql(name="factsprzedaze", con=conn, if_exists="replace", index=False, dtype=fakty_typy)
    produkty_df.to_sql(name="dimprodukt", con=conn, if_exists="replace", index=False, dtype=produkty_typy)
    lokalizacje_df.to_sql(name="dimlokalizacja", con=conn, if_exists="replace", index=False, dtype=lokalizacje_typy)
    platnosci_df.to_sql(name="dimplatnosc", con=conn, if_exists="replace", index=False, dtype=platnosci_typy)
    daty_df.to_sql(name="dimdata",con=conn, if_exists="replace", index=False, dtype=daty_typy)




