from bs4 import BeautifulSoup
from pathlib import Path 
import spacy

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

import multiprocessing as mp

import time
import os

sp = spacy.load('en_core_web_sm')
sp.max_length = 30000000

def extract_word(one_file):
    with open(one_file, "rb") as f:
        soup = BeautifulSoup(f, "html.parser")
        text = soup.get_text()
    doc = sp(text)
    clean = "" 
    for word in doc:
        if word.pos_ in ['ADJ', 'NOUN', 'PROPN']:
            clean = " ".join((clean, word.text.lower()))
    return clean

if __name__ == "__main__":
    tic = time.perf_counter()
    user_name = os.getlogin()
    print("Using user name: {}".format(user_name))

    user_dir = "C:\\Users\\"
    mail_dir = "AppData\\Local\\Packages\\microsoft.windowscommunicationsapps_8wekyb3d8bbwe" \
                "\\LocalState\\Files\\S0\\"
    mail_sub_dir = "1\\EFMData\\"

    mail_full_dir = Path().joinpath(user_dir, user_name, mail_dir, mail_sub_dir)
    print("Searching directory path: {}".format(mail_full_dir))

    files = Path(mail_full_dir).glob("*.dat")
    files = list(files)
    print("Files: {}".format(len(files)))

    num_cores = mp.cpu_count()
    print(f"Num cores: {num_cores}")

    results = []
    with mp.Pool(processes=num_cores) as p:
        results += p.map(extract_word, [file for file in files])
    clean = " ".join(results)

    wordcloud = WordCloud(stopwords=STOPWORDS).generate(clean)

    toc = time.perf_counter()
    print(f"Completed in {toc - tic:0.4f} seconds")

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

