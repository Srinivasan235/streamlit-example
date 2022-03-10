import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
stopwords = list(STOP_WORDS)
from heapq import nlargest
nlp = spacy.load('en_core_web_sm')

st.title("Summarize Text")
sentence = st.text_area('Please paste your article :', height=300)
percent = st.slider('Select Max percentage?', 0, 130, 25)
percent = percent/100
button = st.button("Summarize")

doc = nlp(sentence)
tokens = (token.text for token in doc)
punctuation = punctuation + '\n'

word_frequency={}
for word in doc:
    if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation:
            if word.text not in word_frequency.keys():
                word_frequency[word.text] = 1
            else:
                word_frequency[word.text]+=1

max_frequency = max(word_frequency.values())

for word in word_frequency.keys():
    word_frequency[word] = word_frequency[word]/max_frequency


sentence_tokens = [sent for sent in doc.sents]


sentence_score = {}

for sent in sentence_tokens:
    for word in sent:
        if word.text.lower() in word_frequency.keys():
            if sent not in sentence_score.keys():
                sentence_score[sent] = word_frequency[word.text.lower()]
            else:
                sentence_score[sent] += word_frequency[word.text.lower()]



select_length = int(len(sentence_tokens)*percent)
summary = nlargest(select_length,sentence_score,key = sentence_score.get)

with st.spinner("Generating Summary.."):
    if button and sentence:
        values = ','.join(str(v) for v in summary)
        st.write(values)



