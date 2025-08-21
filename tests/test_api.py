#!/usr/bin/env python3
"""
API 테스트 파일
Flask 애플리케이션의 엔드포인트들을 테스트
"""

import json
import os
import sys
import unittest

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


class TestAPI(unittest.TestCase):
    """API 테스트 클래스"""

    def setUp(self):
        """테스트 설정"""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        """헬스체크 엔드포인트 테스트"""
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")

    def test_chart_specs_endpoint(self):
        """차트 사양 엔드포인트 테스트"""
        response = self.app.get("/api/charts/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("data", data)

    def test_chart_data_endpoint(self):
        """차트 데이터 엔드포인트 테스트"""
        response = self.app.get("/api/data/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("line_chart_data", data)
        self.assertIn("bar_chart_data", data)

    def test_invalid_chart_data(self):
        """존재하지 않는 차트 데이터 요청 테스트"""
        response = self.app.get("/api/charts/nonexistent_chart")
        self.assertEqual(response.status_code, 404)

    def test_cors_headers(self):
        """CORS 헤더 테스트"""
        response = self.app.get("/health")
        self.assertIn("Access-Control-Allow-Origin", response.headers)


if __name__ == "__main__":
    unittest.main()
