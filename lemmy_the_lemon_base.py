# Filename: lemmy_the_lemon_v0.0.3 beta.py
# Author: Mohammad Ismail - mnimoh17
# Date Last Updated: November 26 2016
# Description: This is a an URL generator created for educational purposes to
# generate website-links that may or may not function of lecture streams.

# DISCLAIMER: This python program should not in anyway be misused or abused
# in any way that goes against any existing policies and is only for education
# al purposes. I will not be held liable for your individual actions and I do
# not condone any actions with the use of this code. Please read through all
# the documentation of the program as I am not liable for any risks/damages
# that may incur due to direct and/or indirect usage of this program.
# Also, please make sure you have all important files saved and backed up.

# CHANGELOG (v 0.0.3 beta):
# ~ Added Icon to Exe
# ~ Added Icon resource to build directory
# ~ Removed hardcoding of Campus Code, and replaced with Global Variable
# CAMPUS_CODE

# *** ~ Stay Tuned for v0.0.3 release: ***
# - Automation of Coursechecking
# - Implementation of the coded webscraping.py

# Imports necessary modules required for the program to work. Detailed
# explanation of why the library was imported explained below

# webbrowser - to open the webpages specified by the program at the end
import webbrowser
# time - module used to pause the python code process to allow the user time to
# exit prior to Lemmy making an appearance
import time
# os is used to access path which is used to store the Lemmy PNG, may be
# updated for later versions. Also used to implement the "shutdown -l" command
import os
# This is used to generate the MessageBox that is ussed when Lemmy is denied
import ctypes
# This imports the webscraper that was built as a friendly name 'scraper' for
# ease of reference.
import webscraping as scraper


# Global Variables
CAMPUS_CODE = str(3)


def get_userinfo():
    '''
    () -> (str, str, str, str, str, str)
    Description: This gets the coursecode from the user and asks whether or not
    the course is half credit (H) or a full credit (Y) course. It also asks for
    their section number.It then returns both the course code and the type of
    credit course along with other user data that is limited to: course code,
    course type, section, lecture, year, and session. None of this data is
    however collected or saved.
    '''
    # This sets the iniital message to display to the user
    welcome = "Welcome enlightened one, case not sensitive is the message"
    # The following prints the previous message that was stored in m1
    print(welcome)
    # This sets the second message to display to the user which is essentially
    # a disclaimer that the progran was only created for educational purposes
    # and not to be misused
    discl = ("Also, Disclaimer: This program was only made for educational" +
             " purposes ONLY and \nI am not resposible for how you use it.\n" +
             "or if you use it at all, please do so only for classes you are" +
             " registered in\n")
    # Prints the disclaimer described above
    print(discl)
    # Outputs to the user that they have been duly warned prior to running the
    # program
    print("You have been warned!\n")
    # Prompts the user to input the year of the lecture.*Continuous Disclaimer*
    # Please only input the current year which you have been granted access to
    # for the term.
    year = input("Lemmy asks what year is it and what session is it?" +
                 "\nie. Fall 2016, Winter 2017. enter year and session as" +
                 "\n2016 and winter or fall respectively." +
                 "\nYear: ")
    # Prompts the user for the session. Once again please only input the
    # session that you are registered in.
    session = input("Session: ")
    # Makes the first character of the inputted string uppercase while making
    # the rest of the string lowercase
    session = session[0].upper() + session[1:].lower()
    # Print an empty line for visual aesthetics
    print()    
    # Takes the coursecode of the course from the user and stores it into
    # crscode variable, and properly prompts the user.
    crscode = input(
        "pls giev Lemmy the Lemon ur coursecode as such" +
        " without quotations \"AAAA##\" ie BIOA01.\nCourse Code: ")
    # In case they did not upper case (Last internal comment)
    # this is to really ensure that case-sensitivity is not an issue with the
    # input provided
    crscode = crscode.upper()
    # Prints an empty line for visual aesthetics
    print()
    # Takes the coursetype of the course whether it is full or half credit
    # and stores it within the variable crstype as a string.
    crsetype = input("Lemmy asks, what type of credit course is it?" +
                     "\nie. half credit or full credit" +
                     ", type h for half or y for full" +
                     "\nCourse Type: ")
    # Once again, this is to maintain that case-insensitivity described to the
    # user earlier prior to this input field
    crsetype = crsetype.upper()
    # Prints an empty line for visual aesthetics
    print(crscode+crsetype+CAMPUS_CODE, year, session," Lecture Sections:")
    sections = scraper.scrape_site(crscode+crsetype+CAMPUS_CODE, year, session)
    refined = scraper.isolate_lectures(sections)
    for item in refined:
        print(item)
    # Prints an empty line for visual aesthetics
    print()    
    # Takes in the course section of the student and is dependant on whether
    # the student has entered in the correct information of the course.
    section_input = input("Lemmy asks which lecture section are you in?" +
                          "\nIf your prof teaches a lecture section" +
                          " that has a" + "\nvalue that is lower than yours," +
                          " enter the lower value" + "\nie. in LEC03 but" +
                          " prof teaches LEC01 and that is " +
                          "weboptioned, choose LEC01"+"\nLecture Section: ")
    # Sets up the string variable section so as to find a non 0 degit and keep
    # that as the actual section number ie. number >= 1
    section = ""
    # uses for loop to iterate through the items in section_input to check if
    # the element is a digit and if it's not a 0 then it adds that digit to
    # the section number
    for i in section_input:
        if (i.isdigit() and str(i) != "0"):
            section += i
    # Prints an empty line for visual aesthetics
    print()
    # Prompts the user to enter a lecture number that they are trying to watch
    # and
    lecture = input("Lemmy asks which lecture are you trying to watch?" +
                    "\nleave the number as a proper number, don't add 0 to 1" +
                    "\nto make 01 or that nonsense." +
                    "\nLecture Number: ")
    # Adds a "0", to the front of an inputted value if it ranges from 0-9 only
    if int(lecture) in range(10):
        lecture = "0" + lecture
    # Automate this process for User Convenience. The user should not be
    # bothered to enter in trivial things but rather should have the option to
    # enter as minimal information as possible making this tool of viable use.
    if len(sections) == 1:
        # If there is only one section, clear the previously entered section to
        # accomodate the database method of storing data.        
        section = ""
    # Returns the 6 inputted/manipulated strings.ie. course code, session, etc.
    return crscode, crsetype, section, lecture, year, session


def make_url(crscode, crsetype, section, lecture, year, session):
    '''
    (str, str, str, str, str, str) -> str
    REQ: len(crscode) > 0
    REQ: len(crsetype) > 0
    REQ: len(lecture) > 0
    REQ: len(year) > 0 and len(year) == 4
    REQ: len(session) > 0 and ((len(session) == 4) or (len(session) == 6))
    Description: This function takes in the user input provided when
    get_user_info() is called or a system generated counterpart of those
    results, and then generates a relevant URL based on the info that is
    provided.
    '''
    # Executes if the section is not a blank string and adds an underscore to
    # the front of the section number
    if (section != ""):
        section = "_" + section
    # Creates the year_session variable by combining year and session with an
    # underscore in between
    year_session = year + "_" + session
    # creates the full coursecode by adding the course code, coursetype, and
    # the campus code "3" to to generate the full course code.
    full_crscode = crscode + crsetype + CAMPUS_CODE
    # Creates the lecture accessed as the full coursecode, plus "_Lecture_"
    # and also the lecture number that is intended to be accessed
    lecture_accessed = full_crscode + "_Lecture_" + lecture
    # This then sets the variable url as the "url" that is to provided to the
    # user.
    url = ("http://lecturecast.utsc.utoronto.ca/lectures/" +
           year_session + "/" + full_crscode+section + "/" + lecture_accessed +
           "/" + lecture_accessed+section+".mp4")
    # Returns the generated URL
    return url


def complete_url_generation():
    '''
    () -> NoneType
    Description: This function completes the url generation process and then
    calls upon both get_user_info() and also make_url() to combine the both
    processes
    '''
    # Initializes the following variables which will be returned by the
    # get_user_info() function
    crscode, crsetype, section, lecture, year, session = get_userinfo()
    # Sets the url variable to the returned url string from make_url()
    url = make_url(crscode, crsetype, section, lecture, year, session)
    # Print Final Disclaimers to the user, still giving them many chances
    # to exit the program. The program will show the use a Creative Commons
    # picture of a cartoon Lemon, whom I amicably named Lemmy the Lemon.
    print("Lemmy is a psychic, and has made you a url would " +
          "you like to go the website?\ntype y for Yes and n" +
          " for No. Lemmy's going give you 10 seconds.\n")
    print("Lemmy lied! Gasp! If his calculation doesn't work," +
          " it doesn't exist or may goofed"+"\nAlso if you say no, Lemmy" +
          " will get mad. But you can always close the window right now.\n" +
          "or enter anything other than y or n and LEAVE.\n")
    # This promps the user for their final decision regarding whether or not
    # they want to be redirected to the URL generation which again may or may
    # not work and I will not be liable for. This is just pure experimentation.
    user_decision = input("Lemmy gave you enough time, DECIDE!: ")
    # Prints to the screen, a farewell message to the user
    print("Thank you! Lemmy bids you Adieu :')")
    # If the user's decision was "y" ie. Yes, it will then redirect them to the
    # generated URL
    if (user_decision == "y"):
        webbrowser.open(url, new=1, autoraise=True)
    # If the answer was "n", ie. No then the program them opens the local lemmy
    # folder which is in the same root directory and consequently the_lemon.png
    # The following was implemented for personal entertainment to allow the
    # user to still play around with the program while avoiding the URL,
    # another educational aspect of the program.
    if (user_decision == "n"):
        url = 'file://' + (os.path.realpath("yolo.png").
                           replace("yolo.png", "lemmy\\the_lemon.png"))
        webbrowser.open(url, new=0, autoraise=True)
        # Creates a messagebox prompt to the user with the indicated message
        ctypes.windll.user32.MessageBoxW(0, "HAVE YOU SEEN LEMMY!?!",
                                         "LEMMY STRIKES AGAIN!", 1)
        # Sleeps the python code for 5 seconds using the time module which
        # was imported earlier
        time.sleep(5)
        # Using the os package which was imported earlier, it passes the
        # "shutdown -l" which merely logs the user out.
        os.system("shutdown -l")

if (__name__ == "__main__"):
    # Calls the complete_url_generation() when __name__ == "__main__"
    complete_url_generation()
