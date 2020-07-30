# yelp-restaurants-flask-app-lda

## Yelp Restaurant Review Impressions

This Flask application uses Gensim's LDA module to model the top words of the two most important topics of all the Yelp reviews for a selected restaurant. 

These top words are displayed as two word clouds, which allows a potentional user to gain impressions of a chosen restaurant without having to read
any of the actual reviews!

The application can be run locally by setting up a python virtual environment in the same directory as the code and then installing the requirements 
from requirements.txt:

> python -m venv env

> source evn/bin/activate

> pip install -r requirements.txt

> python application.py

That's it! The application is now available on your local browser to play with and change to your heart's content.

You can even install the application - as is - on AWS Elastic Beanstalk, by compressing all the files with a zip program and then uploading the zipped 
file to a fresh Elastic Beanstalk application using your own AWS account.

Due to the English language model included for Spacy, it *could* get expensive, however. ;)
