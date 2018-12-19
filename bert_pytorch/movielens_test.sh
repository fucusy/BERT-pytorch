source ../env/bin/activate
python dataset/data/movielens_corpus.py -m ./dataset/data/ml-100k -o ./dataset/data/
cat dataset/data/train_sentences.txt >> dataset/data/movielens100k_sentences.txt
cat dataset/data/test_sentences.txt >> dataset/data/movielens100k_sentences.txt
python dataset/vocab.py -c dataset/data/movielens100k_sentences.txt -o dataset/data/movielens100k_sentences_vocab.txt
python __main__.py -c ./dataset/data/train_sentences.txt -v ./dataset/data/movielens100k_sentences_vocab.txt -o /tmp/model.movielens100k.pickle --b 32 --lr 100
