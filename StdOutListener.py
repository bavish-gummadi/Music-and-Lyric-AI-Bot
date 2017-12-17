import tweepy
consumer_key = 'dkXRLqG8EgYC9GOmsR8kTqXV4'
consumer_secret = 'sjyfYIQxuSn6qAbzo5iLEaFLWPVHLiJOak73nx61JZZhumfrpE'  
access_token = '938527466771177472-DeNwYIQJXnHxUF66aluqA9ZiCwMD0jc'
access_token_secret = 'wmgWdLB56LPU00RwFpGuUzfwImX9Rgj05HxsZ6UtqM5xI'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class StdOutListener(tweepy.StreamListener):
    #Handles data from the stream

    def on_status(self, status):
        print('Tweet text: ' + status.text)
        api.update_status('Hello to you as well!')


    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True

if __name__ == '__main__':
    listener = StdOutListener()
    
    stream = tweepy.Stream(auth, listener)
    stream.filter(follow=['938527466771177472'], track=['Atharva'])
