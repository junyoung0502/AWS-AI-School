import asyncio
import re
from typing import List, Dict, Optional, Iterator
from dataclasses import dataclass

# 1. UI 관련 함수
class UI:
    @staticmethod
    def show_list(data_list: List[str], price_dict: Optional[Dict[str, str]] = None) -> List[str]:
        try:
            index_list = []
            for i, option in enumerate(data_list):
                index_list.append(str(i+1))

                if price_dict != None:
                    price = price_dict.get(option, "가격 정보가 없습니다.")
                    print(f"{i+1}. {option} (가격: {price}원)")
                else:
                    print(f"{i+1}. {option}")

            return index_list
        except:
            print("\n 번호 출력 중 오류가 발생했습니다.")
            return []

    @staticmethod
    async def get_user_input(prompt: str) -> str:
        # 실행 스레드를 분리하여 input이 전체를 멈추지 않게 함
        return await asyncio.to_thread(input, prompt)

    @staticmethod
    async def input_function(i_list: List[str], item_list: List[str]) -> object:
        while True:
            try:
                user_input = await UI.get_user_input("\n 번호를 입력해주세요: ")
                
                if user_input in i_list:
                    select_item = item_list[int(user_input)-1]
                    name = select_item.name if hasattr(select_item, 'name') else select_item
                    print(f"\n '{name}'을(를) 선택하셨습니다.")
                    return select_item
                else:
                    print("\n 잘못된 입력입니다. 다시 입력하세요.")
                    
            except Exception: 
                print("\n 잘못된 입력 형식이거나 오류가 발생했습니다.")
                continue

            

# 2. 인증 관련 함수
class AuthManager:
    @staticmethod
    def log_in(user: Dict[str, 'Person']) -> Optional['Person']:
        while True:
            try:
                print("\n 로그인 (q: 종료)")
                input_id = input("아이디를 입력해주세요: ")
                if input_id == 'q': return None 

                input_pw = input("비밀번호를 입력해주세요: ")

                if input_id in user:
                    if user[input_id].pw == input_pw:
                        print("\n 로그인 성공")
                        print(f"{user[input_id].name}님, 반갑습니다.")
                        return user[input_id] 
                    else:
                        print("\n 비밀번호가 일치하지 않습니다.")
                else:
                    print("\n 아이디가 존재하지 않습니다.")
            except:
                print("\n 오류가 발생했습니다.")
                continue

    @staticmethod
    def sign_up(user: Dict[str, 'Person']) -> None:
        while True:
            try:
                print("\n 회원가입 (q: 종료)")
                input_id = input("아이디를 입력해주세요: ")
                if input_id == 'q': return

                if not re.match(r'^[a-zA-Z0-9]{5,20}$', input_id):
                    print("\n 아이디는 5~20자의 영문/숫자만 가능합니다.")
                    continue
                elif input_id in user:
                    print("이미 존재하는 아이디 입니다.")
                    continue

                while True:
                    input_pw = input("비밀번호를 입력해주세요: ")
                    if not re.match(r'^[a-zA-Z0-9!@*]{5,20}$', input_pw):
                        print("\n 비밀번호 형식이 올바르지 않습니다.")
                        continue
                    
                    input_name = input("이름을 입력해주세요: ")
                    user[input_id] = Customer(input_id, input_pw, input_name)
                    print(f"{input_name}님, 가입이 완료되었습니다.")
                    return
            except:
                print("\n 오류가 발생했습니다.")
                continue

# 3. 데이터 모델 클래스
@dataclass
class Stadium:
    def __init__(self, region: str, name: str, fee: str):
        self.region = region
        self.name = name
        self.fee = fee

class Reservation:
    def __init__(self, customer_id: str, stadium: Stadium, time: str):
        self.customer_id = customer_id
        self.stadium = stadium
        self.time = time
        self.status = "승인 대기중"

    def __str__(self):
        return f"[예약] ID:{self.customer_id} | {self.stadium.name} | {self.time} | 상태:{self.status}"

    def print_receipt(self):
        if self.status != "예약 확정":
            print("\n [알림] 예약이 확정되지 않아 영수증을 출력할 수 없습니다.")
            return
        
        print("\n" + "="*30)
        print("[ 풋살장 예약 영수증 ]")
        print("="*30)
        print(f" 예약자 : {self.customer_id}")
        print(f" 구장명 : {self.stadium.name} ({self.stadium.region})")
        print(f" 예약시간 : {self.time}")
        print(f" 결제금액 : {self.stadium.fee}원")
        print("-" * 30)
        print(" 이용해 주셔서 감사합니다.")
        print("="*30)

@dataclass
class Person:
    def __init__(self, user_id: str, pw: str, name: str):
        self.id = user_id
        self.pw = pw
        self.name = name

class Customer(Person):
    def __init__(self, user_id: str, pw: str, name: str):
        super().__init__(user_id, pw, name)
        self.my_reservations: List[Reservation] = []

    async def make_reservation(self, stadium: Stadium, time: str, server_db: List[Reservation]) -> Reservation:
        # [변경] time.sleep 제거 -> 대기 없이 즉시 실행
        print(f"\n[시스템] '{stadium.name}' 예약 처리 중...")
        
        new_res = Reservation(self.id, stadium, time)
        self.my_reservations.append(new_res)
        server_db.append(new_res)
        
        print("[시스템] 예약 완료.")
        return new_res

class Admin(Person):
    def approve_reservation(self, server_db: List[Reservation]):
        waiting_list = [r for r in server_db if r.status == "승인 대기중"]
        if not waiting_list:
            print("\n[관리자] 대기 중인 예약이 없습니다.")
            return
        
        display_list = [str(r) for r in waiting_list]
        index_list = UI.show_list(display_list)
        
        sel = input("\n처리할 예약 번호 (0:취소): ")
        if sel in index_list:
            idx = int(sel) - 1
            target = waiting_list[idx]
            act = input("승인(y) / 거절(n): ")
            if act.lower() == 'y': target.status = "예약 확정"; print("승인됨.")
            elif act.lower() == 'n': target.status = "거절됨"; print("거절됨.")
        else:
            if sel != '0': print("잘못된 입력.")

def get_log_generator(reservation_list: List[Reservation]):
    for res in reservation_list:
        yield f"[LOG] {res.time} - {res.customer_id} ({res.status})"
