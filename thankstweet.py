# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.10.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import tweepy
import datetime
import random

account = "@account"
check_days = 7
n_people = 10

time_now = datetime.datetime.now()

consumer_key = 'consumer key'
consumer_secret = 'consumer secret'
access_token = 'access token'
access_token_secret = 'access token secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True)


# -

def tweet_check(account, check_days, time_now):
    
    tweets = tweepy.Cursor(api.user_timeline, id=account).items(100)

    rt_ids = []

    for tw in tweets:
        if time_now - (tw.created_at + datetime.timedelta(hours=9)) <= datetime.timedelta(days=check_days):
            if (tw.text.startswith('RT')) or (tw.text.startswith('@')):
                pass
            else:
                if tw.retweet_count >= 1:
                    rt_ids.append(tw.id)

    return rt_ids


def rtuser_check(rt_ids):
    
    rt_users = []

    for ids in rt_ids:
        retweets = api.retweets(id=ids)
        for rt in retweets:
            rt_users.append("@" + rt.user.screen_name)

    return rt_users


def rpuser_check(account, check_days, time_now):
    
    mentions = tweepy.Cursor(api.mentions_timeline, id=account).items(100)
    
    mn_users = []
    
    for mn in mentions:
        if time_now - (mn.created_at + datetime.timedelta(hours=9)) <= datetime.timedelta(days=check_days):
            mn_users.append("@" + mn.user.screen_name)
            
    return mn_users


def user_tweet(users, time_now, n_people):

    if len(users) != 0:
        if len(set(users)) <= n_people:
            tweet_content = '\n\n'.join(set(users))
        else:
            random_users = random.sample(set(users), n_people)
            tweet_content = '\n\n'.join(random_users)
        api.update_status("今週もみなさんのリプライとリツイート、ありがとうございます！\n\n" +  tweet_content + "\n\n" + time_now.strftime("%Y/%m/%d %H:%M:%S") + "\n\n#リプRT感謝砲") 
    elif len(users) == 0:
        api.update_status("今週は残念ながら、リプライもリツイートもありませんでした..." + "\n\n" + time_now.strftime("%Y/%m/%d %H:%M:%S") + "\n\n#リプRT感謝砲")


def main(account, check_days, time_now, n_people):
    rt_ids = tweet_check(account, check_days, time_now)
    rt_users = rtuser_check(rt_ids)
    mn_users = rpuser_check(account, check_days, time_now)
    
    users = rt_users + mn_users

    user_tweet(users, time_now, n_people)


if __name__ == '__main__':
    main(account, check_days, time_now, n_people)




