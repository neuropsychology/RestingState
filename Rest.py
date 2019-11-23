# -*- coding: utf-8 -*-
"""
EEG Resting-State procedure.
Authors: Makowski et al.
Copyright: L'École de Neuropsychologie
Site: https://github.com/neuropsychology/RestingState
"""

#==============================================================================
# Load modules
#==============================================================================
import os  # For creating directories
import winsound  # For beeps
import datetime  # Get current time
import pandas as pd  # Dataframe management

import neuropsydia as n  # Load Neuropsydia
import neurokit as nk  # Save data


# =============================================================================
# Parameters
# =============================================================================
language = "en"
testmode = False

# Set duration time (in minutes)
if testmode is True:
    duration = 0.05
else:
    duration = 5



#==============================================================================
# Initialization
#==============================================================================
# Initialize neuropsydia
n.start()
# Display start screen
n.start_screen(name="Rest", language=language)

#Initialize trigger
trigger = n.Trigger(TTL=False, photosensor="black", photosensor_size = 2.5)


# Register the participant
n.newpage("white")
participant_id = n.ask("ID:")
path_participant = "data/" + participant_id
os.mkdir(path_participant)

 # Create empty dictionary for data storing
data = {"Index":{}}


#==============================================================================
# Start
#==============================================================================

# Display instructions
if language == "fr":
    n.instructions("Gardez les yeux fermés pendant toute la durée de la séquence (environ 5 minutes).\nNe pensez à rien de particulier mais essayez de ne pas vous endormir.\nLe début et la fin de la séquence vous seront mentionnés par un bip sonore.")
    n.instructions("Fermez les yeux.", end_text = "Appuyez sur ENTRER pour commencer.")
else:
   n.instructions("Keep your eyes closed during the whole sequence (approximately 5 minutes).\n\nDon't think about anything in particular but simply try to stay awake.\n\nYou will here a beep that will indicate the beginning and the end of the seqence.", end_text = "Press ENTER to continue.")
   n.instructions("Please close your eyes.", end_text = "Press ENTER to start.")



# Display a countdown
n.newpage("grey", auto_refresh=False)
# Maintain the white light for the photosensor
trigger.stop()
n.countdown(sound=True, melody=[1000, 1500])

data["Index"]["Duration"] = duration
# Display a grey screen
data["Index"]["Rest_Start"] = datetime.datetime.now()  # Save start time
n.newpage("grey", auto_refresh=False)  # Grey background
# Trigger the photosensor
trigger.start()
n.refresh()  # Actually render on screen
n.time.wait(duration, unit="min")  # Wait the selected amount of time

# Play a super jingle
for i in [1500, 1000]:
    winsound.Beep(i, 25)


# Subjective Evaluation
data["Index"] = n.resting_state_brief_assessment(data["Index"], test="Rest_", language="en")

data["Index"]["Rest_End"] = datetime.datetime.now()  # Save end time

# Save data
df = pd.DataFrame.from_dict(data, orient="index")  # Transform dictionary to dataframe
df["Participant_ID"] = participant_id
n.save_data(df, filename="Rest", path=path_participant, participant_id=participant_id, index=False)


# Display end screen
n.end_screen(name="Rest", language="en")
n.close()