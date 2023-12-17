import streamlit as st
import pickle
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from content_based_recommendations import content_based_recommendations
from item_based_recommendations import item_based_recommendations
from kcgn_recommendations import kcgn_recommendations

#Load data

with open("demo_data/ratings.pkl", "rb") as fs:
  data = pickle.load(fs)
with open("demo_data/category.pkl", "rb") as fs:
  category = pickle.load(fs)
with open("demo_data/times.pkl", "rb") as fs:
  times = pickle.load(fs)
with open("demo_data/trust.pkl", "rb") as fs:
  trust = pickle.load(fs)

user = pd.read_csv("demo_data/user_detail.csv")
rest = pd.read_csv("demo_data/rest_detail.csv")

with open("demo_data/test_data.pkl", 'rb') as fs:
  test = pickle.load(fs)
with open("demo_data/mappingUser.pkl", 'rb') as fs:
  mapping_user = pickle.load(fs)
with open("demo_data/mappingItem.pkl", 'rb') as fs:
  mapping_item = pickle.load(fs)

with open("demo_data/recommendations.pkl", 'rb') as fs:
  recommendations = pickle.load(fs)

#Get Functions
def get_user_name(id):
  return user[user.user_id == id].name.values[0]
def get_user_review_count(id):
  return user[user.user_id == id].review_count.values[0]
def get_user_average_stars(id):
  return user[user.user_id == id].average_stars.values[0]

def get_rest_name(id):
  return rest[rest.business_id == id].name.values[0]
def get_rest_category(id):
  return rest[rest.business_id == id].category.values[0]
def get_rest_city(id):
  return rest[rest.business_id == id].city.values[0]
def get_rest_review_count(id):
  return rest[rest.business_id == id].review_count.values[0]
def get_rest_stars(id):
  return rest[rest.business_id == id].stars.values[0]

def Get_Id_of_User_List(userid_list):
  return [mapping_user.get(key) for key in userid_list]
def Get_Id_of_Item_List(itemid_list):
  return [mapping_item.get(key) for key in itemid_list]
def Get_Id_of_User(userid):
  return mapping_user.get(userid)
def Get_Id_of_Item(itemid):
  return mapping_item.get(itemid)
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
def Get_Id_List_by_UserId(user_id):
  user_index = get_key(mapping_user, user_id)
  test_item_id = Get_Id_of_Item_List(test_group.get(user_index))
  return test_item_id

#Processing test dataframe
test = pd.DataFrame(test, columns=['id','rec_id'])

user_id = test.id.unique()
rest_id = test.rec_id.unique()

test_user_id = Get_Id_of_User_List(user_id)
test_item_id = Get_Id_of_Item_List(rest_id)

category = category.loc[(category.index.isin(test_item_id)),:]
data = data.loc[(data.index.isin(test_user_id)),(data.columns.isin(test_item_id))]

test_group = test.groupby(['id'])['rec_id'].apply(list).to_dict()

#Recommendation System

st.title("""
:rainbow[Restaurant Recommendation System]
""")

selected = option_menu(None, ["Home", "Content-based", "Collaborative", 'Model-based'],
    icons=['house', 'shop', "bi bi-people-fill", 'bezier'],
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected == "Home":
  st.header('Welcome to my Demo', divider='rainbow')
  st.image("demo_data/input.png")
if selected == "Content-based":
  st.sidebar.header(f"You selected {selected}", divider='rainbow')
  selected_user = st.sidebar.selectbox('Select a user to recommend',data.index.values)
  st.sidebar.title("User detail")
  st.sidebar.write("*User_id*: ", selected_user)
  st.sidebar.write("*User_name*: ", get_user_name(selected_user))
  st.sidebar.write("*User_review_count*: ", get_user_review_count(selected_user))
  st.sidebar.write("*User_average_stars*: ", get_user_average_stars(selected_user))
  st.sidebar.title("Recommendation options")
  selected_k = st.sidebar.selectbox('Select top k restaurant you want to recommend',range(1,10), index=None, placeholder="Select top ...")
  st.sidebar.write('You selected:', selected_k)

  with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
      pass
    with col3:
      pass
    with col2 :
      center_button = st.button('Get')

  if center_button:
    recommendation = content_based_recommendations(category, rest, mapping_item, mapping_user,test_group, selected_user, data.loc[selected_user, Get_Id_List_by_UserId(selected_user)].idxmax(), selected_k)
    recommendation = pd.DataFrame(recommendation)
    recommendation.columns = ['Rest_id', "Name", "Category", "City", "Stars", "Review_count"]
    st.markdown("""
    <style>
    dataframe {background-color: #CCFFCC;}
    </style>
    """, unsafe_allow_html=True)
    st.dataframe(
      recommendation,
      column_config={
        "Stars": st.column_config.NumberColumn(
            format="%.1f ⭐",
        )
    })

if selected == "Collaborative":
  st.sidebar.header(f"You selected {selected}", divider='rainbow')
  selected_user = st.sidebar.selectbox('Select a user to recommend',data.index.values)
  st.sidebar.title("User detail")
  st.sidebar.write("*User_id*: ", selected_user)
  st.sidebar.write("*User_name*: ", get_user_name(selected_user))
  st.sidebar.write("*User_review_count*: ", get_user_review_count(selected_user))
  st.sidebar.write("*User_average_stars*: ", get_user_average_stars(selected_user))
  st.sidebar.title("Recommendation options")
  selected_k = st.sidebar.selectbox('Select top k restaurant you want to recommend',range(1,10), index=None, placeholder="Select top ...")
  st.sidebar.write('You selected:', selected_k)
  with st.sidebar:
      col1, col2, col3 = st.columns(3)
      with col1:
        pass
      with col3:
        pass
      with col2 :
        center_button = st.button('Get')

  if center_button:
    recommendation = item_based_recommendations(data, rest, mapping_item, mapping_user,test_group, selected_user, data.loc[selected_user, Get_Id_List_by_UserId(selected_user)].idxmax(), selected_k)
    recommendation = pd.DataFrame(recommendation)
    recommendation.columns = ['Rest_id', "Name", "Category", "City", "Stars", "Review_count"]
    st.markdown("""
    <style>
    dataframe {background-color: #CCFFCC;}
    </style>
    """, unsafe_allow_html=True)
    st.dataframe(
      recommendation,
      column_config={
        "Stars": st.column_config.NumberColumn(
            format="%.1f ⭐",
        )
    })
    

if selected == "Model-based":
  st.sidebar.header(f"You selected {selected}", divider='rainbow')
  selected_user = st.sidebar.selectbox('Select a user to recommend', data.index.values)
  st.sidebar.title("User detail")
  st.sidebar.write("*User_id*: ", selected_user)
  st.sidebar.write("*User_name*: ", get_user_name(selected_user))
  st.sidebar.write("*User_review_count*: ", get_user_review_count(selected_user))
  st.sidebar.write("*User_average_stars*: ", get_user_average_stars(selected_user))
  st.sidebar.title("Recommendation options")
  selected_k = st.sidebar.selectbox('Select top k restaurant you want to recommend',range(1,10), index=None, placeholder="Select top ...")
  st.sidebar.write('You selected:', selected_k)

  with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
      pass
    with col3:
      pass
    with col2 :
      center_button = st.button('Get')
  if center_button:
    recommendation = kcgn_recommendations(rest, mapping_item, mapping_user,recommendations, selected_user, selected_k)
    recommendation = pd.DataFrame(recommendation)
    recommendation.columns = ['Rest_id', "Name", "Category", "City", "Stars", "Review_count"]
    st.markdown("""
    <style>
    dataframe {background-color: #CCFFCC;}
    </style>
    """, unsafe_allow_html=True)
    st.dataframe(
      recommendation,
      column_config={
        "Stars": st.column_config.NumberColumn(
            format="%.1f ⭐",
        )
    })
st.text("")
st.text("")


st.text("")