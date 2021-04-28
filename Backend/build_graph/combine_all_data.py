import copy
import json
from tqdm import tqdm

mua_bp_file = '../ER/mua_bp_id.json'
mua_ewg_file = '../ER/mua_ewg_id.json'
bp_ewg_ingre_file = '../ER/bp_ewg_ingre_name.json'
bp_file = '../data_raw/beautypedia.jl'
mua_file = '../data_raw/mua_meta_data.jl'
ewg_file = '../data_raw/agg_ewg_data.jl'

all_output_file = '../data/all_data.json'
cleaned_output_file = '../data/cleaned_data.json'

age_list = ['19-24', '30-35', '25-29', '44-55', '56 & Over', 'Under 18', '36-43']
eyes_color_list = ['Blue', 'Brown', 'Black', 'Violet', 'Other', 'Gray', 'Hazel', 'Green']
skin_type_list = ['Very Dry', 'Dry', 'Medium', 'Fair-Medium', 'Fair', 'Combination', 'Oily', 'Very Oily',
                  'Sensitive', 'Acne-prone', 'Normal', 'Neutral']
skin_color_list = ['Tan', 'Olive', 'Deep Dark', 'Warm', 'Dark', 'Medium Brown', 'Normal']
hair_style_list = ['Coarse', 'Straight', 'Kinky', 'Medium', 'Fine', 'Wavy', 'Curly', 'Relaxed']
hair_color_list = ['Red', 'Grey', 'Brown', 'Black', 'Silver', 'Brunette', 'Blond']


def deleteDuplicate(reviews):
    temp_list = list(set([str(i) for i in reviews]))
    reviews = [eval(i) for i in temp_list]
    return reviews


def agg_mua_reviews(data):
    reviews = data['reviews']
    age_counter = {}
    skin_type_counter = {}
    skin_color_counter = {}
    hair_style_counter = {}
    hair_color_counter = {}
    eyes_counter = {}
    deduplicate_reviews = deleteDuplicate(reviews)
    for review in deduplicate_reviews:
        score = review['user_rating']
        if score is None:
            continue
        review = review['user_details']
        age, skin_list, hair_list, eye = review['user_age'], review['user_skin_type'], review['user_hair_style'], \
                                         review['user_eyes']
        if age in age_list and age not in age_counter:
            age_counter[age] = 0
        for skin in skin_list:
            if skin in skin_type_list and skin not in skin_type_counter:
                skin_type_counter[skin] = 0
            elif skin in skin_color_list and skin not in skin_color_counter:
                skin_color_counter[skin] = 0
        for hair in hair_list:
            if hair in hair_style_list and hair not in hair_style_counter:
                hair_style_counter[hair] = 0
            elif hair in hair_color_list and hair not in hair_color_counter:
                hair_color_counter[hair] = 0
        if eye in eyes_color_list and eye not in eyes_counter:
            eyes_counter[eye] = 0

        # Positive review, +1
        if score > 3.0:
            add_on = 1
        else:
            add_on = -1
        if age in age_list:
            age_counter[age] += add_on
        for skin in skin_list:
            if skin in skin_type_list:
                skin_type_counter[skin] += add_on
            elif skin in skin_color_list:
                skin_color_counter[skin] += add_on
        for hair in hair_list:
            if hair in hair_style_list:
                hair_style_counter[hair] += add_on
            elif hair in hair_color_list:
                hair_color_counter[hair] += add_on
        if eye in eyes_color_list:
            eyes_counter[eye] += add_on

    reviews_agg_res = {'age_counter': age_counter, 'skin_type_counter': skin_type_counter,
                       'skin_color_counter': skin_color_counter, 'hair_style_counter': hair_style_counter,
                       'hair_color_counter': hair_color_counter, 'eyes_counter': eyes_counter}

    data['reviews'] = reviews_agg_res

    return data


# Make product_id as the key of each json/dict
def rebuild_file(file_name):
    json_res = {}
    with open(file_name, 'r') as file:
        for line in tqdm(file):
            result = json.loads(line)
            product_id = str(result['product_id'])
            if file_name == mua_file:
                result = agg_mua_reviews(result)
            json_res.update({product_id: result})

    return json_res


def get_combined_index(mua_bp, mua_ewg):
    bp_ewg_mua = {}
    counter = {}
    for mua, bp in mua_bp.items():
        bp = str(bp)
        if bp not in bp_ewg_mua:
            bp_ewg_mua[bp] = {'ewg': None, 'mua': []}
        if bp not in counter:
            counter[bp] = {}

        bp_ewg_mua[bp]['mua'].append(mua)
        if mua in mua_ewg:
            ewg = mua_ewg[mua]
            ewg = str(ewg)
            if ewg not in counter[bp]:
                counter[bp][ewg] = 0
            bp_ewg_mua[bp]['ewg'] = ewg
            counter[bp][ewg] += 1

    for bp in bp_ewg_mua:
        if counter[bp]:
            bp_ewg_mua[bp]['ewg'] = max(counter[bp], key=counter[bp].get)

    return bp_ewg_mua


def get_all_data(bp_ewg_mua_index, bp, ewg, mua):
    all_data = {}
    for bp_id in bp_ewg_mua_index:
        all_data[bp_id] = {}
        bp_data = bp[bp_id]
        all_data[bp_id].update({'bp': bp_data})

        ewg_id = bp_ewg_mua_index[bp_id]['ewg']
        if ewg_id and ewg_id in ewg:
            ewg_data = ewg[ewg_id]
            all_data[bp_id].update({'ewg': ewg_data})

        mua_id_list = bp_ewg_mua_index[bp_id]['mua']
        all_data[bp_id]['mua'] = []
        for mua_id in mua_id_list:
            if mua_id and mua_id in mua:
                mua_data = mua[mua_id]
                all_data[bp_id]['mua'].append(mua_data)

    output = open(all_output_file, 'w')
    output.write(json.dumps(all_data, indent=4))
    output.close()

    return all_data


def get_cleaned_data(bp_ewg_mua_index, bp, ewg, mua, bp_ewg_ingre):
    """
    BP as MAIN DATASET
    1. COMBINE EWG TO BP
        Add new attributes: Brand URL, Colors, Overall Concerns, Other Concerns, Ingredient;
        Repeated attributes: Name ("Other Name"), sub_category (append to list);
        id, category, Brand Name X

    2. COMBINE MUA TO BP
        Add new attributes: rating, repurchase_pct, packaging_rate, reviews (Need more merging);
        Repeated attributes: Name ("Other Name"), sub_category & img_url (append to list);
        id, category, brand_name, product_description X

    """
    cleaned_data = {}
    for bp_id in bp_ewg_mua_index:
        cleaned_data[bp_id] = {}

        # BP, Add new columns
        bp_data = bp[bp_id]
        cleaned_data[bp_id] = copy.deepcopy(bp_data)
        cleaned_data[bp_id]['ingredient'] = []
        cleaned_data[bp_id]['buy_url'] = []
        cleaned_data[bp_id]['other_names'] = []
        cleaned_data[bp_id]['brand_url'] = []
        cleaned_data[bp_id]['sub_category'] = [cleaned_data[bp_id]['sub_category']]
        cleaned_data[bp_id]['image_url'] = [cleaned_data[bp_id]['image_url']]

        # BP add ingredient ER
        if bp_data['ingredient']:
            for bp_ingr in bp_data['ingredient']:
                if bp_ingr in bp_ewg_ingre:
                    cleaned_data[bp_id]['ingredient'].append(bp_ewg_ingre[bp_ingr])
                else:
                    cleaned_data[bp_id]['ingredient'].append(bp_ingr)

        # EWG
        ewg_id = bp_ewg_mua_index[bp_id]['ewg']
        if ewg_id and ewg_id in ewg:
            ewg_data = ewg[ewg_id]
            # Add
            brand_url = ewg_data['Brand URL']
            colors = ewg_data['Colors']
            overall_concerns = ewg_data['Overall Concerns']
            other_concerns = ewg_data['Other Concerns']
            cleaned_data[bp_id]['brand_url'].append(brand_url)
            cleaned_data[bp_id].update({'colors': colors, 'overall_concerns': overall_concerns,
                                        'other_concerns': other_concerns})

            # Add Where to purchase
            buy_url = ewg_data["Buy URL"]
            if buy_url not in cleaned_data[bp_id]['buy_url']:
                cleaned_data[bp_id]['buy_url'].append(buy_url)

            # Replace
            ingredient = ewg_data['Ingredient']
            cleaned_data[bp_id]['ewg_ingredient'] = ingredient

            # Repeated
            name = ewg_data['Name']
            sub_category = ewg_data['sub_category']
            cleaned_data[bp_id]['other_names'].append(name)
            cleaned_data[bp_id]['sub_category'].append(sub_category)

        # MUA
        mua_id_list = bp_ewg_mua_index[bp_id]['mua']
        if mua_id_list:
            sub_category_set = set()
            name_set = set()
            img_url_set = set()

            rating_list = []
            review_cnt_list = []
            repurchase_pct_list = []

            total_age_counter = {}
            total_skin_counter = {}
            total_skin_color_counter = {}
            total_hair_counter = {}
            total_hair_color_counter = {}
            total_eyes_counter = {}

            for mua_id in mua_id_list:
                if mua_id and mua_id in mua:
                    mua_data = mua[mua_id]
                    img_url = mua_data['img_url']
                    sub_category = mua_data['sub_category']
                    name = mua_data['product_name']
                    img_url_set.add(img_url)
                    sub_category_set.add(sub_category)
                    name_set.add(name)

                    score = mua_data['rating']
                    if score is None:
                        score = 0
                    review_cnt = mua_data['review_cnt']
                    if review_cnt is None:
                        review_cnt = 0
                    repurchase_pct = mua_data['repurchase_pct']
                    if repurchase_pct is None:
                        repurchase_pct = 0
                    rating_list.append(score)
                    review_cnt_list.append(review_cnt)
                    repurchase_pct_list.append(repurchase_pct)

                    age_counter = mua_data['reviews']['age_counter']
                    skin_type_counter = mua_data['reviews']['skin_type_counter']
                    skin_color_counter = mua_data['reviews']['skin_color_counter']
                    hair_style_counter = mua_data['reviews']['hair_style_counter']
                    hair_color_counter = mua_data['reviews']['hair_color_counter']
                    eyes_counter = mua_data['reviews']['eyes_counter']

                    for k, v in age_counter.items():
                        if k not in total_age_counter:
                            total_age_counter[k] = 0
                        total_age_counter[k] += v

                    for k, v in skin_type_counter.items():
                        if k not in total_skin_counter:
                            total_skin_counter[k] = 0
                        total_skin_counter[k] += v

                    for k, v in skin_color_counter.items():
                        if k not in total_skin_color_counter:
                            total_skin_color_counter[k] = 0
                        total_skin_color_counter[k] += v

                    for k, v in hair_style_counter.items():
                        if k not in total_hair_counter:
                            total_hair_counter[k] = 0
                        total_hair_counter[k] += v

                    for k, v in hair_color_counter.items():
                        if k not in total_hair_color_counter:
                            total_hair_color_counter[k] = 0
                        total_hair_color_counter[k] += v

                    for k, v in eyes_counter.items():
                        if k not in total_eyes_counter:
                            total_eyes_counter[k] = 0
                        total_eyes_counter[k] += v

            if rating_list:
                avg_score = sum(rating_list) / len(rating_list)
            else:
                avg_score = None
            if review_cnt_list:
                total_review_cnt = sum(review_cnt_list)
                mua_url = mua[mua_id_list[review_cnt_list.index(max(review_cnt_list))]]['product_url']
            else:
                total_review_cnt = None
                mua_url = ''
            if repurchase_pct_list:
                avg_repurchase_pct = sum(repurchase_pct_list) / len(repurchase_pct_list)
            else:
                avg_repurchase_pct = None

            cleaned_data[bp_id]['other_names'] += list(name_set)
            cleaned_data[bp_id]['sub_category'] += list(sub_category_set)
            cleaned_data[bp_id]['image_url'] += list(img_url_set)

            cleaned_data[bp_id].update({'mua_rating': round(avg_score * 2, 0) / 2, 'mua_review_cnt': total_review_cnt,
                                        'repurchase_pct': avg_repurchase_pct, 'mua_url': mua_url})

            cleaned_data[bp_id].update({'age_counter': total_age_counter, 'skin_type_counter': total_skin_counter,
                                        'skin_color_counter': total_skin_color_counter,
                                        'hair_style_counter': total_hair_counter,
                                        'hair_color_counter': total_hair_color_counter,
                                        'eyes_counter': total_eyes_counter})

        cleaned_data[bp_id]['ingredient'] = list(set(cleaned_data[bp_id]['ingredient']))
        cleaned_data[bp_id]['buy_url'] = list(set(cleaned_data[bp_id]['buy_url']))
        cleaned_data[bp_id]['other_names'] = list(set(cleaned_data[bp_id]['other_names']))
        cleaned_data[bp_id]['brand_url'] = list(set(cleaned_data[bp_id]['brand_url']))
        cleaned_data[bp_id]['sub_category'] = list(set(cleaned_data[bp_id]['sub_category']))
        cleaned_data[bp_id]['image_url'] = list(set(cleaned_data[bp_id]['image_url']))

    output = open(cleaned_output_file, 'w')
    output.write(json.dumps(cleaned_data, indent=4))
    output.close()

    return cleaned_data


def main():
    # bp 1-1 agg_ewg, 1-* mua.
    mua_bp = json.load(open(mua_bp_file, 'r', encoding='utf-8'))
    mua_ewg = json.load(open(mua_ewg_file, 'r', encoding='utf-8'))
    bp_ewg_ingre = json.load(open(bp_ewg_ingre_file, 'r', encoding='utf-8'))

    bp_ewg_mua_index = get_combined_index(mua_bp, mua_ewg)
    # print(bp_ewg_mua_index)

    bp = rebuild_file(bp_file)
    ewg = rebuild_file(ewg_file)
    mua = rebuild_file(mua_file)

    all_data = get_all_data(bp_ewg_mua_index, bp, ewg, mua)
    clean_data = get_cleaned_data(bp_ewg_mua_index, bp, ewg, mua, bp_ewg_ingre)


if __name__ == "__main__":
    main()
