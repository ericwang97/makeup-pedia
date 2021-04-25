import time
import json
import rltk
from tqdm import tqdm
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cleaned_input_file = path.replace('\\', '/') + '/data/cleaned_data.json'
output_file = '../reco_result/result.json'

sub_category_sim_thres = 0.8
reviews_thres = 30
top_K = 3


def clean_subcategory(subcategory):

    return subcategory.replace('Face', '').replace('Lip', '').replace('Eye', '').replace('Foundation', '')


def get_similarity(n1, n2):
    jw = rltk.jaro_winkler_similarity(n1.lower(), n2.lower())
    jaccard = len(set(n1.lower()).intersection(n2.lower())) / len(set(n1.lower()).union(n2.lower()))

    return max(jaccard, jw)


def get_all_category_keys(cleaned_input):
    category_sub = {}
    for item in cleaned_input:
        category = cleaned_input[item]['category']
        if category not in category_sub:
            category_sub[category] = set()
        subcategory_key = set(cleaned_input[item]['sub_category'])
        category_sub[category] = category_sub[category].union(subcategory_key)

    return category_sub


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


def get_avg_counter_score(item_data, age, skin, skin_color, hair, hair_color, eye):
    review_cnt = item_data['mua_review_cnt']
    age_counter = item_data['age_counter']
    skin_type_counter = item_data['skin_type_counter']
    skin_color_counter = item_data['skin_color_counter']
    hair_style_counter = item_data['hair_style_counter']
    hair_color_counter = item_data['hair_color_counter']
    eyes_counter = item_data['eyes_counter']
    counters = [age_counter, skin_type_counter, skin_color_counter, hair_style_counter, hair_color_counter, eyes_counter]
    if not any(counters):
        return None
    # min_sum, max_sum = sum([min(counter.values()) for counter in counters if counter]), \
    #                    sum([max(counter.values()) for counter in counters if counter])
    # max_gap = max_sum - min_sum

    age_score, skin_score, skin_color_score, hair_score, hair_color_score, eye_score = 0, 0, 0, 0, 0, 0
    if age in age_counter:
        age_score = age_counter[age]
    if skin in skin_type_counter:
        skin_score = skin_type_counter[skin]
    if skin_color in skin_color_counter:
        skin_color_score = skin_color_counter[skin_color]
    if hair in hair_style_counter:
        hair_score = hair_style_counter[hair]
    if hair_color in hair_color_counter:
        hair_color_score = hair_color_counter[hair_color]
    if eye in eyes_counter:
        eye_score = eyes_counter[eye]

    norm_counter_score = (age_score + skin_score + skin_color_score + hair_score +
                          hair_color_score + eye_score) / (4 * review_cnt)

    return norm_counter_score


def reco(cleaned_input, request):
    category, subcategory, age, skin, skin_color, hair, hair_color, eye = request['category'], request['subcategory'], \
                                                                          request['age'], request['skin'], \
                                                                          request['skin_color'], request['hair'], \
                                                                          request['hair_color'], request['eye']
    score_list = []
    for item in cleaned_input:

        item_category = cleaned_input[item]['category']
        item_subcategory = cleaned_input[item]['sub_category']

        if category != item_category:
            continue

        sim = [get_similarity(clean_subcategory(subcategory), clean_subcategory(each)) for each in item_subcategory]
        # print(sim, [(clean_subcategory(subcategory), clean_subcategory(each)) for each in item_subcategory])
        if max(sim) < sub_category_sim_thres:
            continue

        review_cnt = cleaned_input[item]['mua_review_cnt']
        if review_cnt < reviews_thres:
            continue

        each_score_list = []
        if cleaned_input[item]['expert_rating']:
            exp_rate = float(cleaned_input[item]['expert_rating']) / 5
            each_score_list.append(exp_rate)
        if cleaned_input[item]['mua_rating']:
            user_rate = cleaned_input[item]['mua_rating'] / 5
            each_score_list.append(user_rate)
        elif cleaned_input[item]['user_rating']:
            user_rate = cleaned_input[item]['user_rating'] / 5
            each_score_list.append(user_rate)

        if cleaned_input[item]['repurchase_pct']:
            repurchase_pct = cleaned_input[item]['repurchase_pct'] / 100
            each_score_list.append(repurchase_pct)
        avg_counter_score = get_avg_counter_score(cleaned_input[item], age, skin, skin_color, hair, hair_color, eye)
        if avg_counter_score is None:
            continue

        # print(avg_counter_score, each_score_list)
        score = avg_counter_score * sum(each_score_list) / len(each_score_list)
        score_list.append((item, score))

    score_list = sorted(score_list, key=lambda x: x[1], reverse=True)

    return score_list


def reco_main(request, debug=False):
    cleaned_input = json.load(open(cleaned_input_file, 'r', encoding='utf-8'))
    score_list = reco(cleaned_input, request)
    top_k = int(request['top_k'])

    # Also genreate least TopK for testing the results!
    # TODO!

    top_K_score_list = score_list[:top_k] + score_list[-top_k:]
    result = [cleaned_input[each[0]] for each in top_K_score_list]

    # For Testing
    if debug:
        # total_age_keys, total_skin_keys, total_hair_keys, total_eyes_keys = get_all_counter_keys(cleaned_input)
        # print(total_age_keys, total_skin_keys, total_hair_keys, total_eyes_keys)
        # category_sub = get_all_category_keys(cleaned_input)
        # print(category_sub)
        print(top_K_score_list)
        # print(cleaned_input[score_list[0][0]])
        output = open(output_file, 'w')
        output.write(json.dumps(result, indent=4))
        output.close()

    return result


if __name__ == "__main__":

    """
    Input: Data, Request (see below, hard code the keys and the value choices)
    Reco: 3 filters when doing Reco: Same category --> similar sub_category (string similarity) 
        --> mua_reviews_cnt > 30 --> use agg_mua_counts for weights, weight * avg(rating + exp rating + repurchase)
    Output: Top K and the Least K results (Least K for comparing whether the result is reasonable)
    """

    """
    Hard code list:
    
    age_list = ['19-24', '30-35', '25-29', '44-55', '56 & Over', 'Under 18', '36-43']
    eyes_color_list = ['Blue', 'Brown', 'Black', 'Violet', 'Other', 'Gray', 'Hazel', 'Green']
    skin_type_list = ['Very Dry', 'Dry', 'Medium', 'Fair-Medium', 'Fair', 'Combination', 'Oily', 'Very Oily',
                      'Sensitive', 'Acne-prone', 'Normal', 'Neutral']
    skin_color_list = ['Tan', 'Olive', 'Deep Dark', 'Warm', 'Dark', 'Medium Brown', 'Normal']
    hair_style_list = ['Coarse', 'Straight', 'Kinky', 'Medium', 'Fine', 'Wavy', 'Curly', 'Relaxed']
    hair_color_list = ['Red', 'Grey', 'Brown', 'Black', 'Silver', 'Brunette', 'Blond']
    
    {'Face Makeup': {'Face Primer', 'Tinted Moisturizer', 'Pressed Powder', 'Cushion Foundation', 
        'Face Powder', 'Powder Foundation', 'Highlighter', 'Color Corrector', 'Facial Powder', 
        'Foundation With Sunscreen', 'Contour', 'Concealer', 'Concealer & Corrector', 'Cream Foundation', 
        'Loose Powder', 'Bronzer', 'Blush Palettes', 'Stick Foundation', 'Setting Spray', 'BB & CC Cream', 
        'Bronzer/Highlighter', 'Foundation', 'Liquid Foundation', 'Blush', 'Makeup Primer', 
        'Foundation Without Sunscreen', 'Foundation Primer', 'Other Foundation'}, 
    
    'Lip Makeup': {'Lip Balm', 'Lip Balm & Treatment', 'Lip Plumper', 'Lip Gloss', 'Lipstick', 
        'Lip Liner', 'Lip Palettes'}, 
    
    'Eye Makeup': {'Eyebrow Makeup', 'Eyelash Primer & Treatment', 'Eyeshadow Palette', 'Eye Primer', 'Mascara', 
        'Eye Liner', 'Eyeshadow', 'Waterproof Mascara', 'Lash Serum', 'Eyebrows', 'False Lashes', 'Eyeliner', 
        'Eye Shadow', 'Eye Palettes', 'Brow Liner', 'Eyeshadow Primer & Base'}}

    """
    request = {
        'category': 'Face Makeup',
        'subcategory': 'Face Powder',
        'age': '19-24',
        'skin': 'Combination',
        'skin_color': 'Warm',
        'hair': 'Straight',
        'hair_color': 'Black',
        'eye': 'Brown',
        'top_k': top_K
    }

    # Guess what you like!
    reco_main(request, debug=True)
