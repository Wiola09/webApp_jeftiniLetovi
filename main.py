import ast
import re
import os
import pandas as pd
import psycopg2
import sqlalchemy
from flask import Flask, render_template, redirect, url_for, request, flash, current_app
from flask_bootstrap import Bootstrap
import simplejson as json
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from datetime import datetime
from psycopg2.extensions import TransactionRollbackError

# Deo koji se odnosi na moje fajlove
from data_manager import db, DataManager, UserData, UserFlight
from flight_data import FlightData
from forms_moje import UnesiPodateZaPretraguForm, UnesiGrad
from notification_manager import NotificationManager
from flight_search import FlightSearch

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "default_value")


app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY
Bootstrap(app)

# CREATE DATABASE
# Prva li nija mi javlja gresku, problem je bio sto sam dodao env vrednost DATABASE_URL1, pa je on nalazi, ne treba je
# dodavati, jer je ence naci pa koristi sqlite
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL1", 'sqlite:///new-flight-collection2.db')
except:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-flight-collection2.db'
    print("izabrao rezervu")

# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app) # Ovaj deo je bio dok je class Nalozi(db.Model): bila definisna u ovom fajlu

db.init_app(app)  # vidi komentar u "data_manager.py"



# deo logovanje regisrovanje
""" The login manager contains the code that lets your application and Flask-Login work together, such as how to load a 
user from an ID, where to send users when they need to log in, and the like.
Once the actual application object has been created, you can configure it for login with:"""
login_manager = LoginManager()
login_manager.init_app(app)

""" The above code allows the app and login manager to work together. User_id allows to display unique data for 
each user at a website (like account info, past purchases, carts, etc.)"""

# bez app_context() javlja gresku, mozda je do verzija Flask-SQLAlchemy==3.0.2
with app.app_context():
    db.create_all()

# Kreiram objekte iz DB, klase su mi zaduzene za manipulaciju klasama u kojima sam
# formirao DB DataManagerFlight(db.Model) i UserFlight(UserMixin, db.Model):
kod = FlightSearch()
objekat_baza = DataManager()
# objekat_db_korisnik = UserData() # TODO TRAZI PARAMETRE U KLASI UserData


@login_manager.user_loader
def load_user(user_id):
    return UserFlight.query.get(int(user_id))
# TODO uraditi reformat da se ne koristi direkno klasa DB vec UserData


@app.route('/favicon.ico')
def favicon():
    """
    Morao sam dodati ovu funkciju jer izgleda da mi base.html nije bio u kontekstu, pa url_for nije radio,
     problem je nastao kada sam dodao footer.html i ejdnostavno favicon nije mogao da bude nađen
    :return: file favicon.ico
    """
    return redirect(url_for('static', filename='images/favicon.ico'))


@app.route('/')
def pocetak():
    """ Početna stranica daje dugmad za logovanej i registrovanje
    :return: prikazuje html stranicu "pocetak.html"
    """
    # Proveravam da li je neki korisnik ulogovan
    # print(current_user, "pocetak")
    return render_template("pocetak.html")


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user_object = UserData.pretrazi_db_po_korisniku(UserData, vrednost_za_pretragu=email)
        # TODO

        if not user_object:
            # metod flash je iz flaska, dodat kod i u *.html stranici
            flash("That email does not exist, please register.")
            return redirect(url_for('register'))

        # Password incorrect
        # Check stored password hash against entered password hashed.
        elif not check_password_hash(user_object.password, password):
            # metod flash je iz flaska, dodat kod i u *.html stranici
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))

        # Email exists and password correct
        else:  # If the user has successfully logged in or registered, you need to use the login_user() function to
            # authenticate them.
            login_user(user_object)
            return redirect(url_for('pocetna_forma_unos', name=current_user.name))

    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Predlog od codeGPT :
        try:
            user_object = UserData.pretrazi_db_po_korisniku(UserData, vrednost_za_pretragu=email)
            if user_object is None:
                UserData(
                    name=name,
                    email=email,
                    password=password,
                ).add_user()
                user = UserFlight.query.filter_by(email=email).first()

            else:
                flash("You've already signed up with that email, log in instead!")

        except:
                db.session.rollback()
                # rukujte s pogreškom na odgovarajući način
        finally:
            db.session.close()

        # Moje resenje
        # try:
        #     user_object = UserData.pretrazi_db_po_korisniku(UserData, vrednost_za_pretragu=email)
        # except:
        #     db.session.rollback()
        #     db.session.commit()
        # # TODO
        # if user_object:
        #     # metod flash je iz flaska, dodat kod i u *.html stranici
        #     flash("You've already signed up with that email, log in instead!")
        #     return redirect(url_for('login'))
        # # db.session.close()
        # UserData(
        #     name=name,
        #     email=email,
        #     password=password,
        # ).add_user()
        # user = UserFlight.query.filter_by(email=email).first()

        # TODO uraditi reformat da se ne koristi direkno klasa DB vec UserData
        """ Kada korisnik pošalje podatke za prijavu (npr. korisničko ime i lozinku), obično se ti podaci proveravaju u 
        bazi podataka kako bi se utvrdilo da li su validni. Ako su podaci validni, korisnik se "autentikuje" 
        (authenticate), što znači da se postavlja current_user objekat na instancu User klase koja predstavlja 
        prijavljenog korisnika.U Flasku se ovo obično radi pomoću login_user() funkcije, koja prima User objekat kao 
        argument i postavlja current_user na taj objekat."""
        login_user(user)
        print()

        return redirect(url_for("pocetna_forma_unos", name=current_user.name, logged_in=current_user.is_authenticated))

    return render_template("register.html")


@app.route('/logout')
def logout():
    print(current_user, "pre logout")
    logout_user()
    print(current_user, "posle logout")
    return redirect(url_for('pocetak', logged_in=current_user.is_authenticated))


# Prvim promenljivu u kojoj cu da pohranim vrednosti koje je izabrao korisnik putem forme u
# funkciji "pocetna_forma_unos"
unos_za_pretragu = {}


@app.route('/pocetna_forma_unos', methods=["GET", "POST"])
@login_required
def pocetna_forma_unos():
    user_name = request.args.get('name')
    if current_app:
        print('HTML kod se nalazi u Flask kontekstu')
    else:
        print('HTML kod se ne nalazi u Flask kontekstu')
    svi_gradovi = objekat_baza.vrati_sve_zapise_iz_db()
    forma = UnesiPodateZaPretraguForm()
    forma.destinacija.choices = [grad.city for grad in svi_gradovi]
    if forma.validate_on_submit():
        if 'submit' in request.form:
            ime_sluzbe = forma.adults.data
            print(ime_sluzbe)
            print(forma.data, "ovo tražim")
            global unos_za_pretragu
            unos_za_pretragu = forma.data
            print(type(forma.data))
            lista_vrednosti = [value for value in forma.data.values()]
            print(lista_vrednosti)
            for i in forma:
                print(i.data)
            return redirect(url_for("pretrazi_let", name=current_user.name, logged_in=current_user.is_authenticated,
                                    recnik=forma.data))
        elif 'submit2' in request.form:
            grad_za_brisanje = forma.destinacija.data
            print(grad_za_brisanje)
            objekat_baza.obrisi_zapis_iz_db(grad_za_brisanje)
            flash(f"The city {grad_za_brisanje} is removed from DB!")
            return redirect(url_for('pocetna_forma_unos', name=current_user.name))
    print(current_user)
    return render_template("pocetna_forma_unos.html", form=forma, name=current_user.name,
                           logged_in=current_user.is_authenticated)


# @app.route("/add", methods=["GET", "POST"])
# def test():
#     objekat_json_list = request.args.get('objekat_let')
#     print(type(objekat_json_list))
#     objekat_list = [json.loads(objekat_json) for objekat_json in objekat_json_list]
#     print(objekat_list, "ovo vraca rezultat")
#     print(type(objekat_list))
#     return "Objekat je uspješno dohvaćen"

def formiraj_google_flights_url(odlaz, destinacija, datum_odlaska, datum_povratka, broj_odraslih=2, broj_dece=4,
                                klasa="economy"):
    URL = "https://www.google.com/travel/flights"
    # Izgled objekta pretrage
    # {'date_from': datetime.date(2023, 4, 3), 'date_to': datetime.date(2023, 5, 2), 'adults': '2', 'children': '0',
    #  'nights_in_dst_from': 1, 'polaziste': 'BEG', 'destinacija': 'Paris', 'nights_in_dst_to': 3, 'submit': True,
    #  'submit2': False,
    #  'csrf_token': 'IjQ3YjVhZTM0ZDllYzVlMTcxMWIwYmIzMjgyYmNhYzU1MGFmNGQwMDEi.ZCnqxg.a8ueSl-QILzNMCPzrAD0MgNdQwk'}

    RECNIK_BROJEVI = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "one", "6": "one",
                      "7": "one", }
    ODLAZ = odlaz
    DESTINACIJA = destinacija
    DATUM_ODLASKA = datum_odlaska
    DATUM_POVRATKA = datum_povratka
    BROJ_ODRASLIH = RECNIK_BROJEVI[unos_za_pretragu['adults']]
    BROJ_DECE = RECNIK_BROJEVI[unos_za_pretragu['children']]
    KLASA = "economy"
    if BROJ_DECE == "zero":
        # Link ispod su samo odrasli, kada ide vrednost za decu zero, ne izbaci dobar link
        link = f"{URL}?q=Flights%20to%20{DESTINACIJA}%20from%20{ODLAZ}%20on%20{DATUM_ODLASKA}%20through%20{DATUM_POVRATKA}%20with%20{BROJ_ODRASLIH}%20adult%20{KLASA}%20class"
    else:
        link = f"{URL}?q=Flights%20to%20{DESTINACIJA}%20from%20{ODLAZ}%20on%20{DATUM_ODLASKA}%20through%20{DATUM_POVRATKA}%20with%20{BROJ_ODRASLIH}%20adult%20and%20{BROJ_DECE}%20children%20{KLASA}%20class"

    return link


# triguruje se sa stranice rezultat <a href="{{ url_for('pretrazi_i_prikazi_let_za_grad2', objekat_let=let['id']) }}"
@app.route('/pretrazi_i_prikazi_let_za_grad2/')
@login_required
def pretrazi_i_prikazi_let_za_grad2():
    id_leta = request.args.get('objekat_let')
    print(podaci_o_letovima["data"][0]["price"], "ova cena")
    for i in podaci_o_letovima["data"]:
        if i["id"] == id_leta:
            print(i)
            broj_ruta = len(i["route"])

            link = formiraj_google_flights_url(i["flyFrom"], i["flyTo"],
                                               (i["route"][0]["local_departure"]).split("T")[0],
                                               (i["route"][-1]["local_arrival"]).split("T")[0])
            print(link)
            return render_template(
                "jel_moguce.html",
                izabran_put=i,
                broj_ruta=broj_ruta,
                logged_in=current_user.is_authenticated,
                link_ka_letu=link,
                unos_za_pretragu=unos_za_pretragu,

                # name=current_user.name
            )

    # ovde nastavite sa kodom za prikaz detalja leta
    return "Objekat je uspješno dohvaćen"


# kreiram promenljivu u koju snimam vrednost pretrage kod.letovi(recnik) iz funkcije pretrazi_let
podaci_o_letovima = []


@app.route("/pretrazi_let", methods=["GET", "POST"])
@login_required
def pretrazi_let():
    """
    Ova flask funkcija preuzima podatke od funkcije "pocetna_forma_unos", koji su u obliku stringa (ali izgleda data
    time vrednosti su ostale), radi obradu ,datetime vrednosti prebacuje ih u strnih, i zatim ceo string konvertuje u
     recnik, zatim vrednost destinacije menjamo iz imena grada u kod grada(radimo pretragu DB), potom po kodu grada
     radimo pretragu API TEQUILA i vrednost vracam u global promenljivu tipa liste podaci_o_letovima,
     (to mi je bitno jer posle koristim ovu promenljivu u funkciji pretrazi_i_prikazi_let_za_grad2,
     a ne radim ponovnu pretragu TEQUILA API , uzimam prvih 5 vrednosti  iz liste podaci_o_letovima, i saljem ih na
      prikaz na stranici "rezultat.html"
    :return: renderuje stranicu "rezultat.html", gde kao jedan od argumenata salje listru sa prvih 5 vrednosti letova
    """
    # iata_kod = request.args.get('naslov')
    string_recnik = request.args.get('recnik')

    # Pronađite sve datetime objekte u stringu
    datetimes = re.findall(r"datetime\.date\(\d+,\s\d+,\s\d+\)", string_recnik)

    # Konvertujte ih u stringove i prebacuje datum u želejni format '01/05/2023'
    for dt in datetimes:
        dt_str = datetime.strptime(dt, "datetime.date(%Y, %m, %d)").strftime("%d""/""%m""/""%Y")
        string_recnik = string_recnik.replace(dt, f"'{dt_str}'")

    # Konvertujte string u rečnik
    recnik = ast.literal_eval(string_recnik)
    # recnik = ast.literal_eval(string_recnik.replace("datetime.date", "date"))

    # def promeni_destinaciju_u_iata():

    # print(type(recnik))
    # print(recnik)
    # print(recnik['destinacija'])
    objekat_iz_db_ptretraga_po_city = objekat_baza.pretrazi_grad_db_po_vrednosti(
        polje_db="city",
        vrednost_za_pretragu=recnik['destinacija']
    )
    # print(objekat_iz_db_ptretraga_po_city.iata_code, "vraca posle pretrage grada po polju city")
    recnik['destinacija'] = objekat_iz_db_ptretraga_po_city.iata_code
    # promeni_destinaciju_u_iata()  Zaboravio sam da se menja vrednost recnik['destinacija']  samo lokalno u funkciji

    global podaci_o_letovima
    podaci_o_letovima = kod.letovi(recnik)
    print(type(podaci_o_letovima), "podaci_o_letovima ")
    # print(podaci_o_letovima)
    # print(type(podaci_o_letovima["data"]), "podaci_o_letovima ")
    # print(podaci_o_letovima["data"])
    lista = podaci_o_letovima["data"][:5]
    print(podaci_o_letovima)
    # return "test"
    # TODO napravi zastitu kad je prazna lista rezultat, to je pponekad za grad Moskva npr.
    return render_template("rezultat.html", rezultat_pretrage=lista, unos_za_pretragu=unos_za_pretragu,
                           logged_in=current_user.is_authenticated)


@app.route("/dodaj_grad", methods=["GET", "POST"])
@login_required
def dodaj_grad():
    forma_grad_za_pretragu = UnesiGrad()
    if forma_grad_za_pretragu.validate_on_submit():
        termin_pretragu = forma_grad_za_pretragu.grad.data

        lista_kod_grada = kod.kod_grada(termin_pretragu)
        print(lista_kod_grada)
        print(type(lista_kod_grada))
        for i in lista_kod_grada:
            print(f"IATA kod {i['code']}, ime grada {i['name']}, ime grada i država {i['slug_en']}")
        return render_template("rezultata_pretarge_grada.html", lista_kod_grada=lista_kod_grada,
                               logged_in=current_user.is_authenticated)

    return render_template("forma_pretraga_grada.html", form=forma_grad_za_pretragu,
                           logged_in=current_user.is_authenticated)


@app.route("/unesi_grad_u_db", methods=["GET", "POST"])
@login_required
def unesi_grad_u_db():
    iata_kod = request.args.get('iata_kod_grada')
    ime_grada = request.args.get('ime_grada')

    print(iata_kod, ime_grada)
    objekat_baza.dodaj_grad_iata(iata_kod, ime_grada)
    flash(f"The city {ime_grada} is added to DB!")

    return redirect(url_for('pocetna_forma_unos', logged_in=current_user.is_authenticated))


# todo? Brisati, mislim da ovu funkciju vise ne koristim
@app.route("/add", methods=["GET", "POST"])
@login_required
def pretrazi_i_prikazi_let_za_grad():
    iata_kod = request.args.get('naslov')
    global podaci_o_letovima
    podaci_o_letovima = kod.letovi(iata_kod)
    print(type(podaci_o_letovima), "podaci_o_letovima ")
    print(type(podaci_o_letovima["data"]), "podaci_o_letovima ")
    # print(podaci_o_letovima["data"])
    lista = podaci_o_letovima["data"][:5]

    return render_template("rezultat.html", rezultat_pretrage=lista, logged_in=current_user.is_authenticated)


"""Samo jednom Kod za dodavanje exel podataka u bazu podataka"""


# objekat_baza = DataManager()
# with app.app_context():
#     objekat_baza.dodaj_exel_u_bazu()

# brisati ? mislim da mi vise ne treba
# objekat_baza = DataManager()
# with app.app_context():
#     objekat_baza.proveri_iata_code_i_dodaj()


# BRISATI TODO
@app.route("/home_prikaz_filmova")
# @login_required
def home_prikaz_filmova():
    recnik = request.args.get('recnik')
    print(recnik, "prenet")
    svi_gradovi = "test"
    svi_gradovi = objekat_baza.vrati_sve_zapise_iz_db()

    return render_template(
        "index.html",
        svi_gradovi=svi_gradovi,
        logged_in=current_user.is_authenticated,
        # name=current_user.name
    )


def brisati():
    # Dodavanje korisnika u bazu
    # name = request.form.get('name')
    # email = request.form.get('email')
    # password = request.form.get('password')
    name = "Miroslav"
    email = "mir@gmail.com"
    password = "123"
    with app.app_context():
        user_object = UserData.pretrazi_db_po_korisniku(UserData, vrednost_za_pretragu=email)

    if user_object:
        # metod flash je iz flaska, dodat kod i u *.html stranici
        print("You've already signed up with that email, log in instead!")
        # return redirect(url_for('login'))
    else:
        with app.app_context():
            UserData(
                name=name,
                email=email,
                password=password,
            ).add_user()
            print("dodat korisnik")


# grad = input("Unesite ime grada")
# kod_grada = kod.kod_grada("Tokyo")
# print(kod_grada)


def pretraga_i_stampa_najeftinijeg_za_sve_iz_baze():
    # PRETRAGA I STAMPA NAJEFTINIJEG LETA ZA SVE
    with app.app_context():
        lista_obejakata_baza = objekat_baza.vrati_sve_zapise_iz_db()
    #     objekat_baza.dodaj_exel_u_bazu()

    for i in lista_obejakata_baza:
        grad = i.city
        kod_grada = kod.kod_grada(grad)
        objekat_pretraga = kod.letovi(kod_grada)
        najjeftiniji = objekat_pretraga["data"][0]["price"]
        datum_odlaska = objekat_pretraga["data"][0]["route"][0]["local_arrival"]
        print(f"Najeftini pobratni let za grad {grad} je {najjeftiniji}, i dana je {datum_odlaska}")


# Funkcija salje mail za sve gradove iz baze
def posalji_na_sve_gradove_iz_baze():
    with app.app_context():
        lista_obejakata_baza = objekat_baza.vrati_sve_zapise_iz_db()
    for i in lista_obejakata_baza:
        grad = i.city
        # Pretraga koda, pretraga letova, slanje maila preko NotificationManager
        kod_grada_sada = kod.kod_grada(grad)
        podaci_o_letovima_druga = FlightData(kod_grada_sada)
        # time.sleep(5)
        mail = podaci_o_letovima_druga.stampaj_podatke_naj_ponuda()
        slati = NotificationManager()
        slati.posalji_mail(mail, f" TRI najeftinija leta od BGD do {grad}")


def pretraga():

    # grad = input("Unesite ime grada") , promenljiva "kod" kod = FlightSearch() je formirana na pocetku programa,
    # pa je sada pozivam
    kod_grada = kod.letovi()
    print(len(kod_grada["data"]))
    for i in range(0, 5):
        print(kod_grada["data"][i]["price"], "EUR")
        # print(type(i["price"]))
    # print(kod_grada)
    # print(kod_grada["data"][2])
    # print(kod_grada["data"][2])
    for i in range(0, 5):
        rute = kod_grada["data"][i]["route"]
        # print(rute)
        # print(type(rute))
        # print(len(rute))
        # print(kod_grada["data"][i]["route"][0]["local_arrival"], f"datum odlaska {i}")
        # print(kod_grada["data"][i]["route"][3]["local_arrival"], f"datum povratka {i}")
        # print(kod_grada["data"][i]["price"], "EUR")
        from datetime import datetime

        # string koji želite da pretvorite u datetime objekat
        date_string = kod_grada["data"][i]["route"][0]["local_arrival"]
        date_string2 = kod_grada["data"][i]["route"][3]["local_arrival"]
        # format string koji odgovara vašem stringu
        format_string = '%Y-%m-%dT%H:%M:%S.%fZ'

        # koristite metodu strptime() da biste parsirali string u datetime objekat
        date_time_obj1 = datetime.strptime(date_string, format_string)
        date_time_obj2 = datetime.strptime(date_string2, format_string)

        delta = date_time_obj2 - date_time_obj1
        # print(delta)
        days = delta.days
        # print(days)
        # print(60 * "*")

    try:
        dictionary_data = json.loads(json.dumps(kod_grada["data"][2]))
        # print(json.dumps(dictionary_data, indent=4))
        # print(json.dumps(kod_grada["data"][2], indent=4))
    except:
        print("pokusao")
    return kod_grada["data"][i]["price"]


# pretraga()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
