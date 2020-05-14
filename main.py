import spacy
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from wordcloud import WordCloud

import matplotlib.pyplot as plt

import re

from tkinter import *
from tkinter import filedialog as fd

import docx

filename = str()

def get_text():
    global filename
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def get_filename():
    global filename
    filename = fd.askopenfilename(filetypes=(("DOCX files", "*.docx"),))

root = Tk()

res = StringVar()

def analyze():
    txt = get_text()

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(txt)
    out = "Recognized named entities:\n"
    for ent in doc.ents:
        out += "{} -- {}\n".format(ent.text, ent.label_)

    tokens = nltk.word_tokenize(txt)
    out += "\nSymsets:\n"
    for token in tokens:
        if re.search(r"[A-Za-z]+", token) != None:
            synsets = wn.synsets(token)
            if len(synsets) > 0:
                print(synsets, "\n\n", synsets[0])
                out += "\n{}".format(token)

                if len(synsets[0].lemmas()) > 0:
                    out += "\n -- Lemmas: "
                for lemma in synsets[0].lemmas():
                    out += lemma.name() + '; '

                if len(synsets[0].hyponyms()) > 0:
                    out += "\n -- Hyponyms: "
                for i in synsets[0].hyponyms():
                    out += i.lemma_names()[0] + '; '

                if len(synsets[0].hypernyms()) > 0:
                    out += "\n -- Hypernyms: "
                for j in synsets[0].hypernyms():
                    out += j.lemma_names()[0] + '; '

    res.set(out)
    result_window()

def gen_wordcloud():
    txt = get_text()
    wordcloud = WordCloud(
        relative_scaling=1.0,
    ).generate(txt)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

def result_window():
    children = Toplevel(root)
    children.title('Result')

    text = Text(children, height=20, width=100)
    scroll = Scrollbar(children)
    scroll.pack(side=RIGHT, fill=Y)
    text.pack(side=LEFT, fill=Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    text.insert(END, res.get())

def help_window():
    children = Toplevel(root)
    children.title('Help')

    helpmsg = """
1. Open a docx file
2. Press "Analyze!" button to see all recognized named entities, lemmas, hyponyms and hypernyms.
3. Press "See word cloud" to see word cloud for the document
    """

    text = Text(children, height=20, width=100)
    scroll = Scrollbar(children)
    scroll.pack(side=RIGHT, fill=Y)
    text.pack(side=LEFT, fill=Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    text.insert(END, helpmsg)

root.title("Semantic analyser")
root.geometry("400x300")

help = Button(text="Open file", command=get_filename)
help.place(relx=.5, rely=.1, anchor="c")

help = Button(text="Analyze!", command=analyze)
help.place(relx=.5, rely=.4, anchor="c")

wordc = Button(text="See word cloud", command=gen_wordcloud)
wordc.place(relx=.5, rely=.6, anchor="c")

help = Button(text="Help", command=help_window)
help.place(relx=.5, rely=.9, anchor="c")

root.mainloop()
