#!/usr/bin/env python3
"""
차트 API 서버 테스트 클라이언트
API 엔드포인트들이 올바르게 작동하는지 테스트합니다.
"""

import json

import requests

BASE_URL = "http://localhost:5001"


def test_api_endpoints():
    """모든 API 엔드포인트를 테스트"""

    print("🚀 차트 API 서버 테스트 시작\n")

    # 1. 루트 엔드포인트 테스트
    print("1. 루트 엔드포인트 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data['message']}")
            print(f"   📋 사용 가능한 엔드포인트: {list(data['endpoints'].keys())}")
        else:
            print(f"   ❌ 실패: HTTP {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        return False
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        return False

    # 2. 모든 차트 사양 테스트
    print("\n2. 모든 차트 사양 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/api/charts")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {len(data)} 개의 차트 라이브러리 지원")
            for lib in data.keys():
                print(f"      - {lib}: {len(data[lib])} 개 차트")
        else:
            print(f"   ❌ 실패: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")

    # 3. 특정 라이브러리 차트 테스트
    print("\n3. 특정 라이브러리 차트 테스트...")
    libraries = ["vega_lite", "echarts", "plotly", "chartjs"]

    for lib in libraries:
        try:
            response = requests.get(f"{BASE_URL}/api/charts/{lib}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {lib}: {len(data)} 개 차트")
            else:
                print(f"   ❌ {lib}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {lib}: {e}")

    # 4. 특정 차트 타입 테스트
    print("\n4. 특정 차트 타입 테스트...")
    chart_types = ["line", "bar"]

    for lib in libraries:
        for chart_type in chart_types:
            try:
                response = requests.get(f"{BASE_URL}/api/charts/{lib}/{chart_type}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ {lib}/{chart_type}: 성공")
                else:
                    print(f"   ❌ {lib}/{chart_type}: HTTP {response.status_code}")
            except Exception as e:
                print(f"   ❌ {lib}/{chart_type}: {e}")

    # 5. 데이터 엔드포인트 테스트
    print("\n5. 데이터 엔드포인트 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/api/data")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {len(data)} 개 데이터셋")
            for key in data.keys():
                if isinstance(data[key], dict):
                    print(f"      - {key}: {len(data[key])} 개 항목")
                else:
                    print(f"      - {key}: {data[key]}")
        else:
            print(f"   ❌ 실패: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")

    # 6. 헬스 체크 테스트
    print("\n6. 헬스 체크 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data['status']}")
        else:
            print(f"   ❌ 실패: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")

    print("\n🎯 API 테스트 완료!")
    return True


def test_chart_spec_validation():
    """차트 사양이 올바른 형식인지 검증"""

    print("\n🔍 차트 사양 검증 테스트...")

    try:
        # ECharts 라인 차트 사양 검증
        response = requests.get(f"{BASE_URL}/api/charts/echarts/line")
        if response.status_code == 200:
            data = response.json()

            # 필수 필드 확인
            required_fields = ["title", "xAxis", "yAxis", "series"]
            missing_fields = [field for field in required_fields if field not in data]

            if not missing_fields:
                print("   ✅ ECharts 라인 차트 사양 검증 통과")
                print(f"      - 제목: {data['title']['text']}")
                print(f"      - X축: {data['xAxis']['name']}")
                print(f"      - Y축: {data['xAxis']['name']}")
                print(f"      - 시리즈: {len(data['series'])} 개")
            else:
                print(
                    f"   ❌ ECharts 라인 차트 사양 검증 실패: 누락된 필드 {missing_fields}"
                )
        else:
            print(
                f"   ❌ ECharts 라인 차트 사양 가져오기 실패: HTTP {response.status_code}"
            )

    except Exception as e:
        print(f"   ❌ 차트 사양 검증 오류: {e}")


def save_chart_specs_to_files():
    """API에서 받은 차트 사양을 파일로 저장"""

    print("\n💾 차트 사양을 파일로 저장...")

    # 출력 디렉토리 생성
    import os

    output_dir = "api_chart_specs"
    os.makedirs(output_dir, exist_ok=True)

    libraries = ["vega_lite", "echarts", "plotly", "chartjs"]
    chart_types = ["line", "bar"]

    for lib in libraries:
        for chart_type in chart_types:
            try:
                response = requests.get(f"{BASE_URL}/api/charts/{lib}/{chart_type}")
                if response.status_code == 200:
                    data = response.json()
                    filename = f"{output_dir}/{lib}_{chart_type}_chart.json"

                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

                    print(f"   ✅ {filename} 저장 완료")
                else:
                    print(f"   ❌ {lib}/{chart_type}: HTTP {response.status_code}")
            except Exception as e:
                print(f"   ❌ {lib}/{chart_type}: {e}")

    print(f"\n📁 모든 차트 사양이 '{output_dir}' 디렉토리에 저장되었습니다.")


if __name__ == "__main__":
    print("=== 차트 API 서버 테스트 클라이언트 ===\n")

    # 서버가 실행 중인지 확인
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 서버가 실행 중입니다.")
        else:
            print("❌ 서버 응답이 비정상입니다.")
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다.")
        print("💡 다음 명령어로 서버를 시작하세요:")
        print("   cd 08_chart_api_server")
        print("   python app.py")
        exit(1)

    # API 테스트 실행
    if test_api_endpoints():
        # 차트 사양 검증
        test_chart_spec_validation()

        # 차트 사양을 파일로 저장
        save_chart_specs_to_files()

        print("\n🎉 모든 테스트가 완료되었습니다!")
        print("\n📋 다음 단계:")
        print("1. FE에서 API 엔드포인트를 호출하여 차트 사양을 가져오세요")
        print("2. 받은 사양을 사용하여 원하는 차트 라이브러리로 차트를 렌더링하세요")
        print("3. 예시: GET /api/charts/echarts/line")
    else:
        print("\n❌ API 테스트에 실패했습니다.")
