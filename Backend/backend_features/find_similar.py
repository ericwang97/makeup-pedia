import json
import rltk
import math
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cleaned_input_file = path.replace('\\', '/') + '/data/cleaned_data.json'

sub_category_sim_thres = 0.8
reviews_thres = 30
top_K = 30


def clean_subcategory(subcategory):
    return subcategory.replace('Face', '').replace('Lip', '').replace('Eye', '').replace('Foundation', '')


def get_similarity(n1, n2):
    jw = rltk.jaro_winkler_similarity(n1.lower(), n2.lower())
    jaccard = len(set(n1.lower()).intersection(n2.lower())) / len(set(n1.lower()).union(n2.lower()))

    return max(jaccard, jw)


def get_cos_sim(v1, v2):

    num = sum([v1[i] * v2[i] for i in range(len(v1))])
    dom = math.sqrt(sum([v1[i] ** 2 for i in range(len(v1))])) * math.sqrt(sum([v2[i] ** 2 for i in range(len(v1))]))

    return num / dom


def get_all_counter_keys(cleaned_input):
    total_age_keys = set()
    total_skin_keys = set()
    total_hair_keys = set()
    total_eyes_keys = set()
    for item in cleaned_input:
        age_key = set(list(cleaned_input[item]['age_counter'].keys()))
        total_age_keys = total_age_keys.union(age_key)
        skin_key = set(list(cleaned_input[item]['skin_type_counter'].keys()))
        total_skin_keys = total_skin_keys.union(skin_key)
        hair_key = set(list(cleaned_input[item]['hair_style_counter'].keys()))
        total_hair_keys = total_hair_keys.union(hair_key)
        eye_key = set(list(cleaned_input[item]['eyes_counter'].keys()))
        total_eyes_keys = total_eyes_keys.union(eye_key)

    return total_age_keys, total_skin_keys, total_hair_keys, total_eyes_keys


def get_counter_score_vec(item_data, all_counter_keys):
    age_counter = item_data['age_counter']
    skin_type_counter = item_data['skin_type_counter']
    skin_color_counter = item_data['skin_color_counter']
    hair_style_counter = item_data['hair_style_counter']
    hair_color_counter = item_data['hair_color_counter']
    eyes_counter = item_data['eyes_counter']
    counters = [age_counter, skin_type_counter, skin_color_counter, hair_style_counter, hair_color_counter,
                eyes_counter]
    # print(counters)
    if not any(counters):
        return None

    counter_sum = sum([sum([abs(i) for i in counter.values()]) for counter in counters if counter])

    counter_score_vec = [0] * len(all_counter_keys)
    for counter in counters:
        for k, v in counter.items():
            if k in all_counter_keys:
                index = all_counter_keys.index(k)
                counter_score_vec[index] = v / counter_sum

    return counter_score_vec


def find(cleaned_input, request):
    product_id = str(request['product_id'])
    product_data = cleaned_input[product_id]
    category = product_data['category']
    subcategory = product_data['sub_category'][0]  # Only choose the first sub category!

    all_counter_keys = []
    for each in get_all_counter_keys(cleaned_input):
        all_counter_keys += list(each)

    product_counter_score_vec = get_counter_score_vec(product_data, all_counter_keys)

    cos_sim_list = []
    for item in cleaned_input:

        item_category = cleaned_input[item]['category']
        item_subcategory = cleaned_input[item]['sub_category']

        if category != item_category:
            continue

        if not item_subcategory:
            continue

        sim = get_similarity(clean_subcategory(subcategory), clean_subcategory(item_subcategory[0]))
        if sim < sub_category_sim_thres:
            continue

        review_cnt = cleaned_input[item]['mua_review_cnt']
        if review_cnt < reviews_thres:
            continue

        counter_score_vec = get_counter_score_vec(cleaned_input[item], all_counter_keys)
        if counter_score_vec is None:
            continue

        # print(review_cnt, sum([abs(i) for i in counter_score_vec]), counter_score_vec)
        cos_sim = get_cos_sim(product_counter_score_vec, counter_score_vec)
        cos_sim_list.append((item, cos_sim))

    cos_sim_list = sorted(cos_sim_list, key=lambda x: x[1], reverse=True)

    return cos_sim_list


def find_main(request, debug=False):
    cleaned_input = json.load(open(cleaned_input_file, 'r', encoding='utf-8'))
    cos_sim_list = find(cleaned_input, request)

    top_K_score_list = cos_sim_list[1:top_K+1]

    result = {'Top': [cleaned_input[each[0]] for each in top_K_score_list]}

    last_K_score_list = cos_sim_list[-top_K:]
    result.update({'Last': [cleaned_input[each[0]] for each in last_K_score_list]})

    # For Testing
    if debug:
        print(top_K_score_list, last_K_score_list)

    return result


if __name__ == "__main__":
    """
    Input: Data, Request (id)
    Find Similar: 3 filters when doing Reco: Same category --> similar sub_category (string similarity) 
        --> mua_reviews_cnt > 30 --> use agg_mua_counts for vector, cos() similarity
    Output: Top K and the Least K results (Least K for comparing whether the result is reasonable)
    """

    request = {
        'id': 2340
    }

    # Guess what you like!
    find_main(request, debug=True)
