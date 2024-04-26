from .DBcommands import *
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import datetime, timedelta
import nltk 
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt


def CleaningHTML(Url,headline): #cleans the body removing all html ellements and removing as much infomation that is not relvent from the data as is possible with my skill level
    response = requests.get(Url)
    Html=response.text
    tree = BeautifulSoup(Html)
    removedhtml=tree.get_text()
    Fillter=removedhtml.split(headline)
    if len(Fillter)<2:
        return False
    
    HighText=0
    Loc=0
    for i in range(0,len(Fillter)):
        if len(Fillter[i])>HighText:
            HighText=len(Fillter[i])
            Loc=i
    seccondFillter=Fillter[Loc].split('\n')
    currentTextboxLength=0
    largeTextBoxEnd=0
    LargeTextBoxLength=0
    EmptyStringsLength=0
    ThirdFilter=""
    for i in seccondFillter:
        data=i
        if i=="":
            data="FfFf"
        ThirdFilter=ThirdFilter+data
        
    
    check='FfFfFfFfFfFf'
    Largestpag=0
    PagLoc=0
    ForthFilter=ThirdFilter.split(check)
    for i in range(0,len(ForthFilter)):
       if len(ForthFilter[i])>Largestpag:
           Largestpag=len(ForthFilter[i])
           PagLoc=i
    text=""
    for i in ForthFilter[PagLoc]:
        text=text+i
    #txt.replace("bananas", "apples")
    text=text.replace('FfFf','\n')
    #print(text)
    return text

def Sentimentclean(text): #determines the sentiment of any given source taking its postive negative and overall as a return
    sia = SentimentIntensityAnalyzer()
    SentimentData=sia.polarity_scores(text)
    Total=SentimentData['pos']-SentimentData['neg'] 
    neg=SentimentData['neg']*-1
    Return=[SentimentData['pos'],neg,Total]
    return Return

def one_month_before(): #determines the date one month before, must be used on the 28th of the month or before to avoid edge cases
    current_datetime = datetime.now()
    current_month = current_datetime.month
    current_day = current_datetime.day
    current_year = current_datetime.year

    if current_month==1:
        current_year=current_year-1
        current_month=12

    else:
        current_month=current_month-1
    if current_month<10:
        current_month="0"+str(current_month)
    if current_day<10:
        current_day="0"+str(current_day)
    current_month=str(current_month)
    current_day=str(current_day)
    current_year=str(current_year)
    returndate=current_year+"-"+current_month+"-"+current_day
    return returndate



"""
Example use case of bellow function
graph1={
    "Xlabel":'Label',
    "Title":"Graph1",
    "Ylabel":"Label",
    "plots":{
        "Xplots":[[0,1,2,3,4,5],[1,2,3,4,5,6]],
        "YPlots":[[0,1,2,3,4,5],[2,3,4,5,6,7]],
        "Label":['label1','label2'],
        "colours":['red','blue']
    }
}
graph2={
    "Xlabel":'Label2',
    "Ylabel":"Label2",
    "Title":"Graph2",
    "plots":{
        "Xplots":[[0,1,2,3,4,5],[1,2,3,4,5,6]],
        "YPlots":[[0,1,2,3,4,5],[1,2,3,4,5,6]],
        "Label":['label1','label2'],
        "colours":['red','blue']
    }
}
"""
def PlotGraphs(graph1,graph2): #takes two grphs and creates png files of the plots that those two would create
    for i in range(0,len(graph1['plots']['Xplots'])):
        plt.plot(graph1['plots']['Xplots'][i], graph1['plots']['YPlots'][i], label=graph1['plots']['Label'][i], color=graph1['plots']["colours"][i])
    
    plt.title(graph1["Title"])
    plt.xlabel(graph1["Xlabel"])
    plt.ylabel(graph1["Ylabel"])
    plt.legend()
    plt.grid(True)
    plt.savefig('plot1_image.png')
    plt.clf()
    for i in range(0,len(graph2['plots']['Xplots'])):
        plt.plot(graph2['plots']['Xplots'][i], graph2['plots']['YPlots'][i], label=graph2['plots']['Label'][i], color=graph2['plots']["colours"][i])
    plt.title(graph2["Title"])
    plt.xlabel(graph2["Xlabel"])
    plt.ylabel(graph2["Ylabel"])
    plt.legend()
    plt.grid(True)
    plt.savefig('plot2_image.png')
    plt.clf()

#https://api.twelvedata.com/time_series?symbol=AAPL&interval=15min&start_date=2020-01-01&end_date=2023-01-01&apikey=5eb91eed0cb149eaa54cb7acc41210ee&source=docs

def GrabNews(SearchTerm,APIKEY,company):
    datebefore=one_month_before()
    APIsearch="https://newsapi.org/v2/everything?q={}&from={}&sortBy=relevancy&apiKey={}&language=en".format(SearchTerm,datebefore,APIKEY)
    res=requests.get(APIsearch)
    open_page=res.json()
    article=open_page['articles']
    values=[]
    for i in article:
        if i['url']!="https://removed.com":
            tem=[]
            tem.append(i["title"])
            tem.append(i["url"])
            data=i["publishedAt"]
            data=data.split("T")
            data2=data[0].split("-")
            List=[]
            List.append(int(data2[0]))
            List.append(int(data2[1]))
            List.append(int(data2[2]))
            data3=data[1].split(":")
            List.append(int(data3[0]))
            List.append(int(data3[1]))
            tem.append(List)
            tem.append(company)
            values.append(tem)
    return values

def UriAddToDB(values,company):
   # values=[["Goodbye Apple Car, Hello Apple Home Robots","https://gizmodo.com/goodbye-apple-car-hello-apple-home-robots-1851386201",[2024,4,4,12,30]]]
    query="SELECT * FROM Urls WHERE company = '{}'".format(company)
    rows = query_db(query)
    URlsindb=[]
    Qrys=[]
    for i in rows:
        URlsindb.append(i['storyUrl'])
    for i in values:
        if i[1] in URlsindb:
            useless=0
        else:
            Headline=i[0]
            Headline=Headline.replace("'","FfFf")
            Headline=Headline.replace('"',"fFfF")
            #print(Headline)
            Qry = f"INSERT INTO Urls (storyUrl, company, headline,storyYear,storyMonth,storyDay,storyHour,storyminute) VALUES ('{i[1]}','{company}', '{Headline}', {i[2][0]},{i[2][1]},{i[2][2]},{i[2][3]},{i[2][4]})"
            Qrys.append(Qry)
            CalQry = write_db(Qry)
    return Qrys

def grabAllStocks():
    values=[["Goodbye Apple Car, Hello Apple Home Robots","https://gizmodo.com/goodbye-apple-car-hello-apple-home-robots-1851386201",[2024,4,4,12,30]]]
    query="SELECT * FROM Companies"
    rows = query_db(query)
    return rows 
def CleanBodyandSentimenttoDb():
    Urls=[]
    query="select * from Urls"
    rows = query_db(query)
    for i in rows:
        Urls.append(i['storyUrl'])
    query2="SELECT * FROM CleanedStories"
    rows2 = query_db(query2)
    URlsindb=[]
    Qrys=[]
    for i in rows2:
        URlsindb.append(i['storyUrl'])
    for i in Urls:
        if i in URlsindb:
            useless=0
        else:
            Qry="SELECT * FROM Urls Where storyUrl='{}'".format(i)
            Result=query_db(Qry,one=True)
            Headline=Result["headline"]
            Headline=Headline.replace("FfFf","'")
            Headline=Headline.replace('fFfF','"')
            cleanedbody=CleaningHTML(i,Headline)
            if cleanedbody !=False:
                SentimetScore=Sentimentclean(cleanedbody)
                cleanedbody=cleanedbody.replace("'","FfFf")
                cleanedbody=cleanedbody.replace('"',"fFfF")
                Qrys.append(SentimetScore)
    return Qrys
@app.route("/")
def index():
    """
    Main Page.
    """
    return CleanBodyandSentimenttoDb()
    #values=GrabNews("Apple",'54de7376d5474ca0a6e7ec9ecd81ca26','Apple')
    #return UriAddToDB(values,"Apple")

    #return grabAllStocks()
    #return GrabNews("Apple",'54de7376d5474ca0a6e7ec9ecd81ca26','Apple')
    #return Sentimentclean('testing the basic premise of this function to see if it works the way i think it would hate hate joy')
    #return flask.render_template("index.html")

@app.route("/initdb")
def database_helper(): #creates the db on load
    
    init_db()
    return "Done"
@app.route('/nltkdownload')
def downloader(): #downloads the nltk resources that are needed for this project to function
    nltk.download()
    return "Done"
