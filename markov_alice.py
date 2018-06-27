"""Generate Markov text from text files."""

import twitter
from random import choice
import sys
import os


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # your code goes here
    with open(file_path) as file:
        whole_text = file.read()
    return whole_text


def make_chains(text_string, n_gram):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """
    all_words_list = text_string.split()

    chains = {}

    for index in range(len(all_words_list)-n_gram):
        chains.setdefault(tuple(all_words_list[index:n_gram + index]), []).append(
            all_words_list[index + n_gram]
            )
        # chains[(word1, word2)] += [new_value]

    return chains


def make_text(chains, n_gram):
    """Return text from chains."""
    # Get the link randomly from imported dict (key) and add to the list 'words'
    # Choose random word from the list of that keys values, append new word to list
    # New key becomes second word from list and third word from list
    # repeat finding value, then new key (tuple of index -2 and -1)
    # keep going whil the tuple can be found in the dict, if not, stop


    words = []

    while True:
        first_words=(choice(list(chains.keys())))
        if first_words[0][0].isupper():
            break
    words.extend(first_words)
    link = tuple(words[-n_gram:])
    while link in chains and len("".join(words)) < 280:
        words.append(choice(chains[link]))
        link = tuple(words[-n_gram:])
    try:
        while words[-1][-1] not in(".", "!", "?"):
            del words[-1]
    except:
        return make_text(chains, n_gram)
    return " ".join(words)


def tweet(sentence):
    """Tweets the given sentence"""

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print(api.VerifyCredentials())

    status = api.PostUpdate(sentence)
    print(status.text)


input_path = sys.argv[1]
n_gram = int(sys.argv[2])



# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, n_gram)

# Produce random text
random_text = make_text(chains, n_gram)

tweet(random_text)
