#!/usr/bin/python3
"""
Queries the Reddit API recursively, parses the title of all hot articles, and prints a sorted count of given keywords.
"""

import requests

def count_words(subreddit, word_list, after=None, count_dict=None):
    """
    Recursively retrieves the titles of all hot articles for a given subreddit, counts the occurrences of given keywords,
    and prints the count in descending order, with tie-breakers sorted alphabetically.
    """
    if count_dict is None:
        count_dict = {}

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'limit': 100, 'after': after}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']
        for post in posts:
            title = post['data']['title'].lower()
            for word in word_list:
                word = word.lower()
                if title.count(word):
                    if word in count_dict:
                        count_dict[word] += title.count(word)
                    else:
                        count_dict[word] = title.count(word)

        after = data['data']['after']
        if after is not None:
            count_words(subreddit, word_list, after, count_dict)
        else:
            sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print("{}: {}".format(word, count))
    else:
        return None

