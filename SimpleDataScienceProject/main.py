from matplotlib import figure
from matplotlib.backend_bases import FigureCanvasBase
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure





# Calling the data with built-in function of pandas
df = pd.read_csv('Dataset/GlobalYouTubeStatistics.csv', encoding='unicode_escape')







# # Data Cleaning Process
df = df.fillna('Data not available')
# # Removing duplicates
df = df.drop_duplicates()




# Data that represents only Educational Channels according to category
education_titles = df[df['category'] == 'Education']['Title']
# Data that represents the Countries where educational contents come from
education_countries = df[df['category'] == 'Education']['Country']
# Data to represent the average value of top 10 YouTube channel subscribers
education_subscribers_average = df[df['category'] == 'Education']['subscribers'].head(10).mean()
# Giving the user the distribution of categories of channels on YouTube
channel_types_distribution = df['category'].value_counts(ascending=True)
# Showing the distribution of Countries where the YouTube channels come from
channel_country_distribution = df['Country'].value_counts(ascending=False)
# Getting top 10 YouTube channels to show brief information
top10 = df.head(10)






#Dropping duplicates to avoid same cases 
df = df.drop_duplicates()
#Filling the NA spots with 0
df = df.fillna(0)

# print(df.describe())

# df['category'].value_counts().plot(kind='bar')
# plt.show()






# Creating the root of Tkinter UI
master = Tk()
master.geometry("1000x800")
master.title ("Global YouTube Giants")
master.minsize(600,600)
# My logo somehow did not show up though
master.iconbitmap("logo.ico")
master.config(background="lightblue")
frame = Frame(master)
frame.pack()
# Trying to show the user what this application does in a plain text
label_title = Label(master, text="Learn about Educational Channels on YouTube",font=("Arial",30), bg='lightblue',fg='white')
label_title.pack()

# Creating a scrollbar for my listbox
scrollbar = tk.Scrollbar(master, width=20)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)


listbox = tk.Listbox(master,width=40,height=40)
listbox.pack(fill=tk.BOTH, side=tk.LEFT
             )
scrollbar.config(command=listbox.yview)
scrollbar.config()

# Function for asking the user for confirmation when whether he really wants to quit.
def on_closing():
    confirm_window = tk.Toplevel(master)
    confirm_window.title("Confirmation")
    confirm_window.geometry("300x200")

    label = tk.Label(confirm_window, text="Are you sure you want to quit?")
    label.pack(padx=20, pady=10)

    quit_button = tk.Button(confirm_window, text="Quit", command=master.destroy)
    quit_button.pack(padx=20, pady=5)

    cancel_button = tk.Button(confirm_window, text="Cancel", command=confirm_window.destroy)
    cancel_button.pack(padx=20, pady=5)

    # Disable closing the main window until user confirms in the confirmation window
    master.attributes("-disabled", True)

    # Re-enable the main window upon closing the confirmation window
    def enable_main_window():
        master.attributes("-disabled", False)

    confirm_window.protocol("WM_DELETE_WINDOW", enable_main_window)

    confirm_window.grab_set()  # To make the confirmation window modal


master.protocol("WM_DELETE_WINDOW", on_closing)

# Assigning a none value for canvas for later control use of it
current_canvas = None

# A function to show the user basic info of the dataset
def show_brief_information():
     rank = df['rank']
     youtubers = df['Youtuber']
     subscribers = df['subscribers']

     for i, (youtuber, subscriber_count, rank) in enumerate(zip(youtubers, subscribers, rank)):
            if i <= 5:  # Stop after the fifth iteration
               listbox.insert(tk.END, f'Rank : {rank}, Youtuber: {youtuber}, Subscribers: {subscriber_count}')


# Showing the user the average subscriber number of top 10 YouTube Channels
def show_average_of_top10_channel_subscribers():
     listbox.insert(0,education_subscribers_average)
# Sorting out all the educational channels from the dataset
def show_ecudaction_channels():
        for title in education_titles:
          listbox.insert(0,title)


#Shows how many channels are from which country in top 1000 YouTube channels
def show_by_country():
     # This function has been created to make sure that the info list is iterated through and we have the correct formed list
     for index, (country, count) in enumerate(channel_country_distribution.items()):
              listbox.insert(index, f"{country}: {count}")

# Function to show min/max number of Subscribers
def find_min_max():
    column = 'subscribers'  # Getting my column name for later use
    max_value = df['subscribers'].max()
    min_value = df['subscribers'].min()
    listbox.insert(0,
                   f'Max Value of {column} is,{max_value}',
                   f'Min Value of {column} is,{min_value}')

# This function shows the distribution 
def show_channel_distribution():


    global current_canvas
    # Deleting the current canvas if it exists
    if current_canvas:
        current_canvas.get_tk_widget() 
    categories_counts = df['channel_type'].value_counts()


    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.pie(categories_counts.head(10), labels=None, autopct='%1.1f%%', startangle=140)
    ax.legend(categories_counts.head(10).index, loc='upper right')
    ax.set_title('Top 10 Channel Types Distribution', fontsize=14)
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    # Changing the canvas to the current so my pie chart do not override each other when called
    current_canvas = canvas


def show_country_distribution():
        
    global current_canvas
    # Deleting the current canvas if it exists here
    if current_canvas:
        current_canvas.get_tk_widget().destroy()
        
        categories_counts = df['Country'].value_counts()
        fig2 = Figure(figsize=(8, 6))
        ax2 = fig2.add_subplot(111)
        ax2.pie(categories_counts.head(10), labels=None, autopct='%1.1f%%', startangle=20)
        ax2.legend(categories_counts.head(10).index, loc='upper right')
        ax2.set_title('Distribution of channels by Countries', fontsize=14)
        ax2.axis('equal')



        canvas = FigureCanvasTkAgg(fig2, master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        # Changing the canvas to the current so my pie chart do not override each other when called
        current_canvas = canvas
      
# Here are the prompts that the user can give
options_columns = {
    "Brief description": show_brief_information,
    "Show Average Subscribers of Top10 Channels": show_average_of_top10_channel_subscribers,
    "Show Education Channels": show_ecudaction_channels,
    "Show Distribution by Country": show_by_country,
    "Show Min/Max for Subsribers": find_min_max,
    "Show Channel Type Distribution": show_channel_distribution,
    "Show Channel Country Distribution": show_country_distribution

}

options = list(options_columns.keys())
combobox = ttk.Combobox(master, values=options, width=70)
combobox.set("Choose one option")
combobox.pack(padx=10, pady=10)
category_var = tk.StringVar(master)

# This function lets the user choose an option from the combobox and see what he chooses
def chooseOption():
    # Getting the input from the user with the UI here
    selectedOption = combobox.get()
    if selectedOption in options_columns:
        options_columns[selectedOption]()
    else:
        return "error"
# Here is the button to do the command the user confirms
button = Button(master, text="Show results", padx=10, pady=10, command=chooseOption, width="20")
button.pack(padx=10, pady=10)


master.mainloop()








