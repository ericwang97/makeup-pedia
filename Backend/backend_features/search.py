import json
import rltk
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cleaned_input_file = path.replace('\\', '/') + '/data/cleaned_data.json'

sub_category_sim_thres = 0.8
name_sim_thres = 0.6


def clean_subcategory(subcategory):
    return subcategory.replace('Face', '').replace('Lip', '').replace('Eye', '').replace('Foundation', '')


def get_similarity(n1, n2):
    jw = rltk.jaro_winkler_similarity(n1.lower(), n2.lower())
    jaccard = len(set(n1.lower()).intersection(n2.lower())) / len(set(n1.lower()).union(n2.lower()))

    return max(jaccard, jw)


def search(cleaned_input, request):

    category, subcategory, name = request['category'], request['subcategory'], request['search_name']

    result = []
    result_id_list = []
    for item in cleaned_input:

        item_category = cleaned_input[item]['category']
        item_subcategory = cleaned_input[item]['sub_category']
        item_name = cleaned_input[item]['product_names']

        if subcategory == item_subcategory[0] and name == item_name:
            result.insert(0, cleaned_input[item])
            result_id_list.insert(0, (item, 1))
            continue

        if category != item_category:
            continue

        if not item_subcategory:
            continue

        subcategory_sim = get_similarity(clean_subcategory(subcategory), clean_subcategory(item_subcategory[0]))
        if subcategory_sim < sub_category_sim_thres:
            continue

        name_sim = get_similarity(name, item_name)
        if name_sim < name_sim_thres:
            continue

        result_id_list.append((item, name_sim))

    result_id_list = sorted(result_id_list, key=lambda x: x[1], reverse=True)
    result_id_list = [item[0] for item in result_id_list]

    return result_id_list


def search_main(request, debug=False):

    cleaned_input = json.load(open(cleaned_input_file, 'r', encoding='utf-8'))
    result_id_list = search(cleaned_input, request)
    result = {'Result': [cleaned_input[item] for item in result_id_list], 'ID': result_id_list}

    # For Testing
    if debug:
        print(result)

    return result


if __name__ == "__main__":
    """
    Input: Data, Request (category, subcategory, name)
    Find Similar: 3 filters when doing Reco: Same category --> similar sub_category (string similarity) 
        --> mua_reviews_cnt > 30 --> use agg_mua_counts for vector, cos() similarity
    Output: Top K and the Least K results (Least K for comparing whether the result is reasonable)
    """

    request = {
        'category': 'Face Makeup',
        'subcategory': 'Face Powder',  # 'Cushion Foundation',
        'search_name': 'Pureness Matifying Compact Oil-Free'  # Pureness Matifying Compact Oil-Free SPF 16
    }

    # Guess what you like!
    search_main(request, debug=True)
