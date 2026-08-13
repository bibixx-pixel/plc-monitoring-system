# db_manager.py
import sys
import sqlite3
from datetime import datetime, date
from contextlib import contextmanager

from src.setting_manager import MySetting

@contextmanager
def get_db():
    conn = sqlite3.connect(MySetting.get('db_path'))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
 
def init_db():
    # 설정 화면에서 테이블명을 바꿀 수 있도록 MySetting.get('table_name')으로 불러온 변수 정의해주기
    table_name =  MySetting.get('table_name')

    # {table_name}이라는 table이 없으면 새로 생성하라는 코드
    with get_db() as conn:
        conn.execute(f"""
                CREATE TABLE if not exists {table_name}(
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                        Low_temperature INTEGER NOT NULL,
                        High_temperature INTEGER NOT NULL, 
                        Measured_temp INTEGER NOT NULL, 
                        Timestamp TIMESTAMP NOT NULL
                );
        """)
        # log 라는 table이 없으면 새로 생성하라는 코드
        conn.execute("""
                CREATE TABLE if not exists log(
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                        alarm_msg TEXT NOT NULL,
                        exception_msg TEXT NOT NULL,
                        Timestamp TIMESTAMP NOT NULL
                );
        """)

def insert_temperature(timestamp, low, high, Measured):
    # 설정 화면에서 테이블명을 바꿀 수 있도록 MySetting.get('table_name')으로 불러온 변수 정의해주기
    table_name =  MySetting.get('table_name')

    # 온도 데이터를 temperature 테이블에 저장하는 함수
    with get_db() as conn:
        cursor = conn.execute(
            f"INSERT INTO {table_name} (Timestamp, Low_temperature, high_temperature, Measured_temp) VALUES (?, ?, ?, ?)",
            (timestamp, low, high, Measured)
        )

def insert_log(timestamp, alarm, exception):
    # 로그 데이터를 log 테이블에 저장하는 함수
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO log (Timestamp, alarm_msg, exception_msg) VALUES (?, ?, ?)",
            (timestamp, alarm, exception)
        )

# 조회한 날짜를 가져오는 함수
def get_date_data(table_name, start_date, end_date):

    # 데이터베이스 연결 (파일이 없으면 자동 생성)
    con = sqlite3.connect('plc_monitoring_system.db')

    # 커서 객체 생성 (SQL 명령 실행을 위해 필요)
    cursor = con.cursor()

    # start_date와 end_date 시간 범위 설정 변수 생성
    start = (f"{start_date} 00:00:00")
    end = (f"{end_date} 23:59:59")

    # 명령어 (온도 테이블에서 Timestamp 컬럼에서 start, end 값을 전달해라.)
    query = (f"SELECT * FROM {table_name} WHERE Timestamp BETWEEN ? AND ?")

    # 데이터 조회 (명령어와 날짜 값 2개를 합쳐서 전달)
    cursor.execute(query, (start, end))

    print("=== 조회한 날짜 목록 ===")
    # fetchall(): 모든 결과를 반환
    rows = cursor.fetchall()

    # DB에서 가져온 start_date, end_date 출력
    for row in rows:
        print(row)

    con.close()

    # 메인 파일로 가져온 데이터 묶음을 돌려보내기
    return rows

if __name__ == "__main__":
    init_db()