import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def Get_Id_of_Item_List(mapping_item, itemid_list):
  return [mapping_item.get(key) for key in itemid_list]
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
def Get_Id_List_by_UserId(mapping_item, mapping_user,test_group, user_id):
  user_index = get_key(mapping_user, user_id)
  test_item_id = Get_Id_of_Item_List(mapping_item, test_group.get(user_index))
  return test_item_id


def calculate_item_sim(data, mapping_item, mapping_user,test_group, user_id, original_item):
  test_item_id = Get_Id_List_by_UserId(mapping_item, mapping_user,test_group, user_id) #101
  df = data.T.loc[(data.T.index.isin(test_item_id)),:] 
  item = data.T.loc[data.T.index == original_item]
  item_sim = cosine_similarity(item, df)
  item_sim = pd.DataFrame(item_sim, columns = df.index)
  return item_sim

def item_based_recommendations(data, rest, mapping_item, mapping_user,test_group, UID, original_item, top_n):
    """
    inputs: original_item <int>: is the id of the item we want to make
                                 recommendation for
            top_n <int>: number of items we want to recommend for the
                         original item
    """
    idx = original_item
    item_sim = calculate_item_sim(data, mapping_item, mapping_user,test_group,UID, original_item)
    print("Your original item is", rest[rest['business_id'] == str(idx)]['name'].values)
    recommends = item_sim.iloc[0].sort_values(ascending = False)[1:].index
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