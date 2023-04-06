import os

import requests

# This class is responsible for talking to the Flight Search API.

TEQUILA_API = os.environ["TEQUILA_API"]


class FlightSearch:

    def __init__(self, kod_grada="BEG"):
        self.data = 0
        self.kod_grada3 = kod_grada
        # self.lista = []

    # This class is responsible for talking to the Flight Search API.

    def kod_grada(self, grad):
        #  Locations API
        url = f"https://tequila-api.kiwi.com/locations/query?term={grad}"
        payload = {}
        headers = {
            'apikey': TEQUILA_API
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        # print(response.text)
        # print(data["locations"])
        # print(data["locations"][0])
        # Za kod:grada postoji bug kada sam trazio Argentina , Buenos Aires , vratio mi ej BA  što je za Banja Luku,
        # pravi podatak se nalazio u [{'id': 'BA_AR',  probati data["locations"][0]["id"] , probati i 'code': 'BUE',
        # Tokio je TYO
        # kod_grada = data["locations"][0]["code"]
        kod_grada = data["locations"]
        return kod_grada

    pass

    def letovi(self, recnik_pretraga):
        import requests
        import datetime as dt
        # In [64]: datetime.datetime.now() - datetime.timedelta(minutes=15)
        # Out[64]: datetime.datetime(2010, 12, 27, 14, 24, 21, 684435)
        sadasnje_vreme = dt.datetime.now()
        # print(sadasnje_vreme)
        sutra = sadasnje_vreme + 160 * dt.timedelta(days=1)

        pola_godine = sadasnje_vreme + 210 * (dt.timedelta(days=1))
        pola_godine_datum = pola_godine.strftime("%d""/""%m""/""%Y")
        # print(sutra)
        sutra_datum = sutra.strftime("%d""/""%m""/""%Y")
        # print(sutra_datum)
        # print(pola_godine_datum)

        # url = f"https://tequila-api.kiwi.com/v2/search?return_from=01/12/2022&return_to={return_to}&dateFrom=01/09/2022&dateTo=01/12/2022&fly_from=BEG&fly_to=ROM&curr=GBP"
        url = "https://tequila-api.kiwi.com/v2/search?"

        # recnik_pretraga = {'date_from': '02/04/2023', 'date_to': '01/05/2023', 'adults': '2', 'children': '0', 'nights_in_dst_from': 1,
        #  'polaziste': 'BEG', 'destinacija': 'Paris', 'nights_in_dst_to': 3, 'submit_flight_data': True,
        #  'csrf_token': 'ImJhZDQ5ZjJjMGZlMDMyMzg0N2Q1M2FjOWY0NWVjNmY0YTNjYmE0ZWEi.ZCdc4A.2Wp0ZosTi_OtpfkFOfQdwQHliAU'}

        print(recnik_pretraga['destinacija'])
        params = {

            "dateFrom": recnik_pretraga['date_from'],
            "dateTo": recnik_pretraga['date_to'],
            # "return_from": "08/10/2022",
            # "return_to": "13/10/2022",
            "nights_in_dst_from": recnik_pretraga['nights_in_dst_from'],
            "nights_in_dst_to": recnik_pretraga['nights_in_dst_to'],
            "adults": int(recnik_pretraga['adults']),
            "children": int(recnik_pretraga['children']),
            # "fly_from": "LON",
            "fly_from": "BEG",
            # "fly_to": self.kod_grada3,
            # "fly_to": "BA_AR",  # Argentina , Buenos Aires
            "fly_to": recnik_pretraga['destinacija'],
            # "fly_to": "TYO",
            "curr": "EUR"
            # "curr": "GBP",
            #              "max_fly_duration":
            #                  integer
            #                  (query)
            #              max itinerary duration in hours, min value 0,  Example: 20
        }

        # params = {
        #
        #     "dateFrom": "01/10/2022",
        #     "dateTo": "05/10/2022",
        #     "return_from": "08/10/2022",
        #     "return_to": "13/10/2022",
        #     "fly_from": "BEG",
        #     "fly_to": "ROM",
        #     "curr": "GBP",
        #
        # }

        payload = {}
        headers = {
            'apikey': TEQUILA_API
        }

        response = requests.request("GET", url, headers=headers, data=payload, params=params)

        self.data = response.json()
        # print(type(self.data), "pretraga")
        # for i in self.data["data"]:
        #     print(i["price"], "GBP")
        # print(len(self.data["data"]))
        print("prosao")

        return self.data
    # print(response.text)
    # print(data["data"])


lista = [{'id': 'paris_fr',
          'active': True,
          'name': 'Paris',
          'slug': 'paris-france',
          'slug_en': 'paris-france',
          'code': 'PAR',
          'alternative_names': [],
          'rank': 9,
          'global_rank_dst': 3,
          'dst_popularity_score': 7702571.0,
          'timezone': 'Europe/Paris',
          'population': 2138551,
          'airports': 4,
          'stations': 8,
          'hotels': 3779,
          'bus_stations': 10,
          'subdivision': None,
          'autonomous_territory': None,
          'country': {'id': 'FR', 'name': 'France', 'slug': 'france', 'code': 'FR'},
          'region': {'id': 'western-europe', 'name': 'Western Europe', 'slug': 'western-europe'},
          'continent': {'id': 'europe', 'name': 'Europe', 'slug': 'europe', 'code': 'EU'},
          'nearby_country': None,
          'location': {'lat': 48.856614, 'lon': 2.352222},
          'tags': [{'tag': 'city break', 'month_to': -1, 'month_from': -1},
                   {'tag': 'culture', 'month_to': -1, 'month_from': -1},
                   {'tag': 'famous cities', 'month_to': -1, 'month_from': -1},
                   {'tag': 'romance', 'month_to': -1, 'month_from': -1},
                   {'tag': 'sightseeing', 'month_to': -1, 'month_from': -1}
                   ],
          'alternative_departure_points': [
              {'id': 'FR-PARI-PAR6', 'distance': 11.62, 'duration': 915.2},
              {'id': 'FR-ORLE-ORLE', 'distance': 128.86, 'duration': 5438.2},
              {'id': 'FR-ROUE-ROUE', 'distance': 131.12, 'duration': 5681.3},
              {'id': 'FR-REIM-REIM', 'distance': 143.0, 'duration': 5737.2},
              {'id': 'XIZ', 'distance': 147.68, 'duration': 6006.4},
              {'id': 'XCR', 'distance': 153.54, 'duration': 8219.9},
              {'id': 'DOL', 'distance': 193.9, 'duration': 7791.3},
              {'id': 'FR-LEHA-LEHA', 'distance': 194.31, 'duration': 7966.1},
              {'id': 'ORY', 'distance': 19.94, 'duration': 1457.5},
              {'id': 'FR-FECA-FECA', 'distance': 201.96, 'duration': 8923.4},
              {'id': 'FR-LEMA-LEMA', 'distance': 207.85, 'duration': 8102.9},
              {'id': 'ZLN', 'distance': 207.93, 'duration': 8379.1},
              {'id': 'LIL', 'distance': 212.86, 'duration': 8541.4},
              {'id': 'XFA', 'distance': 218.98, 'duration': 8504.4},
              {'id': 'XDB', 'distance': 219.99, 'duration': 8479.5},
              {'id': 'XJY', 'distance': 22.01, 'duration': 1470.5},
              {'id': 'FR-LILL-TOUR', 'distance': 230.02, 'duration': 9094.3},
              {'id': 'FR-CAEN-CAEN', 'distance': 232.14, 'duration': 9082.2},
              {'id': 'TUF', 'distance': 236.44, 'duration': 9139.5},
              {'id': 'XJT', 'distance': 236.87, 'duration': 9124.4},
              {'id': 'QMO', 'distance': 240.88, 'duration': 9259},
              {'id': 'CFR', 'distance': 244.34, 'duration': 9701.4},
              {'id': 'CDG', 'distance': 26.55, 'duration': 1613.5},
              {'id': 'CRL', 'distance': 280.84, 'duration': 10777.2},
              {'id': 'FR-PARI-PAR1', 'distance': 2.87, 'duration': 323.7},
              {'id': 'XHP', 'distance': 2.88, 'duration': 391.7},
              {'id': 'FR-CALA-CALA', 'distance': 288.1, 'duration': 10929},
              {'id': 'FR-DUNK-DUN0', 'distance': 292.15, 'duration': 11484.1},
              {'id': 'FR-DUNK-DUNK', 'distance': 292.36, 'duration': 11682.6},
              {'id': 'XPG', 'distance': 3.04, 'duration': 352.6},
              {'id': 'XGB', 'distance': 3.59, 'duration': 405.7},
              {'id': 'FR-PARI-PA11', 'distance': 3.99, 'duration': 441.4},
              {'id': 'FR-PARI-PARI', 'distance': 4.21, 'duration': 450.2},
              {'id': 'XED', 'distance': 44.22, 'duration': 2444.5},
              {'id': 'FR-PARI-PAR3', 'distance': 6.13, 'duration': 594.9},
              {'id': 'FR-PARI-PA10', 'distance': 6.28, 'duration': 632.4},
              {'id': 'BVA', 'distance': 80.84, 'duration': 3971.4},
              {'id': 'FR-PARI-PAR9', 'distance': 8.6, 'duration': 816.7},
              {'id': 'FR-PARI-PAR2', 'distance': 9.41, 'duration': 858}],
          'providers': [1028, 1035, 1053, 1064, 1096, 1128, 1148, 1163, 1165, 1171, 1175, 1179, 1224, 1227, 1229, 1282,
                        1283, 1291, 1329],
          'car_rentals': [
              {'provider_id': 1175,
               'providers_locations':
                   ['479433', '644548', '1550196', '4397726', '482993', '1921331', '1357038', '2951106', '393996',
                    '394061', '4294864', '4339142', '458098', '1550211', '2403851', '243254', '2775606']},
              {'provider_id': 1175, 'providers_locations': ['458073', '3723216', '2624116', '3882570', '1392478',
                                                            '1550166', '1550121', '2869686', '1392898', '1550151',
                                                            '2601131', '2776201', '1387651', '1550106', '1610616',
                                                            '1004003', '1387691', '2060186', '2775751', '1377648',
                                                            '2006683', '1429816', '2601136', '2308546', '2776191',
                                                            '458103', '1551111', '1610641', '1377678', '1003998',
                                                            '1550136', '1921741', '1975158', '1388001', '3713296',
                                                            '1387226', '1387731', '1056796', '1677353', '1387306',
                                                            '2775846', '2775821', '2799826', '1610666', '2601091',
                                                            '457968', '248574', '1387186', '1392488', '2775836',
                                                            '1550046', '2412676', '458108', '3713346', '458088',
                                                            '2060696', '2601256', '458093', '1357653', '458083',
                                                            '1549491', '1550181', '458078']}],
          'type': 'city'},
         {'id': 'CDG', 'int_id': 9667, 'airport_int_id': 9667, 'active': True, 'code': 'CDG', 'icao': 'LFPG',
          'name': 'Charles de Gaulle Airport', 'slug': 'charles-de-gaulle-paris-france',
          'slug_en': 'charles-de-gaulle-paris-france',
          'alternative_names': ['Aéroport de Paris-Charles-de-Gaulle', 'Paris (CDG)'], 'rank': 21, 'global_rank_dst': 8,
          'dst_popularity_score': 5298581.0, 'timezone': 'Europe/Paris',
          'city': {'id': 'paris_fr', 'name': 'Paris', 'code': 'PAR', 'slug': 'paris-france',
                   'continent': {'id': 'europe', 'name': 'Europe', 'slug': 'europe', 'code': 'EU'},
                   'region': {'id': 'western-europe', 'name': 'Western Europe', 'slug': 'western-europe'},
                   'autonomous_territory': None, 'subdivision': None, 'nearby_country': None,
                   'country': {'id': 'FR', 'name': 'France', 'slug': 'france', 'code': 'FR'}},
          'location': {'lat': 49.009722, 'lon': 2.547778},
          'alternative_departure_points': [{'id': 'FR-PLAI-PARC', 'distance': 16.69, 'duration': 796},
                                           {'id': 'LIL', 'distance': 190.06, 'duration': 7266.3},
                                           {'id': 'XCR', 'distance': 198.74, 'duration': 8435.4},
                                           {'id': 'DOL', 'distance': 213.47, 'duration': 8513.2},
                                           {'id': 'FR-PARI-PA10', 'distance': 22.52, 'duration': 1236.7},
                                           {'id': 'FR-PARI-PAR9', 'distance': 27.21, 'duration': 1569.5},
                                           {'id': 'FR-PARI-PAR3', 'distance': 27.37, 'duration': 1497.7},
                                           {'id': 'FR-PARI-PA11', 'distance': 27.6, 'duration': 1586.1},
                                           {'id': 'FR-PARI-PARI', 'distance': 28.62, 'duration': 1581.7},
                                           {'id': 'FR-PARI-PAR1', 'distance': 30.33, 'duration': 1711.6},
                                           {'id': 'FR-PARI-PAR2', 'distance': 30.48, 'duration': 1747},
                                           {'id': 'ORY', 'distance': 44.54, 'duration': 2554.2},
                                           {'id': 'XJY', 'distance': 45.49, 'duration': 2562.7},
                                           {'id': 'BVA', 'distance': 78.32, 'duration': 3340.6}],
          'tags': [{'tag': 'sightseeing', 'month_to': -1, 'month_from': -1},
                   {'tag': 'culture', 'month_to': -1, 'month_from': -1},
                   {'tag': 'famous cities', 'month_to': -1, 'month_from': -1},
                   {'tag': 'romance', 'month_to': -1, 'month_from': -1},
                   {'tag': 'city break', 'month_to': -1, 'month_from': -1}],
          'providers': [1028, 1035, 1053, 1064, 1096, 1128, 1148, 1163, 1165, 1175, 1227, 1229, 1282, 1283, 1291, 1329],
          'special': [{'id': 'le-cimetiere-de-pere-lachaise_poi', 'name': 'Le Cimetiere de Pere Lachaise',
                       'slug': 'le-cimetiere-de-pere-lachaise'},
                      {'id': 'louvre-museum_poi', 'name': 'Louvre Museum', 'slug': 'louvre-museum'},
                      {'id': 'eiffel-tower_poi', 'name': 'Eiffel Tower', 'slug': 'eiffel-tower'},
                      {'id': 'giverny_poi', 'name': 'Giverny', 'slug': 'giverny'},
                      {'id': 'versailles_poi', 'name': 'Versailles', 'slug': 'versailles'},
                      {'id': 'notre-dame_poi', 'name': 'Notre Dame', 'slug': 'notre-dame'}],
          'tourist_region': [{'id': 'ile-de-france_poi', 'name': 'Ile de France', 'slug': 'ile-de-france'},
                             {'id': 'greater-paris_poi', 'name': 'Greater Paris', 'slug': 'greater-paris'},
                             {'id': 'autoroute-utrecht-paris_poi', 'name': 'Autoroute Utrecht Paris',
                              'slug': 'autoroute-utrecht-paris'}],
          'car_rentals': [{'provider_id': 1175, 'providers_locations': ['644548']}], 'new_ground': False,
          'routing_priority': 0, 'type': 'airport'},
         {'id': 'ORY', 'int_id': 2684, 'airport_int_id': 2684, 'active': True, 'code': 'ORY', 'icao': 'LFPO',
          'name': 'Paris Orly', 'slug': 'paris-orly-paris-france', 'slug_en': 'paris-orly-paris-france',
          'alternative_names': ['Aéroport de Paris-Orly', 'Paris Orly (ORLY 2)'], 'rank': 41, 'global_rank_dst': 26,
          'dst_popularity_score': 2167378.0, 'timezone': 'Europe/Paris',
          'city': {'id': 'paris_fr', 'name': 'Paris', 'code': 'PAR', 'slug': 'paris-france',
                   'continent': {'id': 'europe', 'name': 'Europe', 'slug': 'europe', 'code': 'EU'},
                   'region': {'id': 'western-europe', 'name': 'Western Europe', 'slug': 'western-europe'},
                   'autonomous_territory': None, 'subdivision': None, 'nearby_country': None,
                   'country': {'id': 'FR', 'name': 'France', 'slug': 'france', 'code': 'FR'}},
          'location': {'lat': 48.723333, 'lon': 2.379444},
          'alternative_departure_points': [{'id': 'BVA', 'distance': 103.43, 'duration': 5376},
                                           {'id': 'XJY', 'distance': 13.15, 'duration': 1045.1},
                                           {'id': 'XCR', 'distance': 162.48, 'duration': 8598.9},
                                           {'id': 'FR-PARI-PARI', 'distance': 18.56, 'duration': 1273.7},
                                           {'id': 'FR-PARI-PA11', 'distance': 19.34, 'duration': 1377.2},
                                           {'id': 'FR-PARI-PAR1', 'distance': 20.27, 'duration': 1403.6},
                                           {'id': 'DOL', 'distance': 211.42, 'duration': 8669.3},
                                           {'id': 'TUF', 'distance': 227.6, 'duration': 8703.3},
                                           {'id': 'LIL', 'distance': 232.53, 'duration': 9528.8},
                                           {'id': 'FR-PARI-PAR3', 'distance': 26.73, 'duration': 1802.8},
                                           {'id': 'FR-PARI-PAR9', 'distance': 29.73, 'duration': 2022.5},
                                           {'id': 'FR-PARI-PAR2', 'distance': 29.97, 'duration': 2007.1},
                                           {'id': 'FR-PARI-PA10', 'distance': 31.05, 'duration': 2080.5},
                                           {'id': 'CDG', 'distance': 46.17, 'duration': 2586.4}],
          'tags': [{'tag': 'sightseeing', 'month_to': -1, 'month_from': -1},
                   {'tag': 'culture', 'month_to': -1, 'month_from': -1},
                   {'tag': 'famous cities', 'month_to': -1, 'month_from': -1},
                   {'tag': 'romance', 'month_to': -1, 'month_from': -1},
                   {'tag': 'city break', 'month_to': -1, 'month_from': -1}],
          'providers': [1035, 1096, 1148, 1227, 1229, 1283, 1291, 1329], 'special': [
             {'id': 'le-cimetiere-de-pere-lachaise_poi', 'name': 'Le Cimetiere de Pere Lachaise',
              'slug': 'le-cimetiere-de-pere-lachaise'},
             {'id': 'versailles_poi', 'name': 'Versailles', 'slug': 'versailles'},
             {'id': 'louvre-museum_poi', 'name': 'Louvre Museum', 'slug': 'louvre-museum'},
             {'id': 'giverny_poi', 'name': 'Giverny', 'slug': 'giverny'},
             {'id': 'notre-dame_poi', 'name': 'Notre Dame', 'slug': 'notre-dame'},
             {'id': 'eiffel-tower_poi', 'name': 'Eiffel Tower', 'slug': 'eiffel-tower'},
             {'id': 'chateau-de-chenonceau_poi', 'name': 'Chateau de Chenonceau', 'slug': 'chateau-de-chenonceau'}],
          'tourist_region': [{'id': 'ile-de-france_poi', 'name': 'Ile de France', 'slug': 'ile-de-france'},
                             {'id': 'greater-paris_poi', 'name': 'Greater Paris', 'slug': 'greater-paris'},
                             {'id': 'autoroute-utrecht-paris_poi', 'name': 'Autoroute Utrecht Paris',
                              'slug': 'autoroute-utrecht-paris'}], 'car_rentals': [], 'new_ground': False,
          'routing_priority': 0, 'type': 'airport'},
         {'id': 'autoroute-utrecht-paris_poi', 'active': True, 'name': 'Autoroute Utrecht Paris',
          'code': 'autoroute-utrecht-paris_poi', 'slug': 'autoroute-utrecht-paris',
          'slug_en': 'autoroute-utrecht-paris', 'alternative_names': [], 'rank': 16, 'global_rank_dst': 2048,
          'category': None, 'type': 'tourist_region'},
         {'id': 'greater-paris_poi', 'active': True, 'name': 'Greater Paris', 'code': 'greater-paris_poi',
          'slug': 'greater-paris', 'slug_en': 'greater-paris', 'alternative_names': [], 'rank': 17,
          'global_rank_dst': 2048, 'category': None, 'type': 'tourist_region'},
         {'id': 'BVA', 'int_id': 7346, 'airport_int_id': 7346, 'active': True, 'code': 'BVA', 'icao': 'LFOB',
          'name': 'Beauvais–Tillé', 'slug': 'beauvais-tille-paris-france', 'slug_en': 'beauvais-tille-paris-france',
          'alternative_names': ['Aéroport de Paris-Beauvais'], 'rank': 77, 'global_rank_dst': 152,
          'dst_popularity_score': 224652.0, 'timezone': 'Europe/Paris',
          'city': {'id': 'paris_fr', 'name': 'Paris', 'code': 'PAR', 'slug': 'paris-france',
                   'continent': {'id': 'europe', 'name': 'Europe', 'slug': 'europe', 'code': 'EU'},
                   'region': {'id': 'western-europe', 'name': 'Western Europe', 'slug': 'western-europe'},
                   'autonomous_territory': None, 'subdivision': None, 'nearby_country': None,
                   'country': {'id': 'FR', 'name': 'France', 'slug': 'france', 'code': 'FR'}},
          'location': {'lat': 49.454444, 'lon': 2.112778},
          'alternative_departure_points': [{'id': 'ORY', 'distance': 103.94, 'duration': 5411.8},
                                           {'id': 'DOL', 'distance': 170.78, 'duration': 8737.6},
                                           {'id': 'LIL', 'distance': 188.92, 'duration': 7522.9},
                                           {'id': 'CFR', 'distance': 221.31, 'duration': 10639.3},
                                           {'id': 'XCR', 'distance': 230.06, 'duration': 11133},
                                           {'id': 'CDG', 'distance': 78.17, 'duration': 3313.4}],
          'tags': [{'tag': 'sightseeing', 'month_to': -1, 'month_from': -1},
                   {'tag': 'culture', 'month_to': -1, 'month_from': -1},
                   {'tag': 'famous cities', 'month_to': -1, 'month_from': -1},
                   {'tag': 'romance', 'month_to': -1, 'month_from': -1},
                   {'tag': 'city break', 'month_to': -1, 'month_from': -1}],
          'providers': [1035, 1148, 1175, 1229, 1282, 1283, 1329],
          'special': [{'id': 'giverny_poi', 'name': 'Giverny', 'slug': 'giverny'},
                      {'id': 'le-cimetiere-de-pere-lachaise_poi', 'name': 'Le Cimetiere de Pere Lachaise',
                       'slug': 'le-cimetiere-de-pere-lachaise'},
                      {'id': 'notre-dame_poi', 'name': 'Notre Dame', 'slug': 'notre-dame'},
                      {'id': 'versailles_poi', 'name': 'Versailles', 'slug': 'versailles'},
                      {'id': 'eiffel-tower_poi', 'name': 'Eiffel Tower', 'slug': 'eiffel-tower'},
                      {'id': 'louvre-museum_poi', 'name': 'Louvre Museum', 'slug': 'louvre-museum'}],
          'tourist_region': [{'id': 'ile-de-france_poi', 'name': 'Ile de France', 'slug': 'ile-de-france'},
                             {'id': 'greater-paris_poi', 'name': 'Greater Paris', 'slug': 'greater-paris'},
                             {'id': 'autoroute-utrecht-paris_poi', 'name': 'Autoroute Utrecht Paris',
                              'slug': 'autoroute-utrecht-paris'}],
          'car_rentals': [{'provider_id': 1175, 'providers_locations': ['479433']}], 'new_ground': False,
          'routing_priority': 0, 'type': 'airport'},
         {'id': 'FR-PARI-PAR1', 'int_id': 719, 'airport_int_id': None, 'active': True, 'code': 'FR-PARI-PAR1',
          'icao': None, 'name': 'Paris - Gare De Lyon', 'slug': 'paris-gare-de-lyon-paris-france',
          'slug_en': 'paris-gare-de-lyon-paris-france', 'alternative_names': [], 'rank': 318, 'global_rank_dst': 2048,
          'dst_popularity_score': 337.0, 'timezone': 'Europe/Paris',
          'city': {'id': 'paris_fr', 'name': 'Paris', 'code': 'PAR', 'slug': 'paris-france',
                   'continent': {'id': 'europe', 'name': 'Europe', 'slug': 'europe', 'code': 'EU'},
                   'region': {'id': 'western-europe', 'name': 'Western Europe', 'slug': 'western-europe'},
                   'autonomous_territory': None, 'subdivision': None, 'nearby_country': None,
                   'country': {'id': 'FR', 'name': 'France', 'slug': 'france', 'code': 'FR'}},
          'location': {'lat': 48.845784, 'lon': 2.373606},
          'alternative_departure_points': [{'id': 'FR-PARI-PAR9', 'distance': 10.69, 'duration': 1151.3},
                                           {'id': 'FR-PARI-PAR2', 'distance': 13.23, 'duration': 1254.6},
                                           {'id': 'FR-PARI-PA11', 'distance': 1.41, 'duration': 179.5},
                                           {'id': 'XCR', 'distance': 151.93, 'duration': 8005.7},
                                           {'id': 'DOL', 'distance': 197.48, 'duration': 8185.3},
                                           {'id': 'ORY', 'distance': 20.05, 'duration': 1419.8},
                                           {'id': 'XJY', 'distance': 21.0, 'duration': 1428.3},
                                           {'id': 'LIL', 'distance': 214.18, 'duration': 8625.7},
                                           {'id': 'FR-PARI-PARI', 'distance': 2.25, 'duration': 272.7},
                                           {'id': 'TUF', 'distance': 236.54, 'duration': 9071.6},
                                           {'id': 'CFR', 'distance': 248.01, 'duration': 10087},
                                           {'id': 'CDG', 'distance': 27.81, 'duration': 1683.3},
                                           {'id': 'FR-PLAI-PARC', 'distance': 40.81, 'duration': 2155.4},
                                           {'id': 'FR-PARI-PA10', 'distance': 7.63, 'duration': 889.1},
                                           {'id': 'BVA', 'distance': 82.87, 'duration': 4315.2},
                                           {'id': 'FR-PARI-PAR3', 'distance': 9.29, 'duration': 962.9}], 'tags': [],
          'providers': [1035, 1064, 1128, 1148, 1171, 1179, 1229, 1283, 1291, 1329], 'special': [],
          'tourist_region': [{'id': 'ile-de-france_poi', 'name': 'Ile de France', 'slug': 'ile-de-france'},
                             {'id': 'greater-paris_poi', 'name': 'Greater Paris', 'slug': 'greater-paris'},
                             {'id': 'autoroute-utrecht-paris_poi', 'name': 'Autoroute Utrecht Paris',
                              'slug': 'autoroute-utrecht-paris'}], 'car_rentals': [], 'new_ground': False,
          'routing_priority': 1, 'type': 'station'},
         {'id': 'autoroute-paris-bordeaux-a10_poi', 'active': True, 'name': 'Autoroute Paris - Bordeaux (A10)',
          'code': 'autoroute-paris-bordeaux-a10_poi', 'slug': 'autoroute-paris-bordeaux-a10-',
          'slug_en': 'autoroute-paris-bordeaux-a10-', 'alternative_names': [], 'rank': 239, 'global_rank_dst': 2048,
          'category': None, 'type': 'tourist_region'},
         {'id': 'FR-PARI-PARI', 'int_id': 218, 'airport_int_id': None, 'active': True, 'code': 'FR-PARI-PARI',
          'icao': None, 'name': 'Paris - Bercy Seine', 'slug': 'paris-bercy-seine-paris-france',
          'slug_en': 'paris-bercy-seine-paris-france', 'alternative_names': [], 'rank': 546, 'global_rank_dst': 2048,
          'dst_popularity_score': 210.0, 'timezone': 'Europe/Paris',
          'city': {'id': 'paris_fr', 'name': 'Paris', 'code': 'PAR', 'slug': 'paris-france',
                   'continent': {'id': 'europe', 'name': 'Europe', 'slug': 'europe', 'code': 'EU'},
                   'region': {'id': 'western-europe', 'name': 'Western Europe', 'slug': 'western-europe'},
                   'autonomous_territory': None, 'subdivision': None, 'nearby_country': None,
                   'country': {'id': 'FR', 'name': 'France', 'slug': 'france', 'code': 'FR'}},
          'location': {'lat': 48.835318, 'lon': 2.380519},
          'alternative_departure_points': [{'id': 'FR-PARI-PARI', 'distance': 0.0, 'duration': 0},
                                           {'id': 'FR-PARI-PA11', 'distance': 1.16, 'duration': 184},
                                           {'id': 'FR-PARI-PAR9', 'distance': 12.55, 'duration': 1282},
                                           {'id': 'FR-PARI-PLA0', 'distance': 13.14, 'duration': 972},
                                           {'id': 'FR-PARI-PAR2', 'distance': 13.89, 'duration': 1321},
                                           {'id': 'FR-PARI-PAR6', 'distance': 14.41, 'duration': 1304},
                                           {'id': 'FR-CHAM-BUSS', 'distance': 14.77, 'duration': 1126},
                                           {'id': 'FR-PARI-AUST', 'distance': 1.62, 'duration': 230},
                                           {'id': 'FR-PARI-PAR1', 'distance': 1.71, 'duration': 217},
                                           {'id': 'FR-PARI-PA22', 'distance': 3.67, 'duration': 434},
                                           {'id': 'XHP', 'distance': 5.36, 'duration': 614},
                                           {'id': 'XGB', 'distance': 5.46, 'duration': 636},
                                           {'id': 'XPG', 'distance': 5.85, 'duration': 682},
                                           {'id': 'FR-PARI-PA19', 'distance': 7.32, 'duration': 820},
                                           {'id': 'FR-PARI-PA10', 'distance': 8.94, 'duration': 1034},
                                           {'id': 'FR-PARI-PAR3', 'distance': 9.97, 'duration': 1030}], 'tags': [],
          'providers': [1028, 1035, 1096, 1163, 1165, 1227, 1282, 1283, 1291], 'special': [],
          'tourist_region': [{'id': 'ile-de-france_poi', 'name': 'Ile de France', 'slug': 'ile-de-france'},
                             {'id': 'greater-paris_poi', 'name': 'Greater Paris', 'slug': 'greater-paris'},
                             {'id': 'autoroute-utrecht-paris_poi', 'name': 'Autoroute Utrecht Paris',
                              'slug': 'autoroute-utrecht-paris'}], 'car_rentals': [], 'new_ground': False,
          'routing_priority': 0, 'type': 'bus_station'}]
