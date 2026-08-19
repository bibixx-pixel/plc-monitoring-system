import sys
from datetime import time, datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QFont
import pyqtgraph as pg

from ui_main import Ui_MainWindow
from src.setting_manager import MySetting
from src.plc_worker import Worker
import src.db_manager as db_manager

# 메인 윈도우 클래스 정의
class MainWindow(QMainWindow):
    # 메인 윈도우 창이 생성될 때 가장 먼저 실행되는 함수
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("plc monitoring system")
        self.worker = None

        # 메인 대시보드 통신 상태 디폴트 값 '통신 대기중' 회색으로 고정
        self.ui.lbl_status.setText("통신 대기중")
        self.ui.lbl_status.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 20px;
            }
        """)

        # 실시간 온도 추이 그래프 온도 데이터 (x축 = 데이터 측정 순서 / y축 = 현재 온도값)
        self.x_data = []  
        self.y_data = []

        # 실시간 온도 추이 그래프 디자인
        self.ui.graph_temperature.setBackground('k')
        self.ui.graph_temperature.setTitle("실시간 온도 추이 그래프")
        self.ui.graph_temperature.setLabel("left", "현재 온도값")
        self.ui.graph_temperature.setLabel("bottom", "데이터 측정 순서")
        self.ui.graph_temperature.addLegend(offset = (1, 1), size = (10, 40), labelTextSize = '7pt', horSpacing = 5, verSpacing = 0)
        self.ui.graph_temperature.showGrid(x=True, y=True)
        self.ui.graph_temperature.setRange(xRange= [0, 100], yRange = [-100, 100])

        # plot (온도 그래프 선 색상 및 두께 세팅 값) 
        self.line = self.ui.graph_temperature.plot(y=self.y_data, pen=pg.mkPen(width=2, color='r'), name="현재 온도값")

        # QDoubleSpinBox 범위 설정 (최/하)
        self.ui.set_high.setRange(-100.0, 100.0)
        self.ui.set_low.setRange(-100.0, 100.0)

        # 조회 온도 변화 추이 그래프 온도 데이터 (x축 = 데이터 측정 순서 / y축 = 조회 시간 기준 온도값, 평균 온도값)
        self.inquiry_x_data = []  
        self.inquiry_y_data = []
        self.inquiry_y_avg_data = []
        self.date_list = []

        # 조회 온도 변화 추이 그래프 디자인
        self.ui.graph_inquiry.setBackground('k')
        self.ui.graph_inquiry.setTitle("조회 온도 변화 추이 그래프")
        self.ui.graph_inquiry.setLabel("left", "온도 리스트")
        self.ui.graph_inquiry.setLabel("bottom", "데이터 측정 순서")
        self.ui.graph_inquiry.addLegend(offset = (1, 1), size = (10, 40), labelTextSize = '7pt', horSpacing = 5, verSpacing = 0)
        self.ui.graph_inquiry.showGrid(x=True, y=True)

        # plot (온도 그래프 선 색상 및 두께 세팅 값) 
        self.line_inquiry = self.ui.graph_inquiry.plot(y=self.inquiry_y_data, pen=pg.mkPen(width=2, color='r'), name="실측 온도 리스트")
        self.line_inquiry_avg = self.ui.graph_inquiry.plot(y=self.inquiry_y_data, pen=pg.mkPen(width=2, color='b'), name="평균값")

        # 십자선 만드는 코드
        self.crosshair_v = pg.InfiniteLine(angle=90, movable=False)
        self.crosshair_h = pg.InfiniteLine(angle=0, movable=False)
        self.ui.graph_inquiry.addItem(self.crosshair_v, ignoreBounds=True)
        self.ui.graph_inquiry.addItem(self.crosshair_h, ignoreBounds=True)

        # 조회 화면 마우스 커서 올리면 나오는 텍스트 디자인 설정
        self.cursor_label = pg.TextItem(text="", color="w", anchor=(0, 1))
        self.ui.graph_inquiry.addItem(self.cursor_label, ignoreBounds=True)

        # 마우스 이동 이벤트를 조절하기 위한 연결 진행
        self.proxy = pg.SignalProxy(
            self.ui.graph_inquiry.scene().sigMouseMoved,
            rateLimit=60,
            slot=self.mouse_moved,
        )

        # 버튼 클릭시 슬롯 함수 연결
        self.ui.inquiry_btn_search.clicked.connect(self.update_inquiry_data)
        self.ui.set_btn_save.clicked.connect(self.save_temperature_settings) 
        self.ui.set_btn_save_2.clicked.connect(self.save_plc_settings) 
        self.ui.set_btn_save_3.clicked.connect(self.save_db_settings) 
        self.ui.set_btn_find.clicked.connect(self.find_db_settings)
        self.ui.connect_pushButton.clicked.connect(self.communication_connect) 
        self.ui.disconnect_pushButton.clicked.connect(self.communication_disconnect)

        # 프로그램 실행하자마자 시스템 로그 창 타이핑 및 마우스 커서 비활성화
        self.ui.txt_system_log.setReadOnly(True)

        # 프로그램 실행하자마자 조회 버튼 비활성화
        self.ui.groupBox.setDisabled(True)
        self.ui.groupBox_2.setDisabled(True)
        self.ui.groupBox_3.setDisabled(True)

        # 프로그램 실행하자마자 설정 화면 비활성화
        self.ui.groupBox_4.setDisabled(True)
        self.ui.groupBox_5.setDisabled(True)
        self.ui.groupBox_6.setDisabled(True)

        # 프로그램 실행하자마자 이전 값 불러오기
        self.load_settings()

        # 프로그램 실행하자마자 db 초기화해주기
        db_manager.init_db()

    # 메인 대시보드 통신 연결 함수 (연결 버튼 전용 - 입력창 검사, 팝업창 출력, 검증 성공/실패 시 UI 상태 변경)
    def communication_connect(self):
        # 설정 화면에서 저장한 PLC 통신 설정 불러오기
        ip = MySetting.get('set_plc')
        port = int(MySetting.get('set_port'))

        # 각각 오브젝트와 연결하여 현재 적혀 있는 문자열 읽어오기
        ip_text = self.ui.search_ip.text()
        port_text = self.ui.search_port.text()

        # ip 입력창이 빈 값인지 확인하고, 비어있다면 팝업창 뜨게하기
        if ip_text == '':
            # 스레드가 실행 중이면 정지 (실행되고 있는지 확인)
            if self.worker and self.worker.isRunning():
                # 정지하고 완전히 끝날 때까지 대기
                self.worker.stop()

            self.update_communication_status("통신 끊김")
            print("입력되지 않았습니다. 다시 IP를 입력해주세요.")
            QMessageBox.information(self, "경고", "입력되지 않았습니다. 다시 IP를 입력해주세요.")
            return

        # port 입력창이 빈 값인지 확인하고, 비어있다면 팝업창 뜨게하기
        if port_text == '':
            # 스레드가 실행 중이면 정지 (실행되고 있는지 확인)
            if self.worker and self.worker.isRunning():
                # 정지하고 완전히 끝날 때까지 대기
                self.worker.stop()

            self.update_communication_status("통신 끊김")
            print("입력되지 않았습니다. 다시 port를 입력해주세요.")
            QMessageBox.information(self, "경고", "입력되지 않았습니다. 다시 port를 입력해주세요.")
            return

        # ip와 ip_text를 비교하여 일치하지 않는다면 팝업창 뜨게하기
        elif ip_text != ip:
            # 스레드가 실행 중이면 정지 (실행되고 있는지 확인)
            if self.worker and self.worker.isRunning():
                # 정지하고 완전히 끝날 때까지 대기
                self.worker.stop()

            self.update_communication_status("통신 끊김")
            print("ip 및 port 번호가 일치하지 않습니다.\n다시 IP 및 port를 입력해주세요.")
            QMessageBox.information(self, "경고", "ip 및 port 번호가 일치하지 않습니다.\n다시 IP 및 port를 입력해주세요.")
            return

        # port 번호가 숫자가 아니라면 팝업창 뜨게하기
        elif not port_text.isdigit():
            # 스레드가 실행 중이면 정지 (실행되고 있는지 확인)
            if self.worker and self.worker.isRunning():
                # 정지하고 완전히 끝날 때까지 대기
                self.worker.stop()

            self.update_communication_status("통신 끊김")
            print("ip 및 port 번호가 일치하지 않습니다.\n다시 IP 및 port를 입력해주세요.")
            QMessageBox.information(self, "경고", "ip 및 port 번호가 일치하지 않습니다.\n다시 IP 및 port를 입력해주세요.")
            return

        # port와 port_text를 비교하여 일치하지 않는다면 팝업창 뜨게하기
        elif int(port_text) != port:
            # 스레드가 실행 중이면 정지 (실행되고 있는지 확인)
            if self.worker and self.worker.isRunning():
                # 정지하고 완전히 끝날 때까지 대기
                self.worker.stop()

            self.update_communication_status("통신 끊김")
            print("ip 및 port 번호가 일치하지 않습니다.\n다시 IP 및 port를 입력해주세요.")
            QMessageBox.information(self, "경고", "ip 및 port 번호가 일치하지 않습니다.\n다시 IP 및 port를 입력해주세요.")
            return

        # 위 조건이 충족되지 않는다면 터미널에 입력된 IP 및 Port 번호 출력하기
        else:    
            print(f"입력된 IP: {ip_text}, Port: {port_text}")
            self.start_work(ip_text, int(port_text))

    # 메인 대시보드 통신 연결 해제 버튼 함수 
    def communication_disconnect(self):
        # 스레드가 실행 중이면 정지 (실행되고 있는지 확인)
        if self.worker and self.worker.isRunning():
            # 정지하고 완전히 끝날 때까지 대기
            self.worker.stop()

            # 조회 버튼 비활성화
            self.ui.groupBox.setDisabled(True)
            self.ui.groupBox_2.setDisabled(True)
            self.ui.groupBox_3.setDisabled(True)

            # 프로그램 실행하자마자 설정 화면 비활성화
            self.ui.groupBox_4.setDisabled(True)
            self.ui.groupBox_5.setDisabled(True)
            self.ui.groupBox_6.setDisabled(True)

            self.update_communication_status("통신 끊김")

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 에러가 발생하여 통신 끊김 발생 시 로그 출력과 DB로 전달할 경고 메시지 변수
            communication_signal_alarm_msg = (f"{now} [안내] 사용자에 의해 PLC 통신 연결이 해제되었습니다.")
                        
            # 메인 대시보드 시스템 로그 창에 통신 끊김 오류 메시지 출력 
            self.update_system_log(communication_signal_alarm_msg)
                        
            # 알람 발생 시 DB 저장
            db_manager.insert_log(communication_signal_alarm_msg, "통신 끊김 발생", now)

    # 스레드 신호 수신 시 실행되는 함수
    def update_communication_status(self, status):
        if status == "통신 연결됨":
            # 조회 버튼 활성화
            self.ui.groupBox.setEnabled(True)
            self.ui.groupBox_2.setEnabled(True)
            self.ui.groupBox_3.setEnabled(True)

            # 프로그램 실행하자마자 설정 화면 활성화
            self.ui.groupBox_4.setEnabled(True)
            self.ui.groupBox_5.setEnabled(True)
            self.ui.groupBox_6.setEnabled(True)

            self.ui.lbl_status.setText("통신 연결됨")
            self.ui.lbl_status.setStyleSheet("""
                QLabel {
                    color: #ADFF2F;
                    font-size: 20px;
                }
            """)

        elif status == "통신 끊김":
            # 조회 버튼 비활성화
            self.ui.groupBox.setDisabled(True)
            self.ui.groupBox_2.setDisabled(True)
            self.ui.groupBox_3.setDisabled(True)

            # 프로그램 실행하자마자 설정 화면 비활성화
            self.ui.groupBox_4.setDisabled(True)
            self.ui.groupBox_5.setDisabled(True)
            self.ui.groupBox_6.setDisabled(True)

            self.ui.lbl_status.setText("통신 끊김")
            self.ui.lbl_status.setStyleSheet("""
                QLabel {
                    color: #FF0000;
                    font-size: 20px;
                }
            """)
        
    # 조회 온도 변화 추이 그래프에 마우스 올리면 나오는 십자선 관련 함수       
    def mouse_moved(self, e):
        # 전달받은 마우스 이벤트 정보(e)에서 첫 번째 값인 '현재 마우스 좌표'를 추출
        pos = e[0]

        # 마우스 좌표(pos)가 그래프 위젯 화면 영역 내부에 위치하는지 확인
        if self.ui.graph_inquiry.sceneBoundingRect().contains(pos):
            # 픽셀 단위의 화면 좌표를 그래프의 실제 데이터(X, Y) 좌표로 변환
            mouse_point = self.ui.graph_inquiry.getPlotItem().vb.mapSceneToView(pos)

            # X축 데이터 좌표를 인덱스로 사용하기 위해 정수(int)로 변환
            idx = int(mouse_point.x())

            # 인덱스(idx)가 데이터 리스트의 전체 개수 범위 내에 있는지 확인
            if 0 <= idx < len(self.inquiry_y_data):
                # 해당 인덱스에 해당하는 날짜/시간 데이터 가져오기
                current_date = self.date_list[idx]

                # 수직 세로선의 X축 위치를 현재 인덱스 위치로 이동
                self.crosshair_v.setPos(idx)

                # 수평 가로선의 Y축 위치를 현재 인덱스의 실측 온도 값 위치로 이동
                self.crosshair_h.setPos(self.inquiry_y_data[idx])

                # 텍스트 라벨에 순번, 일시, 실측 온도, 평균 온도 값을 소수점 둘째 자리까지 표시
                self.cursor_label.setText(
                    f"순번 = {idx}, 일시 = {current_date}, 실측 온도 = {self.inquiry_y_data[idx]:.2f}, 평균 온도 = {self.inquiry_y_avg_data[idx]:.2f}"
                )

                # 텍스트 라벨의 위치를 (인덱스, 실측 온도) 좌표로 설정
                self.cursor_label.setPos(idx, self.inquiry_y_data[idx])

                # 텍스트 라벨의 위치를 (인덱스, 평균 온도) 좌표로 재설정 (위 위치를 덮어씀)
                self.cursor_label.setPos(idx, self.inquiry_y_avg_data[idx])

    # 조회 화면 데이터 업데이트 함수
    def update_inquiry_data(self):
        # 현재 선택된 시간(시스템 시간)을 가져오기
        start_date = self.ui.dt_start.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        end_date = self.ui.dt_end.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        print(start_date, end_date)

        # 설정 화면에서 테이블명을 바꿀 수 있도록 MySetting.get('table_name')으로 불러온 변수 정의해주기
        table_name =  MySetting.get('table_name')

        # db_manager 파일에서 조회한 시작 및 종료 일자 가져오기
        rows = db_manager.get_date_data(table_name, start_date, end_date)

        # 리스트에서 실측 온도만 뽑아오기 
        temp_list = [float(row[3]) for row in rows]

        # 리스트에서 날짜만 뽑아오기 
        self.date_list = [str(row[4][5:16]) for row in rows]

        if len(temp_list) == 0:
            print("조회된 데이터가 없습니다.")
            QMessageBox.information(self, "안내", "조회된 데이터가 없습니다.")
            return
        
        else:
            avg = sum(temp_list) / len(temp_list)
            high = max(temp_list)
            low = min(temp_list)
     
            # 터미널에 평균, 상한, 하한 텍스트 출력
            print(f"{avg:.2f} ℃")
            print(f"{high:.2f} ℃")
            print(f"{low:.2f} ℃")

            # 실제 조회 화면에서 텍스트로 출력
            self.ui.inquiry_avg.setText(f"{avg:.2f} ℃")
            self.ui.inquiry_high.setText(f"{high:.2f} ℃")
            self.ui.inquiry_low.setText(f"{low:.2f} ℃")

        # x축 최대 눈금 제한
        xMAXTickN = 6

        # 조회 화면 그래프 x축 길이대로 가져오기 / y축 실측 온도 리스트 / y축 평균 온도 리스트 복사해서 가져오기 
        self.inquiry_x_data = list(range(len(temp_list)))  
        self.inquiry_y_data = temp_list
        self.inquiry_y_avg_data = [avg for x in temp_list]

        # 전체 위치와 날짜를 짝지은 원본 리스트(x_ticks) 만들기
        x_ticks = [(i, self.date_list[i]) for i in self.inquiry_x_data]

        # x축 객체를 가져오기
        x_axis = self.ui.graph_inquiry.getAxis('bottom')
        # 축 객체의 형태(x_ticks 위치와 날짜) 리스트를 전달해주기
        x_axis.setTicks([x_ticks])

        # 겹치는 x축 레이블 자동 숨김 옵션 켜기
        x_axis.hideOverlappingLabels = True

        # 15개로 솎아낸 데이터 담아둘 리스트 준비라기
        xticklist = []

        # 데이터가 15개보다 많으면 솎아내기
        if len(x_ticks) > xMAXTickN:
            # 데이터를 개수대로 나눌 때, 딱 떨어지는 정수 간격을 담아둘 변수 생성
            tick_interval = len(x_ticks)//xMAXTickN
            # x_ticks 리스트에서 몇 번째 데이터부터 인덱싱할지 결정하는 초깃값 인덱스 변수
            tick_key = 0

            # 설정한 최대 눈금 개수(xMAXTickN + 1)만큼 반복문 실행
            for i in range(xMAXTickN+1):
                # 1. 현재 tick_key(인덱스 위치)에 해당하는 (순번, 날짜) 데이터를 가져와 변수(xticklist)에 추가
                xticklist.append(x_ticks[tick_key])
                # 2. 다음 눈금을 뽑기 위해 계산해 둔 정수 간격(tick_interval)만큼 인덱스 위치를 이동
                tick_key += tick_interval

                # Tick키가 리스트 범위를 넘지 않도록 조건문 추가
                # 이동한 인덱스(tick_key)가 전체 데이터 개수 이상이 되면
                if tick_key >= len(x_ticks):
                    # 리스트의 맨 마지막 데이터 인덱스(전체 개수 - 1)로 강제 고정
                    tick_key = len(x_ticks)-1

            # 솎아낸 리스트를 x축에 적용        
            x_axis.setTicks([xticklist])

        # 데이터가 15개 이하면 솎아낼 필요 없이 원본 그대로 적용    
        else:
            x_axis.setTicks([x_ticks])

        # 실제 조회 화면에서 그래프 갱신
        self.line_inquiry.setData(self.inquiry_x_data, self.inquiry_y_data)
        self.line_inquiry_avg.setData(self.inquiry_x_data, self.inquiry_y_avg_data)

    def get_data(self, temp_data):
        # X축 순번(0, 1, 2...) 데이터 추가
        self.x_data.append(len(self.x_data))

        # Y축 실측 온도 데이터 추가
        self.y_data.append(temp_data)

        # 선 객체(PlotDataItem)의 setData를 활용해 차트 실시간 갱신
        self.line.setData(self.x_data, self.y_data)

    # 설정 화면에서 온도 상/하한 값 설정 저장하기
    def save_temperature_settings(self):
        buttonReply = QMessageBox.question(
        self, '저장', "저장하시겠습니까?", 
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.No
        )

        if buttonReply == QMessageBox.Yes:
            # 화면에서 읽어온 값을 창이 켜져 있는 동안 기억할 수 있게 클래스 변수(self)에 저장
            self.limit_high = self.ui.set_high.value()
            self.limit_low = self.ui.set_low.value()
        
            # 값이 잘 들어왔는지 임시로 확인하기 위한 터미널 출력 코드
            print(f"상한: {self.limit_high}, 하한: {self.limit_low}")

            # 설정 이름표(Key)와 실제 값(Value)을 MySetting 함수에 전달하여 저장 요청
            MySetting.set('limit_high', self.limit_high)
            MySetting.set('limit_low', self.limit_low)

            # setText는 글자만 받으므로 f-string을 써서 문자열로 바꿔줌.
            self.ui.dash_high.setText(f"{self.limit_high} ℃")
            self.ui.dash_low.setText(f"{self.limit_low} ℃")

        else:
            pass

    # 온도 상/하한치 이탈 감지 함수
    def check_temperature_limit(self, temp_data):
        high = float(MySetting.get('limit_high'))
        low = float(MySetting.get('limit_low'))

        if temp_data > high:
            print(f"[경고] 상한치 이탈! 현재 온도: {temp_data:.1f}°C / 온도 상한치 기준 {high}°C")
        elif temp_data < low:
            print(f"[경고] 하한치 이탈! 현재 온도: {temp_data:.1f}°C / 온도 하한치 기준 {low}°C")

        # 대시보드 화면의 글자 라벨에 값 띄우기.
        self.ui.dash_current.setText(f"{temp_data:.1f}°C")
        # setText는 글자만 받으므로 f-string을 써서 문자열로 바꿔줌.
        self.ui.dash_high.setText(f"{high} ℃")
        self.ui.dash_low.setText(f"{low} ℃")

    def update_system_log(self, alarm_msg):
        # 대시보드 화면의 시스템 로그창에 로그 띄우기
        self.ui.txt_system_log.append(alarm_msg) 

    # 메인 스레드
    def start_work(self, ip = "192.168.1.10", port = 2011):
        # 스레드가 실행 중이면 정지 (실행되고 있는지 확인)
        if self.worker and self.worker.isRunning():
                # 정지하고 완전히 끝날 때까지 대기
                self.worker.stop()

        # 새 스레드 생성
        self.worker = Worker(ip, port)

        # 시그널을 받아 통신 연결 (통신 연결, 통신 끊김)
        self.worker.communication_signal.connect(self.update_communication_status)

        # 시그널을 받아 UI 갱신 (온도 이탈 감지 연결)
        self.worker.temp_signal.connect(self.check_temperature_limit)

        # 시그널을 받아 UI 갱신 (온도 이탈 감지 후 시스템 로그와 연결)
        self.worker.log_signal.connect(self.update_system_log)

        # 실시간 차트 그리기 시그널 연결
        self.worker.temp_signal.connect(self.get_data)

        # 스레드 시작
        self.worker.start()

    # 설정 화면에서 plc ip 및 port 번호 설정 저장하기
    def save_plc_settings(self):
        buttonReply = QMessageBox.question(
        self, '저장', "저장하시겠습니까?", 
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.No
        )

        if buttonReply == QMessageBox.Yes:
            # 화면에서 읽어온 값을 창이 켜져 있는 동안 기억할 수 있게 클래스 변수(self)에 저장
            self.set_plc = self.ui.set_plc_ip.text()
            self.set_port = self.ui.set_plc_port.text()

            # 값이 잘 들어왔는지 임시로 확인하기 위한 터미널 출력 코드
            print(f"plc ip: {self.set_plc}, port: {self.set_port}") 

            # 설정 이름표(Key)와 실제 값(Value)을 MySetting 함수에 전달하여 저장 요청
            MySetting.set('set_plc', self.set_plc)
            MySetting.set('set_port', self.set_port)

        else:
            pass

    def load_settings(self):
        # PLC 통신 설정 불러오기 (프로그램 종료 후 재부팅 시 글자 불러오기)
        ip_val = MySetting.get('set_plc')
        port_val = MySetting.get('set_port')

        # PLC IP 및 Port 불러오기
        self.ui.set_plc_ip.setText(ip_val)
        self.ui.set_plc_port.setText(port_val)

        # 온도 상/하한 설정값 불러오기 (프로그램 종료 후 재부팅 시 글자 불러오기)
        high_val = MySetting.get('limit_high')
        low_val = MySetting.get('limit_low')

        # DB 설정값 불러오기 (프로그램 종료 후 재부팅 시 글자 불러오기)
        db_val = MySetting.get('db_path')
        table_val = MySetting.get('table_name')

        # DB 파일 경로 및 table명 불러오기
        self.ui.set_db_path.setText(db_val)
        self.ui.set_db_table.setText(table_val)

        # 설정 화면의 숫자 조절 칸에 불러온 값 세팅
        # setValue는 숫자를 받으므로 오류 방지를 위하여 float()로 감싸줌.
        self.ui.set_high.setValue(float(high_val))
        self.ui.set_low.setValue(float(low_val)) 

        # 대시보드 화면의 글자 라벨에 값 띄우기
        # setText는 글자만 받으므로 f-string을 써서 문자열로 바꿔줌.
        self.ui.dash_high.setText(f"{high_val} ℃")
        self.ui.dash_low.setText(f"{low_val} ℃")

    def find_db_settings(self):
        # 데이터베이스(DB) 파일 경로 찾기
        # 반환되는 튜플의 첫 번째 값(경로)은 file에, 두 번째 값(선택한 필터 문자열)은 check 변수에 나누어 담음.
        file, check = QFileDialog.getOpenFileName(self, 'DB 파일 선택', "./", "All Files (*);;Text Files (*.txt)")

        # check 변수에 값이 존재할 때(즉, 사용자가 취소하지 않고 정상적으로 파일을 선택했을 때)만 setText()를 수행하므로, 취소 버튼을 눌렀을 때 기존 입력창 값이 지워지는 것을 방지해 줌.
        if check:
            self.ui.set_db_path.setText(file)

    # 설정 화면에서 DB 파일 및 테이블 값 설정 저장하기
    def save_db_settings(self):
        buttonReply = QMessageBox.question(
        self, '저장', "저장하시겠습니까?", 
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.No
        )

        if buttonReply == QMessageBox.Yes:
            # 화면에서 읽어온 값을 창이 켜져 있는 동안 기억할 수 있게 클래스 변수(self)에 저장
            self.db_path = self.ui.set_db_path.text()
            self.db_table = self.ui.set_db_table.text()

            # 설정 이름표(Key)와 실제 값(Value)을 MySetting 함수에 전달하여 저장 요청
            MySetting.set('db_path', self.db_path)
            MySetting.set('table_name', self.db_table)

        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 