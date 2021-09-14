import json
from tokenization.token import (load, tokenize)
from definitions import ROOT_DIR


def handing_input_dataset_grouping(dataset):
    data = dataset
    data_update = data[['Question', 'General Category']]
    data_update = data_update.mask(data_update.eq(None)).dropna()

    return data_update


def get_dict_of_group():
    dict_of_new_groups = {
        "Multiplication and division": 1,
        "Addition and subtraction": 2,
        "Fractions": 3,
        "Mixed operations": 4,
        "Measurements": 5,
        "Figures": 6,
        "Number": 7,
        "Modelling": 8,
        "Geometry": 9,
        "Time": 10,
        "Comparison": 11,
        "Estimation": 12,
        "Logic": 13,
        "Series and pattern": 14,
        "Graph": 15,
        "Probability": 16,
        "Money": 17,
        "Other": 18,
        1: "Multiplication and division",
        2: "Addition and subtraction",
        3: "Fractions",
        4: "Mixed operations",
        5: "Measurements",
        6: "Figures",
        7: "Number",
        8: "Modelling",
        9: "Geometry",
        10: "Time",
        11: "Comparison",
        12: "Estimation",
        13: "Logic",
        14: "Series and pattern",
        15: "Graph",
        16: "Probability",
        17: "Money",
        18: "Other",
    }

    dict_of_groups = {'number_properties': 1,
                      'geometry': 2,
                      'measurement': 3,
                      'algebra': 4,
                      'data_and_probability': 5,
                      1: 'number_properties',
                      2: 'geometry',
                      3: 'measurement',
                      4: 'algebra',
                      5: 'data_and_probability',
                      }
    return dict_of_new_groups


def create_data_with_lemma(tokens_list):
    """ input text. Output lemma's from input text """

    list_map = []
    error_set = set()

    for token in tokens_list:
        try:
            if token['lemma_'] is None:
                continue
            if stop_lemmas_type(token):
                continue
            list_map.append(token['lemma_'].lower())
        except KeyError:
            error_set.add(token['lemma_'].lower())
            print(error_set)

    return list_map


def create_lemma_statistics_data_dict(tokens_list):
    """ Calculate lemma numeration dict """
    lemma_dict = {}

    for token in tokens_list:
        if lemma_dict.get(token['lemma_'].lower()) is None:
            lemma_dict[token['lemma_'].lower()] = len(lemma_dict)
        else:
            continue

    return lemma_dict


def stop_lemmas_type(token):
    dict_filter = {
        # 'ADJ': 0,
        # 'ADP': 0,
        # 'ADV': 0,
        # 'AUX': 0,
        # 'CCONJ': 0,
        # 'DET': 0,
        # 'INTJ': 0,
        # 'NOUN': 0,
        'NUM': 1,
        # 'PART': 0,
        # 'PRON': 0,
        # 'PROPN': 0,
        'PUNCT': 1,
        # 'SCONJ': 0,
        'SYM': 1,
        # 'VERB': 0,
        # 'X': 0,
        'SPACE': 1,
    }
    res = dict_filter.get(token['pos_'])
    if dict_filter.get(token['pos_']):
        return True
    else:
        return False


def filter_question_from_group(data, group_to_filter='number_properties'):
    dict_of_groups = get_dict_of_group()
    question_filtered = {'Group': [], 'Question': []}
    for i in range(len(data['Group'])):
        num = dict_of_groups[group_to_filter]
        num1 = data.iloc[i, 1]
        if data.iloc[i, 1] == dict_of_groups[group_to_filter]:
            question_filtered['Group'].append(data.iloc[i, 1])
            question_filtered['Question'].append(data.iloc[i, 0])
    return question_filtered


def lemma_statistics_grouping(dataset):
    dict_of_groups = get_dict_of_group()
    group_lemma_dict = {'number_properties': {},
                        'geometry': {},
                        'measurement': {},
                        'algebra': {},
                        'data_and_probability': {}}

    group_new_lemma_dict = {
        "Multiplication and division": {},
        "Addition and subtraction": {},
        "Fractions": {},
        "Mixed operations": {},
        "Measurements": {},
        "Figures": {},
        "Number": {},
        "Modelling": {},
        "Geometry": {},
        "Time": {},
        "Comparison": {},
        "Estimation": {},
        "Logic": {},
        "Series and pattern": {},
        "Graph": {},
        "Probability": {},
        "Money": {},
        "Other": {},
    }

    data = handing_input_dataset_grouping(dataset)

    for string in range(data['Question'].count()):
        try:
            load_question = load(data.iloc[string, 0])
            load_target = data.iloc[string, 1]
            if load_target not in group_new_lemma_dict.keys():
                continue

            tokenized = tokenize(load_question)

            load_data_list = create_data_with_lemma(tokenized)

            for item in load_data_list:
                if group_new_lemma_dict[load_target].get(item) is None:
                    group_new_lemma_dict[load_target][item] = 1
                else:
                    group_new_lemma_dict[load_target][item] += 1

            print(f"Обработано {string+1} задач из {data['Question'].count()}")

        except InterruptedError:
            # print('Error >>> SIGSEGV')
            continue

        json.dump(group_new_lemma_dict, open(ROOT_DIR + "/Statistics/lemma_statistics_grouping.json", "w"))

