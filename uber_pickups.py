import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('pk nyc')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis = 'columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


n_to_load = st.slider('How much data do you want?', 1, 100000)

data_load_state = st.text('Loading data...')
data = load_data(n_to_load)
st.write('DONE !!! (using st.cache)')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

x = st.slider('Select a value')
st.write(x, 'carré = ', x**2)
# st.write(x, 'squared is', x * x)
#
st.subheader('Map of all pickups')
st.map(data)
hour_to_filter = 17
st.write(f'{hour_to_filter}:00')
filtered_data = data[data[DATE_COLUMN].dt.hour == 17]

latitude = st.slider('LATIUDE', 40.5, 41.0)
st.subheader(f'Map of all pickups above latitude: {latitude}')
st.map(data[data['lat']>= latitude])

st.subheader('Map of all pickups at 16h')
st.map(data[data[DATE_COLUMN].dt.hour == 16])


hour = st.slider('Hour', 0, 23)
st.subheader('Map of all pickups at %s o\'clock' % hour)
st.map(data[data[DATE_COLUMN].dt.hour == hour])

st.write(x*3-2*x**2)

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'