import string
from collections import defaultdict, Counter
import httpx
from matplotlib import pyplot as plt
import concurrent.futures

def get_text(url):
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(url):
    text = get_text(url)
    if text:
        text = remove_punctuation(text)
        words = text.split()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            mapped_values = list(executor.map(map_function, words))
        shuffled_values = shuffle_function(mapped_values)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            reduced_values = list(executor.map(reduce_function, shuffled_values))

        return dict(reduced_values)
    else:
        return None

def visualize_top_words(result):
    top_10 = Counter(result).most_common(10)
    labels, values = zip(*top_10)
    plt.figure(figsize=(10, 5))
    plt.barh(labels, values, color='g')
    plt.xlabel('Кількість')
    plt.ylabel('Слово')
    plt.title('10 найпопулярніших слів')
    plt.show()

if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks01/0100011.txt"

    result = map_reduce(url)

    print("Результат:", result)
    visualize_top_words(result)