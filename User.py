import json
class User():
    def __init__(self, user_id):
        self.user_id = user_id
        self.neighbors = []

        # Read tweet data that written by Utils class
        with open("test.json", "r") as f:
            self.data = json.load(f)
            self.tweets = self.data["data"]

    # Get users that frequently appear in this user's tweets.
    def __get_mentions(self):
        self.mention_dict = {}
        for tweet in self.tweets:
            if ("entities" in tweet):
                tweet_entities = tweet["entities"]
                if ("mentions" in tweet_entities):
                    tweet_mention = tweet_entities["mentions"]
                    for mention in tweet_mention:
                        to_add = self.mention_dict.get(mention["id"], 0)
                        self.mention_dict[mention["id"]] = to_add + 1
    
    # Select frequent users from mentions dictionary that exceed the threshold
    def get_neighbors(self, threshold=0.05):
        self.__get_mentions()
        sorted_items = sorted(self.mention_dict.items(), key=lambda x:x[1], reverse=True)

        for i in range(int(len(sorted_items) * threshold) + 1):
            self.neighbors.append(sorted_items[i][0])

        return self.neighbors
    
    def save_neighbors(self):
        # If not fetch neighbors yet, then call get_neighbors
        if len(self.neighbors) == 0:
            self.get_neighbors()
        # Update data
        self.data["neighbors"] = self.neighbors
        # Write file
        with open("test.json", "w") as f:
            json.dump(self.data, f)



user = User(1234)
user.save_neighbors()


# print(user.tweets[0]['entities']['mentions'])