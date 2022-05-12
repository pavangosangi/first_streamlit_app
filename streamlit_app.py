import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title('My Mom\'s Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruits_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruits_list = my_fruits_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick Some Fruits: ", list(my_fruits_list.index))
fruits_to_show = my_fruits_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.title('Fruitvice Fruit Advice!')
fruit_choice = streamlit.text_input('What Fruit would you like information about?', 'kiwi')
streamlit.write('The User Entered', fruit_choice)
fruitvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
fruitvice_normalized = pd.json_normalize(fruitvice_response.json())
streamlit.dataframe(fruitvice_normalized)
