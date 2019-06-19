from twitter import Twitter, OAuth
import time
import datetime as dt


def upload(file, description):
    print("Entered Twitter.")
    api_key = 'rGOeSdg0myCTnIW4TX7pZv9Wo'
    app_secret = 'TIi91jacTbdbTP9nBWb0kQBEUJIQp9tIMNUiCcxptrGxIwQoYk'
    access_token = '39085479-GVWUkFdCdnFv1z4sgrq6DcuRQWIg1lgFtOmaexYsF'
    access_token_secret = 'WXsvkhm78eOfpzDPZBKkBFfU1Z0I1Ulm4O3mZaQ2ku5On'

    my_auth = OAuth(token=access_token,
                    token_secret=access_token_secret,
                    consumer_key=api_key,
                    consumer_secret=app_secret)

    t = Twitter(auth=my_auth)

    with open(file, "rb") as image:
        image_data = image.read()
    upload_link = Twitter(domain='upload.twitter.com', auth=my_auth)
    image_id = upload_link.media.upload(media=image_data)["media_id_string"]
    print(str(dt.datetime.now()) + " Uploading to Twitter ...")
    t.statuses.update(status=description, media_ids=",".join([image_id]))
    print(str(dt.datetime.now()) + " Uploaded to Twitter.")
    time.sleep(60)
