from re import sub
import pysrt
import spacy
from lxml import etree

# Input: .srt file
# Output: single string containing all text from .srt file
def subs_to_string(file_path):
  subs = pysrt.open(file_path)
  text_list = []

  for sub in subs:
      text_list.append(sub.text)

  text = " ".join(text_list)
  return text


# parse words with spacy, remove punctuation
def parse_words(text):
  nlp = spacy.load('ja_core_news_sm')
  doc = nlp(text)

  parsed_words = []

  for token in doc:
      if((not token.is_stop) and (not token.is_digit) and (not token.is_punct) and (not token.is_space) and (token.lemma_ != '～') and (token.lemma_ != '♪')):
          parsed_words.append(token.lemma_)
  
  return parsed_words


# Remove words present in given file
def filter_words(word_list, filter_file_path):
  filtered_words = []

  with open(filter_file_path) as file:
      contents = file.read()
      for word in word_list:
          if(word not in contents):
              filtered_words.append(word)
  
  return filtered_words


# Remove word duplicates
def remove_dups(word_list):
  unique_words = set(word_list)
  return unique_words


# Parse dictionary
def parse_dictionary_jp():
  dictionary_path = 'dictionaries/JMdict_e.xml'
  return etree.parse(dictionary_path)


# Define and print words in Quizlet format (Japanese)
def define_words_quizlet_jp(word_list):
  tree = parse_dictionary_jp()
  
  for element in tree.findall("./entry/k_ele/keb"):
      if(element.text in word_list):
          print(element.text, end=" ")
          
          prononciation = element.getparent().getparent().findall('./r_ele/reb')[0]
          print("(" + prononciation.text + ")", end=", ")
          
          english_trans = element.getparent().getparent().findall('./sense/gloss')[0]
          print(english_trans.text)


# Define and print words in Quizlet format (Japanese)
def define_words_anki_jp(word_list):
  tree = parse_dictionary_jp()

  for element in tree.findall("./entry/k_ele/keb"):
    if(element.text in word_list):
        print(element.text, end=", ")
        
        prononciation = element.getparent().getparent().findall('./r_ele/reb')[0]
        print(prononciation.text, end=", ")
        
        english_trans = element.getparent().getparent().findall('./sense/gloss')[0]
        print(english_trans.text)


def main():
  # FILL IN WITH OWN FILE PATHS
  subtitle_file_path = 'data/test.srt'
  filter_words_file_path = 'data/test_filter.txt'

  text = subs_to_string(subtitle_file_path)
  parsed_words = parse_words(text)
  filtered_words = filter_words(parsed_words, filter_words_file_path)
  unique_words = remove_dups(filtered_words)
  define_words_quizlet_jp(unique_words)


if __name__ == "__main__":
  main()