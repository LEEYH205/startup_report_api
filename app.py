#!/usr/bin/env python3
"""
가맹점수 분석 차트 API 서버
FE에서 차트 사양을 가져올 수 있는 REST API를 제공합니다.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import json
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

app = Flask(__name__)
CORS(app)  # CORS 활성화

# Swagger API 설정
api = Api(
    app,
    version='1.0',
    title='가맹점수 분석 차트 API',
    description='가맹점수 분석 결과를 차트 사양(spec) 형태로 제공하는 REST API',
    doc='/docs',
    default='charts',
    default_label='차트 관련 API',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY'
        }
    }
)

# API 모델 정의
chart_response_model = api.model('ChartResponse', {
    'message': fields.String(description='응답 메시지'),
    'data': fields.Raw(description='차트 사양 데이터')
})

error_model = api.model('Error', {
    'error': fields.String(description='에러 메시지'),
    'status': fields.Integer(description='HTTP 상태 코드')
})

# 차트 네임스페이스
charts_ns = api.namespace('api/charts', description='차트 사양 관련 API')
data_ns = api.namespace('api/data', description='원본 데이터 관련 API')

@app.route('/')
def index():
    """API 루트 엔드포인트"""
    return jsonify({
        "message": "가맹점수 분석 차트 API 서버",
        "version": "1.0.0",
        "endpoints": {
            "charts": "/api/charts",
            "data": "/api/data",
            "vega_lite": "/api/charts/vega_lite",
            "echarts": "/api/charts/echarts",
            "plotly": "/api/charts/plotly",
            "chartjs": "/api/charts/chartjs"
        }
    })

@charts_ns.route('/')
class AllCharts(Resource):
    @api.doc('get_all_charts')
    @api.response(200, 'Success', chart_response_model)
    def get(self):
        """모든 차트 라이브러리의 사양을 반환"""
        return {
            "message": "모든 차트 사양 조회 성공",
            "data": {
                "vega_lite": {
                    "line_chart": get_vega_lite_line_chart_spec(),
                    "bar_chart": get_vega_lite_bar_chart_spec()
                },
                "echarts": {
                    "line_chart": get_echarts_line_chart_option(),
                    "bar_chart": get_echarts_bar_chart_option()
                },
                "plotly": {
                    "line_chart": get_plotly_line_chart_figure(),
                    "bar_chart": get_plotly_bar_chart_figure()
                },
                "chartjs": {
                    "line_chart": get_chartjs_line_chart_config(),
                    "bar_chart": get_chartjs_bar_chart_config()
                }
            }
        }

@charts_ns.route('/vega_lite')
class VegaLiteCharts(Resource):
    @api.doc('get_vega_lite_charts')
    @api.param('type', '차트 타입 (line, bar, all)', enum=['line', 'bar', 'all'])
    @api.response(200, 'Success')
    def get(self):
        """Vega-Lite 차트 사양만 반환"""
        chart_type = request.args.get('type', 'all')
        
        if chart_type == 'line':
            return get_vega_lite_line_chart_spec()
        elif chart_type == 'bar':
            return get_vega_lite_bar_chart_spec()
        else:
            return {
                "line_chart": get_vega_lite_line_chart_spec(),
                "bar_chart": get_vega_lite_bar_chart_spec()
            }

@charts_ns.route('/echarts')
class EChartsCharts(Resource):
    @api.doc('get_echarts_charts')
    @api.param('type', '차트 타입 (line, bar, all)', enum=['line', 'bar', 'all'])
    @api.response(200, 'Success')
    def get(self):
        """ECharts 차트 옵션만 반환"""
        chart_type = request.args.get('type', 'all')
        
        if chart_type == 'line':
            return get_echarts_line_chart_option()
        elif chart_type == 'bar':
            return get_echarts_bar_chart_option()
        else:
            return {
                "line_chart": get_echarts_line_chart_option(),
                "bar_chart": get_echarts_bar_chart_option()
            }

@charts_ns.route('/plotly')
class PlotlyCharts(Resource):
    @api.doc('get_plotly_charts')
    @api.param('type', '차트 타입 (line, bar, all)', enum=['line', 'bar', 'all'])
    @api.response(200, 'Success')
    def get(self):
        """Plotly 차트 figure만 반환"""
        chart_type = request.args.get('type', 'all')
        
        if chart_type == 'line':
            return get_plotly_line_chart_figure()
        elif chart_type == 'bar':
            return get_plotly_bar_chart_figure()
        else:
            return {
                "line_chart": get_plotly_line_chart_figure(),
                "bar_chart": get_plotly_bar_chart_figure()
            }

@charts_ns.route('/chartjs')
class ChartJSCharts(Resource):
    @api.doc('get_chartjs_charts')
    @api.param('type', '차트 타입 (line, bar, all)', enum=['line', 'bar', 'all'])
    @api.response(200, 'Success')
    def get(self):
        """Chart.js 차트 설정만 반환"""
        chart_type = request.args.get('type', 'all')
        
        if chart_type == 'line':
            return get_chartjs_line_chart_config()
        elif chart_type == 'bar':
            return get_chartjs_bar_chart_config()
        else:
            return {
                "line_chart": get_chartjs_line_chart_config(),
                "bar_chart": get_chartjs_bar_chart_config()
            }

@data_ns.route('/')
class ChartData(Resource):
    @api.doc('get_chart_data')
    @api.param('type', '데이터 타입 (line, bar, all)', enum=['line', 'bar', 'all'])
    @api.response(200, 'Success')
    def get(self):
        """원본 차트 데이터 반환"""
        data_type = request.args.get('type', 'all')
        
        if data_type == 'line':
            return LINE_CHART_DATA
        elif data_type == 'bar':
            return BAR_CHART_DATA
        else:
            return {
                "line_chart_data": LINE_CHART_DATA,
                "bar_chart_data": BAR_CHART_DATA
            }

@charts_ns.route('/<library>/<chart_type>')
class SpecificChart(Resource):
    @api.doc('get_specific_chart')
    @api.param('library', '차트 라이브러리', enum=['vega_lite', 'echarts', 'plotly', 'chartjs'])
    @api.param('chart_type', '차트 타입', enum=['line', 'bar'])
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request', error_model)
    @api.response(500, 'Internal Server Error', error_model)
    def get(self, library, chart_type):
        """특정 라이브러리의 특정 차트 타입 사양 반환"""
        
        chart_functions = {
            'vega_lite': {
                'line': get_vega_lite_line_chart_spec,
                'bar': get_vega_lite_bar_chart_spec
            },
            'echarts': {
                'line': get_echarts_line_chart_option,
                'bar': get_echarts_bar_chart_option
            },
            'plotly': {
                'line': get_plotly_line_chart_figure,
                'bar': get_plotly_bar_chart_figure
            },
            'chartjs': {
                'line': get_chartjs_line_chart_config,
                'bar': get_chartjs_bar_chart_config
            }
        }
        
        if library not in chart_functions:
            api.abort(400, f"지원하지 않는 라이브러리: {library}")
        
        if chart_type not in chart_functions[library]:
            api.abort(400, f"지원하지 않는 차트 타입: {chart_type}")
        
        try:
            chart_spec = chart_functions[library][chart_type]()
            return chart_spec
        except Exception as e:
            api.abort(500, f"차트 사양 생성 실패: {str(e)}")

@app.route('/health')
def health_check():
    """헬스 체크 엔드포인트"""
    return jsonify({"status": "healthy", "service": "chart-api-server"})

@app.route('/redoc')
def redoc():
    """ReDoc API 문서"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>가맹점수 분석 차트 API - ReDoc</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
        body {
            margin: 0;
            padding: 0;
        }
    </style>
</head>
<body>
    <redoc spec-url="/swagger.json"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js"></script>
</body>
</html>
'''

if __name__ == '__main__':
    print("🚀 가맹점수 분석 차트 API 서버 시작...")
    print("📊 사용 가능한 엔드포인트:")
    print("  - GET /api/charts : 모든 차트 사양")
    print("  - GET /api/charts/{library} : 특정 라이브러리의 차트 사양")
    print("  - GET /api/charts/{library}/{type} : 특정 차트 사양")
    print("  - GET /api/data : 원본 데이터")
    print("  - GET /health : 헬스 체크")
    print("\n🌐 서버가 http://localhost:5001 에서 실행됩니다.")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
