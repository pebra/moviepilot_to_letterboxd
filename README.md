### Update 2021-01-27
I forked this project since moviepilot's website structure seems to have changed from using a table structure instead of a list to display the movie ratings.


# Moviepilot to letterboxd converter
## Script to log into moviepilot webpage via CLI and exporting all watched movies of a certain given user of https://www.moviepilot.de/

### Prerequisites

* Python 3
* pip
* credentials of your moviepilot account
* username you want to export watched movies for
* read https://letterboxd.com/about/importing-data (be sure about what you're trying to do, because an import might overwrite previously made letterboxd logs!!)

### Installation

* Code: clone repo
    ```
    git clone https://github.com/krumax/moviepilot_to_letterboxd.git
    ```
* Install packages:
    ```
    pip3 install -r requirements.txt 
    ```
* Run application
    ```
    python3 script.py
    ```

### Usage

Run the script, enter moviepilot credentials and username you want to export watched movies for.

You'll have to wait until the script has finisched scraping the pages from moviepilot. A file is creating beside the script file with the name of the user you exported movies for.

The generated csv file contains 'Title', 'Year', 'Rating10' of every watched movie from moviepilot.de

Final result should be a csv file, you can easily import into your letterboxd account (e.g. by creating a new list and hitting the IMPORT button).

### Troubleshooting

"Moviepilot movies do not match with those from letterboxd."

I assume, that the titles from moviepilot.de are generally in german, but letterboxd's primary source of truth is the english/original title. You have to manually change the missing movies during importing the movies. Thats pretty easy.
