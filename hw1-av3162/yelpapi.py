
import requests
import json
import time
import pandas as pd
import datetime 

endpoint = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'Bearer 9eR-MQxXucF9di3Xp7R0NXKIq16aKy3aM8Ktf_cIggE_JakUU5RbTaP4g68nxCokllylzAs5zo5PUXFABAIwoGHRsTe0B4aMH43zjLPtpNcg16S_pziSc1e-_1MjZXYx'}

unique_restaurants = set()
total_restaurants = []

cuisines = ['italian', 'mexican', 'chinese', 'mediterranean', 'japanese', 'thai']

for cuisine in cuisines:
    restraunts_fetched = 0
    offset = 0
    if len(total_restaurants) > 5000 :
        break
    while 50 + offset <= 1000 :

        params = {
            'term' : 'restaurant',
            'location' : 'Manhattan',
            'limit' : 50,
            'offset' : offset,
            'categories' : cuisine
        }
        offset += 50
        response = requests.get(endpoint, headers=headers, params=params)
        data = response.json()
        try : 
            if data['total'] > 0 :
                bussinesses = data['businesses']
                if not bussinesses :
                    print("None are bussinesses")
                else :
                    for business in bussinesses:
                        if  business['id'] not in unique_restaurants:
                            unique_restaurants.add(business['id'])
                            restraunts_fetched = restraunts_fetched + 1
                            business['cuisine'] = cuisine
                            total_restaurants .append(business)
            else :
                print(restraunts_fetched, " ", cuisine,"\n")
                break
            time.sleep(2)
        except Exception as e : 
            print(data)
            print(e)
            break


for restaurant in total_restaurants :
    restaurant['rating'] = str(restaurant['rating'])
    restaurant['coordinates']['latitude'] = str(restaurant['coordinates']['latitude'])
    restaurant['coordinates']['longitude'] = str(restaurant['coordinates']['longitude'])
    restaurant['insertedAtTimestamp'] = str(datetime.datetime.now())

#Drop unused keys
keys_to_remove = ['alias', 'image_url', 'categories', 'transactions', 'distance', 'price', 'is_closed']
df = pd.DataFrame(total_restaurants)
df = df.drop(keys_to_remove, axis=1)

for cuisine in cuisines : 
    cuisine_restaurants = df[df['cuisine'] == cuisine]
    cuisine_restaurants_json = cuisine_restaurants.to_dict(orient='records')

    with open(f'restaurants_{cuisine}.json', 'w') as file:
        json.dump(cuisine_restaurants_json, file)



