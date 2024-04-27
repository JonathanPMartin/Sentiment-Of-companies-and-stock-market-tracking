from .DBcommands import *
import requests
import random
from bs4 import BeautifulSoup
#import datetime
from datetime import datetime, timedelta
import nltk 
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
startdate="2024-03-26"
Apikeys=["0896662f0e03431aa59a190506001d9a","07e4ef2350934283b8519fe475e501d5","f0d9b0a2e4e347e8a55e6c013ee110c5","b97537e068a84b3c9bb61108472df551","14a82a26f5b6493ab0ce8462709bae76","e3fff7fc440542c9923ebfd16005136f","2a026f3d832d4ba892d4a598b75157f8","16c656e972334d27bb0b94f37605f4f9","d5db1012f44841cd8aedd9bf0f53ef90","71d65b2753fc4b75b03e5414650cb0c1","54de7376d5474ca0a6e7ec9ecd81ca26"]

def CleaningHTML(Url,headline): #cleans the body removing all html ellements and removing as much infomation that is not relvent from the data as is possible with my skill level
    response = requests.get(Url, verify=False)
    code=response.status_code
    if code<300:
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
    else:
        return "False"

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

RandColour="#"
hexcolours=["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
for i in range(0,6):
    RandColour=RandColour+hexcolours[random.randint(0,15)]

graph1={
    "Xlabel":'Label',
    "Title":"Graph1",
    "Ylabel":"Label",
    "plots":{
        "Xplots":[[datetime(2024, 4, 26, 9, 30), datetime(2024, 4, 26, 10, 0), datetime(2024, 4, 26, 10, 30),
             datetime(2024, 4, 26, 11, 0), datetime(2024, 4, 26, 11, 30), datetime(2024, 4, 26, 12, 0)]],
        "YPlots":[[100, 110, 105, 115, 120, 125]],
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
        "colours":[RandColour,'blue']
    }
}
"""
def PlotGraphs(graph1,graph2):
    for i in range(0,len(graph1['plots']['Xplots'])):
        plt.plot(graph1['plots']['Xplots'][i], graph1['plots']['YPlots'][i], label=graph1['plots']['Label'][i], color=graph1['plots']["colours"][i])
    
    plt.title(graph1["Title"])
    plt.xlabel(graph1["Xlabel"])
    plt.ylabel(graph1["Ylabel"])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.legend()
    plt.grid(True)
    plt.savefig('plot1_image.png')
    plt.clf()
    for i in range(0,len(graph2['plots']['Xplots'])):
        plt.plot(graph2['plots']['Xplots'][i], graph2['plots']['YPlots'][i], label=graph2['plots']['Label'][i], color=graph2['plots']["colours"][i], linestyle='',marker='o',markersize=0.5)
    plt.title(graph2["Title"])
    plt.xlabel(graph2["Xlabel"])
    plt.ylabel(graph2["Ylabel"])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.legend()
    plt.grid(True)
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
    
    #print(APIsearch)
    #return []

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
def CleanBodyandSentimenttoDb(company):
    Urls=[]
    query="select * from Urls WHERE company='{}'".format(company)
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
            company=Result["company"]
            
            Headline=Headline.replace("FfFf","'")
            Headline=Headline.replace('fFfF','"')
            
            cleanedbody=CleaningHTML(i,Headline)
            if cleanedbody !=False:
                if company in cleanedbody: #checks if the data collected contains the company itself as the cleaning method is not perfect , if it doesnt does not add it to the db
                    SentimetScore=Sentimentclean(cleanedbody)
                    cleanedbody=cleanedbody.replace("'","FfFf")
                    cleanedbody=cleanedbody.replace('"',"fFfF")
                    Qrys.append(SentimetScore)
                    Qry = f"INSERT INTO CleanedStories (storyUrl, Cleanedbody) VALUES ('{i}','{cleanedbody}')"
                    CalQry = write_db(Qry)
                    Qry = f"INSERT INTO storySentiment (Cleanedbody,pos,neg,overall) VALUES ('{cleanedbody}',{SentimetScore[0]},{SentimetScore[1]},{SentimetScore[2]})"
                    CalQry = write_db(Qry)
    return Qrys
def MassAddUrlDatatodb(Val):
    Qry="SELECT * FROM Companies"
    companies=[]
    Result=query_db(Qry)
    for i in Result:
        companies.append(i['company'])
    
    tem=Val*100
    
    Apikey=Apikeys[Val]
    tem2=0
    for j in range(0,100):
        tem2=tem+j
        company=companies[tem2]
        values=GrabNews(company,Apikey,company)
        UriAddToDB(values,company)
    return companies
def stokcswithdata(compaines):
    current_datetime = datetime.now()
    current_month = current_datetime.month
    current_day = current_datetime.day
    current_year = current_datetime.year
    if current_month<10:
        current_month="0"+str(current_month)
    if current_day<10:
        current_day="0"+str(current_day)
    current_month=str(current_month)
    current_day=str(current_day)
    current_year=str(current_year)
    currentdate=current_year+"-"+current_month+"-"+current_day

    for i in compaines:
        Qry="SELECT * FROM Companies Where company='{}'".format(i)
        QryResult=query_db(Qry,one=True)
        stock=QryResult["stock"]
        url=f"https://api.twelvedata.com/time_series?symbol={stock}&interval=15min&start_date={startdate}&end_date={currentdate}&apikey=5eb91eed0cb149eaa54cb7acc41210ee&source=docs"
        res=requests.get(url)
        open_page=res.json()
        if "values" in open_page.keys():
            values=open_page['values']
            for j in values:
                Data=j["datetime"].split(" ")
                value=j["close"]
                bigTime=Data[0].split("-")
                smallTime=Data[1].split(":")
                year=int(bigTime[0])
                month=int(bigTime[1])
                day=int(bigTime[2])
                hour=int(smallTime[0])
                Min=int(smallTime[1])
                #f"INSERT INTO Urls (storyUrl, company, headline,storyYear,storyMonth,storyDay,storyHour,storyminute) VALUES ('{i[1]}','{company}', '{Headline}', {i[2][0]},{i[2][1]},{i[2][2]},{i[2][3]},{i[2][4]})"   
                Testqry=f"SELECT * FROM stockvalue WHERE stock='{stock}' AND stockYear={year} AND stockMonth={month} AND stockDay={day}" 
                responce=query_db(Testqry) 
                if True: #requries table purge to work sucks but it is what it is
                    qry=f"INSERT INTO stockvalue(stock,stockYear,stockMonth,stockDay,stockHour,stockminute,stockvalue) Values('{stock}',{year},{month},{day},{hour},{Min},{value})"
                    CalQry = write_db(qry)
        #https://api.twelvedata.com/time_series?symbol=AAPL&interval=15min&start_date=2020-01-01&end_date=2023-01-01&apikey=5eb91eed0cb149eaa54cb7acc41210ee&source=docs
    return compaines
def grabSentimentbyco(company):
    RetunObject=[]
    qry=f"SELECT * FROM Urls where company='{company}'"
    responce=query_db(qry) 
    for i in responce:
         headline=i['headline']
         year=i['storyYear']
         month=i['storyMonth']
         day=i['storyDay']
         hour=i['storyHour']
         miniute=i['storyminute']
         Url=i['storyUrl']
         Qry=f"SELECT * FROM CleanedStories WHERE storyUrl='{Url}'"
         TestQry=query_db(Qry)
         score=0
         TestCheck=False
        
         if len(TestQry)==1:
            TestCheck=True
            body=TestQry[0]['Cleanedbody']
            ThirdQry=f"SELECT * FROM storySentiment WHERE Cleanedbody='{body}'"
            ThirdResponce=query_db(ThirdQry, one=True)
            score=ThirdResponce['overall']
         if TestCheck:
             tem={
                 "company":company,
                 "year":year,
                 "month":month,
                 "day":day,
                 "hour":hour,
                 "minute":miniute,
                 "value":score
             }
             RetunObject.append(tem)
  
   
    return RetunObject
def getStockvaluebyco(company):
    qry=f"SELECT * FROM Companies WHERE company='{company}'"
    responce=query_db(qry, one=True)
    stock=responce['stock']
    seccondqry=f"SELECT * FROM stockvalue WHERE stock='{stock}'"
    SeccondResponce=query_db(seccondqry)
    Returnobject=[]
    for i in SeccondResponce:
        year=i['stockYear']
        month=i['stockMonth']
        day=i['stockDay']
        hour=i['stockHour']
        minute=i['stockminute']
        value=i['stockvalue']
        tem={
            "company":company,
            "year":year,
            "month":month,
            "day":day,
            "hour":hour,
            "minute":minute,
            "value":value
        }
        Returnobject.append(tem)
    return Returnobject

def feedingTheGraphs(company):
    stockinfo=getStockvaluebyco(company)
    publicview=grabSentimentbyco(company)
    StockYValues=[]
    StockXValues=[]
    PublicYVales=[]
    PublicXVales=[]
    for i in stockinfo:
        TimeData = datetime(i["year"], i["month"],i["day"], i["hour"], i["minute"])
        StockXValues.append(TimeData)
        StockYValues.append(i["value"])
    for i in publicview:
        TimeData = datetime(i["year"], i["month"],i["day"], i["hour"], i["minute"])
        PublicXVales.append(TimeData)
        PublicYVales.append(i["value"])
    
    graph1={
        "Xlabel":'Date',
        "Title":company,
        "Ylabel":"Stock Values",
        "plots":{
             "Xplots":[StockXValues],
             "YPlots":[StockYValues],
             "Label":[company],
            "colours":['red','blue']
        }
    }
    graph2={
        "Xlabel":'Date',
        "Title":company,
        "Ylabel":"Public Perception",
        "plots":{
             "Xplots":[PublicXVales],
             "YPlots":[PublicYVales],
             "Label":[company],
            "colours":['red','blue']
        }
    }
    PlotGraphs(graph1,graph2)

@app.route("/")
def index():
    """
    Main Page.
    """
    feedingTheGraphs("Walmart")
    #return getStockvaluebyco("Walmart")
    #return grabSentimentbyco("Walmart")
    #return stokcswithdata()
    return flask.render_template("index.html")

@app.route("/stocks/<company>")
def stocks(company):
    List=[company]
    return stokcswithdata(List)
@app.route("/collecturls/<id>")
def colllecturls(id):
    id=int(id)
    return MassAddUrlDatatodb(id)

@app.route("/cleanstories/<company>")
def cleanstories(company):
    return CleanBodyandSentimenttoDb(company)

@app.route("/initdb")
def database_helper(): #creates the db on load
    
    init_db()
    return "Done"
@app.route('/nltkdownload')
def downloader(): #downloads the nltk resources that are needed for this project to function
    nltk.download()
    return "Done"
