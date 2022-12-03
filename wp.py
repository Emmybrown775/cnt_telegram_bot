import requests
import json
import html
import datetime as dt
from requests.auth import HTTPBasicAuth


class WP:

    def __init__(self):
        self.user = "admin"
        self.password = "WWZy HIrO msVm 8K0f XMrG QrX6"
        self.today_date = dt.datetime.now()
        self.const = f"Open Heaven For Teens {self.today_date.date().day} {self.today_date.strftime('%B')} 2022"
        self.sourceURL = "https://flatimes.com/wp-json/wp/v2/posts?per_page=20"
        self.wpBaseUrl = "https://christnestteens.com/"
        self.postStatus = "publish"

    def post_op(self):
        response_API = requests.get(self.sourceURL)
        data = response_API.json()
        parse_json = {}
        for posts in data:
            title = html.unescape(posts["title"]["rendered"])
            if self.const in title:
                parse_json = posts
        print(parse_json)

        if parse_json != {}:
            get_article_title = parse_json["title"]["rendered"]

            get_article_content = parse_json['content']["rendered"]

            WP_url = self.wpBaseUrl + "/wp-json/wp/v2/posts"

            auth = HTTPBasicAuth(self.user, self.password)

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            payload = json.dumps({
                "status": self.postStatus,
                "title": get_article_title,
                "content": get_article_content,
                "categories": 14

            })

            response = requests.request(
                "POST",
                WP_url,
                data=payload,
                headers=headers,
                auth=auth
            )

            if response.status_code == 201:
                return self.get_last_post()
            else:
                return "UnSuccessful please try again"

        else:
            return "Flattimes Doesn't Have This Currently please try again later "

    def get_date(self):
        return str(self.today_date)

    def get_last_post(self):
        response2 = requests.get(url="https://christnestteens.com/wp-json/wp/v2/posts")
        data2 = response2.json()
        link = data2[0]["link"]
        title = html.unescape(data2[0]["title"]["rendered"])
        return f"{link}/ \n\n\n {title}"


