'''
Use KaggleWord to produce random forest analysis
Tiffany Fabianac Modified code from:
    - https://youtu.be/AJVP96tAWxw
    - Siraj Raval
'''


import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import nltk

if __name__ == '__main__':
    train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'labeledTrainData.csv'), header=0, delimiter=",", quoting=3)
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), 'testData.csv'), header=0, delimiter=",", quoting=3)

    print 'The first review is:'
    print train['Snippit'][0]
    raw_input("Press Enter to continue...")

    print 'Download text data sets'
    nltk.download()
    clean_train_reviews = []
    print "Cleaning and parsing the training set...\n"
    for i in xrange(0, len(train['Snippit'])):
        clean_train_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(train['Snippit'][i], True)))

    print "Creating the bag of words...\n"
    vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
    train_data_features = vectorizer.fit_transform(clean_train_reviews)
    train_data_features = train_data_features.toarray()

    print "Training Random forest..."
    forest = RandomForestClassifier(n_estimators=100)
    forest = forest.fit(train_data_features, train['W/L?'])
    clean_test_reviews=[]

    print "Cleaning and parsing \n"
    for i in xrange(0,len(test['Snippit'])):
        clean_test_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(test['Snippit'][i], True)))
    test_data_features = vectorizer.transform(clean_test_reviews)
    test_data_features = test_data_features.toarray()

    print "Predicting test labels...\n"
    result = forest.predict(test_data_features)
    output = pd.DataFrame(data={"Accuracy":"", "Sentiment":result, "Ticker":test["Ticker"], "Date":test["Date"]})
    output.to_csv(os.path.join(os.path.dirname(__file__), 'randomForestResults.csv'), index=False, quoting=3)
    print "Wrote results to randomForestResults.csv"



