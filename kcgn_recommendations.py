import pandas as pd
import numpy as np

def Get_Id_of_Item_List(mapping_item, itemid_list):
  return [mapping_item.get(key) for key in itemid_list]
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
def Get_Id_List_by_UserId(mapping_item, mapping_user,test_group, user_id):
  user_index = get_key(mapping_user, user_id)
  test_item_id = Get_Id_of_Item_List(mapping_item, test_group.get(user_index).get('recommendations'))
  return test_item_id

def kcgn_recommendations(rest, mapping_item, mapping_user,test_group, UID, top_n):
    recommends = Get_Id_List_by_UserId(mapping_item, mapping_user,test_group, UID)
    cba1 = []
    for i in range(top_n):
        rec_restaurant = recommends[i]
        cba1.append([
          rec_restaurant,
          rest[rest['business_id'] == rec_restaurant]['name'].values[0],
          rest[rest['business_id'] == rec_restaurant]['category'].values[0],
          rest[rest['business_id'] == rec_restaurant]['city'].values[0],
          rest[rest['business_id'] == rec_restaurant]['stars'].values[0],
          rest[rest['business_id'] == rec_restaurant]['review_count'].values[0],
        ])
        #print("my number ", i+1, " recommendation is ",    rest[rest['business_id'] == rec_restaurant]['name'].values)
    return cba1