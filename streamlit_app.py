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

streamlit.header("View Our Fruit List - Add Your Favorites!")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruits List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
   
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('"+new_fruit+"')")
        return "Thanks for adding "+new_fruit

add_my_fruit = streamlit.text_input('What Fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
streamlit.stop()



