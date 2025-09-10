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


def load_gender_population_data():
    """유동인구 성별 데이터를 로드합니다."""

    population_file = "data/pocheon_population_etl_2024_fixed.csv"

    if not os.path.exists(population_file):
        print("⚠️ 유동인구 CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_gender_data()

    try:
        # CSV 파일 로드
        df = pd.read_csv(population_file)

        # 성별 컬럼 확인
        male_cols = [
            col for col in df.columns if col.startswith("M_") and col.endswith("_CNT")
        ]
        female_cols = [
            col for col in df.columns if col.startswith("F_") and col.endswith("_CNT")
        ]

        # 성별 총 인구 계산
        total_male = df[male_cols].sum().sum()
        total_female = df[female_cols].sum().sum()

        gender_data = {"남성": int(total_male), "여성": int(total_female)}

        print("✅ 유동인구 성별 데이터를 성공적으로 로드했습니다.")
        return gender_data

    except Exception as e:
        print(f"⚠️ 유동인구 CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_gender_data()


def load_area_population_data():
    """읍면동별 총 유동인구 데이터를 로드합니다."""

    population_file = "data/pocheon_population_etl_2024_fixed.csv"

    if not os.path.exists(population_file):
        print("⚠️ 유동인구 CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_area_data()

    try:
        # CSV 파일 로드
        df = pd.read_csv(population_file)

        # 연령대/성별 컬럼 분리
        age_gender_cols = [
            col
            for col in df.columns
            if any(x in col for x in ["M_", "F_"]) and "CNT" in col
        ]

        # 읍면동별 총 인구 계산
        area_population = (
            df.groupby("ADMI_NM")[age_gender_cols]
            .sum()
            .sum(axis=1)
            .sort_values(ascending=False)
        )

        area_data = area_population.to_dict()

        print("✅ 읍면동별 유동인구 데이터를 성공적으로 로드했습니다.")
        return area_data

    except Exception as e:
        print(f"⚠️ 읍면동별 유동인구 CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_area_data()


def load_age_gender_population_data():
    """연령대별 성별 유동인구 데이터를 로드합니다."""

    population_file = "data/pocheon_population_etl_2024_fixed.csv"

    if not os.path.exists(population_file):
        print("⚠️ 유동인구 CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_age_gender_data()

    try:
        # CSV 파일 로드
        df = pd.read_csv(population_file)

        # 연령대/성별 컬럼 분리
        age_gender_cols = [
            col
            for col in df.columns
            if any(x in col for x in ["M_", "F_"]) and "CNT" in col
        ]

        # 남성 연령대별
        male_cols = [col for col in age_gender_cols if col.startswith("M_")]
        male_age_data = df[male_cols].sum()

        # 여성 연령대별
        female_cols = [col for col in age_gender_cols if col.startswith("F_")]
        female_age_data = df[female_cols].sum()

        # 연령대 라벨 매핑
        age_labels = {
            "M_10_CNT": "10대",
            "M_15_CNT": "15대",
            "M_20_CNT": "20대",
            "M_25_CNT": "25대",
            "M_30_CNT": "30대",
            "M_35_CNT": "35대",
            "M_40_CNT": "40대",
            "M_45_CNT": "45대",
            "M_50_CNT": "50대",
            "M_55_CNT": "55대",
            "M_60_CNT": "60대",
            "M_65_CNT": "65대",
            "M_70_CNT": "70대+",
            "F_10_CNT": "10대",
            "F_15_CNT": "15대",
            "F_20_CNT": "20대",
            "F_25_CNT": "25대",
            "F_30_CNT": "30대",
            "F_35_CNT": "35대",
            "F_40_CNT": "40대",
            "F_45_CNT": "45대",
            "F_50_CNT": "50대",
            "F_55_CNT": "55대",
            "F_60_CNT": "60대",
            "F_65_CNT": "65대",
            "F_70_CNT": "70대+",
        }

        male_age_data_labeled = male_age_data.rename(index=age_labels)
        female_age_data_labeled = female_age_data.rename(index=age_labels)

        age_gender_data = {
            "남성": male_age_data_labeled.to_dict(),
            "여성": female_age_data_labeled.to_dict(),
        }

        print("✅ 연령대별 성별 유동인구 데이터를 성공적으로 로드했습니다.")
        return age_gender_data

    except Exception as e:
        print(f"⚠️ 연령대별 성별 유동인구 CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_age_gender_data()


def get_hardcoded_gender_data():
    """하드코딩된 성별 유동인구 데이터를 반환합니다."""
    return {"남성": 200766852, "여성": 144861837}  # 58.1%  # 41.9%


def get_hardcoded_area_data():
    """하드코딩된 읍면동별 유동인구 데이터를 반환합니다."""
    return {
        "소흘읍": 102260649,
        "포천동": 35902500,
        "선단동": 33522744,
        "신북면": 28724232,
        "가산면": 23335189,
        "군내면": 23258512,
        "영북면": 21199597,
        "일동면": 19391904,
        "이동면": 15215484,
        "내촌면": 11660110,
        "영중면": 11651256,
        "관인면": 7285466,
        "화현면": 7094244,
        "창수면": 5126801,
    }


def get_hardcoded_age_gender_data():
    """하드코딩된 연령대별 성별 유동인구 데이터를 반환합니다."""
    return {
        "남성": {
            "10대": 5830177,
            "15대": 7493635,
            "20대": 12972730,
            "25대": 15846025,
            "30대": 15313281,
            "35대": 12225977,
            "40대": 15217041,
            "45대": 16362816,
            "50대": 22166662,
            "55대": 24991200,
            "60대": 25178248,
            "65대": 18626080,
            "70대+": 8492979,
        },
        "여성": {
            "10대": 5739710,
            "15대": 6161940,
            "20대": 9089491,
            "25대": 10357401,
            "30대": 9735658,
            "35대": 8889869,
            "40대": 10955883,
            "45대": 12117343,
            "50대": 16100652,
            "55대": 17742588,
            "60대": 17405796,
            "65대": 13645395,
            "70대+": 6920111,
        },
    }


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


def load_yearly_trend_data():
    """연도별 총 가맹점수 추이 데이터를 로드합니다."""
    try:
        # CSV 파일 경로
        retail_file = "data/지역별_도소매별_가맹점수_현황.csv"
        service_file = "data/지역별_서비스별_가맹점수_현황.csv"
        food_file = "data/지역별_외식별_가맹점수_현황.csv"

        # 파일 존재 확인
        if not all(os.path.exists(f) for f in [retail_file, service_file, food_file]):
            print("⚠️ 연도별 추이 CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
            return get_hardcoded_yearly_trend_data()

        # CSV 파일 로드
        retail_df = pd.read_csv(retail_file)
        service_df = pd.read_csv(service_file)
        food_df = pd.read_csv(food_file)

        # 연도별 총 가맹점수 계산
        retail_total = retail_df.groupby("yr")["allFrcsCnt"].first()
        service_total = service_df.groupby("yr")["allFrcsCnt"].first()
        food_total = food_df.groupby("yr")["allFrcsCnt"].first()

        yearly_trend_data = {
            "도소매": retail_total.to_dict(),
            "서비스": service_total.to_dict(),
            "외식": food_total.to_dict(),
        }

        print("✅ 연도별 총 가맹점수 추이 데이터를 성공적으로 로드했습니다.")
        return yearly_trend_data

    except Exception as e:
        print(f"⚠️ 연도별 추이 CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_yearly_trend_data()


def get_hardcoded_yearly_trend_data():
    """하드코딩된 연도별 총 가맹점수 추이 데이터를 반환합니다."""
    return {
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


def load_growth_rate_data():
    """연도별 성장률 데이터를 로드합니다."""
    try:
        # CSV 파일 경로
        retail_file = "data/지역별_도소매별_가맹점수_현황.csv"
        service_file = "data/지역별_서비스별_가맹점수_현황.csv"
        food_file = "data/지역별_외식별_가맹점수_현황.csv"

        # 파일 존재 확인
        if not all(os.path.exists(f) for f in [retail_file, service_file, food_file]):
            print("⚠️ 성장률 CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
            return get_hardcoded_growth_rate_data()

        # CSV 파일 로드
        retail_df = pd.read_csv(retail_file)
        service_df = pd.read_csv(service_file)
        food_df = pd.read_csv(food_file)

        # 연도별 총 가맹점수 계산
        retail_total = retail_df.groupby("yr")["allFrcsCnt"].first()
        service_total = service_df.groupby("yr")["allFrcsCnt"].first()
        food_total = food_df.groupby("yr")["allFrcsCnt"].first()

        # 성장률 계산 (전년 대비)
        retail_growth = retail_total.pct_change() * 100
        service_growth = service_total.pct_change() * 100
        food_growth = food_total.pct_change() * 100

        growth_rate_data = {
            "도소매": retail_growth.to_dict(),
            "서비스": service_growth.to_dict(),
            "외식": food_growth.to_dict(),
        }

        print("✅ 연도별 성장률 데이터를 성공적으로 로드했습니다.")
        return growth_rate_data

    except Exception as e:
        print(f"⚠️ 성장률 CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_growth_rate_data()


def get_hardcoded_growth_rate_data():
    """하드코딩된 연도별 성장률 데이터를 반환합니다."""
    return {
        "도소매": {
            2017: None,
            2018: 12.15,
            2019: 2.56,
            2020: 2.36,
            2021: 6.99,
            2022: 4.26,
            2023: -5.72,
            2024: 15.80,
        },
        "서비스": {
            2017: None,
            2018: 6.68,
            2019: 0.62,
            2020: -2.68,
            2021: 10.33,
            2022: 24.24,
            2023: -6.63,
            2024: 30.60,
        },
        "외식": {
            2017: None,
            2018: 9.68,
            2019: 5.18,
            2020: 6.97,
            2021: 4.41,
            2022: 19.90,
            2023: -0.35,
            2024: 12.22,
        },
    }


def load_time_period_population_data():
    """시간대별 유동인구 데이터를 로드합니다."""
    try:
        # CSV 파일 경로
        population_file = "data/pocheon_population_etl_2024_fixed.csv"

        # 파일 존재 확인
        if not os.path.exists(population_file):
            print("⚠️ 시간대별 유동인구 CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
            return get_hardcoded_time_period_data()

        # CSV 파일 로드
        df = pd.read_csv(population_file)

        # 시간대별 그룹핑 (6-9, 9-12, 12-15, 15-18, 18-21, 21-24)
        time_periods = {
            "06-09": (6, 9),
            "09-12": (9, 12),
            "12-15": (12, 15),
            "15-18": (15, 18),
            "18-21": (18, 21),
            "21-24": (21, 24),
        }

        time_period_data = {}
        for period_name, (start_hour, end_hour) in time_periods.items():
            if start_hour == 21:  # 21-24시
                mask = df["hour"].between(start_hour, 23)
            else:
                mask = df["hour"].between(start_hour, end_hour - 1)

            period_data = df[mask]
            total_population = period_data["total_population"].sum()
            time_period_data[period_name] = total_population

        print("✅ 시간대별 유동인구 데이터를 성공적으로 로드했습니다.")
        return time_period_data

    except Exception as e:
        print(f"⚠️ 시간대별 유동인구 CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_time_period_data()


def get_hardcoded_time_period_data():
    """하드코딩된 시간대별 유동인구 데이터를 반환합니다."""
    return {
        "06-09": 125000,
        "09-12": 180000,
        "12-15": 220000,
        "15-18": 195000,
        "18-21": 160000,
        "21-24": 95000,
    }


def load_closing_rate_data():
    """연도별 폐점률 데이터를 로드합니다."""
    try:
        # CSV 파일 경로
        retail_file = "data/주요도소매별_가맹점_개폐점현황.csv"
        service_file = "data/주요서비스별_가맹점_개폐점현황.csv"
        food_file = "data/주요외식별_가맹점_개폐점현황.csv"

        # 파일 존재 확인
        if not all(os.path.exists(f) for f in [retail_file, service_file, food_file]):
            print("⚠️ 폐점률 CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
            return get_hardcoded_closing_rate_data()

        # CSV 파일 로드
        retail_df = pd.read_csv(retail_file)
        service_df = pd.read_csv(service_file)
        food_df = pd.read_csv(food_file)

        # 연도별 평균 폐점률 계산
        retail_closing = retail_df.groupby("yr")["endCncltnRt"].mean()
        service_closing = service_df.groupby("yr")["endCncltnRt"].mean()
        food_closing = food_df.groupby("yr")["endCncltnRt"].mean()

        closing_rate_data = {
            "도소매": retail_closing.to_dict(),
            "서비스": service_closing.to_dict(),
            "외식": food_closing.to_dict(),
        }

        print("✅ 연도별 폐점률 데이터를 성공적으로 로드했습니다.")
        return closing_rate_data

    except Exception as e:
        print(f"⚠️ 폐점률 CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_closing_rate_data()


def get_hardcoded_closing_rate_data():
    """하드코딩된 연도별 폐점률 데이터를 반환합니다."""
    return {
        "도소매": {
            2017: 7.7,
            2018: 6.0,
            2019: 8.9,
            2020: 12.0,
            2021: 10.7,
            2022: 10.6,
            2023: 8.8,
            2024: 10.6,
        },
        "서비스": {
            2017: 12.9,
            2018: 11.9,
            2019: 10.4,
            2020: 10.9,
            2021: 9.8,
            2022: 8.7,
            2023: 12.1,
            2024: 11.3,
        },
        "외식": {
            2017: 13.8,
            2018: 12.2,
            2019: 11.4,
            2020: 11.9,
            2021: 12.3,
            2022: 13.2,
            2023: 16.1,
            2024: 16.4,
        },
    }


def load_opening_closing_rate_data():
    """2024년 업종별 개폐점률 데이터를 로드합니다."""
    try:
        # CSV 파일 경로
        retail_file = "data/주요도소매별_가맹점_개폐점현황.csv"
        service_file = "data/주요서비스별_가맹점_개폐점현황.csv"
        food_file = "data/주요외식별_가맹점_개폐점현황.csv"

        # 파일 존재 확인
        if not all(os.path.exists(f) for f in [retail_file, service_file, food_file]):
            print("⚠️ 개폐점률 CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
            return get_hardcoded_opening_closing_rate_data()

        # CSV 파일 로드
        retail_df = pd.read_csv(retail_file)
        service_df = pd.read_csv(service_file)
        food_df = pd.read_csv(food_file)

        # 2024년 데이터만 필터링
        retail_2024 = retail_df[retail_df["yr"] == 2024]
        service_2024 = service_df[service_df["yr"] == 2024]
        food_2024 = food_df[food_df["yr"] == 2024]

        opening_closing_data = {
            "도소매": {
                "업종": retail_2024["indutyMlsfcNm"].tolist(),
                "개점률": retail_2024["newFrcsRt"].tolist(),
                "폐점률": retail_2024["endCncltnRt"].tolist(),
            },
            "서비스": {
                "업종": service_2024["indutyMlsfcNm"].tolist(),
                "개점률": service_2024["newFrcsRt"].tolist(),
                "폐점률": service_2024["endCncltnRt"].tolist(),
            },
            "외식": {
                "업종": food_2024["indutyMlsfcNm"].tolist(),
                "개점률": food_2024["newFrcsRt"].tolist(),
                "폐점률": food_2024["endCncltnRt"].tolist(),
            },
        }

        print("✅ 2024년 업종별 개폐점률 데이터를 성공적으로 로드했습니다.")
        return opening_closing_data

    except Exception as e:
        print(f"⚠️ 개폐점률 CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_opening_closing_rate_data()


def get_hardcoded_opening_closing_rate_data():
    """하드코딩된 2024년 업종별 개폐점률 데이터를 반환합니다."""
    return {
        "도소매": {
            "업종": ["편의점", "기타도소매", "화장품", "(건강)식품", "종합소매점"],
            "개점률": [15.2, 12.8, 8.5, 6.3, 18.2],
            "폐점률": [10.6, 14.2, 7.8, 9.1, 12.5],
        },
        "서비스": {
            "업종": ["교육(외국어)", "교육(교과)", "자동차관련", "기타교육", "이미용"],
            "개점률": [11.8, 9.2, 7.5, 8.9, 6.7],
            "폐점률": [13.2, 11.5, 9.8, 10.2, 8.4],
        },
        "외식": {
            "업종": ["치킨", "한식", "커피", "기타외식", "분식"],
            "개점률": [14.5, 16.8, 18.2, 12.3, 9.7],
            "폐점률": [16.4, 18.9, 15.6, 14.2, 11.8],
        },
    }


def load_net_growth_rate_data():
    """순증가율 데이터를 로드합니다."""
    try:
        # CSV 파일 경로
        retail_file = "data/주요도소매별_가맹점_개폐점현황.csv"
        service_file = "data/주요서비스별_가맹점_개폐점현황.csv"
        food_file = "data/주요외식별_가맹점_개폐점현황.csv"

        # 파일 존재 확인
        if not all(os.path.exists(f) for f in [retail_file, service_file, food_file]):
            print("⚠️ 순증가율 CSV 파일을 찾을 수 없습니다. 하드코딩된 데이터를 사용합니다.")
            return get_hardcoded_net_growth_rate_data()

        # CSV 파일 로드
        retail_df = pd.read_csv(retail_file)
        service_df = pd.read_csv(service_file)
        food_df = pd.read_csv(food_file)

        # 순증가율 계산 (개점률 - 폐점률)
        retail_df["netGrowthRt"] = retail_df["newFrcsRt"] - retail_df["endCncltnRt"]
        service_df["netGrowthRt"] = service_df["newFrcsRt"] - service_df["endCncltnRt"]
        food_df["netGrowthRt"] = food_df["newFrcsRt"] - food_df["endCncltnRt"]

        # 연도별 평균 순증가율
        retail_net = retail_df.groupby("yr")["netGrowthRt"].mean()
        service_net = service_df.groupby("yr")["netGrowthRt"].mean()
        food_net = food_df.groupby("yr")["netGrowthRt"].mean()

        net_growth_data = {
            "도소매": retail_net.to_dict(),
            "서비스": service_net.to_dict(),
            "외식": food_net.to_dict(),
        }

        print("✅ 순증가율 데이터를 성공적으로 로드했습니다.")
        return net_growth_data

    except Exception as e:
        print(f"⚠️ 순증가율 CSV 파일 로드 실패: {e}. 하드코딩된 데이터를 사용합니다.")
        return get_hardcoded_net_growth_rate_data()


def get_hardcoded_net_growth_rate_data():
    """하드코딩된 순증가율 데이터를 반환합니다."""
    return {
        "도소매": {
            2017: 10.2,
            2018: 12.3,
            2019: 8.1,
            2020: 2.5,
            2021: 5.8,
            2022: 6.4,
            2023: 9.2,
            2024: 7.8,
        },
        "서비스": {
            2017: 4.1,
            2018: 6.2,
            2019: 8.6,
            2020: 7.1,
            2021: 9.2,
            2022: 11.3,
            2023: 5.9,
            2024: 7.7,
        },
        "외식": {
            2017: 2.2,
            2018: 4.8,
            2019: 6.6,
            2020: 5.1,
            2021: 3.7,
            2022: 1.8,
            2023: -1.2,
            2024: -0.5,
        },
    }


# 데이터 로드
LINE_CHART_DATA, BAR_CHART_DATA = load_chart_data()
GENDER_PIE_DATA = load_gender_population_data()
AREA_POPULATION_DATA = load_area_population_data()
AGE_GENDER_DATA = load_age_gender_population_data()
TIME_PERIOD_DATA = load_time_period_population_data()
YEARLY_TREND_DATA = load_yearly_trend_data()
GROWTH_RATE_DATA = load_growth_rate_data()
CLOSING_RATE_DATA = load_closing_rate_data()
OPENING_CLOSING_RATE_DATA = load_opening_closing_rate_data()
NET_GROWTH_RATE_DATA = load_net_growth_rate_data()

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


def get_vega_lite_pie_chart_spec():
    """성별 유동인구 비율 - Vega-Lite 파이 차트 사양"""
    gender_data = GENDER_PIE_DATA
    data = [{"성별": k, "인구수": v} for k, v in gender_data.items()]
    # total = sum(gender_data.values())  # 사용되지 않음

    # 퍼센트 계산
    for item in data:
        item["비율"] = round((item["인구수"] / sum(gender_data.values())) * 100, 1)

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "성별 유동인구 비율 (2024)",
            "fontSize": 16,
            "fontWeight": "bold",
        },
        "width": 400,
        "height": 400,
        "data": {"values": data},
        "mark": {"type": "arc", "innerRadius": 0, "outerRadius": 100},
        "encoding": {
            "theta": {
                "field": "인구수",
                "type": "quantitative",
                "scale": {"type": "linear"},
            },
            "color": {
                "field": "성별",
                "type": "nominal",
                "scale": {"domain": ["남성", "여성"], "range": ["#87ceeb", "#ffb6c1"]},
                "legend": {
                    "orient": "bottom",
                    "labelFontSize": 12,
                    "titleFontSize": 12,
                },
            },
            "tooltip": [
                {"field": "성별", "type": "nominal"},
                {"field": "인구수", "type": "quantitative", "title": "인구수", "format": ","},
                {
                    "field": "비율",
                    "type": "quantitative",
                    "title": "비율 (%)",
                    "format": ".1f",
                },
            ],
        },
        "view": {"stroke": None},
        "config": {
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


def get_echarts_pie_chart_option():
    """성별 유동인구 비율 - ECharts 파이 차트 옵션"""
    gender_data = GENDER_PIE_DATA
    data = []
    # total = sum(gender_data.values())  # 사용되지 않음

    for name, value in gender_data.items():
        percentage = round((value / sum(gender_data.values())) * 100, 1)
        data.append(
            {
                "name": name,
                "value": value,
                "label": {"formatter": f"{name}\n{value:,}명\n({percentage}%)"},
            }
        )

    return {
        "title": {
            "text": "성별 유동인구 비율 (2024)",
            "left": "center",
            "textStyle": {"fontSize": 16, "fontWeight": "bold"},
        },
        "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b}: {c}명 ({d}%)"},
        "legend": {
            "orient": "horizontal",
            "bottom": "5%",
            "left": "center",
            "textStyle": {"fontSize": 12},
        },
        "series": [
            {
                "name": "유동인구",
                "type": "pie",
                "radius": ["40%", "70%"],
                "center": ["50%", "50%"],
                "data": data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
                "label": {
                    "show": True,
                    "position": "outside",
                    "fontSize": 12,
                    "fontWeight": "bold",
                },
                "labelLine": {"show": True},
                "itemStyle": {"color": {"남성": "#87ceeb", "여성": "#ffb6c1"}},
            }
        ],
        "color": ["#87ceeb", "#ffb6c1"],
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
                "hovertemplate": (
                    "<b>도소매</b><br>연도: %{x}년<br>가맹점수: %{y:,}개<extra></extra>"
                ),
            },
            {
                "x": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                "y": [65164, 69518, 69948, 68071, 75102, 93298, 87107, 113790],
                "type": "scatter",
                "mode": "lines+markers",
                "name": "서비스",
                "marker": {"symbol": "square", "size": 8},
                "line": {"width": 3},
                "hovertemplate": (
                    "<b>서비스</b><br>연도: %{x}년<br>가맹점수: %{y:,}개<extra></extra>"
                ),
            },
            {
                "x": [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                "y": [101737, 111586, 117368, 125550, 131085, 157192, 156638, 175768],
                "type": "scatter",
                "mode": "lines+markers",
                "name": "외식",
                "marker": {"symbol": "triangle-up", "size": 8},
                "line": {"width": 3},
                "hovertemplate": (
                    "<b>외식</b><br>연도: %{x}년<br>가맹점수: %{y:,}개<extra></extra>"
                ),
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
                "hovertemplate": ("<b>%{x}</b><br>평균 가맹점수: %{y:,}개<extra></extra>"),
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


def get_plotly_pie_chart_figure():
    """성별 유동인구 비율 - Plotly 파이 차트 사양"""
    gender_data = GENDER_PIE_DATA
    labels = list(gender_data.keys())
    values = list(gender_data.values())
    # total = sum(values)  # 사용되지 않음

    # 퍼센트 계산
    # percentages = [round((v / total) * 100, 1) for v in values]  # 사용되지 않음

    return {
        "data": [
            {
                "labels": labels,
                "values": values,
                "type": "pie",
                "hole": 0.3,  # 도넛 차트
                "marker": {
                    "colors": ["#87ceeb", "#ffb6c1"],
                    "line": {"color": "#000000", "width": 2},
                },
                "textinfo": "label+percent",
                "textposition": "outside",
                "hovertemplate": (
                    "<b>%{label}</b><br>"
                    "인구수: %{value:,}명<br>"
                    "비율: %{percent}<br>"
                    "<extra></extra>"
                ),
                "textfont": {"size": 12, "color": "black"},
                "showlegend": True,
            }
        ],
        "layout": {
            "title": {
                "text": "성별 유동인구 비율 (2024)",
                "font": {"size": 18, "color": "black"},
            },
            "legend": {"orientation": "h", "x": 0.5, "xanchor": "center", "y": -0.1},
            "margin": {"l": 30, "r": 30, "t": 60, "b": 60},
            "width": 500,
            "height": 500,
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


def get_chartjs_pie_chart_config():
    """성별 유동인구 비율 - Chart.js 파이 차트 설정"""
    gender_data = GENDER_PIE_DATA
    labels = list(gender_data.keys())
    data = list(gender_data.values())

    return {
        "type": "pie",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "유동인구",
                    "data": data,
                    "backgroundColor": ["#87ceeb", "#ffb6c1"],
                    "borderColor": ["#4682b4", "#ff69b4"],
                    "borderWidth": 2,
                }
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "성별 유동인구 비율 (2024)",
                    "font": {"size": 16, "weight": "bold"},
                },
                "legend": {
                    "position": "bottom",
                    "labels": {"padding": 20, "font": {"size": 14}},
                },
                "tooltip": {
                    "callbacks": {
                        "label": (
                            "function(context) { "
                            "const total = context.dataset.data.reduce("
                            "(a, b) => a + b, 0); "
                            "const percentage = ((context.raw / total) * 100)."
                            "toFixed(1); "
                            "return context.label + ': ' + "
                            "context.raw.toLocaleString() + "
                            "'명 (' + percentage + '%)'; "
                            "}"
                        )
                    }
                },
            },
        },
    }


def get_chartjs_area_population_config():
    """읍면동별 총 유동인구 - Chart.js 막대 차트 설정"""
    area_data = AREA_POPULATION_DATA
    labels = list(area_data.keys())
    data = list(area_data.values())

    return {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "총 유동인구",
                    "data": data,
                    "backgroundColor": "rgba(135, 206, 235, 0.7)",
                    "borderColor": "#87ceeb",
                    "borderWidth": 1,
                }
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "포천시 읍면동별 총 유동인구 (2024)",
                    "font": {"size": 16, "weight": "bold"},
                },
                "legend": {"display": False},
                "tooltip": {
                    "callbacks": {
                        "label": (
                            "function(context) { "
                            "return context.parsed.y.toLocaleString() + '명'; "
                            "}"
                        )
                    }
                },
            },
            "scales": {
                "x": {
                    "title": {"display": True, "text": "읍면동"},
                    "ticks": {"maxRotation": 45, "minRotation": 45},
                },
                "y": {
                    "title": {"display": True, "text": "총 유동인구 (명)"},
                    "beginAtZero": True,
                    "ticks": {
                        "callback": (
                            "function(value) { return value.toLocaleString(); }"
                        )
                    },
                },
            },
        },
    }


def get_chartjs_age_gender_config():
    """연령대별 성별 유동인구 - Chart.js 막대 차트 설정"""
    age_gender_data = AGE_GENDER_DATA
    age_labels = list(age_gender_data["남성"].keys())

    return {
        "type": "bar",
        "data": {
            "labels": age_labels,
            "datasets": [
                {
                    "label": "남성",
                    "data": [age_gender_data["남성"][age] for age in age_labels],
                    "backgroundColor": "rgba(31, 119, 180, 0.7)",
                    "borderColor": "#1f77b4",
                    "borderWidth": 1,
                },
                {
                    "label": "여성",
                    "data": [age_gender_data["여성"][age] for age in age_labels],
                    "backgroundColor": "rgba(255, 182, 193, 0.7)",
                    "borderColor": "#ffb6c1",
                    "borderWidth": 1,
                },
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "연령대별 성별 유동인구 (2024)",
                    "font": {"size": 16, "weight": "bold"},
                },
                "legend": {
                    "position": "top",
                    "labels": {"padding": 20, "font": {"size": 14}},
                },
                "tooltip": {
                    "mode": "index",
                    "intersect": False,
                    "callbacks": {
                        "label": (
                            "function(context) { return context.dataset.label + ': ' + "
                            "context.parsed.y.toLocaleString() + '명'; }"
                        )
                    },
                },
            },
            "scales": {
                "x": {
                    "title": {"display": True, "text": "연령대"},
                    "ticks": {"maxRotation": 45, "minRotation": 45},
                },
                "y": {
                    "title": {"display": True, "text": "유동인구 (명)"},
                    "beginAtZero": True,
                    "ticks": {
                        "callback": (
                            "function(value) { return value.toLocaleString(); }"
                        )
                    },
                },
            },
        },
    }


def get_chartjs_yearly_trend_config():
    """연도별 업종별 총 가맹점수 추이 - Chart.js 라인 차트 설정"""
    yearly_trend_data = YEARLY_TREND_DATA
    years = sorted(list(yearly_trend_data["도소매"].keys()))

    return {
        "type": "line",
        "data": {
            "labels": years,
            "datasets": [
                {
                    "label": "도소매",
                    "data": [yearly_trend_data["도소매"][year] for year in years],
                    "borderColor": "#1f77b4",
                    "backgroundColor": "rgba(31, 119, 180, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "circle",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
                {
                    "label": "서비스",
                    "data": [yearly_trend_data["서비스"][year] for year in years],
                    "borderColor": "#ff7f0e",
                    "backgroundColor": "rgba(255, 127, 14, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "rect",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
                {
                    "label": "외식",
                    "data": [yearly_trend_data["외식"][year] for year in years],
                    "borderColor": "#2ca02c",
                    "backgroundColor": "rgba(44, 160, 44, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "triangle",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
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
                "legend": {"display": True, "position": "top"},
                "tooltip": {
                    "callbacks": {
                        "label": (
                            "function(context) { return context.dataset.label + ': ' + "
                            "context.parsed.y.toLocaleString() + '개'; }"
                        )
                    },
                },
            },
            "scales": {
                "x": {
                    "title": {"display": True, "text": "연도"},
                    "grid": {"display": True, "alpha": 0.3},
                },
                "y": {
                    "title": {"display": True, "text": "총 가맹점수 (개)"},
                    "beginAtZero": True,
                    "grid": {"display": True, "alpha": 0.3},
                    "ticks": {
                        "callback": (
                            "function(value) { return value.toLocaleString(); }"
                        )
                    },
                },
            },
        },
    }


def get_chartjs_time_period_config():
    """시간대별 유동인구 변화 - Chart.js 라인 차트 설정"""
    time_period_data = TIME_PERIOD_DATA
    time_labels = list(time_period_data.keys())
    time_values = list(time_period_data.values())

    return {
        "type": "line",
        "data": {
            "labels": time_labels,
            "datasets": [
                {
                    "label": "유동인구",
                    "data": time_values,
                    "borderColor": "#ff6b6b",
                    "backgroundColor": "rgba(255, 107, 107, 0.1)",
                    "borderWidth": 3,
                    "pointStyle": "circle",
                    "pointRadius": 8,
                    "pointHoverRadius": 10,
                    "fill": True,
                    "tension": 0.4,
                },
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "시간대별 유동인구 변화",
                    "font": {"size": 16, "weight": "bold"},
                },
                "legend": {"display": True, "position": "top"},
                "tooltip": {
                    "callbacks": {
                        "label": (
                            "function(context) { return context.dataset.label + ': ' + "
                            "context.parsed.y.toLocaleString() + '명'; }"
                        )
                    },
                },
            },
            "scales": {
                "x": {
                    "title": {"display": True, "text": "시간대"},
                    "grid": {"display": True, "alpha": 0.3},
                },
                "y": {
                    "title": {"display": True, "text": "유동인구 (명)"},
                    "beginAtZero": True,
                    "grid": {"display": True, "alpha": 0.3},
                    "ticks": {
                        "callback": (
                            "function(value) { return value.toLocaleString(); }"
                        )
                    },
                },
            },
        },
    }


def get_chartjs_growth_rate_config():
    """연도별 업종별 가맹점수 성장률 - Chart.js 라인 차트 설정"""
    growth_rate_data = GROWTH_RATE_DATA
    years = sorted(
        [year for year in growth_rate_data["도소매"].keys() if year is not None]
    )

    return {
        "type": "line",
        "data": {
            "labels": years,
            "datasets": [
                {
                    "label": "도소매",
                    "data": [growth_rate_data["도소매"][year] for year in years],
                    "borderColor": "#1f77b4",
                    "backgroundColor": "rgba(31, 119, 180, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "circle",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
                {
                    "label": "서비스",
                    "data": [growth_rate_data["서비스"][year] for year in years],
                    "borderColor": "#ff7f0e",
                    "backgroundColor": "rgba(255, 127, 14, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "rect",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
                {
                    "label": "외식",
                    "data": [growth_rate_data["외식"][year] for year in years],
                    "borderColor": "#2ca02c",
                    "backgroundColor": "rgba(44, 160, 44, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "triangle",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "연도별 업종별 가맹점수 성장률",
                    "font": {"size": 16, "weight": "bold"},
                },
                "legend": {"display": True, "position": "top"},
                "tooltip": {
                    "callbacks": {
                        "label": (
                            "function(context) { return context.dataset.label + ': ' + "
                            "context.parsed.y.toFixed(2) + '%'; }"
                        )
                    },
                },
            },
            "scales": {
                "x": {
                    "title": {"display": True, "text": "연도"},
                    "grid": {"display": True, "alpha": 0.3},
                },
                "y": {
                    "title": {"display": True, "text": "성장률 (%)"},
                    "beginAtZero": False,
                    "grid": {"display": True, "alpha": 0.3},
                    "ticks": {
                        "callback": (
                            "function(value) { return value.toFixed(1) + '%'; }"
                        )
                    },
                },
            },
            "elements": {"line": {"tension": 0.1}},
            "interaction": {"intersect": False, "mode": "index"},
        },
    }


def get_chartjs_closing_rate_config():
    """연도별 업종별 평균 폐점률 추이 - Chart.js 라인 차트 설정"""
    closing_rate_data = CLOSING_RATE_DATA
    years = sorted(list(closing_rate_data["도소매"].keys()))

    return {
        "type": "line",
        "data": {
            "labels": years,
            "datasets": [
                {
                    "label": "도소매",
                    "data": [closing_rate_data["도소매"][year] for year in years],
                    "borderColor": "#1f77b4",
                    "backgroundColor": "rgba(31, 119, 180, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "circle",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
                {
                    "label": "서비스",
                    "data": [closing_rate_data["서비스"][year] for year in years],
                    "borderColor": "#ff7f0e",
                    "backgroundColor": "rgba(255, 127, 14, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "rect",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
                {
                    "label": "외식",
                    "data": [closing_rate_data["외식"][year] for year in years],
                    "borderColor": "#2ca02c",
                    "backgroundColor": "rgba(44, 160, 44, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "triangle",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "연도별 업종별 평균 폐점률 추이",
                    "font": {"size": 16, "weight": "bold"},
                },
                "legend": {"display": True, "position": "top"},
                "tooltip": {
                    "callbacks": {
                        "label": (
                            "function(context) { return context.dataset.label + ': ' + "
                            "context.parsed.y.toFixed(1) + '%'; }"
                        )
                    },
                },
            },
            "scales": {
                "x": {
                    "title": {"display": True, "text": "연도"},
                    "grid": {"display": True, "alpha": 0.3},
                },
                "y": {
                    "title": {"display": True, "text": "폐점률 (%)"},
                    "beginAtZero": True,
                    "grid": {"display": True, "alpha": 0.3},
                    "ticks": {
                        "callback": (
                            "function(value) { return value.toFixed(1) + '%'; }"
                        )
                    },
                },
            },
        },
    }


def get_chartjs_opening_closing_rate_config():
    """2024년 업종별 개폐점률 - Chart.js 막대 차트 설정"""
    opening_closing_data = OPENING_CLOSING_RATE_DATA

    # 도소매 데이터
    retail_industries = opening_closing_data["도소매"]["업종"]
    retail_opening = opening_closing_data["도소매"]["개점률"]
    retail_closing = opening_closing_data["도소매"]["폐점률"]

    return {
        "type": "bar",
        "data": {
            "labels": retail_industries,
            "datasets": [
                {
                    "label": "신규 개점률",
                    "data": retail_opening,
                    "backgroundColor": "rgba(54, 162, 235, 0.7)",
                    "borderColor": "#36a2eb",
                    "borderWidth": 1,
                },
                {
                    "label": "폐점률",
                    "data": retail_closing,
                    "backgroundColor": "rgba(255, 99, 132, 0.7)",
                    "borderColor": "#ff6384",
                    "borderWidth": 1,
                },
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "2024년 도소매 업종별 개폐점률",
                    "font": {"size": 16, "weight": "bold"},
                },
                "legend": {"display": True, "position": "top"},
                "tooltip": {
                    "callbacks": {
                        "label": (
                            "function(context) { return context.dataset.label + ': ' + "
                            "context.parsed.y.toFixed(1) + '%'; }"
                        )
                    },
                },
            },
            "scales": {
                "x": {
                    "title": {"display": True, "text": "업종"},
                    "ticks": {"maxRotation": 45, "minRotation": 45},
                },
                "y": {
                    "title": {"display": True, "text": "비율 (%)"},
                    "beginAtZero": True,
                    "ticks": {
                        "callback": (
                            "function(value) { return value.toFixed(1) + '%'; }"
                        )
                    },
                },
            },
        },
    }


def get_chartjs_net_growth_rate_config():
    """연도별 업종별 평균 순증가율 추이 - Chart.js 라인 차트 설정"""
    net_growth_data = NET_GROWTH_RATE_DATA
    years = sorted(list(net_growth_data["도소매"].keys()))

    return {
        "type": "line",
        "data": {
            "labels": years,
            "datasets": [
                {
                    "label": "도소매",
                    "data": [net_growth_data["도소매"][year] for year in years],
                    "borderColor": "#1f77b4",
                    "backgroundColor": "rgba(31, 119, 180, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "circle",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
                {
                    "label": "서비스",
                    "data": [net_growth_data["서비스"][year] for year in years],
                    "borderColor": "#ff7f0e",
                    "backgroundColor": "rgba(255, 127, 14, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "rect",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
                {
                    "label": "외식",
                    "data": [net_growth_data["외식"][year] for year in years],
                    "borderColor": "#2ca02c",
                    "backgroundColor": "rgba(44, 160, 44, 0.1)",
                    "borderWidth": 2,
                    "pointStyle": "triangle",
                    "pointRadius": 6,
                    "pointHoverRadius": 8,
                },
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "연도별 업종별 평균 순증가율 추이",
                    "font": {"size": 16, "weight": "bold"},
                },
                "legend": {"display": True, "position": "top"},
                "tooltip": {
                    "callbacks": {
                        "label": (
                            "function(context) { return context.dataset.label + ': ' + "
                            "context.parsed.y.toFixed(1) + '%'; }"
                        )
                    },
                },
            },
            "scales": {
                "x": {
                    "title": {"display": True, "text": "연도"},
                    "grid": {"display": True, "alpha": 0.3},
                },
                "y": {
                    "title": {"display": True, "text": "순증가율 (%)"},
                    "beginAtZero": False,
                    "grid": {"display": True, "alpha": 0.3},
                    "ticks": {
                        "callback": (
                            "function(value) { return value.toFixed(1) + '%'; }"
                        )
                    },
                },
            },
            "elements": {"line": {"tension": 0.1}},
            "interaction": {"intersect": False, "mode": "index"},
        },
    }


# ===== 사용 예시 =====

if __name__ == "__main__":
    print("=== 가맹점수 분석 및 유동인구 차트 사양 파일 ===")
    print("\n사용 가능한 차트 사양:")
    print(
        "1. Vega-Lite: get_vega_lite_line_chart_spec(), "
        "get_vega_lite_bar_chart_spec(), get_vega_lite_pie_chart_spec()"
    )
    print(
        "2. ECharts: get_echarts_line_chart_option(), "
        "get_echarts_bar_chart_option(), get_echarts_pie_chart_option()"
    )
    print(
        "3. Plotly: get_plotly_line_chart_figure(), "
        "get_plotly_bar_chart_figure(), get_plotly_pie_chart_figure()"
    )
    print(
        "4. Chart.js: get_chartjs_line_chart_config(), "
        "get_chartjs_bar_chart_config(), get_chartjs_pie_chart_config(), "
        "get_chartjs_area_population_config(), get_chartjs_age_gender_config()"
    )

    print("\n=== 데이터 구조 ===")
    print("라인 차트 데이터:", LINE_CHART_DATA)
    print("바 차트 데이터:", BAR_CHART_DATA)
    print("파이 차트 데이터:", GENDER_PIE_DATA)
    print("읍면동별 유동인구 데이터:", AREA_POPULATION_DATA)
    print("연령대별 성별 유동인구 데이터:", AGE_GENDER_DATA)
