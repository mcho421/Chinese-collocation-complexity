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
            worddict = parse(sentence, ltp)
            text_dict[sentence_id] = {'worddict': worddict, 'sent': sentence}

    return text_dict
