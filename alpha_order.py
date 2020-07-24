''' Find the order of an alphabet given a list of words in alphabetical
order. If insufficient information is provided, it returns None '''

def order(words):
    ''' Construct a graph where nodes are the letters in 'words' and edges
    point from any given letter (except the last in each word) to the
    following letter. Pass a set of all letters found and the graph to
    'helper()'. The return value of 'helper()' is then returned '''
    graph = dict()
    letters = set()
    for w in words:
        for i, c in enumerate(w[:-1]):
            next_letter = w[i+1]
            if next_letter == c:
                continue
            if c in graph:
                graph[c].add(next_letter)
            else:
                graph[c] = {next_letter}
            letters.add(c)
        letters.add(w[-1])
    return helper(letters, graph)

def helper(letters, graph, order=''):
    ''' Recursively finds the order of the alphabet represented by 'graph'
    and 'letters'. Operates based off the following idea: each letter will
    not be referenced by any of the alphabetically proceeding letters, thus
    one can determine which letter is missing, add it to 'order', remove it
    from 'graph' and 'letters', and run 'helper()' with the updated
    parameters. Once 'letters' is empty, it returns 'order'. If more than one
    letter is not referenced by the remaining letters, it immediately returns
    None '''
    found = set()
    for nodes in graph.values():
        found.update(nodes)
    not_found = letters.difference(found)
    length = len(not_found)
    if length == 0 or length > 1:
        return None
    next_node = not_found.pop()
    letters.remove(next_node)
    if not letters:
        return order+next_node
    del graph[next_node]
    return helper(letters, graph, order+next_node)
