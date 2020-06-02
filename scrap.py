import requests
import pandas as pd
import webbrowser
import os
import time
import pickle


def nextUrl(lastpage):
    if lastpage is None:
        return "http://www.reddit.com/hot.json"
    else:
        return 'http://www.reddit.com/hot.json?after=' + lastpage


def getData(url):
    scrap_url = nextUrl(url)
    print('Connecting to reddit... ' + scrap_url)
    res = requests.get(scrap_url, headers={'User-agent': 'YOUR NAME Bot 0.1'})
    data = res.json()
    LAST_CHECK_POINT = data['data']['after']
    return data, LAST_CHECK_POINT,


def saveData(data):
    if data is None:
        print("Unable to read response...")
    else:
        df = pd.DataFrame(columns=['title', 'subreddit', 'created', 'num_comments'])
        children = data['data']['children']
        for i in range(len(children)):
            title = children[i]['data']['title']
            subreddit = children[i]['data']['subreddit']
            created = children[i]['data']['created']
            num_comments = children[i]['data']['num_comments']
            dict = {'title': title, 'subreddit': subreddit, 'created': created, 'num_comments': num_comments}
            df.loc[i] = pd.Series(dict)

        pd.concat([pd.DataFrame(data), df], ignore_index=True)

        last_save_df = None
        try:
            last_save_df = pd.read_csv('data/reddit_data.csv')
        except:
            pass

        if last_save_df is not None:
            appended = last_save_df.append(df)
            appended.to_csv('data/reddit_data.csv', index=False)
        else:
            df.to_csv('data/reddit_data.csv', index=False)


def loadData(page=1, last_point=None):
    if (page > 1):
        for num in range(page):
            data, last_point = getData(last_point)
            saveData(data)
            print('Waiting for 3 seconds to proceed another request...')

            with open(LAST_CHECK_POINT_PATH, 'wb') as fp:
                if last_point is not None:
                    print('Checkpoint saved... ' + last_point)
                    pickle.dump(last_point, fp)

            time.sleep(3)  # sleeps 3 seconds before continuing
    else:
        data, last_point = getData(None)
        saveData(data)
    return last_point


''''''

LAST_CHECK_POINT_PATH = 'data/last_checkpoint.pck'
LAST_CHECK_POINT = None
try:
    with open(LAST_CHECK_POINT_PATH, 'rb') as fp:
        LAST_CHECK_POINT = pickle.load(fp)
except:
    LAST_CHECK_POINT = None
    pass


#

# Create a web page view of the data for easy viewing
print("Last checkpoint was "+ str(LAST_CHECK_POINT))

LAST_CHECK_POINT = loadData(30, LAST_CHECK_POINT)

finalDf = pd.read_csv('data/reddit_data.csv')
html = finalDf.to_html()

# Save the html to a temporary file
with open("data.html", "w") as f:
    f.write(html)

# Open the web page in our web browser
full_filename = os.path.abspath("data.html")
webbrowser.open("file://{}".format(full_filename))
