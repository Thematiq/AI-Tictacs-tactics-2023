import streamlit as st
import pandas as pd
import altair as alt
import leafmap.foliumap as leafmap

from streamlit_echarts import st_echarts

# NUCLEAR
# https://pie.net.pl/elektrownie-jadrowe-zapewnia-polsce-prawie-40-proc-zapotrzebowania-na-energie-i-podniosa-pkb-o-ponad-1-proc/
REACTOR_TWH = 81 / 6

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

KG_TO_TON = 1e-3

# https://www.sciencedirect.com/science/article/pii/S0360544217303730
ENERGY_LOSS = (0.1 + 0.25) / 2

# TONS CO2
BASE_CO2_PER_YEAR = COMBUSTION_CARS * CO2_PER_KM * KM_PER_YEAR * KG_TO_TON

# AVERAGE PASSENGERS PER BUS
AVG_PASSENGERS = 1
# AVERAGE KM PER BUS
AVG_KM_BUS = 45
# AVERAGE CONSUMPTION
AVG_CONSUMPTION = (1790 + 2350) / 2
# AVERAGE_PEOPLE IN CAR
AVG_PEOPLE_IN_CAR = 1.5



def co2_map():
    st.markdown("### Emisja CO2 w Europie")
    st.markdown("Polskie elektrownie są w czołówce najbardziej emisyjnych elektrownii w Europie.")
    st.markdown(
        "Aż 70% energii w Polsce jest produkowanej w oparciu o węgiel kamiennny lub brunatny. Są to najbardziej emisyjne rodzaje pozyskiwania energii.")

    filepath = "./datasets/co2_emission_country.csv"
    m = leafmap.Map(center=[50, 20], zoom=4, tiles="stamentoner", max_zoom=5, min_zoom=3)
    m.add_heatmap(
        filepath,
        latitude="latitude",
        longitude="longitude",
        value="co2_emission_intensity",
        name="CO2 emission",
        radius=40,
    )
    m.to_streamlit(height=700)
    st.markdown("Źródło: Dane dla 2016r. z EEA Europe")


def mobility():
    st.markdown("Polacy są trzecim miejscu w liczbie posiadanych aut na osobę w Unii Europejskiej.")
    st.markdown("Auta elektryczne stanowią zaledwie **~0.32%** wszystkich samochodów w naszym kraju.")


emission_csv = pd.read_csv('datasets/co2-elektrownie.csv', encoding='latin2', sep=';')
production_csv = pd.read_csv('datasets/energia.csv', encoding='latin2', sep=';')
electric_car_csv = pd.read_csv('datasets/electric.csv')
country_emission = pd.read_csv('datasets/co2_emission_country.csv')

powerplant_co2 = \
emission_csv[(emission_csv['Rok'] == 2020) & (emission_csv['Wyszczególnienie'].str.contains('Region'))][
    'Emisja CO2 [t]'].sum()
production_gwh = float(production_csv[(production_csv['Parametr'] == 'RAZEM') & (production_csv['Rok'] == '2020') & (
            production_csv['Zmienna'] == 'Produkcja energii elektrycznej')] \
    ['Dane'].str.replace(',', '.').astype(float))
# Wh per km
electric_car_eff = electric_car_csv['Efficiency'].str.split(' ', 0).str[0].median()

WH_TO_GWH = 1e-9

# CO2 KG per GWH
CO2_PER_GWH = float(powerplant_co2 / production_gwh) * 1000

print(f'CO2 PER GWH {CO2_PER_GWH}')

CO2_PER_KM_ELECTRIC_CAR = CO2_PER_GWH * electric_car_eff * WH_TO_GWH * (1 / (1 - ENERGY_LOSS))

def car_slider() -> float:
    st.markdown("#### Kierowcy, którzy zmienili samochody spalinowe na elektryczne")
    st.markdown("Procentowy udział kierowców aut elektrycznych")
    return st.slider('s1', min_value=0, max_value=100, label_visibility="collapsed") / 100


def country_select() -> float:
    return float(country_emission[country_emission['country'] == \
                            st.selectbox('##### Użyj intensywności emisji kraju', country_emission['country'].unique())]['co2_emission_intensity'])


def bus_slider() -> float:
    st.markdown("#### Kierowcy, którzy korzystają z samochodów spalinowych oraz autobusów")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("##### Procent kierowców")
        bus_share = st.slider('s2',
                              min_value=0, max_value=100, label_visibility="collapsed") / 100
    with col2:
        st.markdown("##### Procentowy udział podróży autobusem")
        bus_pop = st.slider('s3',
                            min_value=0, max_value=100, label_visibility="collapsed") / 100
    return (bus_share * bus_pop)


def co2_kpi(old_co2, lost_co2, added_co2):
    new_co2 = old_co2 - lost_co2 + added_co2

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Spadek CO2 z samochodów spalinowych',
                  value=f'{lost_co2:,.0f} ton'.replace(',', ' '),
                  delta=f'{(lost_co2 / old_co2) * 100:.2f}%')
    with col2:
        st.metric('Wzrost CO2 z produkcji energii elektryczne',
                  value=f'{added_co2:,.0f} ton'.replace(',', ' '),
                  delta=f'{(added_co2 / old_co2) * 100:.2f}%',
                  delta_color="inverse")
    with col3:
        st.metric('Zmiana CO2',
                  value=f'{(added_co2 - lost_co2):,.0f} ton'.replace(',', ' '),
                  delta=f'{((new_co2 - old_co2) / old_co2) * 100:.2f}%',
                  delta_color="inverse")


def countries_bar_chart():
    chart = alt.Chart(country_emission).mark_bar().encode(
        x=alt.X('country:N', sort='y'),
        y='co2_emission_intensity:Q'
    )

    st.altair_chart(chart, use_container_width=True)


def gwh_par(gwh_changed, current_gwh):
    print(f'GWH change {gwh_changed}, production {current_gwh}')
    st.markdown(f'Do zasilenia tych samochodów będziemy musieli zwiększyć naszą '
                f'produkcję prądu o {gwh_changed / current_gwh * 100:.2f}%.')


def dashboard():
    st.set_page_config(layout="wide")

    st.title("Analiza emisji CO2 i mobilności w Polsce")
    co2_map()

    st.markdown("### Analiza stanu mobilności ")
    mobility()

    st.markdown("### Symulacja emisji CO2 w zależności od wykorzystywanych środków transportu")
    car_change = car_slider()
    # g CO2 / kWH == kg CO2 / MWH == t CO2 / GWH
    bus_change = bus_slider()
    co2_per_gwh = country_select()
    print(f'{co2_per_gwh}')
    print(f'{electric_car_eff}')
    co2_per_km_el = co2_per_gwh * electric_car_eff * WH_TO_GWH * (1 / (1 - ENERGY_LOSS))
    co2_per_km_bus = AVG_CONSUMPTION * co2_per_gwh * WH_TO_GWH * (1 / (1 - ENERGY_LOSS))

    print(f'CO2 fuel {CO2_PER_KM * KG_TO_TON} T/km')
    print(f'CO2 el {co2_per_km_el} T/km')
    print(f'CO2 bus {co2_per_km_bus} T/km')

    lost_co2 = COMBUSTION_CARS * (car_change + bus_change) * CO2_PER_KM * KM_PER_YEAR * KG_TO_TON

    added_gwh = COMBUSTION_CARS * car_change * electric_car_eff * WH_TO_GWH * (1 / (1 - ENERGY_LOSS)) * KM_PER_YEAR

    added_car_co2 = COMBUSTION_CARS * car_change * co2_per_km_el * KM_PER_YEAR
    added_bus_co2 = (COMBUSTION_CARS * bus_change / (AVG_PASSENGERS / AVG_PEOPLE_IN_CAR)) *\
                    AVG_KM_BUS * co2_per_km_bus

    added_co2 = added_car_co2 + added_bus_co2

    co2_kpi(BASE_CO2_PER_YEAR, lost_co2, added_co2)

    countries_bar_chart()

    gwh_par(added_gwh, production_gwh)

    print(f'Power plants CO2 {CO2_PER_GWH * production_gwh / 1000:,.0f}')
    print(f'Cars CO2 {BASE_CO2_PER_YEAR:,.0f}')


dashboard()
