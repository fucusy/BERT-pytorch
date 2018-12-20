# encode=utf-8
import random


def generate_sentences(text_path, rng):
    """
    a lot of word in the text_path

    lines: a list of sentences
    """
    max_seq_length = 128
    max_predictions_per_seq = 20
    dupe_factor = 10
    short_seq_prob = 0.1

    all_documents = [[]]
    sentences = []
    for line in open(text_path, 'r', encoding='utf8'):
        line = line.strip()
        if not line:
            all_documents.append([])
        tokens = line.split()
        all_documents[-1].append(tokens)

    rng.shuffle(all_documents)
    for _ in range(dupe_factor):
        for i, document in enumerate(all_documents):
            max_num_tokens = max_seq_length - 3
            target_seq_length = max_num_tokens
            if rng.random() < short_seq_prob:
                target_seq_length = rng.randint(2, max_num_tokens)

            current_chunk = []
            current_length = 0
            j = 0
            while j < len(document):
                segment = document[j]
                current_chunk.append(segment)
                current_length += len(segment)
                if j >= len(document) - 1 or current_length >= target_seq_length:
                    if current_chunk:
                        a_end = 1
                        if len(current_chunk) >= 2:
                            a_end = rng.randint(1, len(current_chunk) - 1)

                        tokens_a = []
                        for k in range(a_end):
                          tokens_a.extend(current_chunk[k])

                        tokens_b = []
                        for k in range(a_end, len(current_chunk)):
                            tokens_b.extend(current_chunk[k])
                        s = ' '.join(tokens_a) + ' \\t ' + ' '.join(tokens_b)
                        sentences.append(s)
                    current_chunk = []
                    current_length = 0
                j += 1
    return sentences

def build():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--input_path", default='./sample_text.txt', type=str)
    parser.add_argument("-o", "--output_path", required=True, type=str)
    parser.add_argument("-r", "--random_seed", required=False, default=12345, type=int)
    args = parser.parse_args()
    rng = random.Random(args.random_seed)
    sentences = generate_sentences(args.input_path, rng)
    with open(args.output_path, 'w', encoding='utf-8') as f:
        for line in sentences:
            f.write(line + '\n')

if __name__ == '__main__':
    build()

