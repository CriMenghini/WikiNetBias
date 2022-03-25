import os
import time
import pickle
import argparse
import subprocess
from sys import argv
import multiprocessing as mp
from collections import defaultdict, Counter

import xml.sax

from WikiParserParallel import WikiXmlHandler, parse_dump


parser = argparse.ArgumentParser(description='Process graphs.')
parser.add_argument('--lang', type=str, help='topic name')

args = parser.parse_args()

lang = args.lang
folder = 'data/dumps/batches/'
list_files = [f for f in os.listdir(folder) if f.startswith('{}wiki-20200920-pages-articles-multistream'.format(lang))]

data_files = [(folder+f, 'data/wikipedia_batches/' + f.split('-')[-1][:-4]) for f in list_files]

print(data_files)

n_proc = len(data_files)#mp.cpu_count()
print(n_proc)



processes = []
for raw_data_path, processed_data_path in data_files:
    p = mp.Process(target=parse_dump, args=(raw_data_path, processed_data_path,))
    processes.append(p)
    p.start()