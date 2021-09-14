import json
from tokenization.token import (load, tokenize)
from definitions import ROOT_DIR


def handing_input_dataset_validation(dataset):
    data = dataset
    data_update = data[['Question', 'Quality Final']]

    data_word = data_update.copy()
    bad = ['Bad', 'bad']
    good = ['Good', 'good']
    agood = ['Agood', 'AGood', 'aGood', 'agood']

    for i in range(data_update.shape[0]):
        if data_update['Quality Final'][i] in bad:
            data_word['Quality Final'][i] = 0
        elif data_update['Quality Final'][i] in good:
            data_word['Quality Final'][i] = 1
        elif data_update['Quality Final'][i] in agood:
            data_word['Quality Final'][i] = 2
        else:
            data_word['Quality Final'][i] = None

    data_update = data_word

    data_update = data_update.mask(data_update.eq(None)).dropna()

    return data_update


def get_dict_of_group():
    dict_of_groups = {'Bad': 0,
                      'Good': 1,
                      'Agood': 2,
                      0: 'Bad',
                      1: 'Good',
                      2: 'Agood',
                      }
    return dict_of_groups


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


def lemma_statistics_validation(dataset):
    dict_of_groups = get_dict_of_group()
    group_lemma_dict = {'Bad': {},
                        'Good': {},
                        'Agood': {}}

    data = handing_input_dataset_validation(dataset)

    for string in range(data['Question'].count()):
        try:
            load_question = load(data.iloc[string, 0])
            load_target = data.iloc[string, 1]
            tokenized = tokenize(load_question)

            load_data_list = create_data_with_lemma(tokenized)

            for item in load_data_list:
                if group_lemma_dict[dict_of_groups[load_target]].get(item) is None:
                    group_lemma_dict[dict_of_groups[load_target]][item] = 1
                else:
                    group_lemma_dict[dict_of_groups[load_target]][item] += 1

            print(f"Обработано {string+1} задач из {data['Question'].count()}")
        except InterruptedError:
            # print('Error >>> SIGSEGV')
            continue

        json.dump(group_lemma_dict, open(ROOT_DIR + "/Statistics/lemma_statistics_validation.json", "w"))
