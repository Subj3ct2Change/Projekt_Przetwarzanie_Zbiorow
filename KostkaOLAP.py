from sqlalchemy import create_engine, text
from GetUserData import get_user_data

user, password, host, port, db_name = get_user_data()

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")

def generate_query(aggregacja):
    if aggregacja == "wartosc":
        return "SELECT SUM(WARTOSC) FROM "
    elif aggregacja == "ilosc":
        return "SELECT SUM(ILOSC) FROM "
    else:
        return "SELECT COUNT(*) FROM "

sorty = ["wartosc", "ilosc", "rabat"]

def check_for_where(string):
    if "WHERE" not in string:
        string += " WHERE "
    else:
        string += " AND "
    return string

with engine.connect() as conn:

    while True:
        user_input = input("Wprowadź operacje (w celu uzyskania informacji wpisz help): ")
        user_input = user_input.replace("\n", "")

        if user_input == "quit" or user_input == "exit" or user_input == "q":
            break

        elif user_input == "help":
            print("Dostępne opcje:\nwartosc - wylistuj wartosc\nilosc - wylistuj ilosc\nrabat - sprawdz rabaty\nquery - wprowadz query\nquit/exit - wyjdz")

        elif user_input == "query":
            query = input("Wprowadź query: ")
            print(f"Query: {query}")
            for x in conn.execute(text(query)):
                print(f"{user_input.capitalize()}: {x[0] if x[0] != None else 0}")

        elif user_input in sorty:
            query = ""
            first_query = generate_query(user_input)
            sortuj_produkt = input("Wprowadź po czym sortować produkty (Produkt_ID, Kategoria, Podkategoria), bądź nic aby było wszystko: ").lower()
            if sortuj_produkt == "produkt_id":
                first_query+= "factsprzedaze"
                wpisz_produkty = input("Wprowadż id produktu (aby wprowadzić więcej, separuj wartości przecinkiem) (1-40): ")
                if len(wpisz_produkty)>0:
                    wpisz_produkty = wpisz_produkty.split(",")
                    query = check_for_where(query)
                    query += "Produkt_ID IN ("
                    for i in range(len(wpisz_produkty)):
                        if i == len(wpisz_produkty)-1:
                            query += f"{wpisz_produkty[i]})"
                        else:
                            query += f"{wpisz_produkty[i]},"
            elif sortuj_produkt.lower() in ["kategoria", "podkategoria"]:
                #'(SELECT f.* FROM factsprzedaze f JOIN dimprodukt p on f.Produkt_ID = p.Produkt_ID WHERE p.Kategoria = "Elektronika") AS TB'
                first_query+= f"(SELECT f.* FROM factsprzedaze f JOIN dimprodukt p on f.Produkt_ID = p.Produkt_ID WHERE "
                if sortuj_produkt.lower() == "kategoria":
                    input_kat = input("Wprowadz kategorie (w przypadku wielu, oddziel przecinkiem): ")
                else:
                    input_kat = input("Wprowadz podkategorie (w przypadku wielu, oddziel przecinkiem): ")
                input_kat = input_kat.split(",")
                for i in range(len(input_kat)):
                    if i == 0:
                        first_query+=f"p.{sortuj_produkt} = '{input_kat[i]}' "
                    elif i == len(input_kat)-1:
                        first_query += f"OR p.{sortuj_produkt} = '{input_kat[i]}')"
                    else: first_query+=f"OR p.{sortuj_produkt} = '{input_kat[i]}' "

                first_query+=" AS T"

            else:
                first_query+= "factsprzedaze"
            print(f"Query na teraz: {first_query+query}")
            sortuj_lokalizacje = input("Wprowadź lokalizacje: ").lower()
            if len(sortuj_lokalizacje)>0:
                sortuj_lokalizacje = sortuj_lokalizacje.split(",")
                query = check_for_where(query)
                query+= "Lokalizacja_ID IN ("
                for i in range(len(sortuj_lokalizacje)):
                    if i == len(sortuj_lokalizacje)-1:
                        query += f"{sortuj_lokalizacje[i]})"
                    else:
                        query += f"{sortuj_lokalizacje[i]},"
            print(f"Query na teraz: {first_query+query}")
            sortuj_date = input("Wprowadz okres czasowy w postaci RRRRMMDD,RRRRMMDD badz sama date: ")
            if 0 < len(sortuj_date):
                sortuj_date = sortuj_date.split(",")
                if len(sortuj_date)<3:
                    query = check_for_where(query)
                    if len(sortuj_date)==1:
                        przed_po = input("Przed, czy po? (Default - po): ").lower()
                        if przed_po == "przed":
                            query += f"Data_ID < {sortuj_date[0]}"
                        else:
                            query += f"Data_ID > {sortuj_date[0]}"
                    else:
                        query+= f"Data_ID > {int(sortuj_date[0])-1} AND Data_ID < {int(sortuj_date[1])+1}"
            print(f"Query na teraz: {first_query+query}")
            sortuj_platnosc = input("Wprowadz metode/metody platnosci: ")
            if len(sortuj_platnosc)>0:
                sortuj_platnosc = sortuj_platnosc.split(",")
                query = check_for_where(query)
                query += "Platnosc_ID IN ("
                for i in range(len(sortuj_platnosc)):
                    if i == len(sortuj_platnosc)-1:
                        query += f"{sortuj_platnosc[i]})"
                    else:
                        query += f"{sortuj_platnosc[i]},"
            print(f"Query na teraz: {first_query+query}")
            sortuj_wartosc = input("Wprowadz wartosc: ")
            if len(sortuj_wartosc)>0:
                query = check_for_where(query)
                up_down = input("> czy <? (Default: >): ")
                query += "Wartosc "
                if up_down == "<":
                    query+= "< "
                else: query+= "> "
                query += sortuj_wartosc
            print(f"Query na teraz: {first_query+query}")
            sortuj_ilosc = input("Wprowadz ilosc: ")
            if len(sortuj_ilosc)>0:
                query = check_for_where(query)
                up_down = input("> czy <? (Default: >): ")
                query += "Ilosc "
                if up_down == "<":
                    query+= "< "
                else: query+= "> "
                query += sortuj_ilosc
            if user_input.lower() == "rabat":
                sortuj_rabat = input("Liczyc transakcje z rabatem? (tak/nie - wtedy transakcje bez rabatu. Default - tak): ")
                if sortuj_rabat.lower() == "nie":
                    query = check_for_where(query)
                    query += "Rabat = 0"
                else:
                    query = check_for_where(query)
                    query += "Rabat > 0"
            else:
                sortuj_rabat = input("Wprowadz, czy uwzglednic transakcje z rabatem (tak/nie/obojetnie): ")
                if sortuj_rabat.lower == "tak":
                    query = check_for_where(query)
                    query += "Rabat > 0"
                elif sortuj_rabat.lower() == "nie":
                    query = check_for_where(query)
                    query += "Rabat = 0"
            query+=";"
            print(f"Query: {first_query+query}")
            for x in conn.execute(text(first_query+query)):
                print(f"{user_input.capitalize()}: {x[0] if x[0]!= None else 0}")


