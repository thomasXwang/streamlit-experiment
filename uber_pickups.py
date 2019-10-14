import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

rows_data = st.slider('Combien de data voulez-vous voir?', 1000, 20000)

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(rows_data)
data_load_state.text('Loading data... done!')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

lat_min = data['lat'].min()
lat_max = data['lat'].max()
st.write('Latitudes : \[', lat_min, ', ', lat_max, '\]')

latitude_filter = st.slider('Latitude minimale', lat_min, lat_max)
st.subheader('Map of pickups above latitude %s' % latitude_filter)
st.write(data[data['lat'] >= latitude_filter])
st.map(data[data['lat'] >= latitude_filter])