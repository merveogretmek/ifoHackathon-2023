import altair as alt
import math
import pandas as pd
import streamlit as st
from PIL import Image

"""
# Which German Business Sector are you?

Take this personality quiz to find out which part of the Volkswirtschaft is your spirit animal.

This uses clustering from the ifo Business Climate Survey taken by thousands of businesses monthly to determine which sector you're responses are most similar to.
Are you the high-tech industry embodied or heavy industry personified? People have chosen careers over less.
"""
#st.set_page_config(page_title='Which Business Sector are you?', page_icon=':heart:')
# QUESTION 1
st.title('How was lunch?')
vg_statebus = st.radio(
"We evaluate our state of business to be",
('Good', 'Satisfiable', 'Bad'))
if vg_statebus == 'Good':
    vg_statebus_index = 1
if vg_statebus == 'Satisfiable':
    vg_statebus_index = 2
    st.text('7/10')
if vg_statebus == 'Bad':
    vg_statebus_index = 3
    st.text('Ooof')

#vg_statebus = give_choice(['Good', 'Satisfiable', 'Bad'])




# QUESTION 2
st.title('How oldschool are you?')
online = st.radio(
    "I would filled out the ifo survey via",
    ("Paper", "Fax", "Online", "Manual collection"))

#assign integers to answers as in ifo survey
if online == 'Paper':
    online_index = 0
if online == 'Fax':
    online_index =  1
    st.text('They said in the Buzzfeed survey')
if online == 'Online' :
    online_index = 2
    st.text('THANK YOU; FINALLY A NORMAL PERSON')
if online == 'Manual collection':
    online_index = 5
    st.text('Fighting unemployment one special request at a time')


# QUESTION 3
st.title('U scared yet?')
vg_comexp = st.radio(
"During the next 6 months our business operation will be",
('Favourable', 'Not changing', 'Unfavourable'))
#assign integers to answers as in ifo survey
if vg_comexp == 'Favourable':
    vg_comexp_index = 1
if vg_comexp == 'Not changing':
    vg_comexp_index = 2
    st.text('Dream on')
if vg_comexp == 'Unfavourable':
    vg_comexp_index = 3
    st.text('You betcha')


# QUESTION 4
st.title('When did you first become important enough that ifo would care about you?')
age = st.radio(
"",
('Before 1980', 'Before 2000', 'After 2000'))
if age == 'Before 1980':
    age_index=0
if age == 'Before 2000':
    age_index=1
    st.text('TikTok is werid, right?')
if age == 'After 2000':
    image = Image.open('images/lindner.webp')
    st.image(image, width = 300)
    age_index=2


# QUESTION 5
st.title('How greedy are you?')
vg_price = st.radio(
"Our prices in the next 3 months will expectedly be",
('Rising', 'Not changing', 'Falling'))
if vg_price == 'Rising':
    vg_price_index = 1
if vg_price == 'Not changing':
    vg_price_index = 2
    st.text('In this economy?')
if vg_price == 'Falling':
    vg_price_index = 3
    st.text('The unwashed masses thank you')

# QUESTION 6
st.title('Are you hot or not?')
vg_demand_vpq = st.radio(
"In the last 3 months the demand situation has been",
('Rising', 'Not changing', 'Falling'))
if vg_demand_vpq == 'Rising':
    vg_price_index = 1
if vg_demand_vpq == 'Not changing':
    vg_price_index = 2
    st.text('You got it guuurl!')
if vg_demand_vpq == 'Falling':
    vg_price_index = 3
    st.text('We will always love you.')

# QUESTION 7
st.title('Labour exploitation attitudes')
vg_demand_vpq = st.radio(
"The number of your employees will be",
('Increasing', 'Not changing', 'Decreasing'))
if vg_demand_vpq == 'Increasing':
    vg_price_index = 1
if vg_demand_vpq == 'Not changing':
    st.text('Coward.')
    vg_price_index = 2
if vg_demand_vpq == 'Decreasing':
    vg_price_index = 3
    st.text('Our condolences.')

data = pd.read_csv("average_answers_by_sector.csv",engine='python')

# Form responses as in the same format as the ifo survey
our_responses = {'vg_statebus': vg_statebus_index, 
                'vg_comexp': vg_comexp_index,
                'vg_priceexp': vg_price_index,
                'is_fax': online_index == 1, # Should be 1 if the respondent answered by fax
                'is_online': online_index == 2, # Should be 1 if the respondent answered online
                'is_neither_online_fax': online_index != 1 and online_index != 2, # Otherwise
                'vg_demand_vpq':vg_price_index,
                'vg_emplexp': 1,
                'year_binned': age_index # AKA age_index 0 if before 1980, 1 if before 2000, 2 otherwise
               }

# This gets the row with the smallest L1 distance to our_responses in the dataframe.
# It output is min_distance_sector wz93 sector code

data['sector'] = data['sector'].replace('0.', '0')
data['sector'] = data['sector'].replace('na', '0')
data['sector'] = data['sector'].astype(int)

#create sector names and assigning them to the variable
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

data['sector_name'] = data['sector'].map(sector_names)

min_distance_sector = None
min_distance = 1000
for index, row in data.iterrows():
    distance = 0
    for key, value in our_responses.items():
        distance += abs(value - row[key])
    if distance < min_distance and row['sector'] != 0:
        min_distance = distance
        min_distance_sector = row['sector']

show_checkbox = st.checkbox('Show result')

if show_checkbox:
    st.title("Sector number " + str(min_distance_sector) + ": " + sector_names[min_distance_sector])
    if min_distance_sector == 15:
        im_path = '1.jpeg'
    elif min_distance_sector == 16:
        im_path = 'pipe.jpeg'
    elif min_distance_sector == 17:
        im_path = 'clothes.jpeg'
    elif min_distance_sector == 18:
        im_path = 'clothes.jpeg'
    elif min_distance_sector == 19:
        im_path = 'leather.jpeg'
    elif min_distance_sector == 21:
        im_path = 'forest.jpeg'
    elif min_distance_sector == 22:
        im_path = 'propaganda.jpeg'
    elif min_distance_sector == 23:
        im_path = 'nukes.jpeg'
    elif min_distance_sector == 24:
        im_path = 'oil.jpeg'
    elif min_distance_sector == 25:
        im_path = 'oil.jpeg'
    elif min_distance_sector == 26:
        im_path = 'mine.jpeg'
    elif min_distance_sector == 28:
        im_path = 'machines.jpeg'
    elif min_distance_sector == 29:
        im_path = 'machines.jpeg'
    elif min_distance_sector == 30:
        im_path = 'nerd.jpeg'
    elif min_distance_sector == 31:
        im_path = 'satelite.jpeg'
    elif min_distance_sector == 32:
        im_path = 'satelite.jpeg'
    elif min_distance_sector == 33:
        im_path = 'machines.jpeg'
    elif min_distance_sector == 34:
        im_path = 'transrapid.jpeg'
    elif min_distance_sector == 35:
        im_path = 'transrapid.jpeg'
    elif min_distance_sector == 36:
        im_path = 'furniture.jpeg'
    else:
        im_path=''
    if len(im_path) > 0:
        image = Image.open("images/"+im_path)
        st.image(image, width = 600)
