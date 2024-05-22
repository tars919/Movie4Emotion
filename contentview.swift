//
//  ContentView.swift
//  Movie4Emotion
//
//  Created by Tarika Selvaraj on 5/21/24.
//

//
//  ContentView.swift
//  MovieRecommendationApp
//
//  Created by Tarika Selvaraj on 5/20/24.
//



//TO DO:
//
//
//#add more movie details -> starcast, breif description, release date,
//#Make the UI more colorful and the UX should be better
//#add a refresh button
//#train against a dataset to show what other people like to watch when feeling this same information
//add the directions and prompting for the user
// add a loading screen for the app
// maybe have it recommend and map the emotions and categories and  create and algorithm where the app will ask the user for emtion and generes they like and will use that to map and respond with the recommendations

//STUFF TO GO BACK AND FIX:
// rows display



import SwiftUI
import SwiftSoup

struct ContentView: View {
    @State private var emotion: String = ""
    @State private var suggestionsCount: String = ""
    @State private var movieSuggestions: [String] = []
    @State private var errorMessage: String?

    let emotionToUrl = [
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
        "excitement": "https://www.imdb.com/search/title/?genres=adventure,action",
        "love": "https://www.imdb.com/search/title/?genres=romance",
        "anxiety": "https://www.imdb.com/search/title/?genres=sci-fi,thriller",
        "contentment": "https://www.imdb.com/search/title/?genres=drama",
        "gratitude": "https://www.imdb.com/search/title/?genres=fantasy",
        "regret": "https://www.imdb.com/search/title/?genres=war",
        "guilt": "https://www.imdb.com/search/title/?genres=sci-fi,crime",
        "jealousy": "https://www.imdb.com/search/title/?genres=romance,drama",
        "pride": "https://www.imdb.com/search/title/?genres=documentary,reality-tv",
        "relief": "https://www.imdb.com/search/title/?genres=comedy,short",
        "hope": "https://www.imdb.com/search/title/?genres=fantasy,family",
        "confusion": "https://www.imdb.com/search/title/?genres=sci-fi,thriller",
        "boredom": "https://www.imdb.com/search/title/?genres=action,mystery"
    ]

    var body: some View {
        VStack {
            Text("Movie4Emotion")
                .font(.largeTitle)
                .padding()
            
            Text("Choose on of theese emotions and type below!")
                .font(.title3)
                .padding()

            TextField("Enter your emotion here", text: $emotion)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            TextField("How many movie suggestions do you want (1-50)", text: $suggestionsCount)
                .keyboardType(.numberPad)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            Button(action: fetchMovieSuggestions) {
                Text("Get Movie Suggestions")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
            .padding()

            if let error = errorMessage {
                Text(error)
                    .foregroundColor(.red)
                    .padding()
            }

            List(movieSuggestions, id: \.self) { suggestion in
                Text(suggestion)
            }
        }
        .padding()
    }

    func fetchMovieSuggestions() {
        guard let urlString = emotionToUrl[emotion.lowercased()] else {
            errorMessage = "Emotion not recognized."
            return
        }

        guard let url = URL(string: urlString) else {
            errorMessage = "Invalid URL."
            return
        }
        
        guard let count = Int(suggestionsCount), count > 0, count <= 50 else {
                   errorMessage = "Please enter a number between 1 and 50."
                   return
               }

        URLSession.shared.dataTask(with: url) { data, response, error in
            if let data = data {
                if let htmlContent = String(data: data, encoding: .utf8) {
                    do {
                        let document = try SwiftSoup.parse(htmlContent)
                        let titleTags = try document.select("a[href^=/title/tt]").array()
                        let titles = try titleTags.prefix(count * 2).map { try $0.text() }
                        DispatchQueue.main.async {
                            movieSuggestions = titles
                            errorMessage = nil
                        }
                    } catch {
                        DispatchQueue.main.async {
                            errorMessage = "Failed to parse HTML."
                        }
                    }
                } else {
                    DispatchQueue.main.async {
                        errorMessage = "Failed to load data."
                    }
                }
            } else {
                DispatchQueue.main.async {
                    errorMessage = "Network error: \(error?.localizedDescription ?? "Unknown error")"
                }
            }
        }.resume()
    }
}
