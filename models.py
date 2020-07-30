#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:26:24 2020

@author: jennifer
"""
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import SelectField

class Form(FlaskForm):
    state = SelectField('state', choices=[
        ('0', 'Select a state'), 
        ('AZ', 'Arizona (6906 restaurants)'), 
        ('NV', 'Nevada (4328) restaurants'), 
        ('WI', 'Wisconson (830 restaurants)')]
    )
    city = SelectField('city', choices=[('0', 'Select a city')])
    cuisine = SelectField('cuisine', choices=[('0', 'Select a cuisine')])

class StateToCity():
    state_city_dict = {
    'AZ': ['Litchfield Park', 'Fountain Hills', 'San Tan Valley', 'Rio Verde', 'Carefree', 
           'Laveen', 'Avondale', 'Peoria', 'Phoenix', 'Paradise Valley', 'Tempe', 
           'Glendale', 'Tonopah', 'Chandler', 'Anthem', 'Goodyear', 'Tortilla Flat', 
           'Central City Village', 'Youngtown', 'New River', 'Ahwatukee', 
           'El Mirage', 'Scottsdale', 'Gold Canyon', 'Buckeye', 'Sun Lakes', 
           'Morristown', 'Gila Bend', 'Guadalupe', 'Maricopa', 'Mesa', 
           'Black Canyon City', 'Casa Grande', 'Gilbert', 'Surprise', 'Fort McDowell', 
           'Tolleson', 'Coolidge', 'Sun City', 'Apache Junction', 'Queen Creek', 'Cave Creek', 
           'Florence', 'Sedona', 'Higley', 'Wickenburg'], 
    'NV': ['Nellis', 'Green Valley', 'Boulder City', 'Clark County', 'Summerlin', 
           'Enterprise', 'Las Vegas', 'Spring Valley', 'Henderson', 'Paradise'], 
    'WI': ['Windsor', 'DeForest', 'Verona', 'McFarland', 'Monona', 'Cottage Grove', 
           'Trempealeau', 'Waunakee', 'Madison', 'Stoughton', 'Middleton', 'Dane', 
           'Sun Prairie', 'Fitchburg']
    }
        
    
class RestaurantData():
    restaurant_data = pd.read_csv('data/restaurants_all_data.csv', sep='\t')
    
class RestaurantText():
    restaurant_text = pd.read_csv('data/restaurant_review_text.csv', sep='\t')