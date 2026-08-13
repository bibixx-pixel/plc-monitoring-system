import sys

from PySide6.QtCore import QSettings

# Setting value
# 프로그램의 설정값을 파일 형태로 저장하는 클래스
class MySetting:
    # 1. QSettings 객체 생성
    # 첫 번째 인자: 조직/회사 이름('oneautomation')
    # 두 번째 인자: 애플리케이션 이름('plc_monitoring_system')
    # 이를 기반으로 운영체제(OS) 내에 설정 데이터를 저장할 전용 경로가 만들어짐
    settings = QSettings('oneautomation', 'plc_monitoring_system')

    # 2. 기본값(Default Values) 딕셔너리 정의
    # 저장된 설정 키(Key)가 존재하지 않을 때 반환할 초기값들
    defaults = {
        'set_plc': '192.168.1.10',
        'set_port': '2011',
        'limit_high': '90.0',
        'limit_low': '30.0',
        'db_path' : './plc_monitoring_system.db',
        'table_name' : 'temperature'
    }

    # @classmethod: 클래스 인스턴스(객체) 생성 없이 'MySetting.set()' 형태로 직접 호출 가능하게 함
    # cls: 클래스 자신(MySetting)을 가리키는 매개변수
    @classmethod
    def set(cls, key, value):
        # QSettings의 setValue 메서드를 호출하여 key와 value 형태 데이터 저장
        cls.settings.setValue(key, value)

    @classmethod
    def get(cls, key):
        # QSettings의 value 메서드를 호출하여 설정 데이터 읽기 및 반환
        return cls.settings.value(
            key,                        # 조회할 설정 키(Key)
            cls.defaults[key],          # 해당 키가 없을 경우 사용할 기본값(Default)
            type(cls.defaults[key])     # 읽어올 데이터의 데이터 타입(Data Type) 지정 (str, int, float 등)
        )

    @classmethod
    def restore_defaults(cls):
        # defaults 딕셔너리의 모든 키-값 쌍(Key-Value Pair)을 순회하며 초기값으로 재설정
        for key, value in cls.defaults.items():
            cls.set(key, value)

    # QSettings 데이터를 실제로 저장하고 있는 시스템 파일 경로를 터미널에 출력
    print(settings.fileName())