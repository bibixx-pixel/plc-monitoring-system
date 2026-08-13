import time
import json
import random
from datetime import datetime

from PySide6.QtCore import QThread, Signal

from src.client import MySocket
import src.db_manager as db_manager
from src.setting_manager import MySetting

# QThread로 작업 스레드는 emit만, 화면 변경은 메인 스레드의 슬롯에서만!
class Worker(QThread):
	# 온도 전달용 시그널
	temp_signal = Signal(float)
	# 시스템 로그 전달용 시그널
	log_signal = Signal(str)
	# 통신 상태 전달용 시그널
	communication_signal = Signal(str)

	def __init__(self, ip, port):
		super().__init__()
		self.power = True
		self.ip = ip
		self.port = port

	def check_temp_limit(self, temp_data):
		high = float(MySetting.get('limit_high'))
		low = float(MySetting.get('limit_low'))

		# 이상 발생 시 시그널과 DB로 전달할 경고 메시지 변수
		alarm_msg = ""

		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		# 상한치 이탈했을 경우, 아래 경고 문구 alarm_msg 변수에 담기
		if temp_data > high:
			alarm_msg = f"{now} [경고] 상한치 이탈! 현재 온도: {temp_data:.1f}°C / 온도 상한치 기준 {high}°C"
		# 하한치 이탈했을 경우, 아래 경고 문구 alarm_msg 변수에 담기 (elif 사용한 이유는 새로운 조건 추가 위함)
		elif temp_data < low:
			alarm_msg = f"{now} [경고] 하한치 이탈! 현재 온도: {temp_data:.1f}°C / 온도 하한치 기준 {low}°C"

		# 이상 발생했을 경우에만 터미널에 알람 메시지 출력
		if alarm_msg:
			print(alarm_msg)

			# 메인 대시보드 시스템 로그 창에 알람 메시지 출력 
			self.log_signal.emit(alarm_msg)

			# 알람 발생 시 DB 저장
			now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			db_manager.insert_log(alarm_msg, "온도 이탈 발생", now)
			print(f"온도 이탈 발생 DB 저장 완료: {alarm_msg}")

	def m_register_connect(self, client_socket, address, alarm):
		# 온도 이상 알람 발생했을 경우 M 레지스터에 쓰기 테스트
		try:
			success = client_socket.mc_write_m_bit(address, alarm)
		
			# 만약 쓰는데 실패했을 경우 터미널 출력
			if success is not True:
				print(f"온도 알림 데이터 쓰기 실패: {success}")
		
				now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
				# M 레지스터 쓰기 이상 발생 시 로그 출력과 DB로 전달할 경고 메시지 변수
				write_m_bit_alarm_msg = (f"{now} PLC 온도 알림 데이터 쓰기 실패: {success}")
		
				# 메인 대시보드 시스템 로그 창에 M 레지스터 오류 메시지 출력 
				self.log_signal.emit(write_m_bit_alarm_msg)
		
				# 알람 발생 시 DB 저장
				db_manager.insert_log(write_m_bit_alarm_msg, "온도 알림 데이터 쓰기 오류 발생", now)
		
		# 쓰는데 오류 발생한 이유 출력
		except Exception as ex:
			print(f"온도 알림 데이터 쓰기 오류 발생: {ex}")
		
		# M 레지스터 읽기 테스트
		try:
			read_result = client_socket.mc_read_m_bit(address)
		
			# 만약 읽는데 실패했을 경우 터미널 출력
			if not isinstance(read_result, int):
				print(f"온도 알림 데이터 읽기 실패: {read_result}")
		
				now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
				# M 레지스터 읽기 이상 발생 시 로그 출력과 DB로 전달할 경고 메시지 변수
				read_m_bit_alarm_msg = (f"{now} PLC 온도 알림 데이터 읽기 실패: {read_result}")
								
				# 메인 대시보드 시스템 로그 창에 M 레지스터 오류 메시지 출력 
				self.log_signal.emit(read_m_bit_alarm_msg)
								
				# 알람 발생 시 DB 저장
				db_manager.insert_log(read_m_bit_alarm_msg, "읽기 오류 발생", now)
		
		# 읽는데 오류 발생한 이유 출력
		except Exception as ex:
			print(f"읽기 오류 발생: {ex}")

	def run(self):
		client_socket = MySocket()

		with open('src/devices.json', 'r') as f:
			device_data = json.load(f)

		temp_read = device_data['plc_d_register']['temp_read']

		try:
			# 서버 소켓에 접속
			client_socket.connect(self.ip, self.port) #temp_read
			self.communication_signal.emit("통신 연결됨")

			count = 0
			while self.power:
				# PLC 데이터 읽기
				# 1초 주기 가상 온도 데이터 생성 (10.0 ~ 100.0 범위의 난수, 실수 표현위해 uniform 사용)
				temp_data = random.uniform(10.0, 100.0)

				# 난수를 D 레지스터에 쓰기 테스트
				try:
					success = client_socket.mc_write_d_word(temp_read, int(temp_data * 10))

					# 만약 쓰는데 실패했을 경우 터미널 출력
					if success is not True:
						print(f"쓰기 실패: {success}")

						now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

						# D 레지스터 쓰기 이상 발생 시 로그 출력과 DB로 전달할 경고 메시지 변수
						write_d_word_alarm_msg = (f"{now} PLC 온도 데이터 쓰기 실패: {success}")

						# 메인 대시보드 시스템 로그 창에 D 레지스터 오류 메시지 출력 
						self.log_signal.emit(write_d_word_alarm_msg)

						# 알람 발생 시 DB 저장
						db_manager.insert_log(write_d_word_alarm_msg, "쓰기 오류 발생", now)

				# 쓰는데 오류 발생한 이유 출력
				except Exception as ex:
					print(f"쓰기 오류 발생: {ex}")

				# high와 low가 얼마인지 불러오기
				high = float(MySetting.get('limit_high'))
				low = float(MySetting.get('limit_low'))

				# 현재 온도 데이터가 상한치보다 클 경우 M100 알람 울리기
				if temp_data > high:
					self.m_register_connect(client_socket, address= 100, alarm= True)
					self.m_register_connect(client_socket, address= 101, alarm= False)

				# 현재 온도 데이터가 하한치보다 낮을 경우 M101 알람 울리기
				elif temp_data < low:
					self.m_register_connect(client_socket, address= 101, alarm= True)
					self.m_register_connect(client_socket, address= 100, alarm= False)

				else:
					self.m_register_connect(client_socket, address= 100, alarm= False)
					self.m_register_connect(client_socket, address= 101, alarm= False)

				# D 레지스터 읽기 테스트
				try:
					read_result = client_socket.mc_read_d_word(temp_read)

					# 만약 읽는데 실패했을 경우 터미널 출력
					if not isinstance(read_result, int):
						print(f"읽기 실패: {read_result}")

						now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

						# D 레지스터 읽기 이상 발생 시 로그 출력과 DB로 전달할 경고 메시지 변수
						read_d_word_alarm_msg = (f"{now} PLC 온도 데이터 읽기 실패: {read_result}")
						
						# 메인 대시보드 시스템 로그 창에 D 레지스터 오류 메시지 출력 
						self.log_signal.emit(read_d_word_alarm_msg)
						
						# 알람 발생 시 DB 저장
						db_manager.insert_log(read_d_word_alarm_msg, "읽기 오류 발생", now)

				# 읽는데 오류 발생한 이유 출력
				except Exception as ex:
					print(f"읽기 오류 발생: {ex}")

				# 작업 스레드: 가상 온도 데이터 송신 시그널 발생 (main.py로)
				self.temp_signal.emit(temp_data)
				# 매초 온도 검사하여 이상 시 시그널 발생
				self.check_temp_limit(temp_data)

				count += 1
				# 입력 값이 정수 또는 실수인지 확인하기
				if isinstance(temp_data, (int, float)):        

					# 10초가 지났는지 확인하기
					if count >= 10:
						now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

						low = float(MySetting.get('limit_low'))
						high = float(MySetting.get('limit_high'))

						try:    
							db_manager.insert_temperature(now, low, high, round(temp_data, 1))

						except Exception as ex:
							print(f"DB 저장 실패: {ex}")

						# 카운트 리셋
						count = 0

				# 입력 값이 정수 또는 실수가 아니라면 아래 문구 출력
				else:
					print(f"[저장 실패] 잘못된 데이터 수신: 값={temp_data}, 타입={type(temp_data)}")

				# 1초 반복 주기 지연
				time.sleep(1)

		# 에러가 발생하여 수집이 중단되었을 경우 문구 출력, 에러의 구체적인 이유를 ex 변수에 자동으로 담아줌.
		except Exception as ex:
			print(f"수집을 중단합니다. 원인: {ex}")
			self.communication_signal.emit("통신 끊김")

			now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

			# 에러가 발생하여 통신 끊김 발생 시 로그 출력과 DB로 전달할 경고 메시지 변수
			communication_signal_alarm_msg = (f"{now} [안내] 통신 끊김: {ex}")
						
			# 메인 대시보드 시스템 로그 창에 통신 끊김 오류 메시지 출력 
			self.log_signal.emit(communication_signal_alarm_msg)
						
			# 알람 발생 시 DB 저장
			db_manager.insert_log(communication_signal_alarm_msg, "통신 끊김 발생", now)

		finally:
			client_socket.close()

	# 멀티쓰레드를 종료하는 메소드
	def stop(self):
		# 멈추라고 신호 주기 (power/working 플래그 끄기)
		self.power = False
		# 이벤트 루프 종료 요청
		self.quit()
		# 스레드가 진짜 완전히 꺼질 때까지 메인 스레드가 3초 대기
		self.wait(3000)
