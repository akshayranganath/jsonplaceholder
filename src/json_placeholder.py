import requests
import logging
import json

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def make_request(url, method='get', data=None, headers=None):
    result = {}
    try:
        if method == 'get':
            resp = requests.get(url)
            if resp.status_code == 200:
                result = resp.json()
                logging.debug(result)
        elif method == 'post':
            resp = requests.post(
                url,
                data=data,
                headers=headers
            )
            logging.debug(resp)
            if resp.status_code == 201:
                result = resp.json()
            else:
                logging.error(
                    f"Unable to create new object: Status {resp.status_code}")
        elif method == 'put':
            resp = requests.put(
                url,
                data=data,
                headers=headers
            )
            logging.debug(resp)
            if resp.status_code == 200 or resp.status_code == 204:
                result = resp.json()
            logging.debug(resp)
        else:
            logging.error(f'Unknown Method: {method}')

    except Exception as e:
        logging.error(e)
    return result


def get_all_posts():
    return make_request('https://jsonplaceholder.typicode.com/posts')


def get_single_post(post_id=1):
    return make_request(f'https://jsonplaceholder.typicode.com/posts/{post_id}')


def get_all_posts_by_user():
    return make_request('https://jsonplaceholder.typicode.com/posts?userId=1')


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
    result = make_request(
        'https://jsonplaceholder.typicode.com/posts',
        method='post',
        # need to do this to ensure the post body has only plain text data
        data=json.dumps(body),
        headers=headers
    )
    return result


def update_post(post_id=100):
    result = {}
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
        resp = make_request(url,
                            method='put',
                            data=json.dumps(item),
                            headers=headers
                            )
        logging.info(resp)
    else:
        logging.error(f'No entry found for post: {post_id}')
    return result


if __name__ == "__main__":
    get_all_posts()
    get_single_post()
    get_all_posts_by_user()
    create_new_post()
    update_post()
