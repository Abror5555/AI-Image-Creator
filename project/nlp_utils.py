import json
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict
from nltk.corpus import stopwords

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# COCO caption faylidan indeks yaratish
stop_words = set(stopwords.words('english'))

def build_keyword_index(caption_file):
    with open(caption_file, 'r') as f:
        data = json.load(f)

    keyword_index = defaultdict(set)

    for item in data['annotations']:
        caption = item['caption'].lower()
        image_id = item['image_id']
        tokens = word_tokenize(caption)
        for token in tokens:
            if token.isalpha() and token not in stop_words:
                keyword_index[token].add(f"{image_id:012}.jpg")

    return {k: list(v) for k, v in keyword_index.items()}


# Foydalanuvchi matnidan kalit so‘zlar
stop_words = set(stopwords.words('english'))
def extract_keywords(text, vocabulary):
    tokens = word_tokenize(text.lower())
    keywords = [word for word in tokens if word in vocabulary and word not in stop_words]
    return list(set(keywords))

