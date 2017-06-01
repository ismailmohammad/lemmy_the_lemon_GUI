from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import requests
from multiprocessing import queues
import webscraping as scraper
from pygame import mixer

def openWebSite(event):
    url = 'http://ismailmohammad.me/'
    webbrowser.open(url, new=0, autoraise=False)

def openGitHub(event):
    url = 'https://github.com/ismailmohammad/lemmy_the_lemon'
    webbrowser.open(url, new=0, autoraise=False)

def limit_to_this(year_sv,number):
    c = year_sv.get()[0:number]
    year_sv.set(c)    

def clear_input_values(event):
    # Clear the year entered
    year_sv.set("")
    # Clear the session
    session.set("Cleared")
    # Clear the coursecode
    coursecode_sv.set("")
    # Clear Course Type
    crstype.set("Cleared")
    # Clear the Search Result Label
    search_label.config(text="")
    search_results.config(text="")
    # Clear any generated URL
    url.set("")
    try:
        selected_section.set("")
        select_section.config(values=list())
    except:
        pass
    try:
        search_results.grid_remove()
    except:
        pass
    try:
        progressbar.grid_remove()
    except:
        pass
    try:
        check_link.grid_remove()
    except:
        pass
    try:
        generate_link.grid_remove()
        frame4.grid_remove()
        frame5.grid_remove()
    except:
        pass
    try:
        visit_link.grid_remove()
    except:
        pass
    try:
        list_of_sections.clear()
    except:
        pass
    try:
        one_section_label.grid_remove()
        one_section.grid_remove()
    except:
        pass
    try:
        mixer.music.stop()
    except:
        pass
    try:
        leave_feedback.grid_remove()
        frame7.grid_remove()
    except:
        pass

def fix_case_sensitive():
    coursecode_sv.set(coursecode_sv.get().upper())    
    
def show_generate_link():
    frame5.grid(row=5,column=0)
    generate_link.grid(row=0,column=0)  

def create_scraper_course(coursecode, crstype, campus_code):
    scraper_course.set(coursecode+crstype+campus_code)

def show_search_results(scraped):
    frame4.grid(row=4,column=0,pady=(10,10))
    try:
        index = 0
        while index < len(scraped):
            scraped[index] = scraped[index][8:]
            scraped[index] = scraped[index].split("|")
            index += 1  
        for item in range(len(scraped)):
            for nested_item in range(len(scraped[item])):
                scraped[item][nested_item] = scraped[item][nested_item][0]+"EC"+scraped[item][nested_item][1:]
        list_of_sections = scraped
        flat_list = []
        for item in list_of_sections:
            for item2 in item:
                flat_list.append(item2)
    except:
        pass
    search_label.config(text=("Search Results for "+coursecode.get()+" :"))
    search_label.grid(row=0,column=0)
    try:
        search_results.config(text=list_of_sections)
    except:
        pass
    search_results.grid(row=0,column=1)    
    select_section_label.grid(row=1,column=0)
    try:
        select_section.config(values=flat_list)
    except:
        pass
    select_section.grid(row=1,column=1)
    select_lecture_label.grid(row=2,column=0)
    select_lecture.grid(row=2,column=1)
    return scraped

def check_site(event):
    try:
        check_exist = requests.head(url.get())
        if check_exist.status_code == 200:
            visit_link.grid(row=0,column=2)
        else:
            url.set("http://i.imgur.com/3UQqrhO.gif")
            visit_link.grid(row=0,column=2)
    except:
        visit_link.grid(row=0,column=2)        
        

def generate_results(event):
    url_to_visit = make_url(coursecode_sv.get(), crstype.get(), selected_section.get(), select_lecture_sv.get(), year_sv.get(), session.get())
    url.set(url_to_visit)
    check_link.grid(row=0,column=1)

def validate_information(event):
    global progressbar
    progressbar = ttk.Progressbar(orient=HORIZONTAL, length=(frame3.winfo_width()), mode='indeterminate')
    progressbar.grid(sticky=S)
    progressbar.start(10)    
    fix_case_sensitive()
    valid = bool()
    if session.get() in session_options:
        valid = True
    else:
        messagebox.showerror("Session Error", "Please select a valid session"+
                            " from the list")
        valid = False
    
    if (year_sv.get().isdigit()) and (int(year_sv.get()) >= 2000):
        valid = True
    else:
        year_sv.set("IVLD")
        messagebox.showerror("Year Error", "Please enter a valid year >2000")
        valid = False
    cscode = coursecode_sv.get()
    if ((cscode[0:4].isalpha()) and (cscode[4:].isdigit()) and (len(cscode) == 6)):
        valid = True
    else:
        coursecode_sv.set("INVLD")
        messagebox.showerror("Coursecode Error", "Please enter a valid Coursecode"+
                            " in the following format without quotations \"AAAA##\" ie BIOA01")
        valid = False
    if (crstype.get() in crstype_options):
        valid = True
    else:
        messagebox.showerror("Course Type Error", "Please select a valid Course Type")    
        valid = False
    if (valid and (offline_sv.get() is False)):
        try:
            create_scraper_course(coursecode.get(), crstype.get(), CAMPUS_CODE)
            list_of_sections = scraper.scrape_site(scraper_course.get(), year_sv.get(), session.get())
            list_of_sections = show_search_results(list_of_sections)
        except:
            list_of_sections = show_search_results(list_of_sections)
        show_generate_link()
    progressbar.stop()
    progressbar.grid_remove()

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
    # Add a 0 to the lecture
    if int(lecture) in range(10):
        lecture = "0" + lecture
    # Checks if there is more than one prof teaching that lecture section
    if (len(search_results.cget('text')) <= 1) or (one_section_sv.get() == 'Yes'):
        section = ""
    # Executes if the section is not a blank string and adds an underscore to
    # the front of the section number
    if (section != ""):
        section = "_" + section[-1]
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

def offline_version(event):
    offline_sv.set(True)
    title_label.config(text='Lemmy The Lemon v1.0.0 GUI - Offline')
    messagebox.showinfo("Offline Version Info","Please enter your lecture"+
                        " section in the form of LECXX ie.LEC01 and"+
                        " the lecture number as an integer ie. 1,2,3, etc"+
                        ". The dropdown menus have been made editable so"+
                        " that the information can be entered manually")
    search_course.grid_remove()
    validate_information(event)
    select_section.config(state='normal')
    select_lecture.config(state='normal')
    one_section_label.grid(row=3,column=0)
    one_section.grid(row=3,column=1)
    show_search_results(list())
    show_generate_link()

def open_url(event):
    url_to_visit = url.get()
    if url_to_visit == "http://i.imgur.com/3UQqrhO.gif":
        mixer.music.play(-1)
    frame7.grid(row=20, pady=(10,0))
    leave_feedback.grid()    
    webbrowser.open(url_to_visit, new=0, autoraise=False)    

def leave_feedback_typeform(event):
    url_to_open = 'https://lilmoh17.typeform.com/to/zhxVhz'
    webbrowser.open(url_to_open, new=0, autoraise=False)    

CAMPUS_CODE = str(3)
    
root = Tk()
root.title("Lemmy The Lemon v1.0.0 GUI")
root.config(bg='#212121')
root.iconbitmap('resources/ismailmohammad_icon.ico')
root.geometry('{}x{}'.format(692, 600))
root.resizable(0,0)

# Initialize pygame mixer
mixer.init()
# Load up the No Linky Mp3
mixer.music.load('resources/no_linky.mp3')

# This is the start of Frame 1 within the design of the Application
# Within Row 0, Column 0 of root

frame1 = Frame(root,bg='white')
frame1.grid(row=0,column=0,sticky=W+E)

lemmy_image = PhotoImage(file="resources/ismailmohammad_logo.png")
label = Label(frame1,image=lemmy_image,cursor='hand2',bg='white')
label.grid(row=0,column=0,padx=(5,20))
label.bind("<Button-1>", openWebSite)

lemmy_image2 = PhotoImage(file="resources/the_lemon.png")
label2 = Label(frame1, image=lemmy_image2,cursor='hand2',bg='white')
label2.grid(row=0,column=2, padx=(20,25))
label2.bind("<Button-1>", openGitHub)

welcome_text = "Welcome enlightened one, case not sensitive is the message\n\n"
disclaimer_text =("Disclaimer: This program was only made for educational" +
             " purposes \n ONLY and I am not resposible for how you use it.\n" +
             "or if you use it at all, please do so only for classes you are" +
             " registered in\n\nYou have been duly warned!")
welcome_disc = Label(frame1, text=welcome_text+disclaimer_text)
welcome_disc.config(font=("Arial", 10),bg='white')
welcome_disc.grid(row=0,column=1)

# This is the start of Frame 2 within the design of this application
# Within Row 1, Column 0 of root

frame2 = Frame(root,bg='#212121')
frame2.grid(row=1,column=0,pady=(10,0))
title_text = "Lemmy the Lemon v1.0.0 GUI"
title_label = Label(frame2,text=title_text,bg='#212121',fg='white')
title_label.config(font=("Arial Black", 20))
title_label.grid(row=0,column=0)



# This is the start of Frame 3 within the design of this application
# Within Row 2, Column 0 of root

frame3 = Frame(root,bg='#BDBDBD')
frame3.grid(row=2,column=0,pady=(10,10))

# Various Labels for Entry Fields
year_lbl = Label(frame3, text="Year: ", justify=LEFT,bg='#BDBDBD')
year_lbl.grid(row=0,column=0,sticky=E)

session_lbl = Label(frame3, text="Session: ",justify=LEFT,bg='#BDBDBD')
session_lbl.grid(row=1,column=0,sticky=E)

coursecode_lbl = Label(frame3, text="Coursecode: ",justify=LEFT,bg='#BDBDBD')
coursecode_lbl.grid(row=2,column=0,sticky=E)

crstype_lbl = Label(frame3, text="Course Type: ",justify=LEFT,bg='#BDBDBD')
crstype_lbl.grid(row=3, column=0,sticky=E)

# Various Entry Fields

year_sv = StringVar()
year_sv.trace("w", lambda name, index, mode, sv=year_sv: limit_to_this(sv, 4))
year = Entry(frame3, textvariable=year_sv,bg='#BDBDBD',relief=FLAT)
year.grid(row=0,column=1,sticky=W)
year.focus_set()

session_options = ['Fall','Winter','Summer']
session = StringVar()
session.set("Fall") # Set Default option to Fall
session_list = ttk.Combobox(frame3,textvariable=session,state='readonly')
session_list['values'] = session_options
session_list.grid(row=1,column=1,sticky=W)

coursecode_sv = StringVar()
coursecode_sv.trace("w", lambda name, index, mode, sv=coursecode_sv: limit_to_this(sv, 6))
coursecode = Entry(frame3, textvariable=coursecode_sv, bg='#BDBDBD', relief=FLAT)
coursecode.grid(row=2,column=1, sticky=W)

crstype = StringVar()
crstype_options = ['H','Y']
crstype.set('H') # Set Default to 
crstype_list = ttk.Combobox(frame3, textvariable=crstype, state='readonly')
crstype_list['values'] = crstype_options
crstype_list.grid(row=3,column=1,sticky=W)

search_image = PhotoImage(file='resources/search_course.png')
search_course = ttk.Button(frame3, image=search_image)
search_course.bind("<Button-1>", validate_information)
search_course.grid(row=20,column=0)

scraper_course = StringVar()

clear_img = PhotoImage(file="resources/clear_input.png")
clear_info = ttk.Button(frame3, image=clear_img)
clear_info.bind("<Button-1>",clear_input_values)
clear_info.grid(row=20,column=1)

# This is the start of frame4

frame4 = Frame(root,bg='#BDBDBD')

list_of_sections = []
search_label = Label(frame4, bg='#BDBDBD')
search_results = Label(frame4, bg='#BDBDBD')

select_section_label = Label(frame4,
                             text=("Choose the smaller value"+
                                   " within the Lecture Section Group: "),
                             bg='#BDBDBD')
selected_section = StringVar()
select_section = ttk.Combobox(frame4, textvariable=selected_section, state='readonly')

select_lecture_label = Label(frame4, text="Choose Lecture to View:",bg='#BDBDBD')
select_lecture_sv = StringVar()
select_lecture_sv.set("1") # Set Default Lecture to '1'
lecture_options = []
for lecture in range(1,73):
    lecture_options.append(str(lecture))
select_lecture = ttk.Combobox(frame4, textvariable=select_lecture_sv, values=lecture_options,state='readonly')

one_section_label = Label(frame4,text="Is there only one WebOptioned section? ",bg='#BDBDBD')
one_section_options = ['Yes','No']
one_section_sv = StringVar()
one_section_sv.set(one_section_options[1])
one_section = ttk.Combobox(frame4,textvariable=one_section_sv, values=one_section_options, state='readonly')

url = StringVar()

# This is Frame 5 of the application
frame5 = Frame(root,bg='#BDBDBD')

gen_img = PhotoImage(file="resources/generate_link.png")
generate_link = ttk.Button(frame5, image=gen_img)
generate_link.bind("<Button-1>", generate_results)

visit_img = PhotoImage(file="resources/visit_link.png")
visit_link = ttk.Button(frame5, image=visit_img)
visit_link.bind("<Button-1>", open_url)

check_img = PhotoImage(file="resources/check_link.png")
check_link = ttk.Button(frame5, image=check_img)
check_link.bind("<Button-1>", check_site)

# This is Frame 6 of the application
frame6 = Frame(root,bg='#BDBDBD')
frame6.grid(row=3,column=0)
offline_sv = BooleanVar()
offline_sv.set(False)
offline_img = PhotoImage(file='resources/offline_version.png')
offline_button = ttk.Button(frame6, image=offline_img)
offline_button.bind('<Button-1>', offline_version)
offline_button.grid(row=0,column=0)

# Frame 7
frame7 = Frame(root,bg='#BDBDBD')
leave_feedback_img = PhotoImage(file='resources/leave_feedback.png')
leave_feedback = ttk.Button(frame7, image=leave_feedback_img)
leave_feedback.bind('<Button-1>', leave_feedback_typeform)

# Mainloops the root variable, or the TK Window
root.mainloop()