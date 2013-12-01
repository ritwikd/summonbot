from praw import Reddit, helpers
from shlex import split
from re import sub as alph
import string
from os import listdir as crdir

def main():
    # Here we use PRAW to fetch a Reddit instance
    redditHandle = Reddit(user_agent="User Summon Bot")
    # Logging into reddit with a username and password
    redditHandle.login('usersummonbot', 'summonbot123')
    
        # Loading list of comments previously replied to
    
    visited = []
    if 'replList.txt' not in crdir('.'):
        path = "~/workspace/summonBot/replList.txt"
    else:
        path = "replList.txt"
    repliedHndl = open(path, "r+")
    for line in repliedHndl.readlines():
        visited.append(line.strip())
    
    # Getting posts from a sub
    allComments = redditHandle.get_subreddit('all').get_comments(limit=None)
    
    # Flatten comments to make parsing easier
    for comment in allComments:
        users = []
        # Check if comment has already been visited 
        if (comment.id not in visited):
            print comment.body
            # Add comment to list of replied
            visited.append(comment.id)
            # Check if user is summoned
            if "/u/" in comment.body:
                    #Split comment into 'words' to parse for user names
                    splitCom = split(comment.body.replace("'", "").replace('"', ""))
                    #Loop through words
                    for word in splitCom:
                        #Check if word has a leading user prefix
                        if "/u/" in word:
                            #Check if user has already been included in this post (i.e., Betelgeuse style summoning)
                            if word[3:] not in users:
                                #Add user to list
                                users.append(word[3:])
      
                    # Iterate through mentioned users
                    for user in users:
                        # Try/except used to prevent exceptions shutting down bot
                        try: 
                            # Alphanumerify the parsed names (remove punctuation, etc.)
                            user = user.translate(string.maketrans("", ""), '"#$%&\'()*+,./:;<=>?@[\\]^`{|}~')
                            # Message user
                            redditHandle.send_message(user, "You have been summoned by " + comment.author.name + ".", comment.author.name + " summoned you in the comment:\n \n" + comment.body + "\n \n Link: " + comment.permalink + "?context=3\n")
                            # Reply to comment with message
                            comment.reply(user + " has been summoned.")
                        except:
                            pass
    # Write list of replied comments to file  
    repliedHndl.seek(0)                      
    repliedHndl.write('\n'.join(visited))
    repliedHndl.close()  

if __name__ == '__main__':
    main()
