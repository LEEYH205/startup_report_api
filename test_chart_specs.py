#!/usr/bin/env python3
"""
차트 사양 테스트 및 JSON 내보내기 예시
FE 개발자가 사용할 수 있도록 차트 사양을 JSON 파일로 내보냅니다.
"""

import json
import os
from chart_specs import (
    get_vega_lite_line_chart_spec,
    get_vega_lite_bar_chart_spec,
    get_echarts_line_chart_option,
    get_echarts_bar_chart_option,
    get_plotly_line_chart_figure,
    get_plotly_bar_chart_figure,
    get_chartjs_line_chart_config,
    get_chartjs_bar_chart_config,
    LINE_CHART_DATA,
    BAR_CHART_DATA
)

def export_chart_specs_to_json():
    """모든 차트 사양을 JSON 파일로 내보내기"""
    
    # 출력 디렉토리 생성
    output_dir = "chart_specs_json"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=== 차트 사양을 JSON으로 내보내기 시작 ===")
    
    # 1. Vega-Lite 사양 내보내기
    print("1. Vega-Lite 사양 내보내기...")
    
    vega_line_spec = get_vega_lite_line_chart_spec()
    with open(f"{output_dir}/vega_lite_line_chart.json", "w", encoding="utf-8") as f:
        json.dump(vega_line_spec, f, ensure_ascii=False, indent=2)
    
    vega_bar_spec = get_vega_lite_bar_chart_spec()
    with open(f"{output_dir}/vega_lite_bar_chart.json", "w", encoding="utf-8") as f:
        json.dump(vega_bar_spec, f, ensure_ascii=False, indent=2)
    
    # 2. ECharts 옵션 내보내기
    print("2. ECharts 옵션 내보내기...")
    
    echarts_line_option = get_echarts_line_chart_option()
    with open(f"{output_dir}/echarts_line_chart.json", "w", encoding="utf-8") as f:
        json.dump(echarts_line_option, f, ensure_ascii=False, indent=2)
    
    echarts_bar_option = get_echarts_bar_chart_option()
    with open(f"{output_dir}/echarts_bar_chart.json", "w", encoding="utf-8") as f:
        json.dump(echarts_bar_option, f, ensure_ascii=False, indent=2)
    
    # 3. Plotly figure 내보내기
    print("3. Plotly figure 내보내기...")
    
    plotly_line_figure = get_plotly_line_chart_figure()
    with open(f"{output_dir}/plotly_line_chart.json", "w", encoding="utf-8") as f:
        json.dump(plotly_line_figure, f, ensure_ascii=False, indent=2)
    
    plotly_bar_figure = get_plotly_bar_chart_figure()
    with open(f"{output_dir}/plotly_bar_chart.json", "w", encoding="utf-8") as f:
        json.dump(plotly_bar_figure, f, ensure_ascii=False, indent=2)
    
    # 4. Chart.js 설정 내보내기
    print("4. Chart.js 설정 내보내기...")
    
    chartjs_line_config = get_chartjs_line_chart_config()
    with open(f"{output_dir}/chartjs_line_chart.json", "w", encoding="utf-8") as f:
        json.dump(chartjs_line_config, f, ensure_ascii=False, indent=2)
    
    chartjs_bar_config = get_chartjs_bar_chart_config()
    with open(f"{output_dir}/chartjs_bar_chart.json", "w", encoding="utf-8") as f:
        json.dump(chartjs_bar_config, f, ensure_ascii=False, indent=2)
    
    # 5. 원본 데이터 내보내기
    print("5. 원본 데이터 내보내기...")
    
    with open(f"{output_dir}/line_chart_data.json", "w", encoding="utf-8") as f:
        json.dump(LINE_CHART_DATA, f, ensure_ascii=False, indent=2)
    
    with open(f"{output_dir}/bar_chart_data.json", "w", encoding="utf-8") as f:
        json.dump(BAR_CHART_DATA, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 모든 차트 사양이 '{output_dir}' 디렉토리에 JSON 파일로 저장되었습니다!")
    
    # 생성된 파일 목록 출력
    print("\n📁 생성된 파일 목록:")
    for filename in sorted(os.listdir(output_dir)):
        filepath = os.path.join(output_dir, filename)
        filesize = os.path.getsize(filepath)
        print(f"  - {filename} ({filesize:,} bytes)")

def test_chart_specs():
    """차트 사양이 올바르게 생성되는지 테스트"""
    
    print("=== 차트 사양 테스트 시작 ===")
    
    try:
        # Vega-Lite 테스트
        print("1. Vega-Lite 사양 테스트...")
        vega_line = get_vega_lite_line_chart_spec()
        vega_bar = get_vega_lite_bar_chart_spec()
        assert vega_line["title"] == "연도별 업종별 총 가맹점수 추이"
        assert vega_bar["title"] == "업종별 전체 기간 평균 가맹점수"
        print("   ✅ Vega-Lite 사양 생성 성공")
        
        # ECharts 테스트
        print("2. ECharts 옵션 테스트...")
        echarts_line = get_echarts_line_chart_option()
        echarts_bar = get_echarts_bar_chart_option()
        assert echarts_line["title"]["text"] == "연도별 업종별 총 가맹점수 추이"
        assert echarts_bar["title"]["text"] == "업종별 전체 기간 평균 가맹점수"
        print("   ✅ ECharts 옵션 생성 성공")
        
        # Plotly 테스트
        print("3. Plotly figure 테스트...")
        plotly_line = get_plotly_line_chart_figure()
        plotly_bar = get_plotly_bar_chart_figure()
        assert plotly_line["layout"]["title"]["text"] == "연도별 업종별 총 가맹점수 추이"
        assert plotly_bar["layout"]["title"]["text"] == "업종별 전체 기간 평균 가맹점수"
        print("   ✅ Plotly figure 생성 성공")
        
        # Chart.js 테스트
        print("4. Chart.js 설정 테스트...")
        chartjs_line = get_chartjs_line_chart_config()
        chartjs_bar = get_chartjs_bar_chart_config()
        assert chartjs_line["options"]["plugins"]["title"]["text"] == "연도별 업종별 총 가맹점수 추이"
        assert chartjs_bar["options"]["plugins"]["title"]["text"] == "업종별 전체 기간 평균 가맹점수"
        print("   ✅ Chart.js 설정 생성 성공")
        
        print("\n🎉 모든 차트 사양 테스트 통과!")
        
    except Exception as e:
        print(f"\n❌ 차트 사양 테스트 실패: {e}")
        return False
    
    return True

def create_html_example():
    """HTML 예시 파일 생성 (ECharts 사용)"""
    
    print("\n=== HTML 예시 파일 생성 ===")
    
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>가맹점수 분석 차트 예시</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        body {
            font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .chart-container {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
            padding: 20px;
        }
        .chart {
            width: 100%;
            height: 500px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .description {
            color: #666;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>🏪 가맹점수 분석 대시보드</h1>
    <p class="description">2017년~2024년 업종별 가맹점수 변화 추이 및 평균 비교</p>
    
    <div class="chart-container">
        <h2>📈 연도별 업종별 총 가맹점수 추이</h2>
        <div id="lineChart" class="chart"></div>
    </div>
    
    <div class="chart-container">
        <h2>📊 업종별 전체 기간 평균 가맹점수</h2>
        <div id="barChart" class="chart"></div>
    </div>

    <script>
        // 차트 초기화
        const lineChart = echarts.init(document.getElementById('lineChart'));
        const barChart = echarts.init(document.getElementById('barChart'));
        
        // 라인 차트 옵션
        const lineOption = {
            "title": {
                "text": "연도별 업종별 총 가맹점수 추이",
                "left": "center",
                "textStyle": {"fontSize": 16, "fontWeight": "bold"}
            },
            "tooltip": {
                "trigger": "axis",
                "formatter": "{b}년<br/>{a}: {c}개"
            },
            "legend": {
                "data": ["도소매", "서비스", "외식"],
                "top": 30
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "3%",
                "containLabel": true
            },
            "xAxis": {
                "type": "category",
                "boundaryGap": false,
                "data": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                "name": "연도",
                "nameLocation": "middle",
                "nameGap": 30
            },
            "yAxis": {
                "type": "value",
                "name": "총 가맹점수",
                "nameLocation": "middle",
                "nameGap": 50
            },
            "series": [
                {
                    "name": "도소매",
                    "type": "line",
                    "data": [48324, 54194, 55581, 56897, 60874, 63470, 59843, 69293],
                    "symbol": "circle",
                    "symbolSize": 6,
                    "lineStyle": {"width": 2},
                    "itemStyle": {"color": "#1f77b4"}
                },
                {
                    "name": "서비스",
                    "type": "line",
                    "data": [65164, 69518, 69948, 68071, 75102, 93298, 87107, 113790],
                    "symbol": "rect",
                    "symbolSize": 6,
                    "lineStyle": {"width": 2},
                    "itemStyle": {"color": "#ff7f0e"}
                },
                {
                    "name": "외식",
                    "type": "line",
                    "data": [101737, 111586, 117368, 125550, 131085, 157192, 156638, 175768],
                    "symbol": "triangle",
                    "symbolSize": 6,
                    "lineStyle": {"width": 2},
                    "itemStyle": {"color": "#2ca02c"}
                }
            ]
        };
        
        // 바 차트 옵션
        const barOption = {
            "title": {
                "text": "업종별 전체 기간 평균 가맹점수",
                "left": "center",
                "textStyle": {"fontSize": 16, "fontWeight": "bold"}
            },
            "tooltip": {
                "trigger": "axis",
                "formatter": "{b}: {c}개"
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "3%",
                "containLabel": true
            },
            "xAxis": {
                "type": "category",
                "data": ["도소매", "서비스", "외식"],
                "name": "업종",
                "nameLocation": "middle",
                "nameGap": 30
            },
            "yAxis": {
                "type": "value",
                "name": "평균 가맹점수 (개)",
                "nameLocation": "middle",
                "nameGap": 50
            },
            "series": [
                {
                    "name": "평균 가맹점수",
                    "type": "bar",
                    "data": [
                        {"value": 11565, "itemStyle": {"color": "#87ceeb"}},
                        {"value": 11078, "itemStyle": {"color": "#90ee90"}},
                        {"value": 19369, "itemStyle": {"color": "#fa8072"}}
                    ],
                    "barWidth": "60%",
                    "label": {
                        "show": true,
                        "position": "top",
                        "formatter": "{c}개"
                    }
                }
            ]
        };
        
        // 차트 렌더링
        lineChart.setOption(lineOption);
        barChart.setOption(barOption);
        
        // 반응형 처리
        window.addEventListener('resize', function() {
            lineChart.resize();
            barChart.resize();
        });
    </script>
</body>
</html>"""
    
    with open("chart_example.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("   ✅ HTML 예시 파일 생성 완료: chart_example.html")

if __name__ == "__main__":
    print("🚀 가맹점수 분석 차트 사양 테스트 및 내보내기 시작\n")
    
    # 1. 차트 사양 테스트
    if test_chart_specs():
        # 2. JSON 파일로 내보내기
        export_chart_specs_to_json()
        
        # 3. HTML 예시 파일 생성
        create_html_example()
        
        print("\n🎯 모든 작업이 완료되었습니다!")
        print("\n📋 다음 파일들을 확인하세요:")
        print("  - chart_specs_json/ : 모든 차트 라이브러리의 JSON 사양")
        print("  - chart_example.html : ECharts를 사용한 실제 차트 예시")
        print("  - README_chart_specs.md : 상세한 사용법 가이드")
        
        print("\n💡 FE 개발자는 chart_specs_json/ 폴더의 JSON 파일을 사용하여")
        print("   원하는 차트 라이브러리로 차트를 구현할 수 있습니다!")
    else:
        print("❌ 차트 사양 테스트 실패로 인해 작업을 중단합니다.")
