# Import required packages
import streamlit as st
from snowflake.snowpark.functions import col

# App Title
st.title("🥤 Customize Your Smoothie")
st.write("Create your own smoothie by selecting up to 5 ingredients!")

# Smoothie name input
title = st.text_input("Name your smoothie")
if title:
    st.write(f"Smoothie name: **{title}**")

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch available fruit options
fruit_table = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
fruit_df = fruit_table.to_pandas()
fruit_list = fruit_df["FRUIT_NAME"].tolist()

# Show fruit options and allow selection
selected_ingredients = st.multiselect(
    "Choose up to 5 ingredients",
    options=fruit_list,
    max_selections=5
)

# If ingredients are selected
if selected_ingredients and title:
    ingredients_string = ', '.join(selected_ingredients)
    st.write(f"📝 Ingredients selected: **{ingredients_string}**")

    # Create SQL INSERT statement
    insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{title}')
    """

    # Submit button
    if st.button("✅ Submit Order"):
        session.sql(insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
elif selected_ingredients and not title:
    st.warning("Please provide a name for your smoothie before submitting.")
