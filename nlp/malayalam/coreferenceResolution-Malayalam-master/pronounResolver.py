# code reused with adaptation from https://github.com/cmward/hobbs
import nltk
import queue as Queue
from nltk import Tree
from collections import defaultdict
from basicFunctions import readFromFile, writeToFile

# As per Treebank Dataset #Prospective Error Point
nominal_labels = ["PRP", "NNPS", "NNP", "NNS", "NN"]


def get_pos(tree, node):
    """ Given a tree and a node, return the tree position
    of the node. 
    """

    for pos in tree.treepositions():
        if tree[pos] == node:
            #print('The get_pos function is being called', tree[pos])
            return pos


def get_dom_np(sents, pos):
    """ Finds the position of the NP that immediately dominates 
    the pronoun.

    Args:
        sents: list of trees (or tree) to search
        pos: the tree position of the pronoun to be resolved
    Returns:
        tree: the tree containing the pronoun
        dom_pos: the position of the NP immediately dominating
            the pronoun
    """

    # start with the last tree in sents
    tree = sents[-1]
    # get the NP's position by removing the last element from
    # the pronoun's
    dom_pos = pos[:-1]
    # print(tree[dom_pos])
    return tree, dom_pos


def walk_to_np_or_s(tree, pos, labelToCheck):
    """ Takes the tree being searched and the position from which 
    the walk up is started. Returns the position of the first NP
    or S encountered and the path taken to get there from the 
    dominating NP. The path consists of a list of tree positions.

    Args:
        tree: the tree being searched
        pos: the position from which the walk is started
    Returns:
        path: the path taken to get the an NP or S node
        pos: the position of the first NP or S node encountered
    """

    #print('The walk_to_np_or_s function is being called')
    path = [pos]
    still_looking = True
    while still_looking:
        # climb one level up the tree by removing the last element
        # from the current tree position
        pos = pos[:-1]
        path.append(pos)
        # if an NP or S node is encountered, return the path and pos
        if labelToCheck in tree[pos].label() or tree[pos].label() == "S":
            still_looking = False
    return path, pos


def bft(tree):
    """ Perform a breadth-first traversal of a tree.
    Return the nodes in a list in level-order.

    Args:
        tree: a tree node
    Returns:
        lst: a list of tree nodes in left-to-right level-order
    """
    #print('The bft(tree) function is being called')
    lst = []
    queue = Queue.Queue()
    queue.put(tree)
    while not queue.empty():
        node = queue.get()
        lst.append(node)
        for child in node:
            if isinstance(child, nltk.Tree):
                queue.put(child)
    return lst


def count_np_nodes(tree, labelToCheck):
    """ Function from class to count NP nodes.
    """
    #print('The count_np_nodes(tree) function is being called')
    np_count = 0
    if not isinstance(tree, nltk.Tree):
        return 0
    elif labelToCheck in tree.label() and tree.label() not in nominal_labels:
        return 1 + sum(count_np_nodes(c, labelToCheck) for c in tree)
    else:
        return sum(count_np_nodes(c, labelToCheck) for c in tree)


def check_for_intervening_np(tree, pos, proposal, pro, labelToCheck):
    """ Check if subtree rooted at pos contains at least 
    three NPs, one of which is: 
        (i)   not the proposal,
        (ii)  not the pronoun, and 
        (iii) greater than the proposal

    Args:
        tree: the tree being searched
        pos: the position of the root subtree being searched
        proposal: the position of the proposed NP antecedent
        pro: the pronoun being resolved (string)
    Returns:
        True if there is an NP between the proposal and the  pronoun
        False otherwise
    """

    #print('The check_for_intervening_np function is being called')
    bf = bft(tree[pos])
    bf_pos = [get_pos(tree, node) for node in bf]

    if count_np_nodes(tree[pos], labelToCheck) >= 3:
        for node_pos in bf_pos:
            if labelToCheck in tree[node_pos].label() \
                    and tree[node_pos].label() not in nominal_labels:
                if node_pos != proposal and node_pos != get_pos(tree, pro):
                    if node_pos < proposal:
                        return True
    return False


def traverse_left(tree, pos, path, pro, labelToCheck, check=1):
    """ Traverse all branches below pos to the left of path in a
    left-to-right, breadth-first fashion. Returns the first potential
    antecedent found. 

    If check is set to 1, propose as an antecedent any NP node 
    that is encountered which has an NP or S node between it and pos. 

    If check is set to 0, propose any NP node encountered as the antecedent.

    Args:
        tree: the tree being searched
        pos: the position of the root of the subtree being searched
        path: the path taked to get to pos
        pro: the pronoun being resolved (string)
        check: whether or not there must be an intervening NP 
    Returns:
        tree: the tree containing the antecedent
        p: the position of the proposed antecedent
    """
    #print('The traverse_left function is being called')
    # get the results of breadth first search of the subtree
    # iterate over them
    breadth_first = bft(tree[pos])

    # convert the treepositions of the subtree rooted at pos
    # to their equivalents in the whole tree
    bf_pos = [get_pos(tree, node) for node in breadth_first]

    if check == 1:
        for p in bf_pos:
            if p < path[0] and p not in path:
                if labelToCheck in tree[p].label():  # and match(tree, p, pro)
                    if check_for_intervening_np(tree, pos, p, pro, labelToCheck) == True:
                        return tree, p

    elif check == 0:
        for p in bf_pos:
            if p < path[0] and p not in path:
                if labelToCheck in tree[p].label():  # and match(tree, p, pro)
                    return tree, p

    return None, None


def traverse_right(tree, pos, path, pro, labelToCheck):
    """ Traverse all the branches of pos to the right of path p in a 
    left-to-right, breadth-first manner, but do not go below any NP 
    or S node encountered. Propose any NP node encountered as the 
    antecedent. Returns the first potential antecedent.

    Args:
        tree: the tree being searched
        pos: the position of the root of the subtree being searched
        path: the path taken to get to pos
        pro: the pronoun being resolved (string)
    Returns:
        tree: the tree containing the antecedent
        p: the position of the antecedent
    """

    breadth_first = bft(tree[pos])
    bf_pos = [get_pos(tree, node) for node in breadth_first]

    for p in bf_pos:
        if p > path[0] and p not in path:
            if labelToCheck in tree[p].label() or tree[p].label() == "S":
                if labelToCheck in tree[p].label() and tree[p].label() not in nominal_labels:
                    # if match(tree, p, pro):
                    return tree, p
                return None, None
            return None, None
        return None, None


def traverse_tree(tree, pro, labelToCheck):
    """ Traverse a tree in a left-to-right, breadth-first manner,
    proposing any NP encountered as an antecedent. Returns the 
    tree and the position of the first possible antecedent.

    Args:
        tree: the tree being searched
        pro: the pronoun being resolved (string)
    """

    #print('The traverse_tree function is being called')
    # Initialize a queue and enqueue the root of the tree
    queue = Queue.Queue()
    queue.put(tree)
    while not queue.empty():
        node = queue.get()
        # if the node is an NP, return it as a potential antecedent
        if labelToCheck in node.label():  # and  match(tree, get_pos(tree,node), pro):
            return tree, get_pos(tree, node)
        for child in node:
            if isinstance(child, nltk.Tree):
                queue.put(child)
    # if no antecedent is found, return None
    return None, None


def walk_to_s(tree, pos):
    """ Takes the tree being searched and the position from which 
    the walk up is started. Returns the position of the first S 
    encountered and the path taken to get there from the 
    dominating NP. The path consists of a list of tree positions.

    Args:
        tree: the tree being searched
        pos: the position from which the walk is started
    Returns:
        path: the path taken to get the an S node
        pos: the position of the first S node encountered
    """
    #print('The walk_to_s(tree, pos) function is being called')
    path = [pos]
    still_looking = True
    while still_looking:
        # climb one level up the tree by removing the last element
        # from the current tree position
        pos = pos[:-1]
        path.append(pos)
        # if an S node is encountered, return the path and pos
        if tree[pos].label() == "S":
            still_looking = False
    return path, pos


def hobbs(sents, pos, labelToCheck):
    """ The implementation of Hobbs' algorithm.

    Args:
        sents: list of sentences to be searched
        pos: the position of the pronoun to be resolved
    Returns:
        proposal: a tuple containing the tree and position of the
            proposed antecedent
    """

    #print('The Hobbs function is being called')
    # The index of the most recent sentence in sents
    sentence_id = len(sents) - 1

    # The number of sentences to be searched
    num_sents = len(sents)

    # Step 1: begin at the NP node immediately dominating the pronoun
    tree, pos = get_dom_np(sents, pos)

    # String representation of the pronoun to be resolved
    pro = tree[pos].leaves()[0].lower()

    # Step 2: Go up the tree to the first NP or S node encountered
    path, pos = walk_to_np_or_s(tree, pos, labelToCheck)
    #print('Path is',path,'\n POS is' ,pos)

    # Step 3: Traverse all branches below pos to the left of path
    # left-to-right, breadth-first. Propose as an antecedent any NP
    # node that is encountered which has an NP or S node between it and pos
    proposal = traverse_left(tree, pos, path, pro, labelToCheck)
    #print('Proposal is',proposal)

    while proposal == (None, None):
        #print("onto the while loop")
        # Step 4: If pos is the highest S node in the sentence,
        # traverse the surface parses of previous sentences in order
        # of recency, the most recent first; each tree is traversed in
        # a left-to-right, breadth-first manner, and when an NP node is
        # encountered, it is proposed as an antecedent
        if pos == ():
            #print('Proposal is',proposal)
            # go to the previous sentence
            sentence_id -= 1
            # if there are no more sentences, no antecedent found
            if sentence_id < 0:
                return None, None
            # search new sentence
            proposal = traverse_tree(sents[sentence_id], pro, labelToCheck)
            if proposal != (None, None):
                #print('Proposal is',proposal)
                return proposal

        # Step 5: If pos is not the highest S in the sentence, from pos,
        # go up the tree to the first NP or S node encountered.
        path, pos = walk_to_np_or_s(tree, pos, labelToCheck)

        # Step 6: If pos is an NP node and if the path to pos did not pass
        # through the nominal node that pos immediately dominates, propose pos
        # as the antecedent.
        if labelToCheck in tree[pos].label() and tree[pos].label() not in nominal_labels:
            for c in tree[pos]:
                if isinstance(c, nltk.Tree) and c.label() in nominal_labels:
                    # and match(tree, pos, pro):
                    if get_pos(tree, c) not in path:
                        proposal = (tree, pos)
                        if proposal != (None, None):
                            #print('Proposal is',proposal)
                            return proposal

        # Step 7: Traverse all branches below pos to the left of path,
        # in a left-to-right, breadth-first manner. Propose any NP node
        # encountered as the antecedent.
        proposal = traverse_left(tree, pos, path, pro, labelToCheck, check=0)
        if proposal != (None, None):
            return proposal

        # Step 8: If pos is an S node, traverse all the branches of pos
        # to the right of path in a left-to-right, breadth-forst manner, but
        # do not go below any NP or S node encountered. Propose any NP node
        # encountered as the antecedent.
        if tree[pos].label() == "S":
            proposal = traverse_right(tree, pos, path, pro, labelToCheck)
            #print('Proposal is',proposal)
            if proposal != (None, None):
                return proposal

    return proposal


def resolvePronouns(tokenisedSentances, wordsList, parsableString, pronouns, returnAllCandidates):

    trees = [Tree.fromstring(s) for s in parsableString]
    locativePronouns = ['അവിടെ']

    resolutionSolutions = {}
    for sentanceNo, pronounsList in pronouns.items():
        tempTrees = trees[:sentanceNo + 1]
        pronounMapToSol = defaultdict(list)
        for pronounNo in pronounsList:
            tempList = []
            pro = wordsList[sentanceNo][pronounNo]
            if pro in locativePronouns:
                # We know locative pronouns should be mapped to locations only.
                labelToCheck = "LOCATIVE"
                pos = get_pos(tempTrees[-1], pro)[:-1]
                tree, pos = hobbs(tempTrees, pos, labelToCheck)
                resolved = tree[pos][0]
                if tree is not None:
                    solutionCandidate = str(tree[pos].leaves()[0])
                    tempList.append(solutionCandidate)
                    print(pro + ' in the sentance refers to ' +
                          tokenisedSentances[sentanceNo] + ' refers to ' + solutionCandidate)
                    pronounMapToSol[pronounNo] = tempList
                    continue

            labels = ["NP", "NN"]  # ,"PRN"]

            for label in labels:
                labelToCheck = label
                pos = get_pos(tempTrees[-1], pro)[:-1]
                tree, pos = hobbs(tempTrees, pos, labelToCheck)
                if tree != None:
                    solutionCandidate = str(tree[pos].leaves()[0])
                    tempList.append(solutionCandidate)
                    print(pro + ' in the sentance ' +
                          tokenisedSentances[sentanceNo] + ' refers to ' + solutionCandidate)
                    if returnAllCandidates == False:
                        break
            finalList = list(set(tempList))
            if finalList:
                pronounMapToSol[pronounNo] = finalList
                print('pronounsmapsol ',pronounMapToSol[pronounNo])
        if pronounMapToSol:
            resolutionSolutions[sentanceNo] = dict(pronounMapToSol)
        pronounMapToSol = {}

    return dict(resolutionSolutions)
