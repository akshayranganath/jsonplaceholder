import requests
from requests.api import get
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def get_url(url):
    result = {}
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            result = resp.json()
            logging.debug(result)
    except Exception as e:
        logging.error(e)
    return result


def post_url(url, data, headers=None):
    result = {}
    try:
        resp = requests.post(
            url,
            data=data,
            headers=headers
        )
        if resp.status_code == 201:
            result = resp.json()
        else:
            logging.error(
                f"Unable to create new object: Status {resp.status_code}")
    except Exception as e:
        logging.error(e)
    return result


def put_url(url, data, headers=None):
    result = {}
    try:
        resp = requests.put(
            url,
            data=data,
            headers=headers
        )
        if resp.status_code == 200 or resp.status_code == 204:
            result = resp.json()
        logging.debug(resp)
    except Exception as e:
        logging.error(e)
    return result


def get_all_posts():
    return get_url('https://jsonplaceholder.typicode.com/posts')


def get_single_post(post_id=1):
    return get_url(f'https://jsonplaceholder.typicode.com/posts/{post_id}')


def get_all_posts_by_user():
    return get_url('https://jsonplaceholder.typicode.com/posts?userId=1')


def create_new_post():
    # create a new post
    body = {
        'userId': 10,
        'title': 'Ask Your Developer',
        'body': 'How to harness the power of software developers and win in 21st century.'
    }
    # force header as JSON
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }
    result = post_url(
        'https://jsonplaceholder.typicode.com/posts',
        # need to do this to ensure the post body has only plain text data
        data=json.dumps(body),
        headers=headers
    )
    print(result)


def update_post(post_id=100):
    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    # first get the post
    item = get_single_post(post_id)

    if item != {}:
        # now change the title
        item['title'] = 'My python adventure'
        # force header as JSON
        headers = {
            'Content-type': 'application/json; charset=UTF-8'
        }
        # update the post
        resp = put_url(url,
                       data=json.dumps(item),
                       headers=headers
                       )
        print(resp)
    else:
        logging.error(f'No entry found for post: {post_id}')


if __name__ == "__main__":
    update_post()
