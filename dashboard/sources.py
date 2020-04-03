from collections import defaultdict
from datetime import datetime

import COVID19Py


class Covid19Data:
    def __init__(self):
        self.total = defaultdict(lambda: defaultdict(int))

        self.covid19 = COVID19Py.COVID19()

        self.refresh_data()
    
    def process_data(self):
        self.countries_map = {}
        self.locations_map = {x['country_code']:x for x in self.locations}

        for location in self.locations:
            self.countries_map[location['country_code']] = location['country']

            self.total[location['country_code']]['confirmed'] += location['latest']['confirmed']
            self.total[location['country_code']]['deaths'] += location['latest']['deaths']
            self.total[location['country_code']]['recovered'] += location['latest']['recovered']
        
        self.latest_total = sorted(self.total.items(), key=lambda x: x[1]['confirmed'])
        self.latest_top = self.latest_total[-20:]

        self.dates = list(self.locations_map['US']['timelines']['confirmed']['timeline'].keys())


    def refresh_data(self):
        self.latest = self.covid19.getLatest()
        self.locations = self.covid19.getLocations(timelines=True)

        self.process_data()
    
    def get_history_data(self, countries, _type, start, end):
        country_total = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for country in countries:
            # country_locations = covid19.getLocationByCountryCode(country, timelines=True)
            country_locations = [x for x in self.locations if x['country_code'] == country]

            for location in country_locations:
                for key, timeline in location['timelines'].items():
                    items = list(timeline['timeline'].items())
                    # for date, cnt in items[start:end]:
                    for i, (date, cnt) in enumerate(items[start:end], start=start):
                        country_total[location['country_code']][date][key] += cnt
                        
                        if i > 0:
                            today = cnt
                            yesterday = items[i - 1][1]
                            
                            # print('----->', items[i - 1][0], yesterday, date, today, today - yesterday)

                            country_total[location['country_code']][date][key + '_new'] += today - yesterday



            from pprint import pprint
            pprint('<=====')
            pprint(country_total[country].items())
            pprint('=====>')
        return country_total
