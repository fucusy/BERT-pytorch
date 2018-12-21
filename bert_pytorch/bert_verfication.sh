source ../env/bin/activate
python dataset/data/create_pretrain_dataset.py -i ./dataset/data/sample_text.txt -o ./dataset/data/sample_text_for_training.txt
python dataset/vocab.py -c dataset/data/sample_text_for_training.txt -o dataset/data/sample_text_for_training_sentences_vocab.txt
python __main__.py  -c ./dataset/data/sample_text_for_training.txt -v ./dataset/data/sample_text_for_training_sentences_vocab.txt -o /tmp/model.bert.verification.pickle --b 8 --lr 2e-5 -hs 768 -l 12 -a 12 -e 200000000
