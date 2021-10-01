from flask import Flask, request, Response
from functools import wraps
#aws의 linux환경에 있을때 적용
#import os
#import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import service.WordDataService as sg
import service.NewsDataService as sn
import util.CmmUtil as cu
import json
import datetime

# datetime은 pip install python-dateutil로 다운로드


application = Flask(__name__)

def as_json(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode("UTF-8")
        return Response(res, content_type="application/json; charset=utf-8")

    return decorated_function

# 영어 단어 검색
@application.route("/wordMeanAPI")
@as_json
def getWordMean():
    # 입력받은 영어단어(띄어쓰기 없어야함)
    search_word = cu.CmmUtil.nvl(request.args.get("search_word"))
    print("검색하는 영어 단어 : " + search_word)

    if search_word is not "":
        res = sg.GetWordDataService.getWordMean(search_word)
        print("서비스에서 넘어온 값 : " + str(res))

        data = {"word": search_word, "mean": res}

    else:
        data = {"word": None, "mean": None}

    print("결과 : " + str(data))
    return data

# 웹 기사 수집
@application.route("/newsDataAPI")
@as_json
def getNewsInfo():
    print("getNewsInfo 시작")

    # 검색할 웹 기사 게시일
    # 어제 날짜 구하기
    searchDate = datetime.datetime.today() - datetime.timedelta(1)
    
    # 검색 결과 가져오기
    res = sn.NewsDataService(searchDate).getNewsInfo()

    print("서비스에서 넘어온 값 : " + str(res))

    data = {"newsInfo": res}

    print("결과 : " + str(data))
    return data


if __name__ == "__main__":
    application.run(host="127.0.0.1", port=8001)

#aws의 linux환경에 있을때 적용
#if __name__ == "__main__":
#    application.run(host="0.0.0.0", port=5000)
