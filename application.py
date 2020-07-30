#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:58:51 2020

@author: jennifer
"""
from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_jsglue import JSGlue

import secrets
import models
import os.path
import TopicModel

secret_key = secrets.token_hex(16)

application = Flask(__name__, instance_relative_config=True)
jsglue = JSGlue(application)
bootstrap = Bootstrap(application)

application.config['SECRET_KEY'] = secret_key

@application.route('/', methods=['GET', 'POST'])
def index():
    form = models.Form()
    
    return render_template('index.html', form=form)

@application.route('/city/<state>')
def city(state):
    state_to_city = models.StateToCity()
    state_to_city_dict = state_to_city.state_city_dict
    
    restaurant_data = models.RestaurantData()
    restaurant_data_df = restaurant_data.restaurant_data
    
    #get cities for selected state
    cities = sorted(state_to_city_dict[state])
    cityArray = []
    
    for city in cities:
        mask = restaurant_data_df['city'] == city
        nr_restaurants = restaurant_data_df[mask].business_id.count()
        
        cityObj = {}
        cityObj['id'] = city
        cityObj['name'] = city + ' (' + str(nr_restaurants) + ' restaurants)'
        cityArray.append(cityObj)
        
    return jsonify({'cities': cityArray})    

@application.route('/cuisine/<city>/<state>')
def cuisine(city, state):
    restaurant_data = models.RestaurantData()
    restaurant_data_df = restaurant_data.restaurant_data    
    
    #get cuisine for selected criteria (city, state)
    state_mask = restaurant_data_df['state'] == state
    city_mask = restaurant_data_df['city'] == city
    df = restaurant_data_df[(state_mask) & (city_mask)]
    
    cuisineSet = set()
    cuisineArray = []
    cuisines = df.categories
    for cuisine in cuisines:
        curr = cuisine.replace('[', '').replace(']', '').replace('\'', '').strip()
        curr_list = curr.split(',')

        for el in curr_list:
            new_cuisine = el.strip()
            if new_cuisine not in cuisineSet:
                cuisineSet.add(new_cuisine)
                cuisine_mask = df['categories'].str.contains(new_cuisine, regex=False)
                nr_restaurants = df[cuisine_mask].business_id.count()
                cuisineObj = {}
                cuisineObj['id'] = new_cuisine
                cuisineObj['name'] = new_cuisine + ' (' + str(nr_restaurants) + ' restaurants)'
                cuisineArray.append(cuisineObj)
    
    return jsonify({'cuisines': cuisineArray})

@application.route('/restaurant/<cuisine>/<city>/<state>')
def restaurant(cuisine, city, state):
    restaurant_data = models.RestaurantData()
    restaurant_data_df = restaurant_data.restaurant_data   
    
    state_mask = restaurant_data_df['state'] == state
    city_mask = restaurant_data_df['city'] == city
    location_df = restaurant_data_df[(state_mask) & (city_mask)]
    cuisine_mask = location_df['categories'].str.contains(cuisine, regex=False)
    df = location_df[cuisine_mask]
    restaurants = df[['business_id', 'name']]
    
    restaurantArray = []
    for i in range(0, restaurants.shape[0]):
        restObj = {}
        restObj['id'] = restaurants.iloc[i]['business_id']
        restObj['name'] = restaurants.iloc[i]['name']
        restaurantArray.append(restObj)
        
    return jsonify({'restaurants': restaurantArray})   
        

@application.route('/impressions/<restaurant_id>')
def impressions(restaurant_id):
    restaurant_text = models.RestaurantText();
    restaurant_text_df = restaurant_text.restaurant_text
    
    mask = restaurant_text_df['business_id'] == restaurant_id
    reviews = restaurant_text_df[mask]
    
    filenames = [
        'static/images/cloud_' + restaurant_id + '_0.png',
        'static/images/cloud_' + restaurant_id + '_1.png',
    ]
    
    restaurant_name = reviews.iloc[0]['name']
    
    if (not os.path.isfile(filenames[0])) & (not os.path.isfile(filenames[1])):
        topic_model = TopicModel.TopicModel()
        lda_model = topic_model.make_lda_model(reviews, restaurant_id)
        filenames = topic_model.make_wordclouds(restaurant_id, lda_model)
    
    return render_template(
        'impressions.html', 
        wordcloud1=filenames[0], 
        wordcloud2=filenames[1], 
        restaurant_name=restaurant_name
    )

    
if __name__ == '__main__':
    application.run(debug=False)
    #application.run(host='0.0.0.0', port=8080, debug=False)