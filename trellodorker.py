#A tool that dorks Trello automatically

import json
import requests
import argparse
from googlesearch import search

parser = argparse.ArgumentParser()
headers = {"Accept": "application/json"}
query = {}

#Sets key and token
credentials = open("creds.txt", "r")
query.__setitem__("key:", credentials.readline())
query.__setitem__("token", credentials.readline())
credentials.close()

parser.add_argument('-i', type=str, required=True, help="Dorking query - a domain or something like that")
parser.add_argument('-o', type=str, required=True, help="Output text file")
parser.add_argument('-a', type=str, help="Additional text you want to dork for, separated by commas.")

args = parser.parse_args()

def googleSearch(query):
    urls = []
    dork = "site:trello.com AND intext:" + query

    if args.a:

        queries = args.a.split(",")

        for i in queries:
            dorkAddition = " AND intext:" + i
            dork += dorkAddition

        for i in search(dork, tld="com", num=10, stop=10, pause=2):
            urls.append(i)

    else:
        for i in search(dork, tld="com", num=10, stop=10, pause=2):
            urls.append(i)

    return urls

def fetchBoardIDs(list_of_urls):
    cards = []
    boards = []

    for url in list_of_urls:
        x = url[19:].split("/")
        category = x[0]
        trello_id = x[1]  

        if category == "c":
            cards.append(trello_id)

        elif category == "b":
            boards.append(trello_id)

    return boards, cards

def getBoardMembers(board_id):
    if board_id is not None:
        users = []
        board_url = "https://api.trello.com/1/boards/" + board_id + '/members'
        board_response = requests.request("GET", board_url, headers=headers, params=query)
        try:
            data = json.loads(board_response.text)

            for user in data:
                users.append(user["id"])
            
            return users

        except:
            pass

    else:
        print("An error occurred.")

def getBoardFromCard(card_id):  
    card_url = "https://api.trello.com/1/cards/" + card_id + '/board'
    card_response = requests.request("GET", card_url, headers=headers, params=query)
    if card_response.text is not None:
        try:
            data = json.loads(card_response.text)
            if data:
                return data["id"]
        except:
            pass

def GetMemberBoards(member_id):
    memberBoards = []
    member_url = "https://api.trello.com/1/members/" + member_id + '/boards'
    member_response = requests.request("GET", member_url, headers=headers, params=query)
    data = json.loads(member_response.text)
    for i in data:
        memberBoards.append(i["name"] + " : " + i["url"])
    return memberBoards

def trelloSearch(ids, outputFile):

    userList = []
    collectedURLs = []

    boards = ids[0]
    cards = ids[1]

    for board_id in boards:
        getBoardMembers(board_id)

    for card_id in cards:
        users = getBoardMembers(getBoardFromCard(card_id))
        if users is not None:
            userList += users

    userList = list(set(userList)) 

    for user in userList:
        collectedURLs += GetMemberBoards(user) 
        percentage = round(((userList.index(user) + 1) / len(userList)) * 100, 2)
        print("Progress:", str(percentage) +  "%")


    collectedURLs = list(set(collectedURLs))

    for address in collectedURLs:
        outputFile.write(address + "\n")

def runTool(company, txt):
    print("Search started.")
    searchURLs = googleSearch(company)
    trello_ids = fetchBoardIDs(searchURLs)
    trelloSearch(trello_ids, txt)
    print("Finished.")
    
output = open(args.o, 'w')

runTool(args.i, output)

output.close()
