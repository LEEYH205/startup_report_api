# 테스트용 파일 - 포맷팅 테스트
import os
import sys

import numpy as np
import pandas as pd
from flask import Flask, jsonify, request


def test_function(x, y):
    """테스트 함수"""
    if x > 0:
        return x + y
    else:
        return x - y


class TestClass:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


if __name__ == "__main__":
    app = Flask(__name__)
    print("Hello World!")
