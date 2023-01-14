import streamlit as st
import pandas as pd

# http://www.cepik.gov.pl/statystyki
CARS_IN_POLAND = 19_178_911
# https://serwisy.gazetaprawna.pl/transport/artykuly/8609065,samochody-elektryczne-w-polsce-raport.html
ELECTRIC_CARS = 62_135

COMBUSTION_CARS = CARS_IN_POLAND - ELECTRIC_CARS
# CO2 per KM
CO2_PER_KM = 0.1362
# Km per year per car
KM_PER_YEAR = 8607

KG_TO_TON = 0.001


BASE_CO2_PER_YEAR = COMBUSTION_CARS * CO2_PER_KM * KM_PER_YEAR * KG_TO_TON


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
                  value=f'{(lost_co2 - added_co2):,.0f} tons'.replace(',', ' '),
                  delta=f'{((old_co2 - new_co2) / old_co2)*100:.2f}%')


def dashboard():
    car_change = car_slider()
    bus_change = bus_slider()

    lost_co2 = COMBUSTION_CARS * (car_change + bus_change) * CO2_PER_KM * KM_PER_YEAR * KG_TO_TON

    co2_kpi(BASE_CO2_PER_YEAR, lost_co2, 0)




dashboard()
