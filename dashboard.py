import streamlit as st
import pandas as pd

# http://www.cepik.gov.pl/statystyki
CARS_IN_POLAND = 19_178_911
# https://serwisy.gazetaprawna.pl/transport/artykuly/8609065,samochody-elektryczne-w-polsce-raport.html
ELECTRIC_CARS = 62_135

COMBUSTION_CARS = CARS_IN_POLAND - ELECTRIC_CARS
# CO2 KG per KM
# https://www.acea.auto/figure/average-co2-emissions-from-new-passenger-cars-by-eu-country/
CO2_PER_KM = 0.1362
# Km per year per car
# https://mubi.pl/poradniki/sredni-roczny-przebieg-w-polsce-w-europie/
KM_PER_YEAR = 8607

KG_TO_TON = 0.001

# https://www.sciencedirect.com/science/article/pii/S0360544217303730
ENERGY_LOSS = (0.1 + 0.25) / 2

BASE_CO2_PER_YEAR = COMBUSTION_CARS * CO2_PER_KM * KM_PER_YEAR * KG_TO_TON


emission_csv = pd.read_csv('datasets/co2-elektrownie.csv', encoding='latin2', sep=';')
production_csv = pd.read_csv('datasets/energia.csv', encoding='latin2', sep=';')
electric_car_csv = pd.read_csv('datasets/electric.csv')

powerplant_co2 = emission_csv[(emission_csv['Rok'] == 2020) & (emission_csv['Wyszczególnienie'].str.contains('Region'))]['Emisja CO2 [t]'].sum()
production_gwh = production_csv[(production_csv['Parametr'] == 'RAZEM') & (production_csv['Rok'] == '2020') & (production_csv['Zmienna'] == 'Produkcja energii elektrycznej')]\
                ['Dane'].str.replace(',', '.').astype(float)
# Wh per km
electric_car_eff = electric_car_csv['Efficiency'].str.split(' ', 0).str[0].median()

WH_TO_GWH = 1e-9

# CO2 KG per GWH
CO2_PER_GWH = float(powerplant_co2 / production_gwh) * 1000

print(f'CO2 PER GWH {CO2_PER_GWH}')

CO2_PER_KM_ELECTRIC_CAR = CO2_PER_GWH * electric_car_eff * WH_TO_GWH * (1 / (1 - ENERGY_LOSS))


st.set_page_config(layout='wide')


def car_slider() -> float:
    return st.slider('Procent samochodów wymienionych na elektryczne', min_value=0, max_value=100) / 100


def bus_slider() -> float:
    col1, col2 = st.columns([1, 1])

    with col1:
        bus_share = st.slider('Procent samochodów korzystających z transportu publicznego',
                              min_value=0, max_value=100) / 100
    with col2:
        bus_pop = st.slider('Udział procentowy podróży autobusem w mobilności',
                            min_value=0, max_value=100) / 100
    return bus_share * bus_pop


def co2_kpi(old_co2, lost_co2, added_co2):
    new_co2 = old_co2 - lost_co2 + added_co2

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Spadek CO2 z samochodów spalinowych',
                  value=f'{lost_co2:,.0f} tons'.replace(',', ' '),
                  delta=f'{(lost_co2 / old_co2) * 100:.2f}%')
    with col2:
        st.metric('Wzrost CO2 z produkcji energii elektryczne',
                  value=f'{added_co2:,.0f} tons'.replace(',', ' '),
                  delta=f'{(added_co2 / old_co2) * 100:.2f}%')
    with col3:
        st.metric('Zmiana CO2',
                  value=f'{(added_co2 - lost_co2):,.0f} tons'.replace(',', ' '),
                  delta=f'{((new_co2 - old_co2) / old_co2)*100:.2f}%')


def dashboard():
    car_change = car_slider()
    bus_change = bus_slider()

    lost_co2 = COMBUSTION_CARS * (car_change + bus_change) * CO2_PER_KM * KM_PER_YEAR * KG_TO_TON
    added_car_co2 = COMBUSTION_CARS * car_change * CO2_PER_KM_ELECTRIC_CAR * KM_PER_YEAR * KG_TO_TON

    co2_kpi(BASE_CO2_PER_YEAR, lost_co2, added_car_co2)


dashboard()
