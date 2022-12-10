import json
import SentimentClassifierTraining
class User():
    def __init__(self, user_id, model):
        self.user_id = user_id
        self.neighbors = []
        self.model = model

        # Read tweet data that written by Utils class
        with open("data/" + str(self.user_id) + ".json", "r") as f:
            self.data = json.load(f)
            self.tweets = self.data["data"]

    # Get users that frequently appear in this user's tweets.
    def __get_mentions(self):
        self.mention_dict = {}
        for tweet in self.tweets:
            # Get the sentiment of this tweet
            isPositive = self.isPositive(tweet["text"])
            if ("entities" in tweet and isPositive):
                tweet_entities = tweet["entities"]
                if ("mentions" in tweet_entities):
                    tweet_mention = tweet_entities["mentions"]
                    for mention in tweet_mention:
                        to_add = self.mention_dict.get(mention["id"], 0)
                        self.mention_dict[mention["id"]] = to_add + 1
    
    # Select frequent users from mentions dictionary that exceed the threshold
    def get_neighbors(self, threshold=0.1):
        self.__get_mentions()
        sorted_items = sorted(self.mention_dict.items(), key=lambda x:x[1], reverse=True)

        for i in range(int(len(sorted_items) * threshold)):
            self.neighbors.append(sorted_items[i][0])

        return self.neighbors
    
    def save_neighbors(self):
        # If not fetch neighbors yet, then call get_neighbors
        if len(self.neighbors) == 0:
            self.get_neighbors()
        # Update data
        self.data["neighbors"] = self.neighbors
        # Write file
        with open("data/" + str(self.user_id) + ".json", "w") as f:
            json.dump(self.data, f)


    def isPositive(self, tweet):
        #TODO: Check
        # processed_tweet = 
        processed_tweet = SentimentClassifierTraining.process_single_tweet_content(tweet)
        result = self.model.predict(processed_tweet)
        return result[0] == 1



# print(user.tweets[0]['entities']['mentions'])