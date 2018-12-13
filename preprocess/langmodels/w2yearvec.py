from collections import defaultdict
import pickle
from math import log
import numpy as np


DENOISING_CUTOFF = 5

def dump_w2yv(word2YearVec, file):

    for i in word2YearVec:
        file.write(i + "++||++" + str(word2YearVec[i]) + '\n')

def load_w2yv(file):
    word2YearVec = defaultdict(list)
    for i,l in enumerate(file):
        key = l.split('++||++')[0]
        vals = []
        for ent in l.split('++||++')[1][1:-2].split(','):
            if ent:
                vals.append(float(ent))
        word2YearVec[key] = vals
    return word2YearVec


if __name__ == "__main__":

    LEN_YEAR_VECTOR = 1019
    year_book = pickle.load(open('../../data_sets/year_book.pickle', 'rb'))
    word2YearVec = defaultdict(list)            # { word -> LIST(year_i -> REAL) }
    totalYearCounts = defaultdict(int)          # { year -> int_tot_wrd_count }

    for year, year_page in enumerate(year_book):
        for word, count in year_page.items():
            try:
                word2YearVec[word][year] = count
            except IndexError:
                for i in range(LEN_YEAR_VECTOR):
                    word2YearVec[word].append(0.0)
                word2YearVec[word][year] = count
            totalYearCounts[year] += count
    word2YearVec = dict(word2YearVec) #from default dict to dict




    #normalize within word
    for i, word in enumerate(word2YearVec):
        _sum_ = 0.0
        for y in range(LEN_YEAR_VECTOR):
            word2YearVec[word][y] /= totalYearCounts[y] if totalYearCounts[y] else 1
            _sum_ += word2YearVec[word][y]

        for y in range(LEN_YEAR_VECTOR):
            word2YearVec[word][y] /= _sum_



    print("creating mapping")
    map = {x:i for i, x in enumerate(word2YearVec.keys())}
    print("creating vals")
    vecs = np.asarray(list(word2YearVec.values()))
    print('pickling')
    pickle.dump(map, open('w2yv_dict_wordnormalized.pickle', 'wb'))
    print('npy saving')
    np.save(open('w2yv_vals_wordnormalized.npy', 'wb'), vecs)
