import os
from ltp import LTP, StnSplit


def parse(sent, ltp):
    d = {}
    res = ltp.pipeline([sent], tasks=["cws", "pos", "dep"])

    wordlist = res.cws[0]
    postags = res.pos[0]
    heads = res.dep[0]['head']
    labels = res.dep[0]['label']

    for i in range(len(wordlist)):
        token = wordlist[i]
        pos = postags[i]
        parent = heads[i] - 1
        relate = labels[i]
        d[i] = {'cont': token, 'pos': pos, 'parent': parent, 'relate': relate}

    return d


def text_process(text, ltp):
    sentence_id, text_dict = 0, {}
    paras = text.split('\n')

    for para in paras:
        para = para.strip()
        if len(para) < 3:
            continue
        sents = StnSplit().split(para)
        for sent in sents:
            if len(sent) < 3:
                continue

            sentence_id += 1
            worddict = parse(sent, ltp)
            text_dict[sentence_id] = {'worddict': worddict, 'sent': sent}

    return text_dict
