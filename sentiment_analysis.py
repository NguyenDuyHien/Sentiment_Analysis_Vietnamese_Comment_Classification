# encoding=utf8
import sys
import re
from pyvi import ViTokenizer
from sensitive_data import dataset, feature_set, no_of_items

reload(sys)
sys.setdefaultencoding('utf8')

# Weighted probability of a word for a category
def weighted_prob(word, category):

    v = len(feature_set)
    count_c = sum(dataset[category].values())
    if word in dataset[category]:
        count_w_c = feature_set[word][category]
    else:
        count_w_c = 0

    weight_prob = (1.0 + count_w_c) / (count_c + v)
    return weight_prob


# To get probability of the test data for the given category
def test_prob(test, category):
    # Tách từ trong câu test
    split_data = re.split('[\s,.;:?!-]', ViTokenizer.tokenize(test.decode('utf-8')))

    data = []
    for i in split_data:
        data.append(i.lower())

    p = 1
    for i in data:
        p *= weighted_prob(i, category)
    return p


# Naive Bayes
def naive_bayes(test):
    '''
        p(A|B) = p(B|A) * p(A) / p(B)
        Ghi chú A - Nhãn
                B - Dữ liệu test
                p(A|B) - Category given the Test data
        Chúng ta loại bỏ p(B) vì giá trị này bằng nhanh với mọi nhãn
    '''
    results = {}
    for i in dataset.keys():
        # Tính toán xác suất cửa từng nhãn - p(A)
        # Số lượng câu trong từng nhãn/tổng số lượng câu
        c_prob = float(no_of_items[i]) / sum(no_of_items.values())

        # p(B|A)
        test_prob1 = test_prob(test, i)

        results[i] = test_prob1 * c_prob

    return results

print 'Vui lòng nhập câu:'
text = raw_input()
result = naive_bayes(text)

if (result['1'] >= result['-1']) and (result['1'] >= result['0']):
    print 'Tích cực'
elif (result['0'] >= result['-1']) and (result['0'] >= result['-1']):
    print 'Trung tính'
else:
    print 'Tiêu cực'