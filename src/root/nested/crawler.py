'''
Created on 1 Jul 2016

@author: Sarah
'''


from lxml import html
import requests
import email
import smtplib

def send(msg):
    TO = 'oneofthebarbers@gmail.com'
    SUBJECT = 'Place a bet'
    TEXT = msg
    
    # Gmail Sign In
    gmail_sender = 'sarahbarberuk@gmail.com'
    gmail_passwd = 'H05t!leSch!zm'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
    
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])
    
    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')
    
    server.quit()
    print("finished")
    return

# Crawling BetFair

betfairPage = requests.get('https://www.betfair.com/exchange/football')
betfairDOM = html.fromstring(betfairPage.content)

betfairLayBets = betfairDOM.xpath("//div[contains(@class, 'event-meta')]/ul/li/ul/li[contains(@class, 'back')]/button/span/text()");
betfairLayBets = [bet.strip() for bet in betfairLayBets]

# the below elements are only for matches that have not yet begun
betfairHomeTeams = betfairDOM.xpath("//li[span[contains(@class, 'willgoinplay')]]/div[contains(@class, 'container-market')]/a/div/div[contains(@class, 'market-info')]/span/span[contains(@class, 'home-team')]/text()");
betfairAwayTeams = betfairDOM.xpath("//li[span[contains(@class, 'willgoinplay')]]/div[contains(@class, 'container-market')]/a/div/div[contains(@class, 'market-info')]/span/span[contains(@class, 'away-team')]/text()");
betfairHomeVsAway = [''] * len(betfairHomeTeams)

for i in range (0, len(betfairHomeTeams)) :
    betfairHomeVsAway[i] = betfairHomeTeams[i] + " v " + betfairAwayTeams[i]

# Crawling Coral

coralPage = requests.get('http://sports.coral.co.uk/football')
coralDOM = html.fromstring(coralPage.content)

coralLayBets = coralDOM.xpath("//div[contains(@class, 'football-matches')]/div/div/div/div/div/div/span[contains(@class, 'odds-decimal')]")
coralLayBets = [bet.strip() for bet in coralLayBets]


coralHomeAndAwayTeams = coralDOM.xpath("//div[contains(@class, 'football-matches')]/div/div/div/div/div[contains(@class, 'bet-title')]/a/span/text()");

# First, just see if there's a good way with Betfair

betfairWinOdds = betfairDOM.xpath("//div[contains(@class, 'event-meta')]/ul/li/ul/li[contains(@class, 'back selection-0')]/button/span/text()");
betfairWinOdds = [odds.strip() for odds in betfairWinOdds]
#Do I have lose and draw the right way round?
betfairLoseOdds = betfairDOM.xpath("//div[contains(@class, 'event-meta')]/ul/li/ul/li[contains(@class, 'back selection-2')]/button/span/text()");
betfairLoseOdds = [odds.strip() for odds in betfairLoseOdds]
betfairDrawOdds = betfairDOM.xpath("//div[contains(@class, 'event-meta')]/ul/li/ul/li[contains(@class, 'back selection-1')]/button/span/text()");
betfairDrawOdds = [odds.strip() for odds in betfairDrawOdds]

for i in range (0, len(betfairWinOdds)):
    if (betfairWinOdds[i] == '') or (betfairLoseOdds[i] == '') or(betfairDrawOdds[i] == '') :
        continue
    total = ((1/float(betfairWinOdds[i])) + (1/float(betfairLoseOdds[i])) + (1/float(betfairDrawOdds[i])))
    if total < 1 :
        match = betfairHomeTeams[i] + " v " + betfairAwayTeams[i]
        msg = "Place a bet for " + betfairHomeVsAway[i] + ". Odds are: Win:" + betfairWinOdds[i] + " Lose:" + betfairLoseOdds[i] + ", Draw:" + betfairDrawOdds[i] + "."
        send(msg)

print("finished")

 

