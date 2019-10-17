"""Transform 1-Billion Google dataset (subset)"""

import os
import numpy as np
from data import preproc as pp


class Transform():

    def __init__(self, source, charset, max_text_length):
        self.source = source
        self.charset = charset
        self.max_text_length = max_text_length
        self.partitions = dict()

    def build(self, only=True):
        m2_list = next(os.walk(self.source))[2]
        lines_en, lines_fr = [], []

        for m2_file in m2_list:
            if "2010" in m2_file and ".en" in m2_file:
                with open(os.path.join(self.source, m2_file)) as f:
                    for line in f:
                        lines_en.append(line)
                    lines_en = list(set(lines_en))[::-1]

            elif "2009" in m2_file and ".fr" in m2_file:
                with open(os.path.join(self.source, m2_file)) as f:
                    for line in f:
                        lines_fr.append(line)
                    lines_fr = list(set(lines_fr))[::-1]

        # if dataset only 'google', english and french will be 70% samples (around 10 M).
        # if dataset is 'all', english and french will be 7% samples (around 1 M).
        # this make a balance samples with the other datasets.
        factor = 0.7 if only else 0.14

        lines_en = lines_en[:int(len(lines_en) * factor)]
        lines_fr = lines_fr[:int(len(lines_fr) * factor)]

        lines = lines_en + lines_fr
        del lines_en, lines_fr

        lines = [y for x in lines for y in pp.split_by_max_length(x, self.max_text_length)]
        lines = [pp.text_standardize(x) for x in lines]
        np.random.shuffle(lines)

        train_i = int(len(lines) * 0.8)
        valid_i = train_i + int((len(lines) - train_i) / 2)

        self.partitions["train"] = lines[:train_i]
        self.partitions["valid"] = lines[train_i:valid_i]
        self.partitions["test"] = lines[valid_i:]
