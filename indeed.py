import requests  #html의 정보를 가져오는 라이브러리!(파이썬 자체 기능도 있지만 requests가 훨씬 강력해서 사용)
from bs4 import BeautifulSoup  #html에서 정보를 추출하는 라이브러리
#soup이라는 애가 데이터를 추출함
LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    #requests 라이브러리 사용해서 indeed 사이트 http를 last page.
    #print(result)를 하면 <response [200]>이 찍히는데 응답 성공이라는 의미임.

    soup = BeautifulSoup(result.text, "html.parser")
    #beautifulsoup 라이브러리 이용해서 requests로 가져온 http의 text 정보를 쭉 가져옴(프린트하면 방대한 text가 출력되곘지)

    pagination = soup.find("div", {"class": "pagination"})
    #자 이제 위에서 모든 text를 가져왔고 그 중 pages 정보를 가져오려고 함
    #soup.find_all('a'). # site page부분 요소검사로 class명 찾아봄. a들 상위로 class가 pagination인 div가 있었음.
    # <a class="pagination" href=https://www.indeed.com/jobs?q=python&limit=50></a>

    links = pagination.find_all('a')
    #div(class:pagination) 하부 anchor를 가져옴.

    pages = []

    for link in links[:-1]:
        # pages.append(link.find("span").string)
        pages.append(int(
            link.string))  #anchor 바로 밑의 string을 가져와도 span에서 가져온거랑 같은 결과
    #각각의 anchor 하부의 span(페이지넘버)들을 pages라는 리스트에 넣어줌

    max_page = pages[-1]
    #이제 page별(20개)로 계속 request 하는 방법을 알아야 함
    #max_page를 range에 넣어서 request를 불러올꺼야
    return max_page


# get_last_page() 라는 마지막 페이지 넘버를 추출하는 함수를 만들었음. 이제 필요한 곳에서 import해서 쓰면됨


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    if company:  #company가 없는 것도 있어서 넣었음.
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
            #company 이름이 span-a에 있는게 있고 span에 있는게 있음.
        company = company.strip()
    else:
        company = None
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    #div(class가 recJobLoc)로 변환된 후 div안의 attribute에 접근하는 개념임.
    job_id = html["data-jk"]
    return {
        'title':
        title,
        'company':
        company,
        'location':
        location,
        "link":
        f"https://www.indeed.com/jobs?q=python&limit=50&fromage=last&radius=25&start=850&vjk={job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):  #last_page는 main.py에서 넣어준 값이 들어감
        print(f"Scrapping Indeed Page: {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        #모든 pages를 requests 사용해서 HTTP를 가져옴
        # print(result.status_code) #status_code로 확인하면 200이 20개 나옴
        soup = BeautifulSoup(result.text, "html.parser")  #soup = 모든 text 추출
        results = soup.find_all(
            "div",
            {"class": "jobsearch-SerpJobCard"})  #result = 모든 text에서 div만 추출
        #results는 html 리스트인데 soup의 리스트이기도 하다.
        for result in results:
            job = extract_job(result)  #인자 result가 html을 담고 있다.
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()  #indeed의 마지막 페이지는 pages 함수에서 추출
    jobs = extract_jobs(last_page)  #마지막 페이지를 jobs 함수에 넣어줌
    return jobs
