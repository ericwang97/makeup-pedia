import rltk
import copy
import json
import csv
import re


############## Product Name ER ##############
@rltk.remove_raw_object
class EWG(rltk.Record):
    @rltk.cached_property
    def id(self):
        return str(self.raw_object['product_id'])

    @rltk.cached_property
    def name(self):
        return self.raw_object['Name'].strip()

    @rltk.cached_property
    def url(self):
        return [c['url'] for c in self.raw_object['Colors']]

    @rltk.cached_property
    def colors(self):
        return [c['Color'] for c in self.raw_object['Colors']]

    @rltk.cached_property
    def brand(self):
        return self.raw_object['Brand Name'].strip()

    @rltk.cached_property
    def category(self):
        return self.raw_object['category'].strip()

    @rltk.cached_property
    def sub_category(self):
        return self.raw_object['sub_category'].strip()


@rltk.remove_raw_object
class MakeupAlley(rltk.Record):
    @rltk.cached_property
    def id(self):
        return str(self.raw_object['product_id'])

    @rltk.cached_property
    def name(self):
        return self.raw_object['product_name'].strip()

    @rltk.cached_property
    def url(self):
        return self.raw_object['product_url'].strip()

    @rltk.cached_property
    def brand(self):
        if self.raw_object['brand_name'] is not None:
            return self.raw_object['brand_name'].strip()
        else:
            return ""

    @rltk.cached_property
    def category(self):
        if self.raw_object['category'] is not None:
            return self.raw_object['category']
        else:
            return ""

    @rltk.cached_property
    def sub_category(self):
        if self.raw_object['sub_category'] is not None:
            return self.raw_object['sub_category']
        else:
            return ""


@rltk.remove_raw_object
class BeautyPedia(rltk.Record):
    @rltk.cached_property
    def id(self):
        return str(self.raw_object['product_id'])

    @rltk.cached_property
    def name(self):
        return self.raw_object['product_names'].strip()

    @rltk.cached_property
    def url(self):
        return self.raw_object['product_links'].strip()

    @rltk.cached_property
    def brand(self):
        if self.raw_object['brand'] is not None:
            return self.raw_object['brand'].strip()
        else:
            return ""

    @rltk.cached_property
    def category(self):
        if self.raw_object['category'] is not None:
            return self.raw_object['category']
        else:
            return ""

    @rltk.cached_property
    def sub_category(self):
        if self.raw_object['sub_category'] is not None:
            return self.raw_object['sub_category']
        else:
            return ""


ewg_data = rltk.Dataset(reader=rltk.JsonLinesReader('agg_ewg_data.jl'), record_class=EWG,
                        adapter=rltk.MemoryKeyValueAdapter())
mua_data = rltk.Dataset(reader=rltk.JsonLinesReader('mua_meta_data.jl'), record_class=MakeupAlley,
                        adapter=rltk.MemoryKeyValueAdapter())
bp_data = rltk.Dataset(reader=rltk.JsonLinesReader('beautypedia.jl'), record_class=BeautyPedia,
                       adapter=rltk.MemoryKeyValueAdapter())


# EWG & MUA
def rule_based_method(r_ewg, r_mua):
    name_score = 0
    ewg_product = r_ewg.name.lower().replace(r_ewg.brand, '')
    mua_product = r_mua.name.split('- | in ')[0].strip()
    sim = rltk.jaro_winkler_similarity(ewg_product, mua_product.lower())
    # name_score = rltk.jaro_winkler_similarity(ewg_product,r_mua.name.lower())
    if sim > 0.7:
        name_score = sim

    brand_score = 0
    # brand_score = rltk.levenshtein_similarity(r_ewg.brand.lower(),r_mua.brand.lower())
    if rltk.levenshtein_distance(r_ewg.brand.lower(), r_mua.brand.lower()) <= min(len(r_ewg.brand),
                                                                                  len(r_mua.brand)) / 3:
        brand_score = 1

    category_score = 0
    cor_cat_dict = {'Bronzer/Highlighter': ['Face', 'Cheeks'], 'Concealer': ['Concealer'],
                    'Facial Powder': ['Pressed Powder', 'Loose Powder'], 'Foundation': ['Foundation'],
                    'Makeup Primer': ['Face Primer', 'Color Corrector'],
                    'Makeup Remover': ['Other Face', 'Other Eyes', 'Other Lips', 'Other Cheeks'],
                    'Brow Liner': ['Eyebrows'], 'Eye Liner': ['Eyeliner'], 'Eye Makeup Remover': ['Other Eyes'],
                    'Eye Shadow': ['Eyeshadow', 'Eye Palettes'], 'Mascara': ['Mascara'],
                    'Eyelash Glue': ['False Lashes', 'Other Eyes'],
                    'Other Eye Makeup': ['False Lashes', 'Other Eyes', 'Eyeshadow'],
                    'Lip Balm': ['Lip Balm & Treatment'], 'Lip balm with SPF': ['Lip Balm & Treatment'],
                    'Lip Gloss': ['Lip Gloss'], 'Lip Liner': ['Lip Liner'], 'Lip Plumper': ['Lip Plumper'],
                    'Lipstick': ['Lipstick'], 'Body Art': [''], 'Glitter': ['']}
    ewg_cat = r_ewg.sub_category
    cor_cat = set(cor_cat_dict[ewg_cat])
    mua_cat = {r_mua.sub_category, r_mua.category}
    if len(cor_cat & mua_cat) > 0:
        category_score = 1

    total = 0.65 * name_score + 0.35 * category_score
    return total > 0.75, total


general_cat_dict = {'Foundation': 'Face', 'Face': 'Face', 'Cheeks': 'Face', 'Lips': 'Lips', 'Eyes': 'Eyes'}
bg = rltk.HashBlockGenerator()
block = bg.generate(
    bg.block(ewg_data, function_=lambda r: r.brand.lower() + r.category),
    bg.block(mua_data, function_=lambda r: r.brand.lower() + general_cat_dict[r.category])
)
pairs = rltk.get_record_pairs(ewg_data, mua_data, block=block)
print(sum(1 for _ in pairs))  # length of candidate pairs: 152304
print(sum(1 for _ in ewg_data))  # length of dataset ebooks: 4711
print(sum(1 for _ in mua_data))  # length of dataset itunes: 29965

## constraint
candidates = {}
for r_ewg, r_mua in pairs:
    result, confidence = rule_based_method(r_ewg, r_mua)
    if result:
        if r_mua.id in candidates:
            candidates[r_mua.id].append(
                [r_ewg.id, r_ewg.name, r_ewg.colors, r_ewg.brand, r_mua.id, r_mua.name, r_mua.brand, confidence])
        else:
            candidates[r_mua.id] = [
                [r_ewg.id, r_ewg.name, r_ewg.colors, r_ewg.brand, r_mua.id, r_mua.name, r_mua.brand, confidence]]

constraint = {}
for muaid, content in candidates.items():
    if len(content) > 1:
        max_conf = 0
        for match in content:
            if match[7] > max_conf:
                max_conf = match[7]
                max_record = match
        constraint[muaid] = max_record
    else:
        constraint[muaid] = content[0]

mua_ewg_id = {}
with open('ewg_mua_pairs_result.txt', 'w', encoding="utf8") as f:
    for muaid, content in constraint.items():
        f.write(str(content))
        f.write('\n')
        mua_ewg_id[int(muaid)] = int(content[0])

with open('mua_ewg_id.json', 'w', encoding="utf8") as f:
    json.dump(mua_ewg_id, f)


# MUA&BP


def rule_based_method(r_mua, r_bp):
    name_score = 0
    mua_product = r_mua.name.split('- | in ')[0].strip().lower()
    bp_product = r_bp.name.lower()
    sim = rltk.jaro_winkler_similarity(mua_product, bp_product)
    # name_score = rltk.jaro_winkler_similarity(mua_product,bp_product)
    if sim > 0.7:
        name_score = sim

    category_score = 0
    cor_cat_dict = {'Eyebrow Makeup': ['Eyebrows'],
                    'Eyelash Primer & Treatment': ['Eye Primer', 'Lash Serum', 'False Lashes', 'Other Eyes', 'Mascara'],
                    'Eyeliner': ['Eyeliner'], 'Eyeshadow': ['Eyeshadow'],
                    'Eyeshadow Palette': ['Eyeshadow', 'Eye Palettes'],
                    'Eyeshadow Primer & Base': ['Eye Primer', 'Other Eyes'], 'Mascara': ['Mascara'],
                    'Waterproof Mascara': ['Mascara'], 'BB & CC Cream': ['BB & CC Cream'],
                    'Blush': ['Blush', 'Blush Palettes', 'Other Cheeks'], 'Bronzer': ['Bronzer', 'Other Cheeks'],
                    'Concealer & Corrector': ['Color Corrector', 'Concealer'], 'Contour': ['Contour'],
                    'Face Powder': ['Loose Powder', 'Pressed Powder', 'Face Palettes', 'Other Face'],
                    'Foundation Primer': ['Face Primer', 'Other Foundation', 'Other Face'],
                    'Foundation With Sunscreen': ['Foundation'], 'Foundation Without Sunscreen': ['Foundation'],
                    'Highlighter': ['Highlighter'], 'Setting Spray': ['Setting Spray'],
                    'Tinted Moisturizer': ['Tinted Moisturizer'],
                    'Lip Gloss': ['Lip Gloss', 'Lip Plumper', 'Other Lips', 'Lip Balm & Treatment'],
                    'Lip Liner': ['Lip Liner'], 'Lipstick': ['Lipstick', 'Other Lips', 'Lip Palettes']}
    bp_cat = r_bp.sub_category
    bp_cor_cat = set(cor_cat_dict[bp_cat])
    mua_cat = {r_mua.sub_category, r_mua.category}
    if len(bp_cor_cat & mua_cat) > 0:
        category_score = 1

    total = 0.65 * name_score + 0.35 * category_score
    return total > 0.75, total


# generate blocks
bg = rltk.HashBlockGenerator()
block = bg.generate(
    bg.block(mua_data, function_=lambda r: r.brand.lower() + general_cat_dict[r.category]),
    bg.block(bp_data, function_=lambda r: r.brand.lower() + r.category)
)

## prediction
pairs = rltk.get_record_pairs(mua_data, bp_data, block=block)
print(sum(1 for _ in pairs))  # length of candidate pairs: 304422
print(sum(1 for _ in mua_data))  # length of dataset: 29965
print(sum(1 for _ in bp_data))  # length of dataset: 4177

## constraint
candidates = {}
for r_mua, r_bp in pairs:
    result, confidence = rule_based_method(r_mua, r_bp)
    if result:
        if r_mua.id in candidates:
            candidates[r_mua.id].append([r_mua.id, r_mua.name, r_mua.brand, r_bp.id, r_bp.name, r_bp.brand, confidence])
        else:
            candidates[r_mua.id] = [[r_mua.id, r_mua.name, r_mua.brand, r_bp.id, r_bp.name, r_bp.brand, confidence]]

constraint = {}
for muaid, content in candidates.items():
    if len(content) > 1:
        max_conf = 0
        for match in content:
            if match[6] > max_conf:
                max_conf = match[6]
                max_record = match
        constraint[muaid] = max_record
    else:
        constraint[muaid] = content[0]

mua_bp_id = {}
with open('bp_mua_pairs_result.txt', 'w', encoding="utf8") as f:
    for muaid, content in constraint.items():
        f.write(str(content))
        f.write('\n')
        mua_bp_id[int(muaid)] = int(content[3])

with open('mua_bp_id.json', 'w', encoding="utf8") as f:
    json.dump(mua_bp_id, f)

############## Ingredient ER ##############

ewg_ingredent = set()
with open('agg_ewg_data.jl', 'r', encoding='utf8') as f:
    ewg_data = f.readlines()
    for r in ewg_data:
        record = json.loads(r)
        for chemical_name in record['Ingredient'].keys():
            if chemical_name not in ewg_ingredent:
                ewg_ingredent.add(chemical_name)

ewg_index = 0
with open('ewg_ingredient.jl', 'w', encoding="utf8") as f:
    for ing in ewg_ingredent:
        json.dump({'id': ewg_index, 'ingredient': ing}, f)
        f.write('\n')
        ewg_index += 1


@rltk.remove_raw_object
class Ingredient(rltk.Record):
    @rltk.cached_property
    def id(self):
        return str(self.raw_object['id'])

    @rltk.cached_property
    def name(self):
        return self.raw_object['ingredient']


bp_data = rltk.Dataset(reader=rltk.JsonLinesReader('bp_ingredient.jl'), record_class=Ingredient,
                       adapter=rltk.MemoryKeyValueAdapter())
ewg_data = rltk.Dataset(reader=rltk.JsonLinesReader('ewg_ingredient.jl'), record_class=Ingredient,
                        adapter=rltk.MemoryKeyValueAdapter())


def rule_based_method(r_bp, r_ewg):
    name_score = rltk.levenshtein_similarity(r_bp.name.lower(),
                                             r_ewg.name.lower())  # rltk.hybrid_jaccard_similarity(r_l_set, r_r_set,
    # threshold=0.6, function=rltk.needleman_wunsch_similarity) #jaccard_index_similarity(r_l_set,r_r_set)
    return name_score > 0.7, name_score


pairs = rltk.get_record_pairs(bp_data, ewg_data)
bp_ingre_2_ewg_ingre = {}
for r_bp, r_ewg in pairs:
    result, confidence = rule_based_method(r_bp, r_ewg)
    if result:
        if r_bp.name not in bp_ingre_2_ewg_ingre:
            bp_ingre_2_ewg_ingre[r_bp.name] = [r_ewg.name, confidence]
        else:
            if confidence > bp_ingre_2_ewg_ingre[r_bp.name][1]:
                bp_ingre_2_ewg_ingre[r_bp.name] = [r_ewg.name, confidence]

for bp_name, ewg_name in bp_ingre_2_ewg_ingre.items():
    bp_ingre_2_ewg_ingre[bp_name] = ewg_name[0]

with open('bp_ewg_ingre_name.json', 'w', encoding='utf8') as f:
    json.dump(bp_ingre_2_ewg_ingre, f)
