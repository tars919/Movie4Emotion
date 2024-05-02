

#go through add all emotions
#go thtough and quote 



#Sentiment analysis to classify movie -> recommending movie based on emotion
#IBDM does not have an API so we need to perform scraping to get the titles

#LXML: Python lxml is the most feature-rich and simple to-utilize library for processing XML and HTML data
#BeautifulSoup: It is a library of Python that is utilized to pull the data from web pages

#The scraper is written in Python and uses lxml for parsing the webpages.
#BeautifulSoup is used for pulling data out of HTML and XML files.

#----> Needed: imports
from wsgiref import headers
from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP


#---> Purpose: main function that will perform the scraping 
#Takes in a emotion
def main(emotion):

    urls = {
        "sad": "https://www.imdb.com/search/title/?genres=drama",
        "disgust": "https://www.imdb.com/search/title/?genres=music",
        "anger": "https://www.imdb.com/search/title/?genres=family",
        "anticipation": "https://www.imdb.com/search/title/?genres=thriller",
        "fear": "https://www.imdb.com/search/title/?genres=sport",
        "enjoyment": "https://www.imdb.com/search/title/?genres=thriller",
        "trust": "https://www.imdb.com/search/title/?genres=western",
        "surprise": "https://www.imdb.com/search/title/?genres=film-noir",
    }

    if emotion not in urls:
        print("Emotion not recognized.")

        
    

    urlhere = urls[emotion]
    headers = {'User-Agent': 'Mozilla/5.0'}
    #http request to get the data from the whole page 
    response = HTTP.get(urlhere, headers=headers)

    # data =response.text

    #using beautifulsoap to parse the data
    #soup = SOUP(data,'lxml')

    #using regex(regular expression) to extract the movie titles from the data 
    #-> attrs gives a way to define attributes on the class
    #title = soup.find_all("a", attrs = {"href" : re.compile(r'\/title\/tt+\*/') })


    if response.status_code == 200:
        soup = SOUP(response.text, 'html.parser')
        title_tags = soup.find_all("a", href=re.compile(r'\/title\/tt+\d+\/'))
        movie_titles = [tag.text for tag in title_tags]
        return movie_titles[:10]  # Return top 5 movie titles had to double the margin when  status code is 200 multiply the total number you want by 2
    else:
        print("Error accessing the webpage. Status code:", response.status_code)
        return []


       


if __name__ == "__main__":
    print("How are you feeling today?")
    print("Here are the options to choose from: surprise, trust, anger, disgust, sad, anticipation, fear, enjoyment")
    emotion = input("Type your response here: ").lower()
    movie_suggestions = main(emotion)

    if movie_suggestions:
        for movie in movie_suggestions:
            print(movie)
    else:
        print("No movie suggestions.")

