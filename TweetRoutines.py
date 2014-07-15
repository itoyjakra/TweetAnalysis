import sys
import json

states = {
        'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado',
        'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii',
        'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts',
        'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi',
        'MT': 'Montana', 'NA': 'National', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico',
        'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands',
        'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'
}

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
