from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
# import time

# 실행 시작 시간 저장
# start = time.time()

class GetWordDataService():

    def getWordMean(search_word):

        url = "https://krdict.korean.go.kr/eng/dicSearchDetail/searchDetailWordsResult?nation=eng&nationCode=6&searchFlag=Y&sort=C&currentPage=1&ParaWordNo=&syllablePosition=&actCategoryList=&all_gubun=ALL&gubun=W&gubun=P&gubun=E&wordNativeCode=1&wordNativeCode=2&wordNativeCode=3&all_sp_code=ALL&sp_code=1&sp_code=2&sp_code=3&sp_code=4&sp_code=5&sp_code=6&sp_code=7&sp_code=8&sp_code=9&sp_code=10&sp_code=11&sp_code=12&sp_code=13&sp_code=14&sp_code=27&imcnt=1&imcnt=2&imcnt=3&searchSyllableStart=&searchSyllableEnd=&searchOp=AND&searchTarget=trans_word&searchOrglanguage=-1&wordCondition=wordSame&query={}&blockCount=10&myViewWord=62696&myViewWord=61190".format(search_word)
        html_doc = urlopen(url)

        # 페이지 전체 가져오기
        soup = BeautifulSoup(html_doc, "html.parser")

        # 영어단어 검색 결과 태그 찾기
        wordMeanList = soup.find("div", {"class": "search_result mt25 printArea"})
        # print(wordMeanList)

        # 결색 결과가 있을 경우 실행
        if wordMeanList is not None:

            # 검색 결과 담을 리스트, 딕셔너리 생성
            mean_list = []
            mean_dic = {}

            # 영어단어 의미와 형태 찾기 (5개까지만 리스트로)
            all_mean = wordMeanList.find_all("span", {"class": "word_type1_17"}, limit=5)
            all_class = wordMeanList.find_all("span", {"class": "word_att_type1"}, limit=5)
            # print(all_mean)
            # print(all_class)

            # 차례대로 사전에 넣어주기
            i = 0
            while i < len(all_mean):

                # 불필요한 태그 제거
                if all_mean[i].sup is not None:
                    all_mean[i].sup.clear()
                if all_class[i].span is not None:
                    all_class[i].span.clear()

                # 영어단어 의미에서 앞뒤 공백 제거
                word_mean = all_mean[i].get_text().strip()
                # 영어단어 형태에서 한글 외 제거
                word_class = re.sub('[^가-힣]', '', all_class[i].get_text())
                # print("뜻 : " + word_mean + ", 형태 : " + word_class)

                # 리스트에 딕셔너리로 넣기
                mean_dic['word_mean'] = word_mean
                mean_dic['word_class'] = word_class
                mean_list.append(mean_dic)

                # 딕셔너리 비워주기
                mean_dic = {}

                i += 1
        else:
            mean_list = None

        print("컨트롤러에 넘겨줄 값(딕셔너리) : " + str(mean_list))
        return mean_list

# 실행 시간
# print("time : ", time.time() - start)
