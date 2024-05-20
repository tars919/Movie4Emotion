#----TO DO----

#add more movie details -> starcast, breif description, release date, 
#Make the UI more colorful and the UX should be better
#add a refresh button
#train against a dataset to show what other people like to watch when feeling this same information 


#make the GUI more colorful and respond more quickly with less bugs 

#potentially create a ios application  
#-> 

#use this to pitch to netflix








#make sofia a birthday gift -> The code thing you guys were talking about 


#OTHER NOTES:
#------------
#- can this be done using an identifier like we did movie title 
#rating of the movie as well


#Another concoise way to do this ->>>>>>> emotion to genere mapping without having to repeat the url many times


#Sentiment analysis to classify movie -> recommending movie based on emotion
#IBDM does not have an API so we need to perform scraping to get the titles

#LXML: Python lxml is the most feature-rich and simple to-utilize library for processing XML and HTML data
#BeautifulSoup: It is a library of Python that is utilized to pull the data from web pages

#The scraper is written in Python and uses lxml for parsing the webpages.
#BeautifulSoup is used for pulling data out of HTML and XML files.

#----> Needed: imports

#For the Gui implementation
from tkinter import Tk, Label, Entry, Button, Frame
from wsgiref import headers
from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP


#---> Purpose: main function that will perform the scraping 
#Takes in a emotion
#Used a generatior for top 20 emotions people feel to categories movies for each type of emotion 
def main(emotion, store):

    #linking one of the main emotion options with a category of movie that lines up with the emotion

    


    urls = {

        "sad": "https://www.imdb.com/search/title/?genres=drama",
        "disgust": "https://www.imdb.com/search/title/?genres=music",
        "anger": "https://www.imdb.com/search/title/?genres=family",
        "anticipation": "https://www.imdb.com/search/title/?genres=thriller",
        "fear": "https://www.imdb.com/search/title/?genres=sport",
        "enjoyment": "https://www.imdb.com/search/title/?genres=thriller",
        "trust": "https://www.imdb.com/search/title/?genres=western",
        "surprise": "https://www.imdb.com/search/title/?genres=film-noir",
        "adrenaline": "https://www.imdb.com/search/title/?genres=action",
        "happy": "https://www.imdb.com/search/title/?genres=comedy", 
        "excitment": "https://www.imdb.com/search/title/?genres=adventure,action",
        "love":"https://www.imdb.com/search/title/?genres=romance",
        "anxiety":"https://www.imdb.com/search/title/?genres=sci-fi,thriller",
        "contentment":"https://www.imdb.com/search/title/?genres=drama" ,
        "gratitude":"https://www.imdb.com/search/title/?genres=fantasy",
        "regret":"https://www.imdb.com/search/title/?genres=war",
        "guilt":"https://www.imdb.com/search/title/?genres=sci-fi,crime",
        "regret":"https://www.imdb.com/search/title/?genres=crime,war",
        "jealousy":"https://www.imdb.com/search/title/?genres=romance,drama" ,
        "pride":"https://www.imdb.com/search/title/?genres=documentary,reality-tv" ,
        "relief":"https://www.imdb.com/search/title/?genres=comedy,short",
        "hope":"https://www.imdb.com/search/title/?genres=fantasy,family",
        "confusion":"https://www.imdb.com/search/title/?genres=sci-fi,thriller",
        "boredom":"https://www.imdb.com/search/title/?genres=action,mystery"
    }
    
   


    #urls = "https://www.imdb.com/search/title/?genres=action,mystery".append(emotion)
    
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

        #store ->>>>>> To allow the user to choose the amount of movie recomendation they want to receive 
        #computation to set the exact margin
        movie = int(store) * 2



        return movie_titles[:movie]  # Return top 5 movie titles had to double the margin when  status code is 200 multiply the total number you want by 2
    else:
        print("Error accessing the webpage. Status code:", response.status_code)
        return []



#creating a method to get the movie reccomendations 
def get_movie(emotion_entry, store_entry, result):
    emotion = emotion_entry.get().lower()
    store = store_entry.get()
    movie_suggestions = main(emotion, store)

    #if condition to set a cond for the gui
    if movie_suggestions:
        result.config(text="\n".join(movie_suggestions))
    else:
        result.config(text="No movie suggestions.")




#method to create the instructions 
def show_instructions(root, next_func):

    instructions_text = ("Welcome to the Movie Recommendation System!\n\n"
                                           "Please follow the instructions to get movie suggestions:\n\n"
                                           "1. How would you categorize your emotion at the moment?.\n"
                                           "2. Here are the options to choose from (Pick 1) :\n"
                                           "3. Sadness, Disgust, Anger, Anticipation, Fear,Enjoyment, Trust, Surprise, Adrenaline, Happiness, Excitement, Love, Anxiety, Contentment, Gratitude, Regret, Guilt, Jealousy, Pride, Relief, Hope,Confusion, Boredom\n\n"
                                           "Click 'Next' to continue to the movie recommendation page.")
    
    instructions_label = Label(root, text= instructions_text)
    instructions_label.pack()

    next_button = Button(root, text="Next", command=next_func)
    next_button.pack()




#another method to create the actual gui
def show_page(root):
    root.title("Movie Recommendation System based of Human emotion")
    
    emotion_label = Label(root, text="Enter your emtoion here: ")
    emotion_label.pack()

    emotion_entry = Entry(root)
    emotion_entry.pack()

    store_label = Label(root, text="How many movie suggestions do you want (1-50):")
    store_label.pack()

    store_entry = Entry(root)
    store_entry.pack()

    result_label = Label(root, text="")
    result_label.pack()

    get_suggestions = lambda: get_movie(emotion_entry, store_entry, result_label)
    submit_button = Button(root, text="Get Movie Suggestions", command=get_suggestions)
    submit_button.pack()

    root.mainloop()



"""

store = input("How many movie suggestions do you want 1-50: \n\n" )
    print("How would you categorize your emotion at the moment?\n\n")
    print("Here are the options to choose from (Pick 1) :   ")
    print("                                                 ")#to add a break 
    print("Sadness, Disgust, Anger, Anticipation, Fear,Enjoyment, Trust, Surprise, Adrenaline, \n
    Happiness, Excitement, Love, Anxiety, Contentment, Gratitude, Regret,\n
    Guilt, Jealousy, Pride, Relief, Hope,Confusion, Boredom")
    print("                                                 ")#to add a break
    emotion = input("Type your response here: ").lower()
    movie_suggestions = main(emotion,store)

    if movie_suggestions:
        for movie in movie_suggestions:
            print(movie)
    else:
        print("No movie suggestions.")


"""


#actual gui method 
def gui():
    root = Tk()
    root.title("Movie Recommendation System")

    frame = Frame(root)
    frame.pack()

    def show_next_page():
        frame.pack_forget()  # Hide the current frame
        show_page(root)  # Show the movie recommendation page

    show_instructions(frame, show_next_page)
    root.mainloop()






if __name__ == "__main__":
    gui()
