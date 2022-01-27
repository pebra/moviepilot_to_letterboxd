#imports
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

LOGIN_URL = "https://www.moviepilot.de/login?next="
SESSION_POST_URL="https://www.moviepilot.de/api/session"
SEARCH_URI = "https://www.moviepilot.de/users/%s/rated/movies?page=%d"

# create a csv file
def create_csv(user):
    with open(str(user) + '.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(('Title','Year','Rating10', 'WatchedDate'))

# write to previously created csv file
def write_to_csv(user, movie):
    with open(str(user) + '.csv', 'a', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow((
          movie['title'],
          movie['year'],
          movie['rating'],
          movie['review_date']
        ))

# request movies pages for selected user as long there are movies to export
def get_movies(request, user):
    i = 1 
   
    while request.get(SEARCH_URI % (user, i)):
       search_document = request.get(SEARCH_URI % (user, i))
       print("reading: "+SEARCH_URI % (user, i))
       i += 1
       soup = BeautifulSoup(search_document._content, 'html.parser')
       scrape_movielist_and_write_to_csv(user, soup)
       no_more_movies_to_export = False
       if (soup.select("table.table-plain-list > tbody > tr") == []):
           no_more_movies_to_export = True
       if (no_more_movies_to_export):
           break

# find movie infos and write them to csv file
def scrape_movielist_and_write_to_csv(user, soup):
    movie = {'title': None, 'year': None, 'rating': None, 'review_date': None}
    movieslist = soup.select("table.table-plain-list > tbody > tr")
    for m in movieslist:
        table_data = m.find_all("td")

        # get title
        movie['title'] = table_data[0].get_text().split("\n")[2].strip()

        # get year
        movie['year'] = table_data[0].get_text().split("\n")[4].split(" ")[-1].strip()

        # get rating
        movie['rating'] = table_data[1].get_text().strip()

        # get review date
        german_date = table_data[2].get_text().strip()
        movie['review_date'] = datetime.strptime(german_date, "%d.%m.%Y").strftime("%Y-%m-%d")

        write_to_csv(user, movie)

# get moviepilot login
def get_mp_login():
    login = input("Moviepilot login: ")
    return login

# get moviepilot password
def get_mp_password():
    password = input("Moviepilot password: ")
    return password

# create a moviepilot session with given credentials
def login_to_moviepilot():
    # request session request
    session = requests.session()

    # request login url
    session.get(LOGIN_URL)

    username = get_mp_login()
    password = get_mp_password()
    
    # create session request payload
    payload = {
        "username": username, 
        "password": password
    }

     # perform login
    session.post(SESSION_POST_URL, data = payload)
    return session

def get_user():
    user = input("Enter the moviepilot username you want to export filmratings for: ")
    print("Search will be done on the user: " + user + ". Your csv will be saved in the current directory under the name: "+user+".csv")
    
    return user.lower().strip()

def main():
    session = login_to_moviepilot()

    # ask for user to export movielist for
    user = get_user()

    # prepare csv for user
    create_csv(user)
    
    # scrape search URL website and write to csv add additional amount of maxpages
    get_movies(session, user)

if __name__ == "__main__":
    main()
