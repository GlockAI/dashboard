import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header('Dashboard Laboratorio 2') 

st.sidebar.subheader('Heat map parameter')
time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

st.sidebar.subheader('Donut chart parameter')
donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

st.sidebar.subheader('Line chart parameters')
plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.sidebar.markdown('''
---
Universidad Autónoma de Chile.
''')

# Primera fila
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Cargar datos
seattle_weather = pd.read_csv('seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('stocks_toy.csv')

# Segunda Fila
c1, c2 = st.columns((7,3))

with c1:
    st.markdown('### Heatmap')
    pivot = seattle_weather.pivot_table(
        index=seattle_weather['date'].dt.weekday,
        columns=seattle_weather['date'].dt.isocalendar().week,  # esta es la forma correcta
        values=time_hist_color,
        aggfunc='median'
    )
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(pivot, cmap='coolwarm', ax=ax)
    ax.set_ylabel('Day of Week')
    ax.set_xlabel('Week of Year')
    st.pyplot(fig)

with c2:
    st.markdown('### Donut chart')
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(stocks[donut_theta], labels=stocks['company'], autopct='%1.1f%%', startangle=90)
    plt.setp(autotexts, size=10, weight="bold")
    ax.axis('equal')
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    st.pyplot(fig)

# Tercera Fila
st.markdown('### Line chart')
fig, ax = plt.subplots(figsize=(10, plot_height/100))
sns.lineplot(data=seattle_weather, x='date', y=plot_data[0], label=plot_data[0])
if len(plot_data) > 1:
    sns.lineplot(data=seattle_weather, x='date', y=plot_data[1], label=plot_data[1])
ax.set_ylabel('Temperature')
st.pyplot(fig)
