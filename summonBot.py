from praw import Reddit, helpers
from shlex import split

redditHandle = Reddit(user_agent = "User Summon Bot")

redditHandle.login('usersummonbot', 'summonbot123')

testSubs = redditHandle.get_subreddit('summonbottest').get_hot(limit=100)

for post in testSubs:
    for comment in helpers.flatten_tree(post.comments):
        if "/u/" in str(comment):
            print "User paged."
            users = []
            splitCom = split(str(comment))
            for item in splitCom:
                if "/u/" in item:
                    users.append(item[3:])
            for user in users:
                comment.reply("User " + user + " paged.")
                print comment.id
                redditHandle.send_message(user, "You have been paged.", "test.")
				

