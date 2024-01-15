import re
from collections import Counter

def my_func():
    '''
    Just a scratch function for testing autoreload.
    '''
    print("all the stuff")
    

def book_words(filepath, split_pat="\W+"):
    """
    Given a `filepath` to a book, split the text into individual words.

    Parameters
    ----------
    filepath : str
        File path to the book.
    split_pat : str, optional
        The regex expression defining each split., by default "\W+"

    Returns
    -------
    list
        list of words, split from the book text.
    """
    with open(filepath, "r") as f:
        book = f.read()
    
    words = re.split(split_pat, book.lower())
    
    return words


def most_common_words(words, n_top=None, stop_words=None):
    """
    Return the `n_top` most common words in a list of `words`

    Parameters
    ----------
    words : list
        list of words to count
    n_top : int, optional
        number of "top" most common words to return, by default None
    stop_words : list, optional
        iterable of stop words to exclude from the most common count, by default None

    Returns
    -------
    list
        list of tuples: (the word, the count), in order of most common to least common.
    """
    if stop_words is not None:
        words = [w for w in words if w not in stop_words]
        
    counter = Counter(words)
    common = counter.most_common(n=n_top)
    
    return common


def check_number(n=3):
    """
    Determines if the input `n` is the number three. If it is, it prints a message.
    """
    # here we're checking the number value for equality to 3
    if n == 3:
        print("it's a three")








