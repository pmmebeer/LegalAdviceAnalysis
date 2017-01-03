import config
import praw
from collections import defaultdict
from textblob import TextBlob
from stopwords import stopwordlist


reddit = praw.Reddit(
    user_agent = config.user_agent,
    client_id = config.client_id,
    client_secret = config.client_secret,
    )

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

def comment_check():

    for comment in reddit.redditor(lookup_user).comments.new(limit=900):
        if comment.subreddit in warning_subreddits:
            warning_sub_dict_comments[str(comment.subreddit)] += 1
        elif comment.subreddit in political_subreddits:
            political_sub_dict_comments[str(comment.subreddit)] += 1


def submission_check():

    for submission in reddit.redditor(lookup_user).submissions.new(limit=100):
        if submission.subreddit in warning_subreddits:
            warning_sub_dict_posts[str(submission.subreddit)] += 1
        elif submission.subreddit in political_subreddits:
            political_sub_dict_posts[str(submission.subreddit)] += 1

subreddit = reddit.subreddit('legaladvice') # Can be modified to be any subreddit

subreddit_tokens = defaultdict(list)

print("Analyzing Submissions...")

for submission in subreddit.hot(limit = 100):
    lookup_user = str(submission.author)

    comment_check()
    submission_check()

    for subreddit in warning_sub_dict_comments:
        submission_blob = TextBlob(str(submission.selftext).lower())
        for word in submission_blob.words:
            if word not in stopwordlist:
                subreddit_tokens[subreddit].append(word)

    for subreddit in warning_sub_dict_posts:
        submission_blob = TextBlob(str(submission.selftext).lower())
        for word in submission_blob.words:
            if word not in stopwordlist:
                subreddit_tokens[subreddit].append(word)

    warning_sub_dict_comments.clear()
    warning_sub_dict_posts.clear()
    political_sub_dict_posts.clear()
    political_sub_dict_comments.clear()

for k,v in subreddit_tokens.items():
    print(k,v)


