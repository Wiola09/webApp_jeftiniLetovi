"""
https://stackoverflow.com/questions/14789668/separate-sqlalchemy-models-by-file-in-flask
@johnny It means that SQLAlchemy() does not have to take app as parameter in the module it is used.
In most examples you can see SQLAlchemy(app) but it requires app from other scope in this case.
Instead you can use uninitialized SQLAlchemy() and use init_app(app) method later
as described in http://stackoverflow.com/a/9695045/2040487. –
"""
import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flight_search import FlightSearch
import requests
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class DataManagerFlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(250), nullable=True)
    iata_code = db.Column(db.String(250), nullable=True)
    lowest_price = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(100), nullable=True)


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def dodaj_exel_u_bazu(self):
        file_path3 = r"static"
        abs_path = os.path.join(os.getcwd(), file_path3)
        print(abs_path)

        df = pd.read_excel(f'{abs_path}/Pocetna_tabela_letova.xlsx', sheet_name='prices')

        for index, row in df.iterrows():
            print(row['City'], row['IATA Code'], row['Lowest Price'])
            data = DataManagerFlight(
                city=row['City'],
                iata_code=row['IATA Code'],
                lowest_price=row['Lowest Price'],
                email=""
            )
            # with app.app_context():
            db.session.add(data)
        db.session.commit()

    def proveri_iata_code_i_dodaj(self):
        # with app.app_context():   # Ne treba kad nije u main
        movie_to_update = DataManagerFlight.query.filter_by(city="Paris").first()
        lista_zapisa = db.session.query(DataManagerFlight).all()
        kod = FlightSearch()
        for i in lista_zapisa:
            if not i.iata_code:
                print(i.iata_code)
                i.iata_code = "TESTING"
            elif i.iata_code == "TESTING":
                i.iata_code = kod.kod_grada(i.city)

        db.session.commit()

    def vrati_sve_zapise_iz_db(self):
        lista_zapisa = db.session.query(DataManagerFlight).all()
        return lista_zapisa

    def obrisi_zapis_iz_db(self, ime_grada_brisanje):
        ime_grada = DataManagerFlight.query.filter_by(city=ime_grada_brisanje).first()
        print(ime_grada)
        try:
            ime_grada = DataManagerFlight.query.filter_by(city=ime_grada_brisanje).first()
            db.session.delete(ime_grada)
            db.session.commit()
            print("obrisano")
        except:
            print("ajmo ponovo")

    def upisi_celiju(self, grad, red):

        kod_grada2 = FlightSearch()
        kod = kod_grada2.kod_grada(grad)
        print(kod)
        price = {
            "price": {'iataCode': kod}
        }

        # response = requests.put(url=f"{URL}/{red}", json=price, headers=zaglavlje)
        # print(response.text)

    pass


    def dodaj_grad_iata(self, iata, ime_grada):
        if DataManagerFlight.query.filter_by(iata_code=iata).first():
            return "grad već psotoji"
        else:
            new_city = DataManagerFlight(city=ime_grada, iata_code=iata)
            db.session.add(new_city)
            db.session.commit()

    def pretrazi_grad_db_po_vrednosti(self, polje_db, vrednost_za_pretragu):
        if polje_db == "city":
            return DataManagerFlight.query.filter_by(city=vrednost_za_pretragu).first()
        elif polje_db == "iata_code":
            return DataManagerFlight.query.filter_by(iata_code=vrednost_za_pretragu).first()
        elif polje_db == "email":
            return DataManagerFlight.query.filter_by(email=vrednost_za_pretragu).first()
        else:
            pass


class UserFlight(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class UserData:
    def __init__(self, email, password, name):
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        self.name = name

    def add_user(self):
        new_user = UserFlight(email=self.email, password=self.password, name=self.name)
        db.session.add(new_user)
        db.session.commit()

    def pretrazi_db_po_korisniku(self, vrednost_za_pretragu):
        return UserFlight.query.filter_by(email=vrednost_za_pretragu).first()