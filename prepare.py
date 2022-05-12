import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd
import acquire
from time import strftime


def basic_clean(text):
    """
    Basic cleaning of text
    """
    text = (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("utf-8", "ignore")
    )
    text = re.sub(r"[^\w\s]", " ", text).lower()
    return text


def tokenize(text):
    """
    Tokenize text
    """
    tokenizer = ToktokTokenizer()
    tokens = tokenizer.tokenize(text)
    return tokens


def stem(tokens, use_tokens=False):
    """
    Stem tokens
    """
    stemmer = nltk.PorterStemmer()
    if use_tokens:
        stems = [stemmer.stem(token) for token in tokens]
    else:
        stems = [stemmer.stem(token) for token in tokens.split()]
    string = " ".join(stems)
    return string


def lemmatize(tokens, use_tokens=False):
    """
    Lemmatize tokens
    """
    lemmatizer = nltk.stem.WordNetLemmatizer()
    if use_tokens:
        lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    else:
        lemmas = [lemmatizer.lemmatize(token) for token in tokens.split()]
    string = " ".join(lemmas)
    return string


def remove_stopwords(
    tokens, extra_stopwords=[], exclude_stopwords=[], use_tokens=False
):
    """
    Remove stopwords from tokens
    """
    stop_words = stopwords.words("english")
    stop_words = set(stop_words).union(set(extra_stopwords))
    stop_words = set(stop_words) - set(exclude_stopwords)
    if use_tokens:
        tokens = [token for token in tokens if token not in stop_words]
        return tokens
    else:
        words = tokens.split()
        filtered_words = [word for word in words if word not in stop_words]
        string_without_stopwords = " ".join(filtered_words)
        return string_without_stopwords
