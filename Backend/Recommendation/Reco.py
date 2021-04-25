import os
import time
import copy
import json
from tqdm import tqdm

cleaned_input_file = '../data/cleaned_data.json'


def main():
    cleaned_input = json.load(open(cleaned_input_file, 'r', encoding='utf-8'))
    print(cleaned_input)


if __name__ == "__main__":
    main()
