#!/usr/bin/python
from nltk import word_tokenize
import string
import os
import getopt
import sys
import re
from node import Node

# Find list of unique tokens in all file path with respect to its document ID
def process_documents(file_path):
    tables = []
    for filename in os.listdir(file_path):
        if filename == ".DS_Store":
            continue
        new_file_path = file_path + filename
        tables.append(process_document(new_file_path, int(filename)))
    dictionary = merge_tables(tables)
    printDict(dictionary)

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
    new_dictionary = dict()
    for key in dictionary:
        posting = dictionary[key]
        cur_node = Node(key, len(posting))
        #dictionary[key] = sorted(posting)
        new_dictionary[cur_node] = sorted(posting)
    return new_dictionary

def printDict(dictionary):
    for key in dictionary:
        k = key.term + ", " + str(key.frequency)
        print k, dictionary[key]

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

directory_of_documents = dictionary_file = postings_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        directory_of_documents = a
    elif o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    else:
        assert False, "unhandled option"
if directory_of_documents == None or dictionary_file == None or postings_file == None:
    usage()
    sys.exit(2)

process_documents(directory_of_documents)