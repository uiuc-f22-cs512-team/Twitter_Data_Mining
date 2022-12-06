import Bayes
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm


def load_data(stemming=True, lowercase=True, silently=False):
    print(f"Stemming is {stemming}")
    print(f"Lowercase is {lowercase}")
    # TODO load dataset
    # train_set, train_labels, test_set, test_labels = load_dataset(stemming, lowercase, silently)
    # return train_set, train_labels, test_set, test_labels


def compute_accuracies(predicted_labels, test_labels):
    yhats = predicted_labels
    assert len(yhats) == len(test_labels), "predicted and gold label lists have different lengths"
    accuracy = sum([yhats[i] == test_labels[i] for i in range(len(yhats))]) / len(yhats)
    tp = sum([yhats[i] == test_labels[i] and yhats[i] == 1 for i in range(len(yhats))])
    tn = sum([yhats[i] == test_labels[i] and yhats[i] == 0 for i in range(len(yhats))])
    fp = sum([yhats[i] != test_labels[i] and yhats[i] == 1 for i in range(len(yhats))])
    fn = sum([yhats[i] != test_labels[i] and yhats[i] == 0 for i in range(len(yhats))])
    return accuracy, fp, fn, tp, tn

# print value and also percentage out of n
def print_value(label, value, numvalues):
   print(f"{label} {value} ({value/numvalues}%)")

# print out performance stats
def print_stats(accuracy, false_positive, false_negative, true_positive, true_negative, numvalues):
    print(f"Accuracy: {accuracy}")
    print_value("False Positive", false_positive,numvalues)
    print_value("False Negative", false_negative,numvalues)
    print_value("True Positive", true_positive,numvalues)
    print_value("True Negative", true_negative,numvalues)
    print(f"total number of samples {numvalues}")
    
def main():
    train_set, train_labels, dev_set, dev_labels = load_data()
    
    predicted_labels_bigram = Bayes.bigramBayes(train_set, train_labels, dev_set)
    predicted_labels_naive = Bayes.naiveBayes(train_set, train_labels, dev_set)

    accuracy, false_positive, false_negative, true_positive, true_negative = compute_accuracies(predicted_labels_bigram,dev_labels)
    nn = len(dev_labels)
    print_stats(accuracy, false_positive, false_negative, true_positive, true_negative, nn, True)

    accuracy, false_positive, false_negative, true_positive, true_negative = compute_accuracies(predicted_labels_naive,dev_labels)
    print_stats(accuracy, false_positive, false_negative, true_positive, true_negative, nn, False)

main()