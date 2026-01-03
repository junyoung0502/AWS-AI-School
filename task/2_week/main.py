import re
import sys
from utils import reserve

#  사전 정보(프로그램 저장 정보)
user = {
    'busan':'ipark',
    'dlwnsdud':'dlwnsdud'
}

place_info = {
    "서울" : {"풋살장 A" : '100,000', "풋살장 B" : '150,000', "풋살장 C" : '200,000'},
    "부산" : {"풋살장 A" : '80,000', "풋살장 B" : '100,000', "풋살장 C" : '150,000'}
}

start_time = ["08:00~09:59", "10:00~11:59", "12:00~13:59", "18:00~19:59", "20:00~21:59", "22:00~23:59"]

user_id = None
running = True

# 서비스 코드
print('''
안녕하십니까. 풋살장 예약 서비스입니다.
로그인 후 접속이 가능합니다.
회원이 아닌 경우, 회원가입이 필요합니다.
''')

while running:

    # 첫 화면
    if user_id == None:
        print('''
        로그인이 필요합니다.
        1. 로그인
        2. 회원가입
        q. 프로그램 종료
        ''')

        # 사용자 입력
        user_input = input("입력해주세요: ")

        # 로그인
        if user_input == "1":
            user_id = reserve.log_in(user)
        # 회원가입
        # id: 글자 수 5~20자, 영문/숫자만 가능 [a-zA-Z]
        # pw: 글자 수 5~20자, 영문/숫자/특수문자 가능(허용 특수문자: '!,@,*')
        # pw에 무조건 영문/숫자/특수문자 하나씩 들어가게 수정 필요
        elif user_input == "2":
            reserve.sign_up(user)
        # 프로그램 종료
        elif user_input == "q":
            print("\n 프로그램을 종료합니다.")
            running=False
        else:
            print("\n 잘못된 입력입니다.")
            continue

    # 로그인 이후 화면
    else:
        while running:
            print(f"\n 사용자: {user_id}")
            print('''
            1. 풋살장 선택
            2. 로그아웃
            q. 프로그램 종료
            ''')

            # 사용자 입력
            user_input = input("\n 번호를 입력해주세요: ")

            # 풋살장 예약 화면
            if user_input == "1":
                print("\n 지역 선택")
                regions = list(place_info.keys())
                
                index_list = reserve.show_list(regions)
                select_region = reserve.input_function(index_list, regions)


                # 풋살장 선택 화면
                print("\n 구장 선택")
                places = list(place_info[select_region].keys())
                place_price = place_info[select_region]

                index_list = reserve.show_list(places, place_price)
                select_place = reserve.input_function(index_list, places)


                # 시간 선택 화면
                print("\n 시간 선택")
                index_list = reserve.show_list(start_time)
                select_time = reserve.input_function(index_list, start_time)

                # 최종 예약 내역 확인
                print(f'''
                [최종 예약 정보]
                지역: {select_region}
                구장: {select_place}
                시간: {select_time}
                가격: {place_info[select_region][select_place]}원

                * 입금 정보
                금일 23:59 이전에 입금이 완료되어야 예약이 확정됩니다.
                ''')


                print(f'''
                1. 예약 화면으로 돌아가기
                2. 로그아웃
                q. 프로그램 종료
                ''')

                # 사용자 입력
                user_input = input("\n 번호를 선택해주세요:")

                # 예약 화면으로 돌아가기
                if user_input == "1":
                    continue

                # 로그아웃
                elif user_input == "2":
                    user_id = None
                    print("\n 로그아웃 되었습니다.")
                    break

                elif user_input == "q":
                    print("\n 프로그램을 종료합니다.")
                    running=False

                else:
                    print("\n 잘못된 입력입니다.")
                    continue

            # 로그아웃
            elif user_input == "2":
                user_id = None
                print("\n 로그아웃 되었습니다.")
                break

            elif user_input == "q":
                print("\n 프로그램을 종료합니다.")
                running=False

            else:
                print("\n 잘못된 입력입니다.")
                continue