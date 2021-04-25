import json
import copy


def main():
    agg_ewg_dict = {}
    with open('../data_raw/ewg_data.jl', 'r', encoding='utf8') as f:
        data = f.readlines()
        for r in data:
            record = json.loads(r)
            dict_key = record['Name'] + record['Brand Name']
            if dict_key not in agg_ewg_dict:
                agg_ewg_dict[dict_key] = copy.deepcopy(record)
                del agg_ewg_dict[dict_key]['Color']
                del agg_ewg_dict[dict_key]['product_url']
                agg_ewg_dict[dict_key]['Colors'] = [{'Color': record['Color'], 'url': record['product_url']}]
            else:
                agg_ewg_dict[dict_key]['Colors'].append({'Color': record['Color'], 'url': record['product_url']})

    with open('../data_raw/agg_ewg_data.jl', 'w', encoding="utf8") as f:
        for record in agg_ewg_dict.values():
            json.dump(record, f)
            f.write('\n')


if __name__ == "__main__":
    main()
