import sys
import json
from USstates import states 

def getStateAbbr(stateName):
    '''
    returns the state abbreviation corresponding to a state name
    '''
    for key, value in states.iteritems():
        if value == stateName:
            return key

def getTweetScore(tweetText, sents):
    '''
    returns the sentiment score of a tweet text
    requires a dictionary of tagged words for scoring
    '''
    totalSent = 0
    for word in tweetText.split():
        if word in sents.keys():
            totalSent += sents[word]
    return totalSent

def initializeScores(states):
    '''
    initialize the state happiness score
    '''
    score = {}
    for key in states.keys():
        score[key] = 0
    return score

def getStateFromTweet(tweet):
    '''
    get the US stsate abbreviation from tweets
    '''
    stateAbbr = ''
    # check for the text field and get rid of special characters
    if ( len(tweet['text']) == len(tweet['text'].encode('utf-8')) ):
        if ( ( tweet['place'] != None ) and ( 'full_name' in tweet['place'].keys() ) ):
            wordPlace = tweet['place']['full_name'].split(',')
            # the state abbreviations are preceeded by a space
            if ( ' USA' in wordPlace[-1] ):
                stateAbbr = getStateAbbr(wordPlace[0])
            elif ( wordPlace[-1][1:] in states.keys() ) or ( wordPlace[-1][1:] in states.values() ):
                if ( len(wordPlace[0]) == len(wordPlace[0].encode('utf-8')) ):
                    stateAbbr = wordPlace[-1][1:]
    return stateAbbr


def getStateScore(fileName, sents):
    '''
    find the state happiness score from a bunch of tweets
    '''
    ftweet = open(fileName, "r")
    stateScore = initializeScores(states)
    for line in ftweet:
        tweet = json.loads(line)
        if 'text' in tweet.keys():
            stateAbbr = getStateFromTweet(tweet)

            if not stateAbbr == '':
                stateScore[stateAbbr] += getTweetScore(tweet['text'], sents)

    ftweet.close()

    return stateScore

def getTopTags(d, n):
    '''
    return the top n most frequent words in a dictionary
    '''
    sword = [ w for w in sorted(d, key=d.get, reverse=True)[:n] ]
    sfreq = [ d[w] for w in sorted(d, key=d.get, reverse=True)[:n] ]
    return zip(sword, sfreq)

def createHashtagDict(fileName):
    '''
    create a dictionary of tweet hashtags from a collection of tweets
    '''
    ftweet = open(fileName, "r")
    hashTagFreq = {}
    for line in ftweet:
        x = json.loads(line)
        if 'entities' in x.keys():
            tag = x['entities']['hashtags']
            if len(tag) > 0:
                text = tag[0]['text']
                if text in hashTagFreq.keys():
                    hashTagFreq[text] += 1
                else:
                    hashTagFreq[text] = 1
        
    return hashTagFreq

def getWordFreq(fileName):
    '''
    get frequency of words from a file of tweets
    '''
    ftweet = open(fileName, "r")
    wFreq = {}
    for line in ftweet:
        x = json.loads(line)
        if 'text' in x.keys():
            text = x['text'].strip()
            for word in text.split():
                word = word.strip()
                if word in wFreq.keys():
                    wFreq[word] += 1
                else:
                    wFreq[word] = 1
    ftweet.close()
        
    return wFreq

def storeSentiment(fileName):
    '''
    store the list of words and their corresponding scores in a dictionary
    '''
    sentiment = {}
    fsent = open(fileName, "r")
    for line in fsent:
        word, score = line.split('\t')
        sentiment[word] = int(score)
    fsent.close()
    return sentiment

def findBestState(scoreDict):
    v=list(scoreDict.values())
    k=list(scoreDict.keys())
    return k[v.index(max(v))]

def main():

    sents = storeSentiment(sys.argv[1])
    scores = getStateScore(sys.argv[2], sents)
    for key, value in scores.items():
        print key, value
    print findBestState(scores)

if __name__ == '__main__':
    main()
