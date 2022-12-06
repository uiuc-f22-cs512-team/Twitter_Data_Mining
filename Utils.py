import requests
import os
import json
import pandas as pd

class Utils():
    def __init__(self):
        self.bearer_token = "AAAAAAAAAAAAAAAAAAAAAKEUhgEAAAAAYo%2FYh5Jpb%2Fau8yaOs%2BO1bojGfFY%3DjkemdnofEolHLUwEzS7STSxqbrheB3FwKlldyCPHia9bF4tUcU"

    # Default user_id is of elonmusk's account.
    def get_tweet_url(self, user_id=44196397):
        return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

    # It's strange because it seems I cannot find those users in Twitter by their username.
    # Maybe they're new users.
    def get_follower_url(self, user_id=44196397):
        return "https://api.twitter.com/2/users/{}/followers".format(user_id)
    
    # Get the current user's following list and it propagates forward.
    def get_following_url(self, user_id=44196397):
        return "https://api.twitter.com/2/users/{}/following".format(user_id)

    def get_params(self, req_type):
        if (req_type == "tweet"):
            return {
                "tweet.fields": "conversation_id,author_id,in_reply_to_user_id,referenced_tweets,created_at,lang,text,entities,id,source,withheld",
                "expansions" : "author_id,in_reply_to_user_id,referenced_tweets.id", 
                "user.fields" : "name,username",
                "max_results" : "10"
                }
        elif (req_type == "follower" or req_type == "following"):
            return {
                "user.fields": "created_at",
                "max_results" : "10"
                }


    def bearer_auth(self, request):
        request.headers['Authorization'] = f"Bearer {self.bearer_token}"
        request.headers['User-Agent'] = "v2UserTweetsPython"

        return request
    
    def connect_to_endpoint(self, url, params):
        response = requests.request("GET", url, auth=self.bearer_auth, params=params)
        print(response.status_code)
        if (response.status_code != 200):
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code,
                    response.text
                )
            )

        return response.json()



test_utils = Utils()
url = test_utils.get_tweet_url()
params = test_utils.get_params("tweet")
json_response = test_utils.connect_to_endpoint(url, params)
print(json.dumps(json_response, indent=4, sort_keys=True))

    