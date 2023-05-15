import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Poha')
streamlit.text('🥣 Upma')
streamlit.text('🥣 Idli')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Apple','Peach'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
def get_fruityvice_data(this_fruit_choise):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choise)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

 #import requests
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)  
except URLError as e:
  streamlit.error()
#streamlit.stop()
streamlit.header("The fruit load list contains :")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()
    
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    streamlit.dataframe(my_data_row)

streamlit.stop()   

def insert_row_snowflake(new_fruit):
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list(fruit_name) values ('from streamlit') ")
    return "Thanks for adding new fruit " + new_fruit

fruit_add = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add New Fruit'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(fruit_add)
    streamlit.text(back_from_function)
    
#fruit_add = streamlit.text_input('What fruit would you like to add?','JackFruit')
#streamlit.write('Thanks for adding ', fruit_add)
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list(fruit_name) values ('from streamlit') ")


