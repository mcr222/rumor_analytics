from collections import Counter
from nltk import NaiveBayesClassifier, classify
import FilterStem
import random

error_count=0
def get_features(text):
    global error_count
    try:
        word_list = FilterStem.f_line_filter(text)
        word_count = {word: count for word, count in Counter(word_list).items()}
        return word_count
    except:
        error_count += 1
    

all_data = []

spam_data = open("Spam_dataset/SMSSpamColletion_spam.txt")
for line in spam_data:
    feature = get_features(line)
    if feature is not None:
        all_data.append((feature, "spam"))
    else:
        error_count += 1 

ham_data = open("Spam_dataset/SMSSpamColletion_ham.txt")
for line in ham_data:
    feature = get_features(line)
    if feature is not None:
        all_data.append((feature, "ham"))
    else:
        error_count += 1 
                     
print all_data[0:3]
print len(all_data)
print error_count
random.shuffle(all_data)
training_set = all_data[:int(len(all_data)*0.8)]
test_set = all_data[int(len(all_data)*0.8):]


classifier = NaiveBayesClassifier.train(training_set)
print classify.accuracy(classifier, training_set)
print classify.accuracy(classifier, test_set)
print classifier.show_most_informative_features(20)
print classifier.classify(get_features('now! now! now! award ton latest txt'))


