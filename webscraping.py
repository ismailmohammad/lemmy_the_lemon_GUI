# Filename: webscraping.py
# Author: Mohammad Ismail - mnimoh17
# Date Last Updated: November 26 2016
# Description: This is an auxilary program to lemmy_the_lemon. It serves for
# webscraping purposes so that more of the process is automated and it is
# less dependant on user interaction/error.

# DISCLAIMER: This python program should not in anyway be misused or abused
# in any way that goes against any existing policies and is only for education
# al purposes. I will not be held liable for your individual actions and I do
# not condone any actions with the use of this code. Please read through all
# the documentation of the program as I am not liable for any risks/damages
# that may incur due to direct and/or indirect usage of this program.
# Also, please make sure you have all important files saved and backed up.

# Changelog (v.0.0.1):
# ~ Initial auxilary script release. Stay tuned for more functionality

# This .py file imports both 'requests' and 'BeautifulSoup4' to successfully
# execute the functions laid out within this file
import requests
# BeautifulSoup Import
import bs4


class InvalidCourseCode(Exception):
    ''' A class to represent an Invalid Course Code Error'''
    # This will be the Exception that will be called later and the error will
    # be caught so the user is notified of complications in the code. This
    # specifically is

# Session IDs - Current as of November 26, 2016
FALL = 9
SUMMER = 5
WINTER = 1


def session_num(session):
    '''
    (str) -> str
    Description: This function sets the session number of for the url query
    based upon the Fall, Winter, and Summer parameters that are initially taken
    in.
    '''
    # Sets up the initial session_num as an empty string
    session_num = ""
    # If it is the Fall session, the corresponding session ID is set as the
    # session_num
    if session == "Fall":
        session_num = FALL
    # If it is the Winter session, the corresponding session ID is set as the
    # session_num
    elif session == "Winter":
        session_num = WINTER
    # If it is the Summer session, the corresponding session ID is set as the
    # session_num
    elif session == "Summer":
        session_num = SUMMER
    # Returns the string cast session number for easy integration into scraper
    # function
    return str(session_num)


def scrape_site(crscode, year, session):
    '''
    (str, str, str) -> list
    Description: This is the main web scraping function that serves as the
    core of this program.
    ~ At the moment, the webscraper takes in a specified course and attempts to
    find that specific course. Development goals include to scrape and provide
    list of all available courses to provide to the user. ~
    '''
    # Gets the appropriate session ID based on the session that was taken in
    # as a parameter
    session = session_num(session)
    # uses a template of the url type and fills in missing information based
    # on taken parameters
    url = ("http://lecturecast.utsc.utoronto.ca/courses.php?year=" + year +
           "&session=" + session)
    # Sends an http request and is expectected to return with code 200.
    res = requests.get(url)
    # Sets up an instance of the BeautifulSoup object, setting it up as an
    # html parser that parses through the html file that was downloaded.
    soup_instance = bs4.BeautifulSoup(res.text, "html.parser")
    # Sets the variable elements to the html tag <td> where the course codes
    # can be found as per the page source
    elements = soup_instance.select('td')
    # Initializes an empty list of final_courses that will eventually be
    # returned
    final_courses = []
    # Use a while loop and initialize its index as 0
    index = 0
    # The loop only runs while cycling through the elements of "elements"
    while (index < len(elements)):
        # Creates a temporary list within the loop that finds all the text and
        # splits the various aspects into different list indices. However there
        # will be many repeats and as such the next while loop will take care
        # of duplicates
        index_list = (elements[index].getText(separator='\n',
                                              strip=True).split())
        # Initializes the second index variable for the second while loop
        index2 = 0
        # Cycles through the second list
        while (index2 < len(index_list)):
            # If the index of the list is equal to the crscode and there are no
            # duplicates already within the final_list, then it adds that
            # element plus the one right after it which contains the lecture
            # sections using the list.append() method.
            if ((index_list[index2] == crscode) and
                ((index_list[index2] + index_list[index2 + 1])
                 not in final_courses)):
                # Appends the required value to the list and avoids duplicates
                (final_courses.append(index_list[index2] +
                                      index_list[index2 + 1]))
            # Increases the index2 by 1 to avoid an infinite while loop and
            # cycle through the loop
            index2 += 1
        # Increases the index by 1 to avoid another infinite while loop and
        # cycles through the loop
        index += 1
    # Uses a try, except block to catch the error if the web_scraping turns
    # up empty, ie. len(final_courses) == 0
    try:
        if (len(final_courses) == 0):
            raise InvalidCourseCode
    # Let's the user know the nature of the Exception being called and provides
    # a specific message
    except InvalidCourseCode:
        print("You've entered an Invalid Coursecode, please ensure that" +
              " this" +
              "\nCoursecode actually exists and is weboptioned")
        pass
    # Returns the final_courses list
    return final_courses

def isolate_lectures(scraped):
    index = 0
    while index < len(scraped):
        scraped[index] = scraped[index][8:]
        scraped[index] = scraped[index].split("|")
        index += 1
    return scraped

if (__name__ == "__main__"):
    # The following settings were used for initial testing of the scraper
    # The year was set to 2016
    year = "2016"
    # The session was set to the "Fall" semester
    session = "Fall"
    # Courses, 1 through 5 were initialized as follows
    c1 = "MAT2A31H3"
    c2 = "CHMA10H3"
    c3 = "BIOA11H3"
    c4 = "MGEA02H3"
    c5 = "ANTA01H3"
    c6 = "NROB60H3"
    c7 = "PSYA02H3"
    c8 = "CHMA11H3"
    # Creates a list of the previously initialized courses
    courses = [c1, c2, c3, c4, c5, c6, c7, c8]
    # Uses a for loop to loop through the courses and prints the list of
    # weboption sections.
    # for course in courses:
        #print(scrape_site(course, year, session))
        
    scraped = scrape_site(c1,year,session)
    
    index = 0
    while index < len(scraped):
        scraped[index] = scraped[index][8:]
        scraped[index] = scraped[index].split("|")
        index += 1
        
    for item in range(len(scraped)):
        for nested_item in range(len(scraped[item])):
            scraped[item][nested_item] = scraped[item][nested_item][0]+"EC"+scraped[item][nested_item][1:]
    
        
    print(scraped)