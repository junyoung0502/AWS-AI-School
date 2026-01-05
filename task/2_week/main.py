import sys
import asyncio
from utils import UI, AuthManager, Stadium, Reservation, Person, Customer, Admin, get_log_generator

stadium_db = {
    "서울": [
        Stadium("서울", "풋살장A", "100,000"),
        Stadium("서울", "풋살장B", "150,000"),
        Stadium("서울", "풋살장C", "200,000")
    ],
    "부산": [
        Stadium("부산", "풋살장A", "80,000"),
        Stadium("부산", "풋살장B", "100,000"),
        Stadium("부산", "풋살장C", "150,000")
    ]
}

start_time = ["08:00~09:59", "10:00~11:59", "12:00~13:59", "18:00~19:59", "20:00~21:59"]

users = {
    "dlwnsdud": Customer("dlwnsdud", "dlwnsdud@", "이준영"),
    "admin": Admin("admin", "admin1111!", "관리자")
}

server_reservation_list = []

async def process_reservation(user, server_db):
    # 1. 지역 선택
    regions = list(stadium_db.keys())
    r_idxs = UI.show_list(regions)
    s_region = await UI.input_function(r_idxs, regions)

    # 2. 구장 선택
    places = stadium_db[s_region]
    p_price = {p.name: p.fee for p in places}
    p_idxs = UI.show_list([p.name for p in places], p_price)
    s_place = await UI.input_function(p_idxs, places)
    
    # 3. 시간 선택
    t_idxs = UI.show_list(start_time)
    s_time = await UI.input_function(t_idxs, start_time)

    # 4. 예약 요청
    new_reservation = await user.make_reservation(s_place, s_time, server_db)
    
    return new_reservation, s_region, s_place, s_time


async def main():
    login_user = None
    running = True

    print('''
    안녕하십니까. 풋살장 예약 서비스입니다.
    로그인 후 접속이 가능합니다.
    회원이 아닌 경우, 회원가입이 필요합니다.
    ''')

    while running:
        if login_user is None:
            print('\n 1. 로그인 | 2. 회원가입 | q. 종료')
            try:
                user_input = input("입력: ")
                if user_input == "1":
                    login_user = AuthManager.log_in(users)
                elif user_input == "2":
                    AuthManager.sign_up(users)
                elif user_input == "q":
                    running = False
                else:
                    print("잘못된 입력")
            except:
                continue

        else:
            if isinstance(login_user, Admin):
                print(f"\n [관리자({login_user.name})] 1.예약승인 | 2.예약보기 | 3.로그아웃")
                sel = input("선택: ")
                if sel == "1":
                    login_user.approve_reservation(server_reservation_list)
                elif sel == "2":
                    print("\n[예약 정보 보기]")
                    for log in get_log_generator(server_reservation_list):
                        print(log)
                elif sel == "3":
                    login_user = None

            elif isinstance(login_user, Customer):
                print(f"\n [고객({login_user.name})] 1.예약하기 | 2.내 예약 | 3.영수증 | 4.로그아웃")
                sel = input("선택: ")

                if sel == "1":
                    try:
                        print("\n[예약하기] 5분 이내에 예약을 완료해주세요!")
                        reservation_data = await asyncio.wait_for(
                            process_reservation(login_user, server_reservation_list), 
                            timeout=30.0  # 테스트용으로 30초 설정
                        )
                        
                        # 시간 내 성공 시
                        new_res, reg, place, time_slot = reservation_data
                        
                        print(f'''
                        [예약 내역 확인]
                        --------------------
                        지역: {reg}
                        구장: {place.name}
                        시간: {time_slot}
                        가격: {place.fee}원
                        --------------------
                        * 입금 정보: 금일 23:59까지 입금 요망
                        ''')
                        
                    except asyncio.TimeoutError:
                        # 300초가 지나면 여기로 튕겨져 나옴
                        print("\n\n" + "!"*30)
                        print(" [TIME OUT] 5분이 지났습니다!")
                        print(" 예약이 취소되고 초기 화면으로 돌아갑니다.")
                        print("!"*30 + "\n")
                    

                elif sel == "2":
                    print("\n[내 예약 목록]")
                    for r in login_user.my_reservations:
                        print(r)

                elif sel == "3":
                    confirmed = [r for r in login_user.my_reservations if r.status == "예약 확정"]
                    if not confirmed:
                        print("출력 가능한 예약이 없습니다.")
                    else:
                        d_list = [f"{r.stadium.name} ({r.time})" for r in confirmed]
                        valid_idxs = UI.show_list(d_list)
                        sel_idx = input("번호 입력 (0: 취소): ")
                        if sel_idx in valid_idxs:
                            idx = int(sel_idx) - 1
                            confirmed[idx].print_receipt()

                elif sel == "4":
                    login_user = None
                    print("로그아웃 되었습니다.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
