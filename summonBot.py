from praw import Reddit, helpers
from shlex import split
from re import sub as alph
import string


# Here we use PRAW to fetch a Reddit instance
redditHandle = Reddit(user_agent="User Summon Bot")
# Logging into reddit with a username and password
redditHandle.login('usersummonbot', 'summonbot123')

# Loading list of comments previously replied to
replied = []
repliedHndl = open("replList.txt", "r+")
for line in repliedHndl.readlines():
    replied.append(line.strip())

print replied


# Getting posts from a sub
commentSubs = redditHandle.get_subreddit('summonbottest').get_hot(limit=100)
# Iterate through each post
for post in commentSubs:
    # List of users to be summoned
    users = []
     
    # Flatten comments to make parsing easier
    for comment in helpers.flatten_tree(post.comments):
        # Check if comment has already been replied to 
        if (comment.id not in replied):
            # Check if user is summoned
            if "/u/" in comment.body:
                    # Process comment to generate user names
                    splitCom = split(comment.body.replace("'", "").replace('"', ""))
                    print splitCom
                    for item in splitCom:
                        if "/u/" in item:
                            if item[3:] not in users:
                                users.append(item[3:])
     
                    print users
                    # Iterate through mentioned users
                    for user in users:
                        # Try/except used to prevent exceptions shutting down bot
                        try: 
                            # Alphanumerify the parsed names (remove punctuation, etc.)
                            user = user.translate(string.maketrans("", ""), '"#$%&\'()*+,./:;<=>?@[\\]^`{|}~')
                            print user
                            # Message user
                            redditHandle.send_message(user, "You have been summoned by " + comment.author.name + ".", comment.author.name + " summoned you in the comment:\n \n" + comment.body + "\n \n Link: " + comment.permalink + "?context=3\n")
                            # Reply to comment with message
                            comment.reply(user + " has been summoned.")
                            # Add comment to list of replied
                            replied.append(comment.id)
                            print user + " has been summoned."
                        except:
                            pass

# Write list of replied comments to file  
repliedHndl.seek(0)                      
repliedHndl.write('\n'.join(replied))
repliedHndl.close()    
