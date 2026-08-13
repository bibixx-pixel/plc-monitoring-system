import socket

class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(3)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mc_read_d_word(self, address):
    # 1. 패킷 조립 (헤더 + 데이터부)
    # 서브헤더(2), 네트웍(1), PLC(1), IO(2), 국(1), 길이(2), 타이머(2), 커맨드(2), 서브(2), 주소(3), 코드(1), 점수(2)
        packet = (
            b'\x50\x00\x00\xFF\xFF\x03\x00' +           # 헤더 고정부
            (12).to_bytes(2, 'little') +                # 데이터 길이 (12 bytes)
            (16).to_bytes(2, 'little') +                # 타이머
            b'\x01\x04\x00\x00' +                       # 읽기 커맨드 & 서브 커맨드 
            (address).to_bytes(3, 'little') +           # 읽을 주소
            b'\xA8' +                                   # 디바이스 코드 (D)
            (1).to_bytes(2, 'little')                   # 읽을 점수 (1개)
        )

        try:
                self.sock.send(packet)
                response = self.sock.recv(1024)

                # 응답 분석: 종료 코드(9~10번 바이트)가 0이면 정상 데이터(11~12번) 반환
                if len(response) >= 11 and response[9:11] == b'\x00\x00' :
                    return int.from_bytes(response[11:13], 'little', signed = True)
                return f"Error: {response.hex().upper()}" if response else "No Response"
        except Exception as e:
            return f"Conn Error: {e}"

    def mc_write_d_word(self, address, value):
    # 1. 패킷 조립 (헤더 + 데이터부)
    # 데이터 길이 계산: 타이머(2) + 커맨드(2) + 서브(2) + 주소(3) + 코드(1) + 점수(2) + 데이터(2) = 14
        packet = (
            b'\x50\x00\x00\xFF\xFF\x03\x00' +           # 헤더 고정부 (7bytes)
            (14).to_bytes(2, 'little') +                # 데이터 길이 (14 bytes)
            (16).to_bytes(2, 'little') +                # CPU 감시 타이머
            b'\x01\x14\x00\x00' +                       # 쓰기 커맨드(0x1401) & 서브 커맨드
            (address).to_bytes(3, 'little') +           # 기록할 시작 주소
            b'\xA8' +                                   # 디바이스 코드 (D Resister)
            (1).to_bytes(2, 'little') +                 # 기록할 점수 (1개)
            (value) .to_bytes(2, 'little')              # 실제 기록할 값
        )

        try:
                self.sock.send(packet)
                # 응답 수신 (쓰기 성공 시 보통 11바이트 응답)
                response = self.sock.recv(1024)

                # 응답 분석: 종료 코드(9~10번 바이트)가 b'\x00\x00'이면 성공
                if len(response) >= 11 and response[9:11] == b'\x00\x00':
                    return True
                else:
                    return f"Fail (code: {response[9:11].hex().upper() if response else 'None'})"
        except Exception as e:
            return f"Conn Error: {e}"

    def mc_read_m_bit(self, address):
        # 1. 패킷 조립 (헤더 + 데이터부)
        # 서브헤더(2), 네트웍(1), PLC(1), IO(2), 국(1), 길이(2), 타이머(2), 커맨드(2), 서브(2), 주소(3), 코드(1), 점수(2)
            packet = (
                b'\x50\x00\x00\xFF\xFF\x03\x00' +           # 헤더 고정부
                (12).to_bytes(2, 'little') +                # 데이터 길이 (12 bytes)
                (16).to_bytes(2, 'little') +                # 타이머
                b'\x01\x04\x01\x00' +                       # 읽기 커맨드 & 비트 서브 커맨드 (0001)
                (address).to_bytes(3, 'little') +           # 읽을 주소
                b'\x90' +                                   # 디바이스 코드 (M Resister)
                (1).to_bytes(2, 'little')                   # 읽을 점수 (1개)
            )
    
            try:
                    self.sock.send(packet)
                    response = self.sock.recv(1024)
    
                    # 응답 분석: 종료 코드(9~10번 바이트)가 0이면 정상 데이터(11~12번) 반환
                    if len(response) >= 11 and response[9:11] == b'\x00\x00' :
                        # 응답의 11번째 바이트 값이 0x10이면 True, 0x00이면 False으로 판별해서 반환하기
                        return 1 if response[11] == 0x10 or response[11] == 0x01 else 0
                    return f"Error: {response.hex().upper()}" if response else "No Response"
            except Exception as e:
                return f"Conn Error: {e}"
    
    def mc_write_m_bit(self, address, value):
        # 1(ON)일 때는 b'\x10', 0(OFF)일 때는 b'\x00' 데이터 1바이트 전달
        # mc_write_m_bit 함수의 매개변수 value로 들어오는 값(True/False 또는 1/0)을 MC 프로토콜 규격에 맞는 바이너리 데이터 형태(b'\x10' 또는 b'\x00')로 변환해 주어야 하기 때문
        if value:
            bit_data = b'\x10'
        else:
            bit_data = b'\x00'

        # 1. 패킷 조립 (헤더 + 데이터부)
        # 데이터 길이 계산: 타이머(2) + 커맨드(2) + 서브(2) + 주소(3) + 코드(1) + 점수(2) + 데이터(1) = 13
        packet = (
            b'\x50\x00\x00\xFF\xFF\x03\x00' +           # 헤더 고정부 (7bytes)
            (13).to_bytes(2, 'little') +                # 데이터 길이 (14 bytes)
            (16).to_bytes(2, 'little') +                # CPU 감시 타이머
            b'\x01\x14\x01\x00' +                       # 쓰기 커맨드 & 비트 서브 커맨드 (0001)
            (address).to_bytes(3, 'little') +           # 기록할 시작 주소
            b'\x90' +                                   # 디바이스 코드 (M Resister)
            (1).to_bytes(2, 'little') +                 # 기록할 점수 (1개)
            bit_data                                    # 실제 기록할 값 (1바이트)
        )
    
        try:
            self.sock.send(packet)
            # 응답 수신 (쓰기 성공 시 보통 11바이트 응답)
            response = self.sock.recv(1024)
    
            # 응답 분석: 종료 코드(9~10번 바이트)가 b'\x00\x00'이면 성공
            if len(response) >= 11 and response[9:11] == b'\x00\x00':
                return True
            else:
                return f"Fail (code: {response[9:11].hex().upper() if response else 'None'})"
        except Exception as e:
            return f"Conn Error: {e}"
        
    def close(self): 
        self.sock.close()
    
if __name__ == "__main__":
    # 상자 만들고 접속하기.
    my_plc = MySocket()
    my_plc.connect("192.168.1.10", 2011)

    # 읽기 테스트
    read_result = my_plc.mc_read_d_word(100)
    print(f"읽기 결과: {read_result}")

    # 쓰기 테스트
    success = my_plc.mc_write_d_word(100, 1234)
    print(f"쓰기 결과: {success}")

    print("-"*35)
    
    if success is True:
        print("결과: PLC 데이터 쓰기 성공!")
    else:
        print(f"결과: {success}")
    print("-"*35)