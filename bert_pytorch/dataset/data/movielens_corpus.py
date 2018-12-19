import pickle
import tqdm
from collections import Counter


def generate_sentences(interaction_path):
    """
    interaction_path: each line in the file contain a tab separated list of
    user id | item id | rating | timestamp.
    The time stamps are unix seconds since 1/1/1970 UTC

    lines: a list of sentences, each sentence is user's >= 4 rated ordered movie ids
    """
    ## $userid -> a list of (movieid, timestamp) which is type (int, int)
    user_id_history = {}
    for line in open(interaction_path, 'r'):
        uid, mid, rating, t = line.strip().split('\t')
        uid = int(uid)
        mid = int(mid)
        t = int(t)
        rating = int(rating)
        if rating >= 4:
            if uid in user_id_history:
                user_id_history[uid].append((mid, t))
            else:
                user_id_history[uid] = [(mid, t)]
    sentences = []
    for uid in sorted(user_id_history.keys()):
        sorted_history = sorted(user_id_history[uid], key=lambda x: x[1])
        movieids = [str(x[0]) for x in sorted_history] 
        mid_idx = int(len(movieids) / 2)
        s = " ".join(movieids[0:mid_idx]) + " \\t " + " ".join(movieids[mid_idx:-1])
        sentences.append(s)
    return sentences

def build():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--movielens_path", default='./ml-100k', type=str)
    parser.add_argument("-o", "--output_path", required=True, type=str)
    args = parser.parse_args()

    train_path = '%s/u1.base' % args.movielens_path
    test_path = '%s/u1.test' % args.movielens_path

    train_sentence_path = '%s/train_sentences.txt' % args.output_path
    with open(train_sentence_path, 'w') as f:
        for line in generate_sentences(train_path):
            f.write(line + '\n')

    test_sentence_path = '%s/test_sentences.txt' % args.output_path
    with open(test_sentence_path, 'w') as f:
        for line in generate_sentences(test_path):
            f.write(line + '\n')

if __name__ == '__main__':
    build()

