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
    # temperature 라는 table이 없으면 새로 생성하라는 코드
    with get_db() as conn:
        conn.execute("""
                CREATE TABLE if not exists temperature(
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

def check_table_exists(db_path, table_name):
    try:
        # 데이터베이스 연결 만들기
        conn = sqlite3.connect(db_path)

        # 커서 만들기
        cursor = conn.cursor()

        # 테이블이 있는지 확인하는 SQL 쿼리를 만들기.
        table_check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name= ?"

        # 커서를 사용하여 쿼리 실행.
        cursor.execute(table_check_query,(table_name,))

        # 결과 가져오기.
        table_exists = cursor.fetchone()

        # 결과 돌려주기.
        if table_exists:
            return True
        else:
            return False

    finally:
        if 'conn' in locals():
            # 커넥션 닫기.
            conn.close()

def insert_temperature(timestamp, low, high, Measured):
    # 온도 데이터를 temperature 테이블에 저장하는 함수
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO temperature (Timestamp, Low_temperature, high_temperature, Measured_temp) VALUES (?, ?, ?, ?)",
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
def get_date_data(start_date, end_date):

    # 데이터베이스 연결 (파일이 없으면 자동 생성)
    con = sqlite3.connect('plc_monitoring_system.db')

    # 커서 객체 생성 (SQL 명령 실행을 위해 필요)
    cursor = con.cursor()

    # start_date와 end_date 시간 범위 설정 변수 생성
    start = (f"{start_date} 00:00:00")
    end = (f"{end_date} 23:59:59")

    # 명령어 (온도 테이블에서 Timestamp 컬럼에서 start, end 값을 전달해라.)
    query = ("SELECT * FROM temperature WHERE Timestamp BETWEEN ? AND ?")

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