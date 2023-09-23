import configparser
import json
import time
from datetime import datetime
from pprint import pprint


from bs4 import BeautifulSoup
from selenium import webdriver


config = configparser.ConfigParser()
config.read("preferences.ini")

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--headless=new")
options.add_argument("--user-data-dir="+rf"{config['PREFERENCES']['UserDataDir']}")
options.add_argument(rf"--profile-directory={config['PREFERENCES']['ProfileName']}")
driver = webdriver.Chrome(options=options)


class Profile:
    __slots__ = ["driver", "verified", "data", "id", "username", "date_created", "given_name", "description", "location",
                 "tweets", "num_tweets", "followers", "following", "profile_image", "thumbnail_image", "links"]

    def __init__(self, username):
        self.username = username
        self.driver = driver
        self.tweets = []
        self.driver.get(f"https://twitter.com/{self.username}")
        time.sleep(5)
        self._load()
        self._parse()

    def _load(self) -> None:
        html = self.driver.page_source
        soup = BeautifulSoup(html, "lxml")

        try:
            tick = soup.find("svg", attrs={"class": "r-1cvl2hr r-4qtqp9 r-yyyyoo r-1xvli5t r-f9ja8p r-og9te1 r-bnwqim r-1plcrui r-lrvibr"})
            self.verified = 1 if tick else 0
            self.data = json.loads(soup.find("script", attrs={"data-testid": "UserProfileSchema-test"}).text)

            tweets = soup.findAll("a", attrs={"class": "css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"})
            self.driver.execute_script("window.scrollTo(0, 2160)")

            for tweet in tweets:
                link = fr"https://twitter.com{tweet.attrs['href']}"
                self.driver.get(link)
                time.sleep(5)

                html = self.driver.page_source
                soup = BeautifulSoup(html, "lxml")

                content = soup.find("div", attrs={"class": "css-901oao r-1nao33i r-37j5jr r-1inkyih r-16dba41 r-135wba7 r-bcqeeo r-bnwqim r-qvutc0"})
                tweet_text = content.text
                hashtags, mentions = [], []

                for i in content.findChildren("span", attrs={"class": "r-18u37iz"}):
                    tag = i.findChild("a").text
                    if tag[0] == "@":
                        mentions.append(tag)
                    elif tag[0] == "#":
                        hashtags.append(tag)

                for i in [*mentions, *hashtags]:
                    tweet_text = tweet_text.replace(i, "")

                stats = [i.findChild("span", attrs={"class": "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}) for i in soup.findAll("div", attrs={"class": "css-1dbjc4n r-xoduu5 r-1udh08x"})]

                for i, x in enumerate(stats):
                    try:
                        num = x.text.replace(",", "")

                        if "K" in num:
                            num = num.replace("K", "")
                            num = int(float(num) * 1_000)
                        elif "M" in num:
                            num = num.replace("M", "")
                            num = int(float(num) * 1_000_000)

                        stats[i] = int(num)
                    except AttributeError:
                        stats[i] = 0

                self.tweets.append({"text": tweet_text, "hashtags": hashtags, "mentions": mentions, "views": stats[0],
                                    "comments": stats[1], "retweets": stats[2], "likes": stats[3], "bookmarks": stats[4]})
        except AttributeError:
            print("Rate limited by Twitter")

    def _parse(self) -> None:
        self.date_created = datetime.strptime(self.data["dateCreated"], "%Y-%m-%dT%H:%M:%S.%fZ") or None
        self.id = self.data["author"]["identifier"]
        self.given_name = self.data["author"]["givenName"] or None
        self.description = self.data["author"]["description"] or None
        self.location = self.data["author"]["homeLocation"]["name"] or None
        self.followers = self.data["author"]["interactionStatistic"][0]["userInteractionCount"] or None
        self.following = self.data["author"]["interactionStatistic"][1]["userInteractionCount"] or None
        self.num_tweets = self.data["author"]["interactionStatistic"][2]["userInteractionCount"] or 0
        self.profile_image = self.data["author"]["image"]["contentUrl"] or None
        self.thumbnail_image = self.data["author"]["image"]["thumbnailUrl"] or None

    def __repr__(self) -> str:
        return f"<Profile username=_{self.username}_ date_created=_{self.date_created}_>"

    def to_dict(self) -> dict:
        return dict(
            verified=self.verified,
            id=self.id,
            username=self.username,
            date_created=self.date_created,
            given_name=self.given_name,
            description=self.description,
            location=self.location,
            tweets=self.tweets,
            num_tweets=self.num_tweets,
            followers=self.followers,
            following=self.following,
            profile_image=self.profile_image,
            thumbnail_image=self.thumbnail_image
        )


# snu = Profile("shivnadaruniv")
# print(snu.to_dict())
# time.sleep(5)
# dtele = Profile("dtele7")
# pprint(dtele.to_dict())
# time.sleep(5)
# bill = Profile("dtele7")
# pprint(bill.to_dict())
