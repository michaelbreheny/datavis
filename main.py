import tweepy
from flask import Flask, render_template, request, json
from tweet_analyzer import create_my_df
from twitter_auth import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# Authentication stuff
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

app = Flask(__name__)
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def stream_tweets(search_term):
    data = []
    counter = 0
    for tweet in tweepy.Cursor(api.search, q='\"{}\" -filter:retweets'.format(search_term), count=100, lang='en',
                               tweet_mode='extended').items():
        tweet_details = {'tweet': tweet.full_text,
                         'location': tweet.user.location,
                         'retweets': tweet.retweet_count,
                         'favorites': tweet.favorite_count,
                         'followers': tweet.user.followers_count
                         }
        data.append(tweet_details)

        counter += 1
        if counter == 500:
            break
        else:
            pass
    with open('data/results.json'.format(search_term), 'w') as f:
        json.dump(data, f)


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    search_term = request.form['query']
    stream_tweets(search_term)

    print('Searching twitter for opinions about "' + search_term + '" ....')
    print('done!')
    return_json()
    return render_template("results.html")


@app.route('/results', methods=['GET', 'POST'])
def return_json():
    items = create_my_df()

    return items


if __name__ == "__main__":
    app.run()
