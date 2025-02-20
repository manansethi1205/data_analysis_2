import os
import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download("punkt_tab")
# Paths
cleaned_dir = "C:/Users/HP/OneDrive/Desktop/internship projects/cleaned_articles"
original_dir = "C:/Users/HP/OneDrive/Desktop/internship projects/scraped_articles"
excel_path = "C:/Users/HP/OneDrive/Desktop/internship projects/data analyst/input.xlsx"
output_excel_path = "C:/Users/HP/OneDrive/Desktop/internship projects/output.xlsx"

# Load positive and negative word lists
def load_word_list(filepath):
    with open(filepath, "r", encoding="ISO-8859-1") as f:
        return {line.strip().lower() for line in f if line.strip()}

positive_words = load_word_list("C:/Users/HP/OneDrive/Desktop/internship projects/positive-words.txt")
negative_words = load_word_list("C:/Users/HP/OneDrive/Desktop/internship projects/negative-words.txt")

# to count personal pronouns
def count_personal_pronouns(text):
    pronoun_pattern = r"\b(I|we|my|ours|us)\b"
    return len(re.findall(pronoun_pattern, text, re.IGNORECASE))

# to count syllables in a word
def count_syllables(word):
    vowels = "aeiouAEIOU"
    count = sum(1 for char in word if char in vowels)

    # Handle special cases (ending in "es" or "ed")
    if word.endswith(("es", "ed")) and len(word) > 2:
        count -= 1
    return max(1, count)  # Ensure at least 1 syllable per word

# Load Excel file
df = pd.read_excel(excel_path)

# Add columns for calculated metrics
df["Positive Score"] = 0
df["Negative Score"] = 0
df["Polarity Score"] = 0.0
df["Subjectivity Score"] = 0.0
df["Average Sentence Length"] = 0.0
df["Percentage of Complex Words"] = 0.0
df["Fog Index"] = 0.0
df["Average Number of Words Per Sentence"] = 0.0
df["Complex Word Count"] = 0
df["Word Count"] = 0
df["Syllable Count Per Word"] = 0.0
df["Personal Pronouns"] = 0
df["Average Word Length"] = 0.0

# Process each cleaned article
for filename in os.listdir(cleaned_dir):
    if filename.endswith(".txt"):
        url_id = filename.split(".")[0]  # Extract URL_ID from filename
        cleaned_path = os.path.join(cleaned_dir, filename)
        original_path = os.path.join(original_dir, filename)  # Uncleaned text

        # Read the cleaned text
        with open(cleaned_path, "r", encoding="utf-8") as f:
            cleaned_text = f.read()

        words = word_tokenize(cleaned_text)  # Tokenize words
        sentences = sent_tokenize(cleaned_text)  # Tokenize sentences

        # Read original text for personal pronoun detection
        with open(original_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        # positive and negative
        positive_score = sum(1 for word in words if word in positive_words)
        negative_score = sum(1 for word in words if word in negative_words)
        
        # Polarity and Subjectivity
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)

        # complex words and syllable count
        num_sentences = len(sentences)
        num_words = len(words)
        num_complex_words = sum(1 for word in words if count_syllables(word) > 2)
        syllable_count_per_word = sum(count_syllables(word) for word in words) / max(1, num_words)

        avg_sentence_length = num_words / max(1, num_sentences)
        percent_complex_words = num_complex_words / max(1, num_words)
        fog_index = 0.4 * (avg_sentence_length + percent_complex_words)
        
        # personal pronoun count
        personal_pronouns = count_personal_pronouns(original_text)

        # average word length
        total_chars = sum(len(word) for word in words)
        avg_word_length = total_chars / max(1, num_words)

        # Update the corresponding row in DataFrame
        df.loc[df["URL_ID"] == url_id, "Positive Score"] = positive_score
        df.loc[df["URL_ID"] == url_id, "Negative Score"] = negative_score
        df.loc[df["URL_ID"] == url_id, "Polarity Score"] = polarity_score
        df.loc[df["URL_ID"] == url_id, "Subjectivity Score"] = subjectivity_score
        df.loc[df["URL_ID"] == url_id, "Average Sentence Length"] = avg_sentence_length
        df.loc[df["URL_ID"] == url_id, "Percentage of Complex Words"] = percent_complex_words
        df.loc[df["URL_ID"] == url_id, "Fog Index"] = fog_index
        df.loc[df["URL_ID"] == url_id, "Average Number of Words Per Sentence"] = avg_sentence_length  # Same as above
        df.loc[df["URL_ID"] == url_id, "Complex Word Count"] = num_complex_words
        df.loc[df["URL_ID"] == url_id, "Word Count"] = num_words
        df.loc[df["URL_ID"] == url_id, "Syllable Count Per Word"] = syllable_count_per_word
        df.loc[df["URL_ID"] == url_id, "Personal Pronouns"] = personal_pronouns
        df.loc[df["URL_ID"] == url_id, "Average Word Length"] = avg_word_length

# Save the updated DataFrame to Excel
df.to_excel(output_excel_path, index=False)

print(f"Text analysis completed! Updated file saved at: {output_excel_path}")
