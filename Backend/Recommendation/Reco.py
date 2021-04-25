import os
import time
import copy
import json
from tqdm import tqdm

cleaned_input_file = '../data/cleaned_data.json'


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


def reco(cleaned_input, age, skins, hairs, eye):

    score_list = []
    for item in cleaned_input:
        age_score, skin_score, hair_score, eye_score = 0, 0, 0, 0
        if age in cleaned_input[item]['age_counter']:
            age_score = cleaned_input[item]['age_counter'][age]
        for skin in skins:
            if skin in cleaned_input[item]['skin_type_counter']:
                skin_score += cleaned_input[item]['skin_type_counter'][skin]
        for hair in hairs:
            if hair in cleaned_input[item]['hair_style_counter']:
                hair_score += cleaned_input[item]['hair_style_counter'][hair]
        if eye in cleaned_input[item]['eyes_counter']:
            eye_score = cleaned_input[item]['eyes_counter'][eye]

        score = age_score + skin_score + hair_score + eye_score
        score_list.append((item, score))

    score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
    print(score_list)
    print(cleaned_input[score_list[0][0]])

    return 0


def reco_main(age, skins, hairs, eye):
    cleaned_input = json.load(open(cleaned_input_file, 'r', encoding='utf-8'))
    total_age_keys, total_skin_keys, total_hair_keys, total_eyes_keys = get_all_counter_keys(cleaned_input)
    # print(total_age_keys, total_skin_keys, total_hair_keys, total_eyes_keys)
    result = reco(cleaned_input, age, skins, hairs, eye)


if __name__ == "__main__":
    age = '19-24'
    skins = ['Oily', 'Sensitive']
    hairs = ['Black', 'Straight']
    eye = 'Brown'
    reco_main(age, skins, hairs, eye)
