from matplotlib import pyplot as plt
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://sklepy:Przetwarzanie123@127.0.0.1/sklepy")

def get_payment_methods_chart():
    labels = []
    sizes = []
    
    query = text("""
        SELECT p.typ, COUNT(f.Platnosc_ID) 
        FROM fakty f 
        JOIN platnosci p ON f.Platnosc_ID = p.id 
        GROUP BY p.typ
    """)
    
    with engine.connect() as conn:
        for row in conn.execute(query):
            labels.append(row[0])
            sizes.append(row[1])

    fig, ax = plt.subplots(figsize=(6, 6), layout='constrained')
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax.set_title('Popularność metod płatności')
    
    plt.savefig("analytics-payments.png")
    print("Wygenerowano wykres płatności.")


def get_category_revenue_chart():
    categories = []
    revenue = []
    
    query = text("""
        SELECT p.Kategoria, SUM(f.Wartosc * f.Ilosc * ((100-f.Rabat)/100)) 
        FROM fakty f 
        JOIN produkty p ON f.Produkt_ID = p.id 
        GROUP BY p.Kategoria
        ORDER BY SUM(f.Wartosc * f.Ilosc * ((100-f.Rabat)/100)) DESC
    """)
    
    with engine.connect() as conn:
        for row in conn.execute(query):
            categories.append(row[0].replace("_", " "))
            revenue.append(float(row[1]))

    fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
    ax.barh(categories, revenue, color='skyblue')
    ax.set_xlabel('Przychód (zł)')
    ax.set_title('Całkowity przychód według kategorii produktów')
    ax.invert_yaxis()
    
    plt.savefig("analytics-categories.png")
    print("Wygenerowano wykres kategorii.")


def get_discount_impact_chart():
    discounts = []
    quantities = []
    
    query = text("""
        SELECT Rabat, Ilosc 
        FROM fakty 
        WHERE Rabat > 0
    """)
    
    with engine.connect() as conn:
        for row in conn.execute(query):
            discounts.append(float(row[0]))
            quantities.append(int(row[1]))

    fig, ax = plt.subplots(figsize=(6, 4), layout='constrained')
    ax.scatter(discounts, quantities, alpha=0.3, color='purple')
    ax.set_xlabel('Wysokość rabatu (%)')
    ax.set_ylabel('Ilość kupionych sztuk')
    ax.set_title('Wpływ rabatu na ilość kupowanych produktów')
    
    plt.savefig("analytics-discounts.png")
    print("Wygenerowano wykres wpływu rabatów.")

if __name__ == "__main__":
    get_payment_methods_chart()
    get_category_revenue_chart()
    get_discount_impact_chart()
