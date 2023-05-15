import streamlit
streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Poha')
streamlit.text('🥣 Upma')
streamlit.text('🥣 Idli')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Apple','Peach'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
import requests
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response.json())

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)


import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

my_cnx1 = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur1 = my_cnx1.cursor()
my_cur1.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row1 = my_cur1.fetchall()
streamlit.header("The fruit load list contains :")
streamlit.dataframe(my_data_row1)

fruit_add = streamlit.text_input('What fruit would you like to add?','JackFruit')
streamlit.write('The user entered ', fruit_add)
sequence_of_parameters = [fruit_add]
my_cur1.executemany("insert into pc_rivery_db.public.fruit_load_list(fruit_name) select parse_json($1)[0]::varchar from values (%s)", [json.dumps(v) for v in sequence_of_parameters])

one_row = my_cur1.fetchone()
print("Opt: " + str(one_row[0]))


