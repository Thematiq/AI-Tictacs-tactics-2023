import streamlit as st
import pandas as pd
import altair as alt
import leafmap.foliumap as leafmap

from streamlit_echarts import st_echarts

# http://www.cepik.gov.pl/statystyki
CARS_IN_POLAND = 19_178_911
# https://serwisy.gazetaprawna.pl/transport/artykuly/8609065,samochody-elektryczne-w-polsce-raport.html
ELECTRIC_CARS = 62_135
# https://www.macrotrends.net/countries/POL/poland/population
POLAND_POPULATION = 32_413_700 # over 18

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
country_emission = pd.read_csv('datasets/co2_emission_country.csv')

powerplant_co2 = \
emission_csv[(emission_csv['Rok'] == 2020) & (emission_csv['Wyszczególnienie'].str.contains('Region'))][
    'Emisja CO2 [t]'].sum()
production_gwh = production_csv[(production_csv['Parametr'] == 'RAZEM') & (production_csv['Rok'] == '2020') & (
            production_csv['Zmienna'] == 'Produkcja energii elektrycznej')] \
    ['Dane'].str.replace(',', '.').astype(float)
# Wh per km
electric_car_eff = electric_car_csv['Efficiency'].str.split(' ', 0).str[0].median()

WH_TO_GWH = 1e-9

# CO2 KG per GWH
CO2_PER_GWH = float(powerplant_co2 / production_gwh) * 1000

print(f'CO2 PER GWH {CO2_PER_GWH}')

CO2_PER_KM_ELECTRIC_CAR = CO2_PER_GWH * electric_car_eff * WH_TO_GWH * (1 / (1 - ENERGY_LOSS))

def co2_map():
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown("### Emisja CO2 w Europie")
        st.markdown("Polskie elektrownie są w czołówce najbardziej emisyjnych elektrownii w Europie.")
        st.markdown(
            "Aż 70% energii w Polsce jest produkowanej w oparciu o węgiel kamiennny lub brunatny. Są to najbardziej emisyjne sposoby pozyskiwania energii.")

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
    
    with col2:
        st.markdown("##")
        st.markdown("##")
        st.markdown("##")
        st.markdown("##")
        st.markdown("Emisja CO2 w przeliczeniu na kWh")
        countries_bar_chart()


def mobility():
    col1, col2 = st.columns([1, 4])

    with col1:
        cars_per_capita = f'<div style="font-family:sans-serif; display: flex; flex-direction:column; justify-content: center; align-items:center"><p style="color:FireBrick; font-size: 42px;">{round(CARS_IN_POLAND / POLAND_POPULATION, 3)}</p><p>samochodów na dorosłą osobę</p></div>'
        st.markdown(cars_per_capita, unsafe_allow_html=True)
        st.markdown("##")
        st.markdown("##")

        electric_percent = ELECTRIC_CARS * 100 / CARS_IN_POLAND 
        electric = f'<div style="font-family:sans-serif; display: flex; flex-direction:column; justify-content: center; align-items:center"><p style="color:FireBrick; font-size: 42px;">{round(electric_percent, 3)}%</p><p>udział samochodów elektrycznych</p></div>'
        st.markdown(electric, unsafe_allow_html=True)
        st.markdown("##")
        st.markdown("##")
       

    with col2:
        st.markdown("##")
        st.markdown("Polacy są trzecim miejscu w liczbie posiadanych aut na osobę w Unii Europejskiej.")

        st.markdown("##")
        st.markdown("##")
        st.markdown("##")
        st.markdown("##")
        st.markdown("Auta elektryczne stanowią zaledwie **~0.324%** wszystkich samochodów w naszym kraju.")

def analysis_desc():
    st.markdown("Celem naszej analizy było sprawdzenie jaki wpływ na emisję dwutlenku węgla, miałaby zmiana samochodów spalinowych na samochody elektryczne lub transport publiczny")
    st.markdown("Na potrzeby stworzenia modelu, przyjeliśmy następujące założenia:")
    st.markdown("- Zmiana udziału samochodów spalinowych na rzecz innych środków komunikacji następuje natychmiastowo.")
    st.markdown("- W momencie zmiany produkcja prądu (oraz jej koszty) rosną, na tyle, aby pokryć zapotrzebowanie.")
    st.markdown("- Nie uwzględniamy kosztów produkcji pojazdów.")
    st.markdown("- Przyjmujemy, że samochody spalinowe mają jednakowy poziom emisji oraz jednakowy średni roczny przebieg, będące średnimi wartościami.")
    st.markdown("- Przyjmujemy, że samochody elektryczne mają jednakowy poziom zużycia prądu oraz jednakowy średni roczny przebieg, będące średnimi wartościami.")


def variants():
    st.markdown("Opracowaliśmy i przeanalizowaliśmy 5 scenariuszy:")
    st.markdown("- **Wariant 1**: X% kierowców wymienia samochód spalinowy na samochód elektryczny. Miks energetyczny pozostaje bez zmian.")
    st.markdown("- **Wariant 2**: to samo co wariant 1, ale zakładamy wzrost udziału OZE przy produkcji potrzebnej energii.")
    st.markdown("- **Wariant 3**: X% kierowców w Y% sytuacji wybiera podróż autobusem zamiast samochodem spalinowym. Miks energetyczny pozostaje bez zmian.")
    st.markdown("- **Wariant 4**: X% kierowców w Y% sytuacji wybiera podróż autobusem zamiast samochodem spalinowym, a Z% kierowców wymiania samochód na elektryczny. Miks energetyczny pozostaje bez zmian.")    
    st.markdown("- **Wariant 5**: X% kierowców w Y% sytuacji wybiera podróż autobusem zamiast samochodem spalinowym, a Z% kierowców wymiania samochód na elektryczny. Zakładamy wzrost udziału OZE przy produkcji potrzebnej energii")
    st.markdown("- **Wariant 6**: Przeprowadziliśmy symulacje przyjmując miks energetyczny z innego kraju")

def car_slider() -> float:
    st.markdown("#### Kierowcy, którzy zmienili samochody spalinowe na elektryczne")
    st.markdown("Procentowy udział kierowców aut elektrycznych")
    return st.slider('s1', min_value=0, max_value=100, label_visibility="collapsed") / 100


def country_select() -> float:
    st.markdown("#### Miks energetyczny z kraju:")
    return float(country_emission[country_emission['country'] == \
                            st.selectbox('##### Użyj intensywności emisji kraju', country_emission['country'].unique(), index=20)]['co2_emission_intensity']) * 1000


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
    return bus_share * bus_pop


def co2_kpi(old_co2, lost_co2, added_co2):
    new_co2 = old_co2 - lost_co2 + added_co2

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Emisja CO2 z samochodów spalinowych',
                  value=f'{lost_co2:,.0f} ton'.replace(',', ' '),
                  delta=f'{(lost_co2 / old_co2) * 100:.2f}%')
    with col2:
        st.metric('Emisja CO2 z produkcji energii elektrycznej',
                  value=f'{added_co2:,.0f} ton'.replace(',', ' '),
                  delta=f'{(added_co2 / old_co2) * 100:.2f}%')
    with col3:
        st.metric('Zmiana CO2',
                  value=f'{(added_co2 - lost_co2):,.0f} ton'.replace(',', ' '),
                  delta=f'{((new_co2 - old_co2) / old_co2) * 100:.2f}%',
                  delta_color="inverse")


def countries_bar_chart():
    chart = alt.Chart(country_emission).mark_bar().encode(
        y=alt.Y('country:N', sort='x', title='Kraj'),
        x=alt.X('co2_emission_intensity:Q', title='Emisja CO2 [g CO2/kWh]'),
        color="country:N",
        tooltip=[
                alt.Tooltip("country:N", title="Kraj"),
                alt.Tooltip("co2_emission_intensity:Q", title="Emisja CO2"),
            ],

    ).interactive()

    st.altair_chart(chart, use_container_width=True)


def dashboard():
    st.set_page_config(layout="wide")

    st.title("Analiza emisji CO2 i mobilności w Polsce")
    co2_map()

    st.markdown("### Analiza stanu mobilności ")
    mobility()

    st.markdown("### Symulacja emisji CO2 w zależności od wykorzystywanych środków transportu")
    analysis_desc()
    car_change = car_slider()
    bus_change = bus_slider()
    co2_per_gwh = country_select()
    co2_per_km_el = co2_per_gwh * electric_car_eff * WH_TO_GWH * (1 / (1 - ENERGY_LOSS))

    lost_co2 = COMBUSTION_CARS * (car_change + bus_change) * CO2_PER_KM * KM_PER_YEAR * KG_TO_TON
    added_car_co2 = COMBUSTION_CARS * car_change * co2_per_km_el * KM_PER_YEAR * KG_TO_TON
    added_bus_co2 = 0
    added_co2 = added_car_co2 + added_bus_co2

    co2_kpi(BASE_CO2_PER_YEAR, lost_co2, added_co2)

    st.markdown("### Analiza scenariuszy")
    variants()



dashboard()
