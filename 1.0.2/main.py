from run import Naver

if __name__ == '__main__':
    # 객체 선언
    naver = Naver()

    # 필요 정보 설정
    naver.n_id = "naver0123"
    naver.n_pw = "123123"
    naver.cafeID = 12345 # 카폐 번호
    naver.menuID = 1 # 게시판(메뉴) 번호
    naver.title = "[Title] Selenium Test"
    naver.content = "[Content] Selenium Test<p>Hello World</p><p>CUCUUC</p>"
    naver.BTime = "13:53:59" # 예약 시간
    # imgUrl 필요 하면 무조건 절대경로 삽입
    # naver.imgUrl = "C:\\Users\\selenium\\sample.png"
    # imgUrl 필요하지 않으면 ""로 처리
    naver.imgUrl = ""

    naver.sleep_sec = 1 # 똥컴 = 1 ~ 3초, 보통 = 0.5 ~ 1초, 짱 = 0.1 ~ 0.5
    # 실행
    # (총 걸리는 시간) = (함수 호출 횟수) x (sleep_sec)ms
    naver.main()