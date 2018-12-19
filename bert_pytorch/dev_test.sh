source ../env/bin/activate
python dataset/vocab.py -c dataset/corpus.small.txt -o dataset/vocab.small.txt
python __main__.py -c ./dataset/corpus.small.txt -v ./dataset/vocab.small.txt -o /tmp/model.pickle --b 1
