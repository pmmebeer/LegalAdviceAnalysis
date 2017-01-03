import config
import praw
from collections import defaultdict
from textblob import TextBlob
from stopwords import stopwordlist

# Initializing reddit instance
reddit = praw.Reddit(
    user_agent = config.user_agent,
    client_id = config.client_id,
    client_secret = config.client_secret,
    )

# Creating list of "warning" subreddits, where users active there may be questionable
warning_subreddits = ['raisedbynarcissists',
                      'relationships',
                      'freeuse',
                      'trees',
                      'drugs',
                      'darknetmarkets',
                      'relationships',
                      'rbnlegaladvice',
                      'theredpill',
                      'legaladviceinaction',
                      'imgoingtohellforthis',
                      'drama',
                      'shitredditsays',
                      'bad_cop_no_donut',
                      'mensrights',
                      'kotakuinaction',
                      'incels',
                      'redpillwomen',
                      'mgtow',
                      'justnomil']
warning_sub_dict_comments = defaultdict(int)
warning_sub_dict_posts = defaultdict(int)

#Creating list of political subreddits
political_subreddits = ['enoughtrumpspam',
                        'the_donald',
                        'libertarian',
                        'politics',
                        'hillaryclinton',
                        'libertarian',
                        'sandersforpresident',
                        'political_revolution']
political_sub_dict_comments = defaultdict(int)
political_sub_dict_posts = defaultdict(int)

def comment_check(): # Checking comments in user's history to see if they're active on our watched subs

    for comment in reddit.redditor(lookup_user).comments.new(limit=900): # Do not exceed 1,000
        if comment.subreddit in warning_subreddits:
            warning_sub_dict_comments[str(comment.subreddit)] += 1 # Increment dict[subreddit] by 1 for each comment
        elif comment.subreddit in political_subreddits:
            political_sub_dict_comments[str(comment.subreddit)] += 1 # Increment dict[subreddit] by 1 for each comment


def submission_check(): # Checking posts in user's history to see if they're active on our watched subs

    for submission in reddit.redditor(lookup_user).submissions.new(limit=100):
        if submission.subreddit in warning_subreddits:
            warning_sub_dict_posts[str(submission.subreddit)] += 1 # Increment dict[subreddit] by 1 for each post
        elif submission.subreddit in political_subreddits:
            political_sub_dict_posts[str(submission.subreddit)] += 1 # Increment dict[subreddit] by 1 for each post

subreddit = reddit.subreddit('legaladvice') # Can be modified to be any subreddit

subreddit_tokens = defaultdict(list) # Creating list to accept dictionary of tokenized posts

print("Analyzing Submissions...")

for submission in subreddit.hot(limit = 100): # Pulling first 100 submissions from subreddit/hot
    lookup_user = str(submission.author) # Setting user for loop equal to submission author

    comment_check()
    submission_check()

    for subreddit in warning_sub_dict_comments:
        submission_blob = TextBlob(str(submission.selftext).lower()) # converting post body to textblob
        for word in submission_blob.words: # Adding word to our token dict if it's not in our stop list
            if word not in stopwordlist:
                subreddit_tokens[subreddit].append(word)

    for subreddit in warning_sub_dict_posts:
        submission_blob = TextBlob(str(submission.selftext).lower()) # converting post body to textblob
        for word in submission_blob.words: # Adding word to our token dict if it's not in our stop list
            if word not in stopwordlist:
                subreddit_tokens[subreddit].append(word)
# Clearing out our dictionary before restarting the loop
    warning_sub_dict_comments.clear()
    warning_sub_dict_posts.clear()
    political_sub_dict_posts.clear()
    political_sub_dict_comments.clear()
# Printing list of tokens (words) by subreddit that OP on our chosen subreddit participated in
for k,v in subreddit_tokens.items():
    print(k,v)


