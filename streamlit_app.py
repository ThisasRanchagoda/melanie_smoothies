# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col,when_matched



# Write directly to the app
st.title(f" Customize your smoothie :cup_with_straw:")
st.write(
  """create your own smoothie
  """
)

import streamlit as st

title = st.text_input("Name of your smoothie")
st.write("The name of your smoothie is", title)



from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'choose upto 5 ingredients',
    
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    
    ingredients_string = ''
    name_on_order=title

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""

    st.write(my_insert_stmt)
    
    time_to_insert = st.button('submit order')


    if time_to_insert:
         session.sql(my_insert_stmt).collect()
         st.success('Your Smoothie is ordered!', icon="✅")


