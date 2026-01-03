import re

class reserve:
    def log_in(user):
        while True:
            print("\n 로그인")
            input_id = input("아이디를 입력해주세요: ")
            input_pw = input("비밀번호를 입력해주세요: ")

            # 아이디, 비밀번호 확인
            if input_id in user:
                if user[input_id] == input_pw:
                    print("\n 로그인 성공")
                    print(f"{input_id}님, 반갑습니다.")
                    return input_id
                    break
                else:
                    print("\n 비밀번호가 일치하지 않습니다.")
                    continue
            else:
                print("\n 아이디가 존재하지 않습니다.")
                continue

    def sign_up(user):
        while True:
            print("\n 회원가입")
            input_id = input("아이디를 입력해주세요: ")

            if not re.match(r'^[a-zA-Z0-9]{5,20}$', input_id):
                print("\n 아이디는 5~20자의 영문/숫자만 입력이 가능합니다.")
                continue

            elif input_id in user:
                print("이미 존재하는 아이디 입니다.")
                continue

            while True:
                input_pw = input("비밀번호를 입력해주세요: ")
                if not re.match(r'^[a-zA-Z0-9!@*]{5,20}$', input_pw):
                    print("\n 비밀번호는 5~20의 영문/숫자/특수문자(!@*)만 입력이 가능합니다.")
                    continue

                else:
                    user[input_id] = input_pw
                    print(f"{input_id}님, 환여합니다. 가입이 완료되었습니다.")
                    return

    def show_list(data_list, price_dict=None):

        index_list = []
        for i, option in enumerate(data_list):
            index_list.append(str(i+1))

            if price_dict != None:
                price = price_dict.get(option, "가격 정보가 없습니다.")
                print(f"{i+1}. {option} (가격: {price}원)")
            else:
                print(f"{i+1}. {option}")

        return index_list

    def input_function(i_list, item_list):
        while True:
            # 사용자 입력
            user_input = input("\n 번호를 입력해주세요:")

            if user_input in i_list:
                # 선택한 번호와 풋살장 매칭
                select_item = item_list[int(user_input)-1]
                print(f"\n {select_item}을 선택하셨습니다.")
                return select_item
            else:
                print("\n 잘못된 입력입니다. 다시 입력하세요.")
                continue