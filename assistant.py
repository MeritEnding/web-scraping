import requests
from bs4 import BeautifulSoup

# pip install beautifulsoup4
# pip install lxml
def create_soup(url):
    res= requests.get(url)
    res.raise_for_status()
    soup =BeautifulSoup(res.text,"lxml")
    return soup

def scrape_weather():
    print("[오늘의 날씨]")
    url ="https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%8C%80%EC%A0%84+%EB%82%A0%EC%94%A8&oquery=%EB%B9%84%EC%84%9C+%EC%98%81%EC%96%B4%EB%A1%9C&tqi=ijM32dqVOsVsscFfdY8ssssssKK-360951"
    soup=create_soup(url)
    # 어제보다 00 도 높다
    cast =soup.find("p", attrs={"class":"summary"}).get_text()
    # 현재 00 도 (최저/ 최고)
    curr_temp =soup.find("div", attrs={"class","temperature_text"}).get_text().replace("°","")
    min_temp =soup.find("span",attrs ={"class":"lowest"}).get_text() # 최저 온도
    max_temp =soup.find("span",attrs ={"class":"highest"}).get_text() # 최고 온도

    # 비 올 확률
    morning_rain_element= soup.find("strong", attrs={"class":"time"}, string ="오전")
    afternoon_rain_element=soup.find("strong", attrs={"class":"time"}, string="오후")
    morning_rain_rate=morning_rain_element.find_next("span",class_="rainfall").get_text()
    afternoon_rain_rate=afternoon_rain_element.find_next("span", class_="rainfall").get_text()
    
    # 미세먼지 , 초미세먼지, 자외선, 일출
    today_chart= soup.find("ul",attrs={"class":"today_chart_list"})
    pm10 =today_chart.find_all("li")[0].get_text() # 미세먼지
    pm25 =today_chart.find_all("li")[1].get_text() # 초미세먼지
    sun =today_chart.find_all("li")[2].get_text() # 자외선
    sun_start= today_chart.find_all("li")[3].get_text() # 일출

    
    # 출력
    print(cast)
    print("현재 {} (최저 {}/ 최고 {})".format(curr_temp,min_temp,max_temp))
    print("오전 {} / 오후 {}".format(morning_rain_rate, afternoon_rain_rate))
    print()
    print("미세먼지 {}".format(pm10))
    print("초미세먼지 {}".format(pm25))
    print("자외선 {}".format(sun))
    print("일출 {}".format(sun_start))
    print()

    '''
    온도를 int로 안 받고 최고기온 00 이렇게 한 번에 받아서 뜨는 오류
    min_temp =int(min_temp)
    max_temp =int(max_temp)
    if(min_temp <= -4):
        print("패딩을 입어주세요 완전 겨울날씨 입니다!")
    elif (-3< min_temp and min_temp <= 9):
        print("오늘은 날씨도 좋은데 코트 어때요?")
    elif (min_temp >9 and min_temp <=23):
        print("오늘은 나가서 놀아야됩니다")
    elif(23<max_temp and max_temp <32):
        print("오늘은 냉장고 속에서 사는것을 추천합니다")
    else:
        print("아이스크림 가게로 대피하세요!!")
    '''


def scrape_headline_news():
    print("[뉴스]")
    url="https://news.naver.com/main/ranking/popularDay.naver"
    soup=create_soup(url)
    news_list =soup.find("ul", attrs={"class":"rankingnews_list"}).find_all("li",limit =3)
    for index, news in enumerate(news_list):
        title =news.div.find("a").get_text().strip()
        link =news.div.find("a")["href"]
        print("{}. {}".format(index+1,title))
        print("  (링크 : {})".format(link))
    print()

if __name__ =="__main__":
    #scrape_weather() # 오늘의 날씨 정보 가져오기 
    scrape_headline_news()