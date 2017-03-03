import getopt
import sys
import pickle
from queryParser import *
from node import Node

def read_dictionary_to_memory(dictionary_file_path):
    dictionary = None
    with open(dictionary_file_path, mode="rb") as df:
        dictionary = pickle.load(df)
        print (dictionary)
    return dictionary

def find_posting_in_disk(dictionary, term, posting_file_path):
    with open(posting_file_path, mode='rb') as pf:
        if term in dictionary:
            pf.seek(dictionary[term].get_pointer())
            return pickle.loads(pf.read(dictionary[term].length))
        else:
            return []

def process_queries(dictionary_file, postings_file, query_file_path, output_file_of_results):
    dictionary = read_dictionary_to_memory(dictionary_file)
    infix_arr = query_file_to_infix(query_file_path)

    for infix in infix_arr:
        results = process_query(infix, dictionary, postings_file)
        write_to_output(results, output_file_of_results)

def write_to_output(results, output_file_of_results):
    print ("result", results)
   # with open(output_file_of_results, mode="wb") as of:
    #    for result in results:
    #        of.write(result)

def process_query(infix_arr, dictionary, posting_file_path):
    result_cache = infix_arr
    final_result = []

    if len(infix_arr) == 1:
        return find_posting_in_disk(dictionary, infix_arr[0], posting_file_path)

    while len(result_cache) > 1:
        result_cache, final_result = process_query_rec(result_cache, dictionary, posting_file_path)
    
    print (final_result)
    return final_result

def process_query_rec(infix_arr, dictionary, posting_file_path):
    if len(infix_arr) == 1:
        return find_posting_in_disk(dictionary, infix_arr[0], posting_file_path)

    result_cache = infix_arr
    final_result = []

    for i in range(0, len(result_cache)):
        item = result_cache[i]
        if type(item) != list and item in OPERATORS:
            first = second = None
            #if item == "NOT":
                
            if item == "AND":
                if type(result_cache[i-2]) == str:
                    first = find_posting_in_disk(dictionary, result_cache[i-2], posting_file_path)
                else:
                    first = result_cache[i-2]
                if type(result_cache[i-1]) == str:
                    second = find_posting_in_disk(dictionary, result_cache[i-1], posting_file_path)
                else:
                    second = result_cache[i-1]
                temp_result = and_operator(first, second)

                new_cache = []
                if i-2 > 0 or i+1 < len(result_cache):
                    wrap_list = [temp_result]
                    new_cache = wrap_list
                    if i-2 > 0:
                        new_cache= result_cache[:i-2] + new_cache
                    if i+1 < len(result_cache):
                        new_cache = new_cache + result_cache[i+1:]
                    result_cache = new_cache
                    break
                else:
                    final_result = temp_result
                    result_cache = []
                    break
                #result_cache = new_cache
            elif item == "OR":
                if type(result_cache[i-2]) == str:
                    first = find_posting_in_disk(dictionary, result_cache[i-2], posting_file_path)
                else:
                    first = result_cache[i-2]
                if type(result_cache[i-1]) == str:
                    second = find_posting_in_disk(dictionary, result_cache[i-1], posting_file_path)
                else:
                    second = result_cache[i-1]
                temp_result = or_operator(first, second)

                new_cache = []
                if (i-2 > 0) or (i+1 < len(result_cache)):
                    wrap_list = [temp_result]
                    new_cache = wrap_list
                    if i-2 > 0:
                        new_cache=result_cache[:i-2] + new_cache
                    if i+1 < len(result_cache):
                        new_cache = new_cache + result_cache[i+1:]
                    result_cache = new_cache
                    break
                else:
                    final_result = temp_result
                    result_cache=[]
                    break
                #result_cache = new_cache
    print (final_result)
    return result_cache, final_result
    
#bill OR Gates AND (vista OR XP) AND NOT mac
def and_operator(list1, list2):
    return list(set(list1).intersection(list2))

def or_operator(list1, list2):
    return list(set().union(list1, list2))
'''
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

'''
#diction = read_dictionary_to_memory("df")
#find_posting_in_disk(diction, "directors", "pf")
process_queries("df", "pf", "queries", "RESULT")
