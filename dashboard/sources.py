import sys
import time
import json
import math
import logging

from collections import defaultdict
from datetime import datetime

import COVID19Py

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class Covid19Data:
    def __init__(self):
        self.total = defaultdict(lambda: defaultdict(int))

        self._last_time_updated = 0
        self._update_every = 600
        self.covid19 = COVID19Py.COVID19(url='http://api:8051')

        self.refresh_data()

        self.population_map = {
            x['country']: x['population']
            for x in json.load(open('country-by-population.json'))
        }
        self.country_country_code_map = {
            x['abbreviation']: x['country']
            for x in json.load(open('country-by-abbreviation.json'))
        }
    
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
        last_time_updated = time.time() - self._last_time_updated

        if last_time_updated > self._update_every:
            log.debug('=====> LAST UPDATED %s seconds ago. Checking again...', last_time_updated)
            self.latest = self.covid19.getLatest()
            self.locations = self.covid19.getLocations(timelines=True)

            self._last_time_updated = time.time()

            self.process_data()
        else:
            log.debug('-----> LAST UPDATED %s seconds ago. Using cache...', last_time_updated)

    def get_dates(self):
        self.refresh_data()

        return self.dates

    def get_history_data(self, countries, _type, start, end):
        self.refresh_data()

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
                            country_total[location['country_code']][date][key + '_new'] += today - yesterday

        return country_total

    def get_rate_by_countries(self, countries, _type):
        self.refresh_data()

        data = []
        for country in countries:
            population = int(self.population_map[self.country_country_code_map[country]])
            # rate_per_mil = math.floor(1000000 / population *  self.total[country][_type])
            rate_per_mil = self.calculate_rate(country, self.total[country][_type])
            data.append({'country': country, 'rate': rate_per_mil})

        data = sorted(data, key=lambda x: x['rate'])
        return data

    def calculate_rate(self, country_code, total,  per=1000000):
        population = int(self.population_map[self.country_country_code_map[country_code]])
        return math.floor(per / population *  total)
