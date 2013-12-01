from praw import Reddit, helpers
from shlex import split
from re import sub as alph


# Here we use PRAW to fetch a Reddit instance
redditHandle = Reddit(user_agent="")
# Logging into reddit with a username and password
redditHandle.login('username', 'password')

# Getting posts from a sub
commentSubs = redditHandle.get_subreddit('subreddit').get_hot(limit=100)

# Loading list of comments previously replied to
replied = []
repliedHndl = open("comments.txt", "r+")
for line in repliedHndl.readlines():
    replied.append(line.strip())
repliedHndl.close()


# Iterate through each post
for post in commentSubs:
    # List of users to be summoned
    users = []
    
    # Flatten comments to make parsing easier
    for comment in helpers.flatten_tree(post.comments):
        # Check if comment has already been replied to 
        if (comment.id not in replied):
            # Check if user is summoned
            if "/u/" in str(comment):
                    # Process comment to generate user names
                    splitCom = split(str(comment))
                    for item in splitCom:
                        if "/u/" in item:
                            if item[3:] not in users:
                                users.append(item[3:])
    
                    # Iterate through mentioned users
                    for user in users:
                        # Try/except used to prevent exceptions shutting down bot
                        try: 
                            # Alphanumerify the parsed names (remove punctuation, etc.)
                            user = alph('[^0-9a-zA-Z+_. ]+', '-', user)
                            # Reply to comment with message
                            comment.reply(user + " has been summoned.")
                            # Message user
                            redditHandle.send_message(user, "You have been summoned by " + comment.author.name + ".", comment.author.name + " summoned you in the comment:\n \n" + comment.body + "\n \n Link: " + comment.permalink + "?context=3\n")
                            # Add comment to list of replied
                            replied.append(comment.id)
                        except:
                            pass

# Write list of replied comments to file                        
repliedHndl = open("replList.txt", "r+")
repliedHndl.write('\n'.join(replied))
repliedHndl.close()	








