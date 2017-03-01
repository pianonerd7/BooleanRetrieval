#!/usr/bin/python
from nltk import word_tokenize
import string
import os

# Find list of unique tokens in all file path with respect to its document ID
def process_documents(file_path):
    tables = []
    for filename in os.listdir(file_path):
        if filename == ".DS_Store":
            continue
        new_file_path = file_path + filename
        tables.append(process_document(new_file_path, int(filename)))
    print merge_tables(tables)

def process_document(file, doc_ID):
    content = open(file, "r").read()
    punctuations = list(string.punctuation)
    result = [i for i in word_tokenize(content) if i not in punctuations]

    table = dict()

    for word in result:
        if word not in table:
            table[word] = doc_ID

    return table

def merge_tables(table_array):
    dictionary = dict()
    for table in table_array:
        for key in table:
            if key not in dictionary:
                dictionary[key] = []
            dictionary[key].append(table[key])
    return sort_dictionary(dictionary)

def sort_dictionary(dictionary):
    for key in dictionary:
        posting = dictionary[key]
        dictionary[key] = sorted(posting)
    return dictionary

process_documents("reuters/training/")
