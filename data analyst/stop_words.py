# iterate over all the files and sort the .txt files
# read those files and store their stopwords in a set by looping through them
# create a cumulative set of stopwords and use that to filter the content

from pathlib import Path
import os

directory = "C:/Users/HP/OneDrive/Desktop/internship projects/data analyst"
stop_words = set()

def load_stop_word(file_path):
    try:
        with open(file_path, "r", encoding="utf-8",errors="replace") as f:
            for line in f:
                word = line.strip()
                if word:  
                    stop_words.add(word.lower())  # Convert to lowercase 
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Load all .txt files in the directory
if not os.path.exists(directory):
    print(f"Error: Directory '{directory}' does not exist.")
else:
    # Loop through all .txt files in the directory
    for name in os.listdir(directory):
        if name.endswith(".txt"):
            file_path = os.path.join(directory, name)
            print(f"Loading stop words from: {file_path}")  # Debugging
            load_stop_word(file_path)

                

