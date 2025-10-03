"""
Vercel Serverless Function
업체 맞춤 형용사·키워드 추천 웹 서비스 v2.0
"""

from flask import Flask, request, jsonify, render_template_string
import sys
import os

# 상위 디렉토리를 sys.path에 추가 (keyword_recommender_v2 import를 위해)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from keyword_recommender_v2 import KeywordRecommenderV2
from ai_keyword_recommender import AIKeywordRecommender

app = Flask(__name__)

# 환경변수에서 AI 모드 확인 (기본값: False)
USE_AI = os.getenv("USE_AI", "false").lower() == "true"

# AI 모드라면 AI 추천기 사용, 아니면 기존 알고리즘 사용
if USE_AI:
    try:
        recommender = AIKeywordRecommender()
    except ValueError as e:
        recommender = KeywordRecommenderV2()
        USE_AI = False
else:
    recommender = KeywordRecommenderV2()

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>업체 맞춤 키워드 추천 서비스 v2.0</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }

        .header p {
            opacity: 0.9;
            font-size: 14px;
        }

        .badge-new {
            background: #ff6b6b;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-left: 10px;
        }

        .content {
            padding: 30px;
        }

        .input-section {
            margin-bottom: 30px;
        }

        .input-section label {
            display: block;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }

        .input-section textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
            line-height: 1.6;
        }

        .input-section textarea:focus {
            outline: none;
            border-color: #667eea;
        }

        .button-group {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }

        button {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }

        .btn-secondary:hover {
            background: #e0e0e0;
        }

        .results {
            display: none;
        }

        .results.show {
            display: block;
        }

        .result-card {
            background: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .result-card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .badge {
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }

        .feature-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }

        .feature-tag {
            background: #e3f2fd;
            color: #1976d2;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
            border: 1px solid #bbdefb;
        }

        .keyword-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }

        .keyword-item {
            background: white;
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            text-align: center;
            font-weight: 500;
            transition: all 0.3s;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .keyword-item:hover {
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }

        .keyword-item.selected {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        .keyword-item input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }

        .selection-controls {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .btn-control {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-select-all {
            background: #e3f2fd;
            color: #1976d2;
        }

        .btn-select-all:hover {
            background: #bbdefb;
        }

        .btn-copy-selected {
            background: #667eea;
            color: white;
        }

        .btn-copy-selected:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }

        .btn-clear-selection {
            background: #f0f0f0;
            color: #333;
        }

        .btn-clear-selection:hover {
            background: #e0e0e0;
        }

        .alert {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }

        .alert-title {
            font-weight: 600;
            color: #856404;
            margin-bottom: 8px;
        }

        .alert-content {
            color: #856404;
            font-size: 14px;
        }

        .info-box {
            background: #e8f4f8;
            border: 1px solid #b3e5fc;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
        }

        .info-box ul {
            margin-left: 20px;
            margin-top: 10px;
        }

        .info-box li {
            margin-bottom: 5px;
            color: #0277bd;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .example-box {
            background: #f0f7ff;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-top: 15px;
            border-radius: 5px;
        }

        .example-box h4 {
            color: #667eea;
            margin-bottom: 10px;
        }

        .example-box p {
            color: #555;
            font-size: 13px;
            line-height: 1.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 업체 맞춤 키워드 추천 서비스<span class="badge-new">v2.0</span></h1>
            <p>네이버 플레이스 실제 업체 정보 형식 지원 · AI 기반 형용사·키워드 추천</p>
        </div>

        <div class="content">
            <div class="input-section">
                <label for="businessInfo">📝 업체 정보 입력 (네이버 플레이스 소개글 전체 복사 붙여넣기)</label>
                <textarea
                    id="businessInfo"
                    rows="12"
                    placeholder="예시:
'몸과 마음을 함께 치유하는' 나비한의원은 내원하시는 모든 분들의 건강과 행복을 기원합니다.
세밀한 진단과 체질별 원인 파악을 통해 개인별 맞춤진료를 진행합니다.
매주 월~목 밤 8시 30분까지 야간진료하는 한의원입니다.

<진료과목>
1. 한방비만클리닉 - 다이어트 전문
2. 한방 탈모클리닉 - PDRN 약침 도입
3. 한방피부클리닉 - 여드름, 아토피 치료
...

※ 네이버 플레이스 업체 소개글을 전체 복사해서 붙여넣으면 자동으로 분석합니다!"></textarea>
            </div>

            <div class="example-box">
                <h4>💡 사용 팁</h4>
                <p>
                ✅ <strong>네이버 플레이스 업체 소개</strong>를 그대로 복사해서 붙여넣으세요<br>
                ✅ 진료과목, 메뉴, 서비스 내용 등이 <strong>길게 작성</strong>되어 있어도 자동으로 분석합니다<br>
                ✅ 야간진료, 주말진료, 전문분야 등 <strong>특별한 강점</strong>을 자동으로 감지합니다<br>
                ✅ 한강뷰, 바다뷰 등 <strong>허위 정보는 자동으로 차단</strong>됩니다
                </p>
            </div>

            <div class="button-group">
                <button class="btn-primary" onclick="getRecommendations()">🚀 키워드 추천받기</button>
                <button class="btn-secondary" onclick="clearAll()">🔄 초기화</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI가 업체 정보를 분석하고 있습니다...</p>
            </div>

            <div class="results" id="results">
                <div class="result-card">
                    <h3>🏢 감지된 업종: <span class="badge" id="businessType"></span></h3>
                </div>

                <div class="result-card" id="featuresCard" style="display:none;">
                    <h3>⭐ 특별 강점 (자동 감지)</h3>
                    <div class="feature-tags" id="featureTags"></div>
                </div>

                <div class="result-card" id="blockedCard" style="display:none;">
                    <div class="alert">
                        <div class="alert-title">🚫 차단된 키워드 (허위정보 방지)</div>
                        <div class="alert-content" id="blockedKeywords"></div>
                    </div>
                </div>

                <div class="result-card">
                    <h3>✅ 추천 키워드 (<span id="keywordCount"></span>개)</h3>
                    <p style="color: #666; font-size: 14px; margin-bottom: 10px;">
                        💡 키워드를 선택한 후 "선택한 키워드 복사" 버튼을 클릭하세요
                    </p>
                    <div class="selection-controls">
                        <button class="btn-control btn-select-all" onclick="selectAllKeywords()">✅ 전체 선택</button>
                        <button class="btn-control btn-copy-selected" onclick="copySelectedKeywords()">📋 선택한 키워드 복사</button>
                        <button class="btn-control btn-clear-selection" onclick="clearSelection()">🔄 선택 초기화</button>
                    </div>
                    <div class="keyword-grid" id="keywordGrid"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function getRecommendations() {
            const businessInfo = document.getElementById('businessInfo').value.trim();

            if (!businessInfo) {
                alert('업체 정보를 입력해주세요!');
                return;
            }

            // 로딩 표시
            document.getElementById('loading').classList.add('show');
            document.getElementById('results').classList.remove('show');

            try {
                const response = await fetch('/api/recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ business_info: businessInfo })
                });

                const data = await response.json();
                displayResults(data);
            } catch (error) {
                alert('오류가 발생했습니다: ' + error.message);
            } finally {
                document.getElementById('loading').classList.remove('show');
            }
        }

        function displayResults(data) {
            // 업종 표시
            document.getElementById('businessType').textContent = data.업종;
            document.getElementById('keywordCount').textContent = data.추천개수;

            // 키워드 그리드 생성 (체크박스 포함)
            const grid = document.getElementById('keywordGrid');
            grid.innerHTML = '';
            data.추천키워드.forEach((keyword, index) => {
                const item = document.createElement('div');
                item.className = 'keyword-item';
                item.dataset.keyword = keyword;

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `keyword-${index}`;
                checkbox.className = 'keyword-checkbox';

                const label = document.createElement('label');
                label.htmlFor = `keyword-${index}`;
                label.textContent = keyword;
                label.style.cursor = 'pointer';

                item.appendChild(checkbox);
                item.appendChild(label);

                // 클릭 시 체크박스 토글 및 스타일 변경
                item.onclick = (e) => {
                    if (e.target !== checkbox) {
                        checkbox.checked = !checkbox.checked;
                    }
                    if (checkbox.checked) {
                        item.classList.add('selected');
                    } else {
                        item.classList.remove('selected');
                    }
                };

                checkbox.onchange = () => {
                    if (checkbox.checked) {
                        item.classList.add('selected');
                    } else {
                        item.classList.remove('selected');
                    }
                };

                grid.appendChild(item);
            });

            // 특별 강점
            if (data.특별강점 && data.특별강점.length > 0) {
                document.getElementById('featuresCard').style.display = 'block';
                const featureTags = document.getElementById('featureTags');
                featureTags.innerHTML = '';
                data.특별강점.forEach(feature => {
                    const tag = document.createElement('div');
                    tag.className = 'feature-tag';
                    tag.textContent = feature;
                    featureTags.appendChild(tag);
                });
            } else {
                document.getElementById('featuresCard').style.display = 'none';
            }

            // 차단된 키워드
            if (data.차단된키워드.length > 0) {
                document.getElementById('blockedCard').style.display = 'block';
                document.getElementById('blockedKeywords').textContent =
                    data.차단된키워드.join(', ');
            } else {
                document.getElementById('blockedCard').style.display = 'none';
            }

            // 결과 표시
            document.getElementById('results').classList.add('show');
            document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
        }

        function selectAllKeywords() {
            const checkboxes = document.querySelectorAll('.keyword-checkbox');
            const allChecked = Array.from(checkboxes).every(cb => cb.checked);

            checkboxes.forEach(checkbox => {
                checkbox.checked = !allChecked;
                const item = checkbox.closest('.keyword-item');
                if (checkbox.checked) {
                    item.classList.add('selected');
                } else {
                    item.classList.remove('selected');
                }
            });
        }

        function copySelectedKeywords() {
            const selectedCheckboxes = document.querySelectorAll('.keyword-checkbox:checked');

            if (selectedCheckboxes.length === 0) {
                alert('키워드를 먼저 선택해주세요!');
                return;
            }

            const selectedKeywords = Array.from(selectedCheckboxes).map(cb => {
                return cb.closest('.keyword-item').dataset.keyword;
            });

            const keywordText = selectedKeywords.join(', ');

            navigator.clipboard.writeText(keywordText).then(() => {
                const originalText = document.querySelector('.btn-copy-selected').textContent;
                document.querySelector('.btn-copy-selected').textContent = '✓ 복사됨!';
                setTimeout(() => {
                    document.querySelector('.btn-copy-selected').textContent = originalText;
                }, 1500);
            }).catch(err => {
                alert('복사 실패: ' + err.message);
            });
        }

        function clearSelection() {
            const checkboxes = document.querySelectorAll('.keyword-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
                checkbox.closest('.keyword-item').classList.remove('selected');
            });
        }

        function clearAll() {
            document.getElementById('businessInfo').value = '';
            document.getElementById('results').classList.remove('show');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """메인 페이지"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """키워드 추천 API"""
    data = request.get_json()
    business_info = data.get('business_info', '')

    if not business_info:
        return jsonify({'error': '업체 정보를 입력해주세요'}), 400

    result = recommender.recommend_keywords(business_info)
    return jsonify(result)

# Vercel은 WSGI app을 자동으로 인식
# 'app' 변수만 export하면 됨
