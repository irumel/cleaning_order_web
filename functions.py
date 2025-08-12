import pymysql
import enc_dec_func as edfunc

host = 'database host address'
user = 'username'
target_string = '78+31j,18+25j,92+46j,48+44j,87+50j,76+9j,51+42j,36+9j,11+42j' # encoded_string
password = edfunc.Decoding(1234, target_string, "your password") # arguments: seed, encoded_string, your password
db = 'database name'


# ==================================== read =====================================

# info 파일을 읽고 info 리스트로 반환합니다
# 입력: 없음
# 출력: info (2차원 리스트 [[str, int, int, int, int, int]])
# info: [[이름, 구역, 값, 누적 횟수, 활성화 여부, 정렬 기준 숫자]]
def read_infofile():
  conn = pymysql.connect(host = host, user = user, password = password, db = db, charset = 'utf8')
  cur = conn.cursor()
  cur.execute("SELECT * FROM ideal")
  row = cur.fetchone()
  ideal_implementer = row[0]

  cur.execute("SELECT * FROM info")

  info = []
  while True:
    row = cur.fetchone()
    if not row: break
    person_info = list(row)
    info.append(person_info)
  conn.close()

  for index, person_info in enumerate(info):
    if person_info[0] == ideal_implementer:
      start_index = index
  
  for i in range(len(info)):
    info[(i+start_index)%len(info)].append(i)

  return info

# ==================================== read =====================================


# ==================================== write ====================================
# 데이터베이스의 history 테이블에 청소 인원을 작성합니다
# 입력: implementer (1차원 리스트 [str, str]), date (str), weekday (str), time (str)
# 출력: 없음
def write_historyfile(implementer, date, weekday, time):
  if not implementer: return

  conn = pymysql.connect(host = host, user = user, password = password, db = db, charset = 'utf8')
  cur = conn.cursor()

  formatted_date = f'{date} ({weekday})'
  formatted_implementer = ' '.join(implementer)
  cur.execute("INSERT into history (date, time, names) values (%s, %s, %s)", (formatted_date, time, formatted_implementer))

  conn.commit()
  conn.close()
# ==================================== write ====================================


# ======================================= get ===================================

# 청소 우선순위 리스트를 반환합니다
# 입력: 없음
# 출력: lst (1차원 리스트 [str, str, str])
def get_priority_list():
  info = read_infofile()
  sorted_info = sorted(info, key=lambda x: (-x[4], x[2], x[5], x[1]))

  lst = []
  for data in sorted_info:
    if data[4]: lst.append(data[0])

  return lst

# 활성화 인원 리스트를 반환합니다
# 입력: 없음
# 출력: activation (2차원 리스트 [[str, int]])
# activation: [[이름, 활성화 여부]]
def get_activation_list():
  info = read_infofile()

  activation = []
  for i in info:
    temp = [i[0], i[4]]
    activation.append(temp)

  return activation

# 데이터베이스에서 history 테이블을 읽어 history 리스트를 반환합니다
# 입력: 없음
# 출력: history (1차원 리스트 [[str, str, str]])
def get_history():
  conn = pymysql.connect(host = host, user = user, password = password, db = db, charset = 'utf8')
  cur = conn.cursor()
  cur.execute("SELECT * FROM history")
  rows = cur.fetchall()

  history_list = []
  for row in rows:
    history_list.append(f'{row[0]} {row[1]}\t{row[2]}\n')
    history_list.append('\n')

  conn.close()
  return history_list
# ======================================= get ===================================


# ==================================== update ===================================

# 데이터베이스의 info 테이블을 청소 인원을 반영하여 갱신합니다
# 입력: implementer (1차원 리스트 [str, str])
# 출력: 없음
def update_implementer(implementer): 
  conn = pymysql.connect(host = host, user = user, password = password, db = db, charset = 'utf8')
  cur = conn.cursor()

  for name in implementer:
    cur.execute("SELECT * FROM info WHERE name = %s", (name, ))
    row = cur.fetchone()
    ideal_update = row[2] + 1
    accumulated_update = row[3] + 1
    cur.execute("UPDATE info SET ideal = %s, accumulated = %s WHERE name = %s", (ideal_update, accumulated_update, name))
  
  conn.commit()
  conn.close()

# 데이터베이스의 info 테이블과 ideal 테이블을 이상적인 상황을 반영하여 갱신합니다
# 입력: implementer (1차원 리스트 [str, str])
# 출력: 없음
def update_ideal(implementer):
  conn = pymysql.connect(host = host, user = user, password = password, db = db, charset = 'utf8')
  cur = conn.cursor()
  cur.execute("SELECT * FROM ideal")
  row = cur.fetchone()
  ideal_implementer = row[0]
  past = ideal_implementer

  cur.execute("SELECT * FROM info")
  info = cur.fetchall()
  num = len(implementer)
  for i in range(len(info)):
    if not num: break
    if (info[i][0] == ideal_implementer):
      if info[i][4]: # 활성화 여부 확인
        ideal_update = info[i][2] - 1
        cur.execute("UPDATE info SET ideal = %s WHERE name = %s", (ideal_update, ideal_implementer))
        ideal_implementer = info[(i+1)%len(info)][0]
        num -= 1
      else:
        ideal_implementer = info[(i+1)%len(info)][0] # 비활성화라면 다음으로 넘어갑니다

  cur.execute("UPDATE ideal SET name = %s WHERE name = %s", (ideal_implementer, past))
  conn.commit()
  conn.close()

# 데이트베이스의 info 테이블을 활성화 상태를 반영하여 갱신합니다
# 입력: activation_list (1차원 리스트 [str, str])
# 출력: 없음
def update_activation(activation_list):
  conn = pymysql.connect(host = host, user = user, password = password, db = db, charset = 'utf8')
  cur = conn.cursor()

  cur.execute("SELECT * FROM info")
  info = cur.fetchall()
  for i in info:
    if (i[0] in activation_list):
      cur.execute("UPDATE info SET activation = %s WHERE name = %s", (1, i[0]))
    else:
      cur.execute("UPDATE info SET activation = %s WHERE name = %s", (0, i[0]))

  conn.commit()
  conn.close()

# ==================================== update ===================================


# ==================================== save =====================================

# info 파일을 청소 인원을 반영하여 작성합니다
# 입력: implementer (1차원 리스트 [str, str])
# 출력: 없음
def save_implementer(implementer):
  if not implementer: return
  update_implementer(implementer)
  update_ideal(implementer)

# info 파일을 활성화 상태를 반영하여 작성합니다
# 입력: activation_list (1차원 리스트 [str, str])
# 출력: 없음
def save_activation(activaion_list):
  if not activaion_list: return
  update_activation(activaion_list)

# ==================================== save =====================================

# 사용되지 않는 함수
def add_person():
  info = read_infofile()

  name = input('추가할 사람의 이름: ').replace(' ', '')
  if not name:
    print('아무것도 입력되지 않음')
    return
  try: number = int(input('구역 (정수): '))
  except: print('잘못된 입력. 추가를 취소합니다.'); return

  info = sorted(info, key=lambda x: x[1])
  index_max = 0
  clean_num_min = 10000
  for i in range(len(info)):
    if info[i][1] == number:
      index_max = i
      if info[i][3] < clean_num_min: clean_num_min = info[i][3]

  info.insert(index_max + 1, [name, number, clean_num_min, clean_num_min, 0, 1])

  # write_infofile(info, None)
