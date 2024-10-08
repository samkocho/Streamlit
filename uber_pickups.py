import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')


# Let's start by writing a function to load the data. 

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
# Allow caching data so that the data loading proces doesn't take too long
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # the nrows parameter tells pandas to only load the first nrows rows of data.
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data




# Now let's test the function and review the output. 

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')
data_load_state.text("Done! (using st.cache_data)")



# st.subheader('Raw data')
# st.subheader('Number of pickups by hour')
# st.write(data)
# Use a button to toggle data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

#Histogram
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

#Map
# st.subheader('Map of all pickups')
# st.map(data)

#Map for the busiest hour:
# hour_to_filter = 17
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h #Filter results with a SLIDER

filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)