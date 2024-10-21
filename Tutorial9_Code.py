import json
from openai import OpenAI

def add_movie_menu():
    movies = []
    while True:
        movie = input("Enter the name of the movie: ")
        movies.append(movie)
        another = input("Do you want to add another movie? (yes/no): ").lower()
        if another == 'yes':
            print("")
        elif another == 'no':
            break
        else:
            print("Invalid Option | Defaults to add movie")
    return movies


def recommend_movies(moviesArr: list):
    api_key = "Open AI API Key"
    client = OpenAI(api_key=api_key)
    assistantId = "Open AI Assistant ID"

    movies_json = json.dumps({"films": moviesArr})

    try:
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": movies_json,
                    "attachments": []
                }
            ]
        )
    except Exception as e:
        print(f"Error creating thread: {e}")
        return

    try:
        run = client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=assistantId
        )
        
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        #print(messages)
        parsed_content = messages.data[0].content[0].text.value
        parsed_content_json = json.loads(parsed_content)
        return parsed_content_json
    
    except Exception as e:
        print(f"Error during run: {e}")


def userPrint(film_data):
    for film in film_data["films"]:
        print(f"Title: {film['title']}")
        print(f"Type: {film['type']}")
        print("Genres:")
        for genre in film["genres"]:
            print("  * " + genre)
        print("-" * 40)

# Run the menu and Get Recommendations
added_movies = add_movie_menu() # Get the data to give to the AI
recommended_movies = recommend_movies(added_movies) # Get AI Response

# Print the data to user
userPrint(recommended_movies) # Show the data to the user
