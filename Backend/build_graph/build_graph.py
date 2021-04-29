import os
import time
import json
from py2neo import Graph, Node


def read_nodes(data_path):
    # Nodes
    Product = set()
    Brand = set()
    Category = set()
    Subcategory = set()
    Ingredient = set()
    IngredientScore = set()
    IngredientAvail = set()
    Pros = set()
    Cons = set()
    Count = set()
    BestFor = set()
    UserTags = set()
    TagWeight = set()
    PurchaseLink = set()
    Colors = set()
    Concerns = set()

    product_details = []
    concerns_set = set()
    tags_set = set()

    # Relationships
    PRODUCED_BY = set()  # Product,Brand
    BELONGS_TO = set()  # Product, Subcategory
    SUBCLASS_OF = set()  # Subcategory, Category
    CONTAINS = set()  # Product, Ingredient
    HAS_SCORE = set()  # Ingredient, IngredientScore
    HAS_AVAILABILITY = set()  # Ingredient,IngredientAvail
    HAS_PROS = set()  # Product, Pros
    HAS_CONS = set()
    IN_NUMBER = set()  # Pros, ProsCount; Cons,ConsCount
    IS_BEST_FOR = set()  # Product, BestFor
    HAS_USER_TAG = set()  # Product, UserTags
    PURCHASE_FROM = set()  # Product, PurchaseLink
    IN_COLOR = set()  # Product, Colors
    HAS_CONCERNS = set()  # Product, GeneralConcerns; Product, OtherConcerns

    count = 0
    with open(data_path, 'r', encoding='utf8') as f:
        raw_data = json.loads(f.read())

    for record in raw_data.values():
        product_dict = {}
        product_dict['description'] = ''
        product_dict['expert_rating'] = ''
        product_dict['jar_package'] = ''
        product_dict['animal_test'] = ''
        product_dict['user_rating'] = ''
        product_dict['user_review_num'] = ''
        product_dict['repurchase_rate'] = ''

        count += 1
        # print(count)
        product_name = record['product_names']
        product_dict['name'] = product_name
        Product.add(product_name)

        product_dict['url'] = record['product_links']
        product_dict['product_id'] = record['product_id']
        product_dict['size'] = record['size']
        if 'claims' in record:
            product_dict['description'] = record['claims']
        if 'expert_rating' in record:
            product_dict['expert_rating'] = int(record['expert_rating'])
        if 'jar_package' in record:
            product_dict['jar_package'] = record['jar_package']
        if 'animal_test' in record:
            product_dict['animal_test'] = record['animal_test']
        if record['user_rating'] is not None:
            product_dict['user_rating'] = record['user_rating']
        if record['user_reviews']['usr_review_summary'] is not None:
            if record['user_reviews']['usr_review_summary']['usr_review_count'] is not None:
                product_dict['user_review_num'] = record['user_reviews']['usr_review_summary']['usr_review_count']
        if 'repurchase_pct' in record:
            if record['repurchase_pct'] != 0:
                product_dict['repurchase_rate'] = record['repurchase_pct']

        category = record['category']
        Category.add(category)
        BELONGS_TO.add((product_name, category))

        sub_category = record['sub_category'][0]
        Subcategory.add(sub_category)
        SUBCLASS_OF.add((sub_category, category))

        brand = record['brand']
        Brand.add(brand)
        PRODUCED_BY.add((product_name, brand))

        if 'ewg_ingredient' not in record:
            ingredients = record['ingredient']
            for ing in ingredients:
                Ingredient.add(ing)
                CONTAINS.add((product_name, ing))
        else:
            ingredients = record['ewg_ingredient']
            for ing, ing_details in ingredients.items():
                Ingredient.add(ing)
                CONTAINS.add((product_name, ing))

                IngredientScore.add(str(ing_details['Score']))
                HAS_SCORE.add((ing, str(ing_details['Score'])))

                IngredientAvail.add(ing_details['Data Availability'])
                HAS_AVAILABILITY.add((ing, ing_details['Data Availability']))

        if record['user_reviews']['usr_review_summary'] is not None:
            pros_tags = record['user_reviews']['usr_review_summary']['usr_pros_summary']
            if pros_tags is not None:
                for tag in pros_tags:
                    Pros.add(tag[1].replace("\"", "\'"))
                    Count.add(str(tag[0]))
                    HAS_PROS.add((product_name, tag[1].replace("\"", "\'")))
                    IN_NUMBER.add((tag[1].replace("\"", "\'"), str(tag[0])))

            cons_tags = record['user_reviews']['usr_review_summary']['usr_cons_summary']
            if cons_tags is not None:
                for tag in cons_tags:
                    Cons.add(tag[1].replace("\"", "\'"))
                    Count.add(str(tag[0]))
                    HAS_CONS.add((product_name, tag[1].replace("\"", "\'")))
                    IN_NUMBER.add((tag[1].replace("\"", "\'"), str(tag[0])))

        bestfor_tags = {}
        user_tags = {}

        pos_reviews = record['user_reviews']['usr_review_details']['positive_reviews']
        if pos_reviews is not None:
            for review in pos_reviews:
                if review['review_best_for'] is not None:
                    for tag in review['review_best_for']:
                        if tag.replace("\"", "\'") in bestfor_tags:
                            bestfor_tags[tag.replace("\"", "\'")] += 1
                        else:
                            bestfor_tags[tag.replace("\"", "\'")] = 1

                routine_time = review['usr_routine_time']
                if routine_time is not None:
                    if routine_time in user_tags:
                        user_tags[routine_time][0] += 1
                    else:
                        user_tags[routine_time] = [1, 'Routine Time']

                if review['usr_def_tag'] is not None:
                    for tag in review['usr_def_tag']:
                        if tag in user_tags:
                            user_tags[tag][0] += 1
                        else:
                            user_tags[tag] = [1, 'Self Description']

        neg_reviews = record['user_reviews']['usr_review_details']['negative_reviews']
        if neg_reviews is not None:
            for review in neg_reviews:
                if review['review_best_for'] is not None:
                    for tag in review['review_best_for']:
                        if tag.replace("\"", "\'") in bestfor_tags:
                            bestfor_tags[tag.replace("\"", "\'")] += 1
                        else:
                            bestfor_tags[tag.replace("\"", "\'")] = 1

                routine_time = review['usr_routine_time']
                if routine_time is not None:
                    if routine_time in user_tags:
                        user_tags[routine_time][0] -= 1
                    else:
                        user_tags[routine_time] = [-1, 'Routine Time']

                if review['usr_def_tag'] is not None:
                    for tag in review['usr_def_tag']:
                        if tag in user_tags:
                            user_tags[tag][0] -= 1
                        else:
                            user_tags[tag] = [-1, 'Self Description']

        if bestfor_tags != {}:
            for t, c in bestfor_tags.items():
                BestFor.add(t)
                TagWeight.add(c)
                IN_NUMBER.add((t, str(c)))
                IS_BEST_FOR.add((product_name, t))

        if record['buy_url'] != []:
            for url in record['buy_url']:
                PurchaseLink.add(url)
                PURCHASE_FROM.add((product_name, url))

        if 'colors' in record:
            for c in record['colors']:
                Colors.add(c['Color'])
                IN_COLOR.add((product_name, c['Color']))

        if 'overall_concerns' in record:
            for concern, level in record['overall_concerns'].items():
                Concerns.add(concern)
                HAS_CONCERNS.add((product_name, concern, level))
                concerns_set.add((concern, 'Overall Concerns', level))

        if 'other_concerns' in record:
            for level, concerns in record['other_concerns'].items():
                for c in concerns:
                    Concerns.add(concern)
                    HAS_CONCERNS.add((product_name, c, level))
                    concerns_set.add((c, 'Other Concerns', level))

        if 'age_counter' in record:
            for age, count in record['age_counter'].items():
                if age in user_tags:
                    user_tags[age][0] += count
                else:
                    user_tags[age] = [count, 'Age']

        if 'skin_type_counter' in record:
            for skin_type, count in record['skin_type_counter'].items():
                if skin_type in user_tags:
                    user_tags[skin_type][0] += count
                else:
                    user_tags[skin_type] = [count, 'Skin Type']

        if 'hair_style_counter' in record:
            for hair_style, count in record['hair_style_counter'].items():
                if hair_style in user_tags:
                    user_tags[hair_style][0] += count
                else:
                    user_tags[hair_style] = [count, 'Hair Style']

        if 'eyes_counter' in record:
            for eyes, count in record['eyes_counter'].items():
                if eyes in user_tags:
                    user_tags[eyes][0] += count
                else:
                    user_tags[eyes] = [count, 'Eye Color']

        if user_tags != {}:
            for t, c in user_tags.items():
                UserTags.add(t)
                TagWeight.add(c[0])
                IN_NUMBER.add((t, str(c[0])))
                HAS_USER_TAG.add((product_name, t, c[1]))
                tags_set.add((t, c[1]))

        product_details.append(product_dict)

    return Product, Brand, Category, Subcategory, Ingredient, IngredientScore, IngredientAvail, Pros, Cons, Count, BestFor, UserTags, TagWeight, PurchaseLink, Colors, Concerns, product_details, concerns_set, tags_set, PRODUCED_BY, BELONGS_TO, SUBCLASS_OF, CONTAINS, HAS_SCORE, HAS_AVAILABILITY, HAS_PROS, HAS_CONS, IN_NUMBER, IS_BEST_FOR, HAS_USER_TAG, PURCHASE_FROM, IN_COLOR, HAS_CONCERNS


def create_node(g, label, nodes):
    print("Generate Node", label)
    for node_name in set(nodes):
        node = Node(label, name=node_name)
        g.create(node)
    print(len(nodes))
    return


def create_product_nodes(g, product_details):
    count = 0
    for product_dict in product_details:
        node = Node("Product", name=product_dict['name'], product_id=product_dict['product_id'],
                    product_url=product_dict['url'], size=product_dict['size'], description=product_dict['description'],
                    expert_rating=product_dict['expert_rating'], jar_package=product_dict['jar_package'],
                    animal_test=product_dict['animal_test'], user_rating=product_dict['user_rating'],
                    user_review_num=product_dict['user_review_num'], repurchase_rate=product_dict['repurchase_rate']
                    )
        g.create(node)
    return


def create_concern_nodes(g, concerns_set):
    count = 0
    for concern in concerns_set:
        node = Node("Concerns", name=concern[0], type=concern[1], level=concern[2])
        g.create(node)
    return


def create_tag_nodes(g, tags_set):
    count = 0
    for tag in tags_set:
        node = Node("UserTags", name=tag[0], attribute=tag[1])
        g.create(node)
    return


def create_relationship(g, start_node, end_node, edges, rel_type):
    print("Generate Edge", rel_type)
    print(len(edges))
    for eg in edges:
        p = eg[0]
        q = eg[1]
        query = 'match(p:%s),(q:%s) where p.name="%s"and q.name="%s" create (p)-[rel:%s]->(q)' % (
            start_node, end_node, p, q, rel_type)
        try:
            g.run(query)
        except Exception as e:
            print(e)
    return


def create_concern_relationship(g, start_node, end_node, edges, rel_type):
    print("Generate Edge", rel_type)
    print(len(edges))
    for eg in edges:
        p = eg[0]
        q = eg[1]
        l = eg[2]
        query = 'match(p:%s),(q:%s) where p.name="%s"and q.name="%s" and q.level="%s" create (p)-[rel:%s]->(q)' % (
            start_node, end_node, p, q, l, rel_type)
        try:
            g.run(query)
        except Exception as e:
            print(e)
    return


def create_tag_relationship(g, start_node, end_node, edges, rel_type):
    print("Generate Edge", rel_type)
    print(len(edges))
    for eg in edges:
        p = eg[0]
        q = eg[1]
        a = eg[2]
        query = 'match(p:%s),(q:%s) where p.name="%s"and q.name="%s" and q.attribute="%s" create (p)-[rel:%s]->(q)' % (
            start_node, end_node, p, q, a, rel_type)
        try:
            g.run(query)
        except Exception as e:
            print(e)
    return


def create_graphnodes(g, nodes_data):
    Product, Brand, Category, Subcategory, Ingredient, IngredientScore, IngredientAvail, Pros, Cons, Count, BestFor, UserTags, TagWeight, PurchaseLink, Colors, Concerns, product_details, concerns_set, tags_set, PRODUCED_BY, BELONGS_TO, SUBCLASS_OF, CONTAINS, HAS_SCORE, HAS_AVAILABILITY, HAS_PROS, HAS_CONS, IN_NUMBER, IS_BEST_FOR, HAS_USER_TAG, PURCHASE_FROM, IN_COLOR, HAS_CONCERNS = nodes_data
    create_product_nodes(g, product_details)
    create_concern_nodes(g, concerns_set)
    create_tag_nodes(g, tags_set)
    create_node(g, 'Brand', Brand)
    create_node(g, 'Category', Category)
    create_node(g, 'Subcategory', Subcategory)
    create_node(g, 'Ingredient', Ingredient)
    create_node(g, 'IngredientScore', IngredientScore)
    create_node(g, 'IngredientAvail', IngredientAvail)
    create_node(g, 'Pros', Pros)
    create_node(g, 'Cons', Cons)
    create_node(g, 'Count', Count)
    create_node(g, 'BestFor', BestFor)
    create_node(g, 'TagWeight', TagWeight)
    create_node(g, 'PurchaseLink', PurchaseLink)
    create_node(g, 'Colors', Colors)
    return


def create_graphrels(g, nodes_data):
    Product, Brand, Category, Subcategory, Ingredient, IngredientScore, IngredientAvail, Pros, Cons, Count, BestFor, UserTags, TagWeight, PurchaseLink, Colors, Concerns, product_details, concerns_set, tags_set, PRODUCED_BY, BELONGS_TO, SUBCLASS_OF, CONTAINS, HAS_SCORE, HAS_AVAILABILITY, HAS_PROS, HAS_CONS, IN_NUMBER, IS_BEST_FOR, HAS_USER_TAG, PURCHASE_FROM, IN_COLOR, HAS_CONCERNS = nodes_data
    create_relationship(g, 'Product', 'Brand', PRODUCED_BY, 'PRODUCED_BY')
    create_relationship(g, 'Product', 'Subcategory', BELONGS_TO, 'BELONGS_TO')
    create_relationship(g, 'Subcategory', 'Category', SUBCLASS_OF, 'SUBCLASS_OF')
    create_relationship(g, 'Product', 'Ingredient', CONTAINS, 'CONTAINS')
    create_relationship(g, 'Ingredient', 'IngredientScore', HAS_SCORE, 'HAS_SCORE')
    create_relationship(g, 'Ingredient', 'IngredientAvail', HAS_AVAILABILITY, 'HAS_AVAILABILITY')
    create_relationship(g, 'Product', 'Pros', HAS_PROS, 'HAS_PROS')
    create_relationship(g, 'Product', 'Cons', HAS_CONS, 'HAS_CONS')
    create_relationship(g, 'Pros', 'Count', IN_NUMBER, 'IN_NUMBER')
    create_relationship(g, 'Cons', 'Count', IN_NUMBER, 'IN_NUMBER')
    create_relationship(g, 'Product', 'BestFor', IS_BEST_FOR, 'IS_BEST_FOR')
    create_tag_relationship(g, 'Product', 'UserTags', HAS_USER_TAG, 'HAS_USER_TAG')
    create_relationship(g, 'Product', 'PurchaseLink', PURCHASE_FROM, 'PURCHASE_FROM')
    create_relationship(g, 'UserTags', 'TagWeight', IN_NUMBER, 'IN_NUMBER')
    create_relationship(g, 'Product', 'Colors', IN_COLOR, 'IN_COLOR')
    create_concern_relationship(g, 'Product', 'Concerns', HAS_CONCERNS, 'HAS_CONCERNS')
    return


def main():
    input_file = '../data/cleaned_data.json'

    nodes_data = read_nodes(input_file)

    graph = Graph(
        host="127.0.0.1",
        http_port=7474,
        user="neo4j",
        password="makeuppedia") 

    # graph = Graph('http://localhost:7474/', username='neo4j', password='makeuppedia')

    nodes_data = read_nodes(input_file)
    create_graphnodes(graph, nodes_data)
    create_graphrels(graph, nodes_data)


if __name__ == "__main__":
    main()
