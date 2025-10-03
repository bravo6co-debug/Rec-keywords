#!/bin/bash

echo "=============================================="
echo "업체 맞춤 키워드 추천 서비스 실행"
echo "=============================================="
echo ""

# 1. 패키지 설치 확인
echo "📦 필요한 패키지 설치 중..."
pip install -q -r requirements.txt

echo "✅ 패키지 설치 완료!"
echo ""

# 2. 테스트 실행 (선택사항)
read -p "먼저 테스트를 실행하시겠습니까? (y/n): " test_choice
if [ "$test_choice" = "y" ] || [ "$test_choice" = "Y" ]; then
    echo ""
    echo "🧪 테스트 실행 중..."
    python keyword_recommender.py
    echo ""
    read -p "웹 서비스를 시작하시겠습니까? (y/n): " web_choice
else
    web_choice="y"
fi

# 3. 웹 서비스 시작
if [ "$web_choice" = "y" ] || [ "$web_choice" = "Y" ]; then
    echo ""
    echo "=============================================="
    echo "🚀 웹 서비스 시작!"
    echo "=============================================="
    echo ""
    echo "📱 브라우저에서 다음 주소로 접속하세요:"
    echo "   http://localhost:5000"
    echo ""
    echo "💡 종료하려면 Ctrl+C를 누르세요"
    echo ""
    python app.py
else
    echo ""
    echo "서비스를 시작하려면 다음 명령어를 실행하세요:"
    echo "  python app.py"
fi
