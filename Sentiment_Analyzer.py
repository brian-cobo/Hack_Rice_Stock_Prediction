
# Library imports
import string
import re

# The code in this file was taken and modified from https://sraf.nd.edu


def parser(doc, lm_dictionary):
    """Takes article and sends it to get analyzed based on the LM Master Dictionary"""
    # 1. Number of words(based on LM_MasterDictionary
    # 2. Proportion of positive words(use with care - see LM, JAR 2016)
    # 3.  Proportion of negative words
    # 4.  Proportion of uncertainty words
    # 5.  Proportion of litigious words
    # 6.  Proportion of modal-weak words
    # 7.  Proportion of modal-moderate words
    # 8.  Proportion of modal-strong words
    # 9.  Proportion of constraining words (see Bodnaruk, Loughran and McDonald, JFQA 2015)
    # 10.  Number of alphanumeric characters (a-z, A-Z)
    # 11.  Number of digits (0-9)
    # 12.  Number of numbers (collections of digits)
    # 13.  Average number of syllables
    # 14.  Average word length
    # 15.  Vocabulary (see Loughran-McDonald, JF, 2015)

    doc = doc.upper()  # for this parse caps aren't informative so shift
    # print(doc)

    # exit(0)
    output_data = analyze_article_contents(doc, lm_dictionary)
    article_info = \
        {
            'numberOfWords': output_data[2],
            'positive_%': output_data[3],
            'negative_%': output_data[4],
            'uncertainty_%': output_data[5],
            'litigious': output_data[6],
            'modal-weak_%': output_data[7],
            'modal-moderate_%': output_data[8],
            'modal-strong_%': output_data[9],
            'constraining_%': output_data[10],
            'num_of_alphanumeric': output_data[11],
            'num_of_digits': output_data[12],
            'num_of_Numbers': output_data[13],
            'avg_num_Of_syllables_per_word': output_data[14],
            'avg_word_length': output_data[15],
            'vocabulary': output_data[16]
        }
    return article_info


def analyze_article_contents(doc, lm_dictionary):
    """Parses through article contents and rates everything based on the words that
       appear according to the master dictionary"""

    vdictionary = {}
    _odata = [0] * 17
    total_syllables = 0
    word_length = 0

    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    for token in tokens:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            _odata[2] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].positive: _odata[3] += 1
            if lm_dictionary[token].negative: _odata[4] += 1
            if lm_dictionary[token].uncertainty: _odata[5] += 1
            if lm_dictionary[token].litigious: _odata[6] += 1
            if lm_dictionary[token].weak_modal: _odata[7] += 1
            if lm_dictionary[token].moderate_modal: _odata[8] += 1
            if lm_dictionary[token].strong_modal: _odata[9] += 1
            if lm_dictionary[token].constraining: _odata[10] += 1
            total_syllables += lm_dictionary[token].syllables

    _odata[11] = len(re.findall('[A-Z]', doc))
    _odata[12] = len(re.findall('[0-9]', doc))
    # drop punctuation within numbers for number count
    doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
    doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    _odata[13] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc))
    _odata[14] = total_syllables / _odata[2]
    _odata[15] = word_length / _odata[2]
    _odata[16] = len(vdictionary)

    # Convert counts to %
    for i in range(3, 10 + 1):
        _odata[i] = (_odata[i] / _odata[2]) * 100

    return _odata


