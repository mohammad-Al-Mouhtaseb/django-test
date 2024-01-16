from django.shortcuts import render
from django.http import HttpResponse
import re
import requests
# import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
import collections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel



# Create your views here.
def index(request):
    return render(request,'demoapp/index.html',{"listdocs":"","listdocstitle":""})



def calculate_tfidf_ranking(query, documents):
    # Combine the query and documents
    all_texts = [query] + documents

    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Calculate the cosine similarity between the query and documents
    cosine_similarities = linear_kernel(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Sort the documents based on cosine similarities in descending order
    document_scores = [(index, score) for index, score in enumerate(cosine_similarities, start=1)]
    document_scores.sort(key=lambda x: x[1], reverse=True)

    # Return the sorted document scores
    return document_scores

def searsh(request):
    q=request.GET['q']
    qsplit=[]
    qsplit=[]
    qsplit=q.split("%20")
    qterms=get_terms(qsplit)

    index=[]
    psision=[]

    listdocstitle=[]
    listdocs=[]
    NoMoreTerm=[]
    NoMoreUrl=[]
    tfidf=[]
    
    if len(qterms)>0:
        qpp=pre_process(qterms)

        for t in qpp:
            if t in inverted_index:
                index = index + inverted_index[t]


        for key, value in index:
            if not key in NoMoreTerm:
                if not docstitle[key] in NoMoreUrl:
                    listdocs.append(docs[key])
                    listdocstitle.append(docstitle[key])
                    NoMoreTerm.append(key)
                    NoMoreUrl.append(docstitle[key])
                    psision.append(value)
        
        if len(index)>0:
            for ttt in qpp:
                tfidf+=calculate_tfidf_ranking(ttt,listdocs)
    return render(request,'demoapp/index.html',{"zip":zip(listdocs,listdocstitle,tfidf,psision),"q":q})



visited = []
to_visit = []

def get_new_link():
    if len(to_visit) == 0:
        return None

    link = to_visit.pop()
    while link in visited:
        if not(len(to_visit) == 0):
            link = to_visit.pop()
        else:
            return None
    return link


def get_link_content(url):
    res = requests.get(url)
    return str(res.content)


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_text_from_content(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def extract_links(content):
    links = []
    for link in BeautifulSoup(content, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href') and re.match('^http+', link['href'].lower()):
            links.append(link['href'])
            print('...extracted ',link['href'])
    to_visit.extend(links)



docs = []
docstitle = []

def crawle(url, max_links_num):
    to_visit.append(url)
    for i in range(max_links_num):
        link = get_new_link()
        if not link:
            break
        print('\nsearching in : ',link)
        link_content = get_link_content(link)
        document = get_text_from_content(link_content)
        docs.append(document)
        docstitle.append(link)

        extract_links(link_content)


crawle('https://www.britannica.com/topic/newspaper',6)
crawle('https://github.com/',2)
crawle('https://www.aiu.edu.sy/',1)
crawle('https://www.britannica.com/place/Syria',2)
crawle('https://www.calendardate.com/todays.htm',1)
# crawle('https://stackoverflow.com/questions/',3)



def invalid_token(t):
    en_stopwords = stopwords.words('english')
    return len(t)<2 or '\\' in t or t in en_stopwords

# def pre_process(terms):
#     lemmatizer = WordNetLemmatizer()
#     en_stopwords = stopwords.words('english')

#     terms_2 = [] # with syn (to prevent infinity loop)

#     if type(terms) == list:
#         for i in terms:
#             i = i.lower()
#             if invalid_token(i):
#                 pass
#             else:
#                 terms_2.append(lemmatizer.lemmatize(i))
#                 for j in wordnet.synsets(i):
#                     terms_2.append(j.name().split('.')[0])
#         terms = list(set(terms_2))
#     else:
#         terms = terms.lower()
#         if invalid_token(terms):
#             pass
#         else:
#             terms_2.append(lemmatizer.lemmatize(terms))
#             for j in wordnet.synsets(terms):
#                 terms_2.append(j.name().split('.')[0])
#         terms = list(set(terms_2))
#     return terms




from dateutil.parser import parse

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False

def pre_process(terms):
    lemmatizer = WordNetLemmatizer()
    en_stopwords = stopwords.words('english')

    terms_2 = [] # with syn (to prevent infinity loop)

    if type(terms) == list:
        for i in terms:
            i = i.lower()
            if is_date(i):
                terms_2.append(parse(i).strftime('YYYY-MM-DD')) # change date format as needed %Y-%m-%d
            
            if invalid_token(i):
                pass
            else:
                terms_2.append(lemmatizer.lemmatize(i))
                for j in wordnet.synsets(i):
                    terms_2.append(j.name().split('.')[0])
        terms = list(set(terms_2))
    else:
        terms = terms.lower()
        if is_date(terms):
            terms_2.append(parse(terms).strftime('YYYY-MM-DD')) # change date format as needed
        
        if invalid_token(terms):
            pass
        else:
            terms_2.append(lemmatizer.lemmatize(terms))
            for j in wordnet.synsets(terms):
                terms_2.append(j.name().split('.')[0])
        terms = list(set(terms_2))
    return terms



def get_terms(docs):
    terms = []

    for i in docs:
        terms = terms + word_tokenize(i)
    terms = list(set(terms))
    terms = pre_process(terms)
    return terms


def build_positional_index(docs):
    inverted_index = {}
    for document_id, docs in enumerate(docs):
        words = re.findall(r"\w+", docs.lower())  # Tokenize and lowercase
        for word_index, word in enumerate(words):
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append((document_id, word_index))
    return inverted_index

inverted_index = build_positional_index(docs)
print('total number of terms : ', len(inverted_index.keys()))