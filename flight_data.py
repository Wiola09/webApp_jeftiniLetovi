from flight_search import FlightSearch
from data_manager import DataManager
import requests


class FlightData:
    # This class is responsible for structuring the flight data.

    def __init__(self, kod_grada):
        self.data = FlightSearch(kod_grada=kod_grada)
        self.novi = self.data.letovi(kod_grada)

    # HINT 1: Try to use the FlightData class to represent the flight data. e.g. You can create attributes for price,
    # departure_airport_code, departure_city etc.
    # data = FlightSearch(kod_grada=)
    # # print(type(data))
    # novi = data.letovi()
    # for i in novi["data"]:
    #     print(i["price"], "GBP")

    def stampaj_podatke_naj_ponuda(self):
        text_lista = []
        # print(response.text)
        #     for i in range(len(self.novi["data"])):
        for i in range(3):
            # sedista = self.novi["data"][i]["availability"]["seats"].text
            # print(type(sedista))
            # if int(self.novi["data"][i]["availability"]["seats"]) > 5:
            price = self.novi["data"][i]["price"]  # "GBP"
            print(price, "cena")
            departure_city_name = self.novi["data"][i]["cityFrom"]
            print(departure_city_name, "departure_city_name")
            departure_airport_iata_code = self.novi["data"][i]["flyFrom"]
            print(departure_airport_iata_code, "departure_airport_IATA_code")
            arrival_city_name = self.novi["data"][i]["cityTo"]
            print(arrival_city_name, "arrival_city_name")
            arrival_airport_iata_code = self.novi["data"][i]["flyTo"]
            print(arrival_airport_iata_code, "arrival_airport_iata_code")

            slobodna_sedista = self.novi["data"][i]["availability"]["seats"]
            print(slobodna_sedista, "Slobodno sedišta")

            prevoznik = self.novi["data"][i]["airlines"]
            print(prevoznik, "Prevoznik")

            infomracije_o_ruti = self.novi["data"][i]["route"]

            print(infomracije_o_ruti, "rute")
            print(len(infomracije_o_ruti), "broj letova")
            broj = 0
            for j in infomracije_o_ruti:

                ruta = j["local_arrival"]
                datum = ruta.split("T")
                print()
                if broj == 0:
                    outbound_date = datum[0]
                    print(outbound_date, "outbound_date")
                    # outbound_date
                if broj == (len(infomracije_o_ruti)-1):
                    inbound_date = datum[0]
                    print(inbound_date, "inbound_date")
                    # inbound_date
                broj += 1
                print(j["local_arrival"], "Dolazna vremena po ruti")

            text = f"Low price alert ! Only £ {price} to fly from {departure_city_name}-{departure_airport_iata_code}" \
                   f" to {arrival_city_name}-{arrival_airport_iata_code}, from {outbound_date} to {inbound_date}, " \
                   f"prevoznik je {prevoznik} preostalo slobodnih mesta {slobodna_sedista}.\n"
            # print(text)
            text_lista.append(text)

            print(60 * "+")
        return text_lista

    def vrati_cenu(self, najnizene_cene):
        # najnizene_cene = {}
        try:
            cena = self.novi["data"][0]["price"]
            print(self.novi["data"][0]["cityTo"])
            najnizene_cene[self.novi["data"][0]["cityTo"]] = cena
        except IndexError:
            pass
        print("prosao kroz vrati cenu")
        # print("Najniže cene su: ", najnizene_cene)
        return cena

        # print(data["data"][66]["availability"]["seats"], "Slobodno sedišta")
        # print(data["data"][66]["airlines"], "Prevoznik")
        # infomracije_o_ruti = data["data"][66]["route"]
        # print(data["data"][66]["route"], "rute")
        # print(type(data["data"][66]["route"]), "tip zapisa")
        # print(len(data["data"][66]["route"]), "broj ruta")
        # for i in infomracije_o_ruti:
        #     print(i["local_arrival"], "Doalzna vremena po ruti")


# podaci_letova = FlightData()
# podaci_letova.stampaj_podatke_naj_ponuda()
