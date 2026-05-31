
/* Jesli serwer MySQL dziala z opcja secure-file-priv, nalezy przetransportowac pliki wygenerowane
w skrypcie w Pythonie do folderu zaufanego, a nastepnie zmienic sciezki na nastepujacych liniach:
33, 52, 67, 86, 101
Można go wyświetlić, wykorzystując polecenie SHOW VARIABLES LIKE "secure_file_priv";

Przykladowe uzycie
SHOW VARIABLES LIKE "secure_file_priv"; 'C:\ProgramData\MySQLServer\Uploads\'

Przykladowa zamiana
LOAD DATA INFILE 'C:/ProgramData/MySQLServer/Uploads/Fakty.csv'
*/

-- Utworzenie bazy danych
DROP DATABASE IF EXISTS hurtownia;

CREATE DATABASE hurtownia;
USE hurtownia;

-- Utworzenie tabeli faktow

CREATE TABLE factSprzedaze (
  Produkt_ID INT NOT NULL,
  Lokalizacja_ID INT NOT NULL,
  Data_faktu INT NOT NULL,
  Platnosc_ID INT NOT NULL,
  Wartosc DECIMAL(10,2) NOT NULL,
  Ilosc INT NOT NULL,
  Rabat DECIMAL(10,2) NOT NULL
);

-- Zaladowanie danych do tabeli faktów
LOAD DATA INFILE 'M:/MySQL/MySQLServerData/Uploads/Fakty.csv'
INTO TABLE factSprzedaze
FIELDS TERMINATED BY ','
ENCLOSED BY '"' LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

SELECT * FROM factSprzedaze;

-- Utworzenie tabeli (wymiaru) produktu i zaladowanie danych

CREATE TABLE dimProdukt (
	Produkt_ID INT NOT NULL,
    Nazwa_Produktu VARCHAR(48) NOT NULL,
    Podkategoria VARCHAR(48) NOT NULL,
    Kategoria VARCHAR(48) NOT NULL,
    CenaBazowa INT NOT NULL
);


LOAD DATA INFILE 'M:/MySQL/MySQLServerData/Uploads/Produkty.csv'
INTO TABLE dimProdukt
FIELDS TERMINATED BY ','
ENCLOSED BY '"' LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

SELECT * FROM dimProdukt;

-- Utworzenie tabeli (wymiaru) lokalizacji i zaladowanie danych

CREATE TABLE dimLokalizacja (
    Lokalizacja_ID INT NOT NULL,
	Nazwa_Lokalizacji VARCHAR(48) NOT NULL
);

LOAD DATA INFILE 'M:/MySQL/MySQLServerData/Uploads/Lokalizacje.csv'
INTO TABLE dimLokalizacja
FIELDS TERMINATED BY ','
ENCLOSED BY '"' LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

SELECT * FROM dimLokalizacja;

-- Utworzenie tabeli (wymiaru) daty i zaladowanie danych

CREATE TABLE dimData (
	Data_ID INT NOT NULL,
    Data_ VARCHAR(10) NOT NULL,
    Rok INT NOT NULL,
    Miesiac INT NOT NULL,
    Dzien INT NOT NULL,
    DzienTygodnia VARCHAR(15) NOT NULL
);

LOAD DATA INFILE 'M:/MySQL/MySQLServerData/Uploads/daty.csv'
INTO TABLE dimData
FIELDS TERMINATED BY ','
ENCLOSED BY '"' LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

SELECT * FROM dimData;

-- Utworzenie tabeli  (wymiaru) platnosci i zaladowanie danych

CREATE TABLE dimPlatnosc (
	Platnosc_ID INT NOT NULL,
    Nazwa_Metody VARCHAR(12) NOT NULL
);

LOAD DATA INFILE 'M:/MySQL/MySQLServerData/Uploads/Platnosci.csv'
INTO TABLE dimPlatnosc
FIELDS TERMINATED BY ','
ENCLOSED BY '"' LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

SELECT * FROM dimPlatnosc;