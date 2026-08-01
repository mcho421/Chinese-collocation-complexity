import os
from ltp import LTP, StnSplit


def build_dependency_tree(sentence, ltp):
    dependency_tree = {}
    res = ltp.pipeline([sentence], tasks=["cws", "pos", "dep"])

    tokens = res.cws[0]
    pos_tags = res.pos[0]
    heads = res.dep[0]['head']
    relations = res.dep[0]['label']

    for i in range(len(tokens)):
        token = tokens[i]
        pos = pos_tags[i]
        parent = heads[i] - 1
        relation = relations[i]
        dependency_tree[i] = {'token': token, 'pos': pos, 'parent': parent, 'relation': relation}

    return dependency_tree


def split_and_build_dependency_trees(text, ltp):
    sentence_dependency_trees = []

    for paragraph in text.split('\n'):
        paragraph = paragraph.strip()
        if len(paragraph) < 3:
            continue
        for sentence in StnSplit().split(paragraph):
            if len(sentence) < 3:
                continue

            dependency_tree = build_dependency_tree(sentence, ltp)
            sentence_dependency_trees.append({'dependency_tree': dependency_tree, 'sentence': sentence})

    return sentence_dependency_trees
