"""
가맹점수 분석 차트 사양(spec) 파일
FE 개발자가 이 사양을 사용하여 차트를 그릴 수 있습니다.
"""

import os

import pandas as pd


def load_chart_data():
    """CSV 파일에서 차트 데이터를 로드합니다."""

    # CSV 파일 경로
    retail_file = "data/지역별_도소매별_가맹점수_현황.csv"
    service_file = "data/지역별_서비스별_가맹점수_현황.csv"
    food_file = "data/지역별_외식별_가맹점수_현황.csv"

    # 파일 존재 확인
    if not all(os.path.exists(f) for f in [retail_file, service_file, food_file]):
        print("⚠️ CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_data()

    try:
        # CSV 파일 로드
        retail_df = pd.read_csv(retail_file)
        service_df = pd.read_csv(service_file)
        food_df = pd.read_csv(food_file)

        # 연도별 총 가맹점수 계산 (allFrcsCnt 컬럼 사용)
        retail_total = retail_df.groupby("yr")["allFrcsCnt"].first()
        service_total = service_df.groupby("yr")["allFrcsCnt"].first()
        food_total = food_df.groupby("yr")["allFrcsCnt"].first()

        # 전체 기간 평균 가맹점수 계산 (frcsCnt 컬럼 사용)
        retail_avg = retail_df["frcsCnt"].mean()
        service_avg = service_df["frcsCnt"].mean()
        food_avg = food_df["frcsCnt"].mean()

        line_data = {
            "도소매": retail_total.to_dict(),
            "서비스": service_total.to_dict(),
            "외식": food_total.to_dict(),
        }

        bar_data = {
            "도소매": round(retail_avg),
            "서비스": round(service_avg),
            "외식": round(food_avg),
        }

        print("✅ CSV 파일에서 데이터를 성공적으로 로드했습니다.")
        return line_data, bar_data

    except Exception as e:
        print(f"⚠️ CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_data()


def get_hardcoded_data():
    """하드코딩된 데이터를 반환합니다 (CSV 로드 실패 시 사용)."""

    # 1. 연도별 업종별 총 가맹점수 추이 (라인 차트)
    line_data = {
        "도소매": {
            2017: 48324,
            2018: 54194,
            2019: 55581,
            2020: 56897,
            2021: 60874,
            2022: 63470,
            2023: 59843,
            2024: 69293,
        },
        "서비스": {
            2017: 65164,
            2018: 69518,
            2019: 69948,
            2020: 68071,
            2021: 75102,
            2022: 93298,
            2023: 87107,
            2024: 113790,
        },
        "외식": {
            2017: 101737,
            2018: 111586,
            2019: 117368,
            2020: 125550,
            2021: 131085,
            2022: 157192,
            2023: 156638,
            2024: 175768,
        },
    }

    # 2. 업종별 전체 기간 평균 가맹점수 (바 차트)
    bar_data = {"도소매": 11565, "서비스": 11078, "외식": 19369}

    return line_data, bar_data


# 데이터 로드
LINE_CHART_DATA, BAR_CHART_DATA = load_chart_data()

# ===== Vega-Lite Specs =====


def get_vega_lite_line_chart_spec():
    """연도별 업종별 총 가맹점수 추이 - Vega-Lite 라인 차트 사양"""
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": "연도별 업종별 총 가맹점수 추이",
        "width": 800,
        "height": 500,
        "data": {
            "values": [
                {"year": 2017, "industry": "도소매", "count": 48324},
                {"year": 2018, "industry": "도소매", "count": 54194},
                {"year": 2019, "industry": "도소매", "count": 55581},
                {"year": 2020, "industry": "도소매", "count": 56897},
                {"year": 2021, "industry": "도소매", "count": 60874},
                {"year": 2022, "industry": "도소매", "count": 63470},
                {"year": 2023, "industry": "도소매", "count": 59843},
                {"year": 2024, "industry": "도소매", "count": 69293},
                {"year": 2017, "industry": "서비스", "count": 65164},
                {"year": 2018, "industry": "서비스", "count": 69518},
                {"year": 2019, "industry": "서비스", "count": 69948},
                {"year": 2020, "industry": "서비스", "count": 68071},
                {"year": 2021, "industry": "서비스", "count": 75102},
                {"year": 2022, "industry": "서비스", "count": 93298},
                {"year": 2023, "industry": "서비스", "count": 87107},
                {"year": 2024, "industry": "서비스", "count": 113790},
                {"year": 2017, "industry": "외식", "count": 101737},
                {"year": 2018, "industry": "외식", "count": 111586},
                {"year": 2019, "industry": "외식", "count": 117368},
                {"year": 2020, "industry": "외식", "count": 125550},
                {"year": 2021, "industry": "외식", "count": 131085},
                {"year": 2022, "industry": "외식", "count": 157192},
                {"year": 2023, "industry": "외식", "count": 156638},
                {"year": 2024, "industry": "외식", "count": 175768},
            ]
        },
        "mark": {"type": "line", "point": True},
        "encoding": {
            "x": {
                "field": "year",
                "type": "ordinal",
                "title": "연도",
                "axis": {"labelAngle": 0},
            },
            "y": {
                "field": "count",
                "type": "quantitative",
                "title": "총 가맹점수",
                "scale": {"domain": [40000, 180000]},
            },
            "color": {
                "field": "industry",
                "type": "nominal",
                "scale": {
                    "domain": ["도소매", "서비스", "외식"],
                    "range": ["#1f77b4", "#ff7f0e", "#2ca02c"],
                },
            },
            "tooltip": [
                {"field": "year", "title": "연도"},
                {"field": "industry", "title": "업종"},
                {"field": "count", "title": "가맹점수", "format": ","},
            ],
        },
        "config": {
            "axis": {"labelFontSize": 12, "titleFontSize": 14},
            "title": {"fontSize": 16, "fontWeight": "bold"},
        },
    }


def get_vega_lite_bar_chart_spec():
    """업종별 전체 기간 평균 가맹점수 - Vega-Lite 바 차트 사양"""
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": "업종별 전체 기간 평균 가맹점수",
        "width": 600,
        "height": 400,
        "data": {
            "values": [
                {"industry": "도소매", "count": 11565},
                {"industry": "서비스", "count": 11078},
                {"industry": "외식", "count": 19369},
            ]
        },
        "mark": {"type": "bar", "width": 60},
        "encoding": {
            "x": {"field": "industry", "type": "nominal", "title": "업종"},
            "y": {
                "field": "count",
                "type": "quantitative",
                "title": "평균 가맹점수 (개)",
                "scale": {"domain": [0, 20000]},
            },
            "color": {
                "field": "industry",
                "type": "nominal",
                "scale": {
                    "domain": ["도소매", "서비스", "외식"],
                    "range": ["#87ceeb", "#90ee90", "#fa8072"],
                },
            },
            "tooltip": [
                {"field": "industry", "title": "업종"},
                {"field": "count", "title": "평균 가맹점수", "format": ","},
            ],
        },
        "config": {
            "axis": {"labelFontSize": 12, "titleFontSize": 14},
            "title": {"fontSize": 16, "fontWeight": "bold"},
        },
    }


# ===== ECharts Specs =====


def get_echarts_line_chart_option():
    """연도별 업종별 총 가맹점수 추이 - ECharts 라인 차트 옵션"""
    return {
        "title": {
            "text": "연도별 업종별 총 가맹점수 추이",
            "left": "center",
            "textStyle": {"fontSize": 16, "fontWeight": "bold"},
        },
        "tooltip": {"trigger": "axis", "formatter": "{b}년<br/>{a}: {c}개"},
        "legend": {"data": ["도소매", "서비스", "외식"], "top": 30},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            "name": "연도",
            "nameLocation": "middle",
            "nameGap": 30,
        },
        "yAxis": {
            "type": "value",
            "name": "총 가맹점수",
            "nameLocation": "middle",
            "nameGap": 50,
            "axisLabel": {"formatter": "{value}"},
        },
        "series": [
            {
                "name": "도소매",
                "type": "line",
                "data": [48324, 54194, 55581, 56897, 60874, 63470, 59843, 69293],
                "markPoint": {"show": False},
                "markLine": {"show": False},
                "symbol": "circle",
                "symbolSize": 6,
                "lineStyle": {"width": 2},
                "itemStyle": {"color": "#1f77b4"},
            },
            {
                "name": "서비스",
                "type": "line",
                "data": [65164, 69518, 69948, 68071, 75102, 93298, 87107, 113790],
                "markPoint": {"show": False},
                "markLine": {"show": False},
                "symbol": "rect",
                "symbolSize": 6,
                "lineStyle": {"width": 2},
                "itemStyle": {"color": "#ff7f0e"},
            },
            {
                "name": "외식",
                "type": "line",
                "data": [
                    101737,
                    111586,
                    117368,
                    125550,
                    131085,
                    157192,
                    156638,
                    175768,
                ],
                "markPoint": {"show": False},
                "markLine": {"show": False},
                "symbol": "triangle",
                "symbolSize": 6,
                "lineStyle": {"width": 2},
                "itemStyle": {"color": "#2ca02c"},
            },
        ],
    }


def get_echarts_bar_chart_option():
    """업종별 전체 기간 평균 가맹점수 - ECharts 바 차트 옵션"""
    return {
        "title": {
            "text": "업종별 전체 기간 평균 가맹점수",
            "left": "center",
            "textStyle": {"fontSize": 16, "fontWeight": "bold"},
        },
        "tooltip": {"trigger": "axis", "formatter": "{b}: {c}개"},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": ["도소매", "서비스", "외식"],
            "name": "업종",
            "nameLocation": "middle",
            "nameGap": 30,
        },
        "yAxis": {
            "type": "value",
            "name": "평균 가맹점수 (개)",
            "nameLocation": "middle",
            "nameGap": 50,
        },
        "series": [
            {
                "name": "평균 가맹점수",
                "type": "bar",
                "data": [
                    {"value": 11565, "itemStyle": {"color": "#87ceeb"}},
                    {"value": 11078, "itemStyle": {"color": "#90ee90"}},
                    {"value": 19369, "itemStyle": {"color": "#fa8072"}},
                ],
                "barWidth": "60%",
                "label": {"show": True, "position": "top", "formatter": "{c}개"},
            }
        ],
    }


# ===== Plotly Specs =====


def get_plotly_line_chart_figure():
    """연도별 업종별 총 가맹점수 추이 - Plotly 라인 차트 사양"""
    return {
        "data": [
            {
                "x": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                "y": [48324, 54194, 55581, 56897, 60874, 63470, 59843, 69293],
                "type": "scatter",
                "mode": "lines+markers",
                "name": "도소매",
                "marker": {"symbol": "circle", "size": 8},
                "line": {"width": 3},
                "hovertemplate": "<b>도소매</b><br>연도: %{x}년<br>가맹점수: %{y:,}개<extra></extra>",
            },
            {
                "x": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                "y": [65164, 69518, 69948, 68071, 75102, 93298, 87107, 113790],
                "type": "scatter",
                "mode": "lines+markers",
                "name": "서비스",
                "marker": {"symbol": "square", "size": 8},
                "line": {"width": 3},
                "hovertemplate": "<b>서비스</b><br>연도: %{x}년<br>가맹점수: %{y:,}개<extra></extra>",
            },
            {
                "x": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                "y": [101737, 111586, 117368, 125550, 131085, 157192, 156638, 175768],
                "type": "scatter",
                "mode": "lines+markers",
                "name": "외식",
                "marker": {"symbol": "triangle-up", "size": 8},
                "line": {"width": 3},
                "hovertemplate": "<b>외식</b><br>연도: %{x}년<br>가맹점수: %{y:,}개<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "연도별 업종별 총 가맹점수 추이",
                "font": {"size": 18, "color": "black"},
            },
            "xaxis": {
                "title": "연도",
                "tickmode": "array",
                "tickvals": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                "ticktext": [
                    "2017",
                    "2018",
                    "2019",
                    "2020",
                    "2021",
                    "2022",
                    "2023",
                    "2024",
                ],
            },
            "yaxis": {
                "title": "총 가맹점수",
                "tickformat": ",",
                "range": [40000, 180000],
            },
            "hovermode": "x unified",
            "showlegend": True,
            "legend": {"x": 0.02, "y": 0.98},
            "margin": {"l": 60, "r": 30, "t": 60, "b": 60},
        },
    }


def get_plotly_bar_chart_figure():
    """업종별 전체 기간 평균 가맹점수 - Plotly 바 차트 사양"""
    return {
        "data": [
            {
                "x": ["도소매", "서비스", "외식"],
                "y": [11565, 11078, 19369],
                "type": "bar",
                "marker": {"color": ["#87ceeb", "#90ee90", "#fa8072"], "opacity": 0.8},
                "hovertemplate": "<b>%{x}</b><br>평균 가맹점수: %{y:,}개<extra></extra>",
                "text": ["11,565개", "11,078개", "19,369개"],
                "textposition": "outside",
            }
        ],
        "layout": {
            "title": {
                "text": "업종별 전체 기간 평균 가맹점수",
                "font": {"size": 18, "color": "black"},
            },
            "xaxis": {"title": "업종"},
            "yaxis": {
                "title": "평균 가맹점수 (개)",
                "tickformat": ",",
                "range": [0, 20000],
            },
            "showlegend": False,
            "margin": {"l": 60, "r": 30, "t": 60, "b": 60},
        },
    }


# ===== Chart.js Specs =====


def get_chartjs_line_chart_config():
    """연도별 업종별 총 가맹점수 추이 - Chart.js 라인 차트 설정"""
    return {
        "type": "line",
        "data": {
            "labels": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            "datasets": [
                {
                    "label": "도소매",
                    "data": [48324, 54194, 55581, 56897, 60874, 63470, 59843, 69293],
                    "borderColor": "#1f77b4",
                    "backgroundColor": "rgba(31, 119, 180, 0.1)",
                    "pointBackgroundColor": "#1f77b4",
                    "pointBorderColor": "#1f77b4",
                    "pointStyle": "circle",
                    "tension": 0.1,
                },
                {
                    "label": "서비스",
                    "data": [65164, 69518, 69948, 68071, 75102, 93298, 87107, 113790],
                    "borderColor": "#ff7f0e",
                    "backgroundColor": "rgba(255, 127, 14, 0.1)",
                    "pointBackgroundColor": "#ff7f0e",
                    "pointBorderColor": "#ff7f0e",
                    "pointStyle": "rect",
                    "tension": 0.1,
                },
                {
                    "label": "외식",
                    "data": [
                        101737,
                        111586,
                        117368,
                        125550,
                        131085,
                        157192,
                        156638,
                        175768,
                    ],
                    "borderColor": "#2ca02c",
                    "backgroundColor": "rgba(44, 160, 44, 0.1)",
                    "pointBackgroundColor": "#2ca02c",
                    "pointBorderColor": "#2ca02c",
                    "pointStyle": "triangle",
                    "tension": 0.1,
                },
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "연도별 업종별 총 가맹점수 추이",
                    "font": {"size": 16, "weight": "bold"},
                },
                "tooltip": {"mode": "index", "intersect": False},
            },
            "scales": {
                "x": {"title": {"display": True, "text": "연도"}},
                "y": {
                    "title": {"display": True, "text": "총 가맹점수"},
                    "beginAtZero": False,
                    "min": 40000,
                    "max": 180000,
                },
            },
        },
    }


def get_chartjs_bar_chart_config():
    """업종별 전체 기간 평균 가맹점수 - Chart.js 바 차트 설정"""
    return {
        "type": "bar",
        "data": {
            "labels": ["도소매", "서비스", "외식"],
            "datasets": [
                {
                    "label": "평균 가맹점수",
                    "data": [11565, 11078, 19369],
                    "backgroundColor": ["#87ceeb", "#90ee90", "#fa8072"],
                    "borderColor": ["#87ceeb", "#90ee90", "#fa8072"],
                    "borderWidth": 1,
                }
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "업종별 전체 기간 평균 가맹점수",
                    "font": {"size": 16, "weight": "bold"},
                },
                "tooltip": {"callbacks": {}},
            },
            "scales": {
                "x": {"title": {"display": True, "text": "업종"}},
                "y": {
                    "title": {"display": True, "text": "평균 가맹점수 (개)"},
                    "beginAtZero": True,
                    "max": 20000,
                },
            },
        },
    }


# ===== 사용 예시 =====

if __name__ == "__main__":
    print("=== 가맹점수 분석 차트 사양 파일 ===")
    print("\n사용 가능한 차트 사양:")
    print(
        "1. Vega-Lite: get_vega_lite_line_chart_spec(), get_vega_lite_bar_chart_spec()"
    )
    print("2. ECharts: get_echarts_line_chart_option(), get_echarts_bar_chart_option()")
    print("3. Plotly: get_plotly_line_chart_figure(), get_plotly_bar_chart_figure()")
    print(
        "4. Chart.js: get_chartjs_line_chart_config(), get_chartjs_bar_chart_config()"
    )

    print("\n=== 데이터 구조 ===")
    print("라인 차트 데이터:", LINE_CHART_DATA)
    print("바 차트 데이터:", BAR_CHART_DATA)
