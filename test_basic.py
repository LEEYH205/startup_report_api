#!/usr/bin/env python3
"""
기본 테스트 파일
CI/CD 파이프라인에서 사용
"""

import os
import sys
import unittest

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.abspath("."))


class TestBasic(unittest.TestCase):
    """기본 테스트 클래스"""

    def test_imports(self):
        """필요한 모듈들이 정상적으로 import 되는지 테스트"""
        try:
            import app  # noqa: F401

            self.assertTrue(True, "app 모듈 import 성공")
        except ImportError as e:
            self.fail(f"app 모듈 import 실패: {e}")

    def test_requirements(self):
        """requirements.txt에 명시된 패키지들이 설치되어 있는지 테스트"""
        required_packages = ["flask", "flask_cors", "flask_restx", "pandas"]

        for package in required_packages:
            try:
                __import__(package)
                self.assertTrue(True, f"{package} 패키지 설치됨")
            except ImportError:
                self.fail(f"{package} 패키지가 설치되지 않음")

    def test_data_files(self):
        """필요한 데이터 파일들이 존재하는지 테스트"""
        required_files = [
            "data/지역별_도소매별_가맹점수_현황.csv",
            "data/지역별_서비스별_가맹점수_현황.csv",
            "data/지역별_외식별_가맹점수_현황.csv",
        ]

        for file_path in required_files:
            self.assertTrue(os.path.exists(file_path), f"데이터 파일이 존재하지 않음: {file_path}")


if __name__ == "__main__":
    unittest.main()
