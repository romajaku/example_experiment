import os           # This library(Operating System) allows us to access and create files on the computer)

import platform     # This one is useful when we want the code to run on different operating systems, and the code to account for it

import random       # Helps generate random or pseudorandom numbers

import time         # Allows us to measure times and control the duration of experiment sections
import datetime     # Alternate option with nicer date formatting

import sys          # Can start program with command line variables that change its behaviour (i.e. start it in terminal or command line and specify num of trials

import csv          # Helps read create and edit comma-separated-values files, basically an excel spreadsheet, good for input and output.

from psychopy import visual, core, event, monitors, gui, data # Different functionalities packets from psychopy itself

from PIL import Image                                         # I sometimes use it to make backgrounds for stuff, like image by hex calue and size

from psychopy.constants import STOPPED, PLAYING, FINISHED     # To test if video or audio is playing

from string import ascii_letters, digits                      # These help verify user keyboard inputs


# Initialize PsychoPy window
win = visual.Window(size=(800, 600), color=(1, 1, 1), units='pix')
# Set up path to stimuli folder
stimuli_folder = 'stimuli'  # This folder will contain text, video, and image stimuli
# Set up path to data folder
data_folder = 'data'  # This folder will contain text, video, and image stimuli
# Array for results
results = []
# Another array for stimuli lists. Its order will be randomized for each trial
stimuli = []

def read_stimuli(file = 'texts.csv'):
    file = os.path.join(stimuli_folder, file)
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        stimuli = random.shuffle(list(reader))  # Convert the reader object to a list and randomize order
        print(stimuli)


def display_text(index):
    """Displays the sentence corresponding to the given index from the stimuli.csv file using PsychoPy visual module."""
    if 0 <= index < len(stimuli):
        sentence = stimuli[index]  # Get the ith sentence (first column)        
        # Create a TextStim object to display the sentence
        text_stim = visual.TextStim(win, text=sentence, color=(-1, -1, -1), height=30)
        text_stim.draw()
        win.flip()  # Show the sentence on the screen
        core.wait(2)  # Display for 2 seconds (you can change the duration)
    else:
        print(f"No sentence at index {index}")


def display_image(index, display_duration=2):
    """Displays an image using PsychoPy for the specified duration (in seconds)."""
    try:
        if 0 <= index < len(images_list):
            image_path = stimuli[index]  # Get the ith image path            
            # Create an ImageStim object to display the image
            image_stim = visual.ImageStim(win, image=os.path.join(stimuli_folder, image_path))
            image_stim.draw()
            win.flip()  # Show the image on the screen
            core.wait(display_duration)  # Display the image for the specified duration
            win.flip(clearBuffer=True)  # Clear the window after displaying the image
        else:
            print(f"No image at index {index}")
    except Exception as e:
        print(f"Error displaying image: {e}")


def display_video(index):
    """Displays a video using PsychoPy's MovieStim3."""
    try:
        if 0 <= index < len(videos_list):
            video_path = stimuli[index]  # Get the ith video path            
            # Create a MovieStim3 object to display the video
            movie_stim = visual.MovieStim3(win, filename=os.path.join(stimuli_folder, video_path))
            
            # Play video until it finishes
            while movie_stim.status != visual.FINISHED:
                movie_stim.draw()
                win.flip()
                
            win.flip(clearBuffer=True)  # Clear the window after the video finishes
        else:
            print(f"No video at index {index}")
    except Exception as e:
        print(f"Error displaying video: {e}")


def get_user_feedback():
    """Displays feedback prompt and waits for a valid key press ('1', '2', or '3')."""
    prompt_text = "Press 1, 2, or 3 to respond."
    
    # Create a TextStim object to display the feedback prompt
    prompt_stim = visual.TextStim(win, text=prompt_text, color=(-1, -1, -1), height=30)
    prompt_stim.draw()
    win.flip()  # Show the prompt on the screen
    
    valid_keys = ['1', '2', '3']
    
    while True:
        keys = event.getKeys()  # Wait for key press
        
        if any(key in keys for key in valid_keys):
            response = keys[0]
            print(f"Valid key {response} pressed")
            results.append(response)
            
            # Clear the window after valid input
            win.flip(clearBuffer=True)
            return response  # Return the valid key pressed
        else:
            # If no valid key is pressed, keep displaying the prompt
            prompt_stim.draw()
            win.flip()


def save_results():
    path = 'data'
    if not os.path.exists(path):
        os.makedirs(path)
    date_time_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    with open(f'data/{date_time_str}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in results:
            writer.writerow(row)


def run_trial(i):
    """Runs a single trial: displays the text and captures user feedback."""
    # Display the text for the ith trial
    display_text(i)
    # Get user feedback
    user_response = get_user_feedback()
    # Process or store the user response if needed
    print(f"User selected: {user_response}")


def main_loop(iterations=10):  # Default value set to 10
    read_stimuli()
    for i in range(iterations):
        run_trial(i)
    save_results()
    win.close()  # Close the PsychoPy window after the loop completes
    
# Example usage
main_loop(2)     # This will run the run_trial function 2 times (custom value)