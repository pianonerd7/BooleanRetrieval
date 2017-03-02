OPERATORS = { "(" : 0, ")" : 0, "NOT" : 1, "AND" : 2, "OR" : 3 }

def query_from_file_to_array(query_file_path):
    queries = []
    with open(query_file_path, mode="r") as qf:
        for line in qf:
            query = line
            if line[-1:] == "\n":
                query = line[:-1]
            queries.append(query)
    print (queries)
    
    for q in queries:
        string_to_word_arr(q)

def string_to_word_arr(query):
    word_arr = []

    for word in query.split():
        if word[0] == "(":
            word_arr.append("(")
            word_arr.append(word[1:])
        elif word[-1:] == ")":
            word_arr.append(word[:-1])
            word_arr.append(")")
        else:
            word_arr.append(word)

#def query_to_stack_shunting_yard(query):



query_from_file_to_array("queries")
