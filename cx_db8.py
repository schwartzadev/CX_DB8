import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import operator
import math
import logging
from sklearn.metrics.pairwise import cosine_similarity

# create logger
logging.basicConfig(format='%(asctime)s %(message)s',)
log = logging.getLogger()
log.setLevel(logging.INFO)

module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]

embed = hub.Module(module_url)

card_tag = ["Jerry Ehman wrote the Wow Siginal"]


card = """
If the evidence gets out to the public while the scientists are still analyzing the signal, Forgan said they could manage the public's expectations by using something called the Rio Scale. It's essentially a numeric value that represents the degree of likelihood that an alien contact is "real." (Forgan added that the Rio Scale is also undergoing an update, and more should be coming out about it in May.)

If the aliens did arrive here, "first contact" protocols likely would be useless, because if they're smart enough to show up physically, they could probably do anything else they like, according to Shostak. "Personally, I would leave town," Shostak quipped. "I would get a rocket and get out of the way. I have no idea what they are here for."

But there's little need to worry. An "Independence Day" scenario of aliens blowing up important national buildings such as the White House is extremely unlikely, Forgan said, because interstellar travel is difficult. (This feeds into something called the Drake Equation, which considers where the aliens could be and helps show why we haven't heard anything from them yet.) [The Father of SETI: Q&A with Astronomer Frank Drake]

Early SETI work
To find a signal, first we have to be listening for it. SETI "listening" is going on all over the world, and in fact, this has been happening for many decades. The first modern SETI experiment took place in 1960. Under Project Ozma, Cornell University astronomer Frank Drake pointed a radio telescope (located at Green Bank, West Virginia) at two stars called Tau Ceti and Epsilon Eridani. He scanned at a frequency astronomers nickname "the water hole," which is close to the frequency of light that's given off by hydrogen and hydroxyl (one hydrogen atom bonded to one oxygen atom). [13 Ways to Find Intelligent Aliens]

In 1977, The Ohio State University SETI's program made international headlines after a project volunteer, Jerry Ehman, wrote, "Wow!" beside a strong signal a telescope there received. The Aug. 15, 1977, "Wow" signal was never repeated, however.
"""

card_words_org = card.split()

ngram_list = []
for i in range(0, len(card_words_org)):
    new_word = card_words_org[i-10:i+10] #make it so that each word takes it's prior words as context as well
    print(new_word)
    new_string = ''
    for word in new_word:
        new_string += word
        new_string += " "
    ngram_list.append(new_string)

card_words = ngram_list
#print(card_words)

def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


def dot_product2(v1, v2):
    return sum(map(operator.mul, v1, v2))


def vector_cos5(v1, v2):
    prod = dot_product2(v1, v2)
    len1 = np.sqrt(dot_product2(v1, v1))
    len2 = np.sqrt(dot_product2(v2, v2))
    return prod / (len1 * len2)


with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    card_tag_embeddings = session.run(embed(card_tag)) #card_tag for user specified
    card_words_embeddings = session.run(embed(card_words))
    #print(cosine_similarity(card_tag_embeddings, card_words_embeddings[0].reshape(1, -1)))
    word_list = []
    count = 0
    token_removed_ct = 0
    for word in card_words_embeddings:
        word = word.reshape(1,-1)
        word_sim = cosine_similarity(card_tag_embeddings, word)
        word_tup = (card_words_org[count], word_sim)
        count += 1
        word_list.append(word_tup)
    sum_str = ""
    removed_str = ""
    for sum_word in word_list:
        if float(sum_word[1]) > 0.25:
            sum_str += str(sum_word[0])
            sum_str += " "
        else:
            token_removed_ct += 1
            removed_str += str(sum_word[0])
            removed_str += " "
    # print(
    print("CARD: ")
    print(card)
    print("GENERATED SUMMARY: ")
    print(sum_str)
    print("tokens removed:" + " " + str(token_removed_ct))
    print("NOT UNDERLINED")
    print(removed_str)


