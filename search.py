import getopt
import sys
import pickle

def read_dictionary_to_memory(dictionary_file_path):
    dictionary = None
    with open(dictionary_file_path, mode="rb") as df:
        dictionary = pickle.load(df)
        print (dictionary)
    return dictionary

def find_posting_in_disk(dictionary, term, posting_file_path):
    with open(posting_file_path, mode='rb') as pf:
        pf.seek(dictionary[term].get_pointer())
        dta = pickle.loads(pf.read(dictionary[term].length))
        print (dta)
        print (type(dta))
        print (dta[0])

def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

dictionary_file = postings_file = file_of_queries = output_file_of_results = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        output_file_of_results = a
    else:
        assert False, "unhandled option"
if dictionary_file == None or postings_file == None or file_of_queries == None or output_file_of_results == None:
    usage()
    sys.exit(2)
