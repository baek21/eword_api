from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


class NewsDataService:

    date = None

    def __init__(self, date):
        self.date = date

    # 링크 주소에서 기사 본문 내용 가져오기
    def getContents(self, newsUrl):

        # print("getContents 시작")

        # 웹 기사 수집 결과 담을 딕셔너리
        news_dic = {}

        # 크롤링할 주소 열기
        newsDoc = urlopen(newsUrl)

        # 페이지 전체 가져오기
        newsSoup = BeautifulSoup(newsDoc, "html.parser")

        # 기사 분야(영문, 숫자만 남기기)
        newsArea = newsSoup.find("div", {"class": "header_bottom_section_tit ellipsis"}).get_text()
        newsArea = re.sub("[^A-Za-z0-9]", " ", newsArea).strip()
        print("newsArea : " + newsArea)

        # 기사 제목(영문, 숫자만 남기기)
        newsTitle = newsSoup.find("h1", {"class": "view_tit"}).get_text()
        newsTitle = re.sub("[^A-Za-z0-9]", " ", newsTitle).strip()
        print("newsTitle : " + newsTitle)

        # 기사 내용(영문, 숫자만 남기기)
        newsContents = newsSoup.find("div", {"class": "view_con"}).get_text()
        newsContents = re.sub("[^A-Za-z0-9]", " ", newsContents).strip()
        print("newsContents : " + newsContents)

        # 딕셔너리에 수집한 기사 정보 넣기(기사 게시일, 분야, 제목, 내용)
        news_dic['newsReg'] = (self.date).strftime('%Y%m%d')
        news_dic['newsArea'] = newsArea
        news_dic['newsTitle'] = newsTitle
        news_dic['newsContents'] = newsContents

        #print(news_dic)

        return news_dic


    # 해당 날짜에 게시된 웹 기사 크롤링하기
    def getNewsInfo(self):

        # 검색할 웹 기사 등록일과 날짜 형태 맞추기
        formatDay = (self.date).strftime('%b %d, %Y')

        print(str(formatDay))

        # 9월일 경우 헤럴드코리아 기사등록일 형태에 맞춰 Sep을 Sept로 수정
        if ("Sep" == str((self.date).strftime('%b'))):
            formatDay = re.sub('Sep', 'Sept', formatDay)

        searchDate = re.sub(' 0', ' ', formatDay)

        # 어제의 모든 기사 링크 담을 Set
        urlSet = set()

        # 검색할 페이지수(1부터 시작)
        pageMinNum = 1
        pageMaxNum = 10
        while pageMinNum <= pageMaxNum:

            print(str(pageMinNum) + " 페이지")

            url = "http://www.koreaherald.com/list.php?ct=020000000000&np={}&mp=1".format(pageMinNum)
            html_doc = urlopen(url)

            # n번째 페이지 전체 가져오기
            soup = BeautifulSoup(html_doc, "html.parser")

            # n번째 페이지의 기사 목록만 가져오기
            news = soup.find("ul", {"class": "main_sec_li main_sec_li_only"}).find_all("li")

            i = 0
            while i < len(news):

                print(str(i + 1) + "번째 기사")

                # 기사 게시일
                newsReg = news[i].find("div", {"class": "main_l_t2"}).span.extract().get_text().strip()
                print("웹 기사 등록일 : " + newsReg)

                # 어제 링크만 수집
                if searchDate == str(newsReg):

                    # 기사 링크 주소
                    newsUrl = "http://www.koreaherald.com" + news[i].a['href'].strip()
                    print("수집된 링크 : " + newsUrl)

                    urlSet.add(newsUrl)

                i += 1

            # 다음 페이지 번호
            pageMinNum = pageMinNum + 1


        # 웹 기사 수집 결과 담을 리스트
        news_list = []

        # set은 인덱싱을 지원하지 않으므로 list로 변환한다.
        urlList = list(urlSet)

        # 수집된 링크로 기사 정보 가져오기
        j = 0
        while(j < len(urlList)):

            # 수집된 결과(딕셔너리)를 리스트에 넣기
            news_list.append(NewsDataService.getContents(self, urlList[j]))

            j += 1

        print("컨트롤러에 넘겨줄 값(딕셔너리) : " + str(news_list))

        return news_list

