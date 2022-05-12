import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(fruit_choice):
    fruitvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    return pd.json_normalize(fruitvice_response.json())
    
streamlit.title('Fruitvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What Fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select current_user(), current_account(),current_region()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from snowflake:")
streamlit.text(my_data_row)

add_fruit_name = streamlit.text_input('What Fruit would you like to add?')
streamlit.write('Thanks for adding ', add_fruit_name)
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('from streamlit')")
