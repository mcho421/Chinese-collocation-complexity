import os
from ltp import LTP, StnSplit


def build_dependency_tree(sentence, ltp):
    dependency_tree = {}
    res = ltp.pipeline([sentence], tasks=["cws", "pos", "dep"])

    tokens = res.cws[0]
    pos_tags = res.pos[0]
    heads = res.dep[0]['head']
    labels = res.dep[0]['label']

    for i in range(len(tokens)):
        token = tokens[i]
        pos = pos_tags[i]
        parent = heads[i] - 1
        relate = labels[i]
        dependency_tree[i] = {'token': token, 'pos': pos, 'parent': parent, 'relate': relate}

    return dependency_tree


def text_process(text, ltp):
    sentence_id, text_dict = 0, {}
    paragraphs = text.split('\n')

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if len(paragraph) < 3:
            continue
        sentences = StnSplit().split(paragraph)
        for sentence in sentences:
            if len(sentence) < 3:
                continue

            sentence_id += 1
            worddict = build_dependency_tree(sentence, ltp)
            text_dict[sentence_id] = {'worddict': worddict, 'sentence': sentence}

    return text_dict
