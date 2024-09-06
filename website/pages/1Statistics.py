import altair as alt
import math
import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
import random

st.title('How is your future going to look like :question:')
st.subheader('You might reconsider your answers after seeing this...')
data_original = pd.read_csv("ForecastFanatics_eval_submission.csv")
import json
data = data_original

# Add the sectors from sector.json
with open('sector.json', 'r') as file:
    sector_dict = json.load(file)
data.dropna(inplace=True, subset='idnum')
data['idnum'] = data['idnum'].astype(int)
data['sector'] = data['idnum'].apply(lambda x: sector_dict[str(x)] if str(x) in sector_dict else 0)

sector_names = {
    0: "no sector",
    15: "Food and Drinks",
    16: 'Tobacco',
    17: 'Textiles',
    18: 'Clothing', 
    19: 'Leather Goods', 
    20: 'Wooden Stuff',
    21: 'Paper Stuff', 
    22: 'Media', 
    23: 'Energy',
    24: 'Chemicals', 
    25: 'Rubber and Plastic Stuff', 
    26: 'Other Non Metallic Stuff',
    27: 'Basic Metals', 
    28: 'Some Metal Products', 
    29: 'Machinery and equipment',
    30: 'Office and Computer', 
    31: 'Electrical Machinery', 
    32: 'Communication Equipment',
    33: 'Precision Instruments', 
    34: 'Motor Vehicles', 
    35: 'Other Transport',
    36: 'Furniture',
}


average_vg_statebus = data.groupby(['sector'])['vg_statebus'].mean().to_frame()
average_vg_statebus['sector'] = average_vg_statebus.index
average_vg_statebus['sector_name'] = average_vg_statebus['sector'].map(sector_names)
#st.bar_chart(data=average_vg_statebus, x='idnum', y='vg_statebus')
barchart = alt.Chart(average_vg_statebus).mark_bar().encode(
    x=alt.X('sector_name', sort=alt.EncodingSortField('vg_statebus', order='ascending'), 
            axis = alt.Axis(title="Sectors")),
    y=alt.Y('vg_statebus', axis=alt.Axis(title="Current State of Business"))
).properties(
    title=alt.TitleParams(text='Average subjective state of business forecasted for 2022', 
                          subtitle='(less is better)'),
    height = 500
)


st.altair_chart(barchart, use_container_width=True)

average_vg_priceexp = data.groupby(['sector'])['vg_priceexp'].mean().to_frame()
average_vg_priceexp['sector'] = average_vg_priceexp.index
average_vg_priceexp['sector_name'] = average_vg_priceexp['sector'].map(sector_names)
piechart = alt.Chart(average_vg_priceexp).mark_arc().encode(
    theta='vg_priceexp',
    color='sector_name',
    tooltip='sector_name'
).properties(
    title=alt.TitleParams(text='Expected domestic price in 2022',
                          subtitle=('less is higher!'))
)

st.subheader('These values might look similar, but look closely to see whose prices will really be up there :money_with_wings:')
st.altair_chart(piechart, use_container_width=True)