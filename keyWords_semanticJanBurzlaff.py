#%% Allright man, let's do a good job!
from selenium.common.exceptions import NoSuchElementException # to handle those errors that 
from selenium import webdriver # libraries needed for scrapping dinamic webpages
import pandas as pd
import time
import codecs
import re
import pyautogui
import urllib.request
import requests
import glob
import os
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
#%%
driver = webdriver.Chrome()
driver.get('https://fortunoff.aviaryplatform.com/collection')

# %%

for i in range(50, 55): #571
    list_of_testimony = []

    print(i)
    link = 'https://fortunoff.aviaryplatform.com/catalog?collection_title[]=&f[description_subject_search_facet_sms][]=topical+::+Holocaust+survivors&indexes[]=&keywords[]=&op[]=&page=' + str(i) + '&resource_description[]=Survival&search_field=advanced&search_type=simple&title_text[]=&transcript[]=&transliteration_status=false&type_of_field_selector[]=simple&type_of_field_selector_single=resource_description&type_of_search[]=simple&update_facets=true'
    driver.get(link)
    list_of_elements = driver.find_elements_by_xpath('//*[@id="documents"]/li')
    for y in range(len(list_of_elements)):
        testimony_link = driver.find_element_by_xpath('//*[@id="documents"]/li[' + str(y+1) + ']/div[2]/div[2]/a').get_attribute('href')
        list_of_testimony.append(testimony_link)
        print(y)

    for testimony in list_of_testimony:
        driver.get(testimony)
        time.sleep(5)
        print(testimony)
        download_html()


#%%
def check_if_exists_by_xpath(xpath):
    """
    The check_if_exist_by_xpath(xpath) function has the role to check if an element exist on the page 
    by providing its xpath.
    """
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#%%
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

# %%
details_df = pd.DataFrame(columns=["Name", "Gender", "CreatedAt", "Abstract"])

def get_subjectAndAbstract(file_path):
    article_details = []

    file = codecs.open(file_path, "r", "utf-8")
    file_content = file.read()
    b = cleanhtml(file_content).split('Abstract')[1]
    abstract = b.split('Subject')[0]
    d = b.split('Subject:')[1]
    subject = d.split('Relation')[0]
    subject = subject.split('Format:')[0]
    name = cleanhtml(file_content).split('Back to Search')[1]
    name = name.split('Holocaust')[0]
    name = name.split("  ")[-1]
    gender = subject.split('topical')
    if 'Men' in gender or 'Women' in gender:
        if 'Men' in gender and 'Women' in gender:
            gender = "More than one"
        elif 'Women' in gender:
            gender = "Feminin"
        else:
            gender = "Masculin"
    else:
        gender = 'None'
    creation = cleanhtml(file_content).split('creation')[1]
    creation = creation.split('Duration:')[0]
    article_details.append(name)
    article_details.append(gender)
    article_details.append(creation)
    article_details.append(abstract)
    print(name)
    print('================-================')
    #print('==================')
    #article_details = pd.DataFrame(article_details, columns=["Name", "Gender", "CreatedAt", "Abstract"])
    details_df.loc[len(details_df)] = article_details
    file.close()
    os.remove(file_path)
    return(details_df)

# %%
def download_html():
    pyautogui.moveTo(1300, 600)
    pyautogui.rightClick()
    pyautogui.moveTo(1400, 720)
    pyautogui.leftClick()
    pyautogui.moveTo(1700, 982)
    pyautogui.leftClick()

    time.sleep(5)

    list_of_files = glob.glob('C:\\Users\\citco\\Downloads\\*.html') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
        
    get_subjectAndAbstract(latest_file)
# %%
details_df.to_excel('holocaust5.xlsx')



# %%
# Let's start working with the text
def pre_process(text):
    text = text.lower() #lowercase
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text) #remove tags
    text = re.sub("(\\d|\\W)+", " ", text) # remove special characters and digits
    return text

def get_stop_words(stop_file_path):
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn):
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])


    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


#%%
data = pd.read_excel('holocaust5.xlsx')
data1 = data

data1['Abstract'] = data1['Abstract'].apply(lambda x:pre_process(x))
data1['Abstract'][2]

# %%
stopwords = get_stop_words("stop.txt") # load the set of stopwords
docs = data1["Abstract"].tolist() # get the text column
# eliminate stopwords and words that appear in 85% of the abstracts
cv = CountVectorizer(max_df=0.85, stop_words=stopwords, max_features=10000)
word_count_vector = cv.fit_transform(docs)
list(cv.vocabulary_.keys())[:20]

#%%
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)

# %%
feature_names = cv.get_feature_names()

#%%
doc = docs[2]
tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))
sorted_items = sort_coo(tf_idf_vector.tocoo())
keywords = extract_topn_from_vector(feature_names, sorted_items, 5)
print("\n=====Doc======")
print(doc)
print("\n===Keywords===")
for k in keywords:
    print(k, keywords[k])

# %%
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
tokenized_doc = data1["Abstract"].apply(lambda x: x.split()) #tokenization
#tokenized_doc = tokenized_doc.apply(lambda x: [item for item in x if item not in stopwords]) #removing stopwords
tokenized_doc = tokenized_doc.apply(lambda x: [item for item in x if item not in stop_words])
detokenized_doc = []
for i in range(len(data1)):
    t = ' '.join(tokenized_doc[i])
    detokenized_doc.append(t)

data1['Abstract'] = detokenized_doc
# %%
vectorizer = TfidfVectorizer(stop_words='english', 
max_features= 1000, # keep top 1000 terms 
max_df = 0.5, 
smooth_idf=True)

X = vectorizer.fit_transform(data1['Abstract'])

X.shape # check shape of the document-term matrix

svd_model = TruncatedSVD(n_components=20, algorithm='randomized', n_iter=100, random_state=122)

svd_model.fit(X)

len(svd_model.components_)
# %%

terms = vectorizer.get_feature_names()

for i, comp in enumerate(svd_model.components_):
    terms_comp = zip(terms, comp)
    sorted_terms = sorted(terms_comp, key= lambda x:x[1], reverse=True)[:7]
    print("Topic " + str(i) + ": ")
    print(sorted_terms[0])
    #for t in sorted_terms:
    #    print(t[0])
    #    print(" ")
# %%
