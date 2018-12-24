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
        uid, mid, rating, t = line.strip().split('::')
        uid = int(uid)
        mid = int(mid)
        t = int(t)
        rating = float(rating)
        if rating >= 4:
            if uid in user_id_history:
                user_id_history[uid].append((mid, t))
            else:
                user_id_history[uid] = [(mid, t)]
    sentences = []
    for uid in sorted(user_id_history.keys()):
        sorted_history = sorted(user_id_history[uid], key=lambda x: x[1])
        movieids = [str(x[0]) for x in sorted_history] 
        s = " ".join(movieids) + '\n'
        sentences.append(s)
    return sentences

def build():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--movielens_path", default='./ml-10M100K', type=str)
    parser.add_argument("-o", "--output_path", required=True, type=str)
    args = parser.parse_args()

    train_path = '%s/r1.train' % args.movielens_path
    test_path = '%s/r1.test' % args.movielens_path

    train_sentence_path = '%s/10m_train_sentences.txt' % args.output_path
    with open(train_sentence_path, 'w') as f:
        for line in generate_sentences(train_path):
            f.write(line + '\n')

    test_sentence_path = '%s/10m_test_sentences.txt' % args.output_path
    with open(test_sentence_path, 'w') as f:
        for line in generate_sentences(test_path):
            f.write(line + '\n')

    movie_path = '%s/movies.dat' % args.movielens_path
    vocab_path = '%s/10m_voc_list.txt' % args.output_path
    predefined = ['[UNK]', '[CLS]', '[SEP]', '[MASK]']
    with open(vocab_path, 'w') as f:
        for w in predefined:
            f.write(w + '\n')
        for line in open(movie_path):
            tid, title, genre = line.split("::")
            print(tid)
            f.write(tid + '\n')


if __name__ == '__main__':
    build()
