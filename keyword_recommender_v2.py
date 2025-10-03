"""
업체 맞춤 형용사·키워드 추천 시스템 v2.0
- 실제 네이버 플레이스 업체정보 형식 지원
- 장문의 설명에서 핵심 특징 자동 추출
- 위치/시설 기반 모순 검증 강화
"""

import re
import random
from typing import List, Dict, Set

class KeywordRecommenderV2:
    """업체 정보 기반 형용사·키워드 추천 엔진"""
    
    def __init__(self):
        # 업종별 형용사 데이터베이스
        self.keyword_db = {
            # 범용 키워드 풀 (모든 업종에 적용 가능)
            "범용": {
                "품질": ["좋은", "훌륭한", "우수한", "최고의", "탁월한", "뛰어난", "퀄리티높은"],
                "서비스": ["친절한", "세심한", "신속한", "정확한", "꼼꼼한", "배려있는", "상냥한"],
                "시설": ["깨끗한", "쾌적한", "편안한", "넓은", "현대적인", "깔끔한", "아늑한"],
                "가격": ["합리적인", "저렴한", "가성비좋은", "적정한", "양심적인", "투명한"],
                "신뢰": ["믿을수있는", "정직한", "양심적인", "성실한", "진실한", "신뢰할수있는"],
                "만족": ["재방문하는", "후회없는", "만족스러운", "추천하는", "단골", "믿고가는"],
                "키워드": ["실력파", "꼼꼼한", "전문적인", "경험많은", "노하우있는", "베테랑"]
            },
            "한의원": {
                "전문성": ["실력있는", "꼼꼼한", "정확한", "전문적인", "경험많은", "노하우있는", "세심한", "숙련된", "베테랑"],
                "신뢰": ["믿음가는", "신뢰할수있는", "양심적인", "정직한", "친절한", "진심어린", "성실한"],
                "시설": ["깨끗한", "쾌적한", "편안한", "아늑한", "현대적인", "위생적인", "넓은"],
                "치료": ["효과좋은", "맞춤진료하는", "체계적인", "섬세한", "든든한", "확실한", "빠른효과", "근본치료하는"],
                "태도": ["상담잘하는", "설명잘하는", "배려있는", "따뜻한", "친근한", "부담없는"],
                "약침": ["약침잘하는", "시술꼼꼼한", "통증적은", "효과빠른"],
                "특징": ["야간진료", "주말진료", "비대면상담", "개인맞춤", "체질맞춤"],
                "분야": ["다이어트잘하는", "탈모잘보는", "피부잘보는", "통증잘보는", "여성질환전문", "소아전문"],
                "만족": ["재방문하는", "후회없는", "만족스러운", "효과만족", "가성비좋은"],
                "키워드": ["믿고가는", "단골한의원", "추천하는", "찐맛집", "숨은명의", "실력파", "꼼꼼진료"]
            },
            "병원": {
                "전문성": ["실력있는", "꼼꼼한", "정확한", "전문적인", "경험많은", "노하우있는"],
                "신뢰": ["믿음가는", "신뢰할수있는", "양심적인", "정직한", "투명한"],
                "시설": ["깨끗한", "쾌적한", "현대적인", "최신의", "넓은", "위생적인"],
                "태도": ["친절한", "상냥한", "설명잘하는", "세심한", "배려있는"],
                "키워드": ["실력파원장", "꼼꼼진료", "양심의료", "단골병원", "믿고가는"]
            },
            "식당": {
                "맛": ["맛있는", "고소한", "진한", "담백한", "깔끔한", "풍미있는", "감칠맛나는", 
                      "달콤한", "짭짤한", "새콤한", "쌉쌀한", "부드러운", "바삭한", "쫄깃한", "입맛돋는"],
                "품질": ["신선한", "푸짐한", "정갈한", "풍성한", "알찬", "신선도높은", "고급재료", 
                        "정성스러운", "손맛있는", "집밥같은", "깔끔한", "위생적인", "품질좋은"],
                "분위기": ["아늑한", "깔끔한", "넓은", "포근한", "세련된", "모던한", "아기자기한", 
                          "감성있는", "로맨틱한", "트렌디한", "고급스러운", "편안한", "조용한", "활기찬"],
                "서비스": ["친절한", "빠른", "세심한", "상냥한", "서비스좋은", "배려있는", "정중한", 
                          "신속한", "정확한", "꼼꼼한", "따뜻한", "밝은", "웃음많은"],
                "가격": ["가성비갑", "저렴한", "합리적인", "적정한", "양심적인", "투명한", "푸짐한", 
                        "알찬", "넉넉한", "후한", "가성비좋은"],
                "특징": ["야식맛집", "배달맛집", "단체모임", "회식장소", "데이트장소", "가족식당", 
                        "혼밥하기좋은", "포장맛집", "룸있음", "주차편한", "24시간", "심야식당"],
                "음식종류": ["한식맛집", "중식맛집", "일식맛집", "양식맛집", "이탈리안맛집", "중국집", 
                           "일본집", "스테이크맛집", "파스타맛집", "피자맛집", "치킨맛집", "떡볶이맛집"],
                "키워드": ["단골맛집", "재방문각", "숨은맛집", "가성비갑", "찐맛집", "맛집인정", 
                          "인정맛집", "추천맛집", "후회없는", "만족스러운", "믿고가는", "실력파"]
            },
            "술집": {
                "분위기": ["분위기좋은", "감성있는", "로맨틱한", "아늑한", "세련된", "모던한", "트렌디한"],
                "술": ["술맛좋은", "다양한술", "전문적인", "고급술", "수입맥주", "와인전문", "칵테일맛집"],
                "안주": ["안주맛있는", "푸짐한", "다양한안주", "신선한", "정갈한", "고급안주"],
                "모임": ["모임하기좋은", "단체모임", "회식장소", "데이트장소", "친구모임", "야식맛집"],
                "시간": ["늦은밤", "야간영업", "24시간", "심야식당", "밤늦게까지"],
                "키워드": ["술집맛집", "분위기갑", "야식맛집", "모임장소", "데이트맛집", "회식맛집"]
            },
            "카페": {
                "맛": ["맛있는", "고소한", "진한", "부드러운", "풍미있는", "달콤한", "향긋한", "신선한"],
                "커피": ["커피맛좋은", "원두좋은", "에스프레소맛집", "핸드드립전문", "바리스타실력좋은"],
                "디저트": ["디저트맛있는", "케이크맛집", "베이커리좋은", "빵맛있는", "수제디저트"],
                "분위기": ["아늑한", "깔끔한", "감성있는", "포근한", "세련된", "인스타감성", "모던한", "트렌디한"],
                "공간": ["넓은", "쾌적한", "편안한", "조용한", "아기자기한", "루프탑", "테라스있는"],
                "서비스": ["친절한", "빠른", "세심한", "상냥한", "배려있는"],
                "용도": ["작업하기좋은", "공부하기좋은", "데이트하기좋은", "모임하기좋은", "혼자가기좋은"],
                "특징": ["인테리어예쁜", "사진맛집", "감성맛집", "뷰맛집", "힐링되는"],
                "키워드": ["카페맛집", "감성카페", "디저트맛집", "분위기좋은", "커피맛집", "숨은카페", "단골카페", "인생카페"]
            },
            "학원": {
                "강의": ["이해잘되는", "체계적인", "열정적인", "친근한", "재미있는", "알기쉬운"],
                "실력": ["실력있는", "경력많은", "전문적인", "노하우있는", "베테랑"],
                "관리": ["꼼꼼한", "세심한", "케어잘하는", "피드백빠른", "소통잘되는"],
                "분위기": ["쾌적한", "깨끗한", "집중잘되는", "분위기좋은", "아늑한"],
                "키워드": ["실력파강사", "성적UP", "소수정예", "관리철저", "학부모만족"]
            },
            "카센터": {
                "기술": ["실력있는", "꼼꼼한", "정확한", "빠른", "전문적인", "숙련된"],
                "신뢰": ["정직한", "양심적인", "믿을수있는", "투명한", "바가지없는"],
                "가격": ["합리적인", "저렴한", "양심적인", "가성비좋은", "적정한"],
                "서비스": ["친절한", "설명잘하는", "세심한", "신속한", "상냥한"],
                "키워드": ["양심정비", "단골카센터", "정직견적", "실력파사장님", "믿고맡기는"]
            },
            "미용실": {
                "실력": ["솜씨좋은", "센스있는", "실력있는", "꼼꼼한", "섬세한", "테크닉좋은"],
                "결과": ["만족스러운", "예쁜", "자연스러운", "세련된", "트렌디한"],
                "분위기": ["깨끗한", "아늑한", "편안한", "고급스러운", "쾌적한"],
                "태도": ["친절한", "상냥한", "세심한", "배려있는", "친근한"],
                "키워드": ["솜씨甲", "단골미용실", "스타일링굿", "펌맛집", "염색잘하는"]
            },
            "헬스장": {
                "시설": ["최신장비", "넓은공간", "깨끗한", "쾌적한", "현대적인", "전문적인"],
                "운동": ["효과적인", "체계적인", "다양한", "전문적인", "안전한"],
                "지도": ["전문강사", "개인트레이너", "체계적인", "꼼꼼한", "동기부여하는"],
                "분위기": ["활기찬", "긍정적인", "열정적인", "친근한", "편안한"],
                "키워드": ["피트니스센터", "헬스클럽", "요가원", "필라테스", "크로스핏"]
            },
            "네일샵": {
                "기술": ["솜씨좋은", "섬세한", "정교한", "창의적인", "트렌디한"],
                "디자인": ["예쁜", "세련된", "독창적인", "아름다운", "완벽한"],
                "시설": ["깨끗한", "위생적인", "편안한", "아늑한", "모던한"],
                "서비스": ["친절한", "세심한", "꼼꼼한", "배려있는", "상냥한"],
                "키워드": ["네일아트", "젤네일", "매니큐어", "페디큐어", "네일디자인"]
            },
            "반려동물병원": {
                "진료": ["전문적인", "꼼꼼한", "정확한", "신속한", "체계적인"],
                "태도": ["따뜻한", "친절한", "배려있는", "세심한", "상냥한"],
                "시설": ["깨끗한", "위생적인", "편안한", "넓은", "현대적인"],
                "특징": ["응급진료", "야간진료", "주말진료", "비대면상담", "예방접종"],
                "키워드": ["동물병원", "펫클리닉", "수의사", "반려동물", "펫케어"]
            },
            "이사청소": {
                "서비스": ["신속한", "정확한", "꼼꼼한", "전문적인", "체계적인"],
                "품질": ["완벽한", "깨끗한", "세심한", "신뢰할수있는", "만족스러운"],
                "가격": ["합리적인", "투명한", "저렴한", "가성비좋은", "적정한"],
                "특징": ["24시간서비스", "주말가능", "비상연락", "보험가입", "장비완비"],
                "키워드": ["이사업체", "청소업체", "이삿짐센터", "이사도우미", "청소전문"]
            },
            "인테리어": {
                "디자인": ["세련된", "모던한", "트렌디한", "감성있는", "아름다운", "세심한", "창의적인"],
                "기술": ["정교한", "섬세한", "전문적인", "숙련된", "경험많은", "노하우있는", "정확한"],
                "품질": ["고품질", "내구성좋은", "완벽한", "우수한", "최고의", "탁월한", "퀄리티높은"],
                "서비스": ["상담잘하는", "설명잘하는", "A/S좋은", "친절한", "세심한", "배려있는", "신속한"],
                "시설": ["깨끗한", "쾌적한", "넓은", "현대적인", "깔끔한", "편안한", "아늑한"],
                "가격": ["합리적인", "투명한", "적정한", "가성비좋은", "양심적인", "저렴한"],
                "특징": ["맞춤디자인", "개인맞춤", "원스톱서비스", "무료상담", "견적투명", "AS보장"],
                "키워드": ["인테리어맛집", "디자인갑", "실력파", "믿고맡기는", "추천하는", "단골업체"]
            }
        }
        
        # 업종 감지 키워드 (핵심 키워드에 가중치 적용)
        self.business_type_keywords = {
            "한의원": {
                "core": ["한의원", "한방", "침", "뜸", "부항", "추나", "약침"],  # 가중치 3
                "related": ["한약", "경락", "기혈", "체질"]  # 가중치 1
            },
            "병원": {
                "core": ["병원", "의원", "클리닉", "진료", "치료", "원장", "의사"],
                "related": ["치과", "내과", "외과", "피부과", "정형외과"]
            },
            "식당": {
                "core": ["식당", "맛집", "음식점", "레스토랑", "메뉴"],
                "related": ["한식", "중식", "일식", "양식", "이탈리안", "고깃집", "찌개", "국밥", "파스타", "피자", "치킨"]
            },
            "술집": {
                "core": ["술집", "펜", "바", "맥주집", "포차", "이자카야", "와인바", "칵테일바"],
                "related": ["야식", "안주", "회식", "모임", "늦은밤", "심야"]
            },
            "카페": {
                "core": ["카페", "커피", "커피숍", "카페테리아", "에스프레소"],  # 가중치 3
                "related": ["디저트", "베이커리", "빵집", "음료", "라떼", "아메리카노"]  # 가중치 1
            },
            "학원": {
                "core": ["학원", "교습소", "과외", "수업", "강의"],
                "related": ["선생님", "과목", "수학", "영어"]
            },
            "카센터": {
                "core": ["카센터", "정비", "정비소", "수리"],
                "related": ["엔진", "타이어", "세차", "오일"]
            },
            "미용실": {
                "core": ["미용실", "헤어", "헤어샵"],
                "related": ["파마", "염색", "커트"]
            },
            "헬스장": {
                "core": ["헬스장", "헬스클럽", "피트니스", "체육관"],
                "related": ["요가", "필라테스", "크로스핏", "운동", "트레이너", "PT"]
            },
            "네일샵": {
                "core": ["네일샵", "네일"],
                "related": ["매니큐어", "페디큐어", "젤네일", "네일아트", "손톱"]
            },
            "반려동물병원": {
                "core": ["동물병원", "펫클리닉", "수의사"],
                "related": ["반려동물", "펫", "강아지", "고양이", "애완동물"]
            },
            "이사청소": {
                "core": ["이사", "청소", "이삿짐"],
                "related": ["이사업체", "청소업체", "이사도우미", "청소도우미"]
            },
            "인테리어": {
                "core": ["인테리어", "리모델링", "인테리어업체", "인테리어디자인"],
                "related": ["리뉴얼", "가구", "가구점", "조명", "조명업체", "바닥재", "벽지", "타일", "도배", "페인트", "목공", "목재", "건축", "건설", "디자인", "가구인테리어"]
            }
        }
        
    def detect_business_type(self, business_info: str) -> str:
        """업종 자동 감지 (가중치 기반)"""
        business_info_lower = business_info.lower()

        # 각 업종별 키워드 매칭 점수 계산 (가중치 적용)
        scores = {}
        for business_type, keyword_dict in self.business_type_keywords.items():
            score = 0
            # 핵심 키워드: 가중치 3
            core_score = sum(3 for keyword in keyword_dict["core"] if keyword in business_info_lower)
            # 연관 키워드: 가중치 1
            related_score = sum(1 for keyword in keyword_dict["related"] if keyword in business_info_lower)

            scores[business_type] = core_score + related_score

        # 디버깅: 점수 출력 (개발 모드에서만)
        # print(f"[DEBUG] 업종 감지 점수: {scores}")

        # 가장 높은 점수의 업종 반환
        if max(scores.values()) > 0:
            detected_type = max(scores, key=scores.get)
            # print(f"[DEBUG] 감지된 업종: {detected_type} (점수: {scores[detected_type]})")
            return detected_type

        # 점수가 모두 0이면 범용 업종으로 처리
        return "범용"
    
    def extract_special_features(self, business_info: str, business_type: str) -> List[str]:
        """업체의 특별한 강점 추출"""
        info_lower = business_info.lower()
        special_keywords = []
        
        # 야간진료/영업
        if any(x in info_lower for x in ["야간", "밤", "저녁"]) and any(x in info_lower for x in ["진료", "영업"]):
            if "8시" in info_lower or "9시" in info_lower:
                special_keywords.append("야간진료")
        
        # 주말진료/영업
        if any(x in info_lower for x in ["토요일", "일요일", "주말", "토/일"]):
            special_keywords.append("주말진료")
        
        # 비대면 가능
        if any(x in info_lower for x in ["비대면", "온라인", "원격", "전화상담"]):
            special_keywords.append("비대면가능")
        
        # 전문 분야 강조 (한의원/병원)
        if business_type in ["한의원", "병원"]:
            if "비만" in info_lower or "다이어트" in info_lower:
                special_keywords.append("다이어트전문")
            if "탈모" in info_lower:
                special_keywords.append("탈모전문")
            if "피부" in info_lower and "여드름" in info_lower:
                special_keywords.append("피부전문")
            if "통증" in info_lower or "디스크" in info_lower:
                special_keywords.append("통증전문")
            if "여성" in info_lower and any(x in info_lower for x in ["생리", "난임", "산후"]):
                special_keywords.append("여성질환전문")
            if "소아" in info_lower or "청소년" in info_lower:
                special_keywords.append("소아청소년전문")
        
        # 음식점 특별 강점 감지
        if business_type in ["식당", "술집"]:
            # 야식/심야 영업
            if any(x in info_lower for x in ["야식", "심야", "늦은밤", "밤늦게", "24시간"]):
                special_keywords.append("야식맛집")
            
            # 배달 서비스
            if any(x in info_lower for x in ["배달", "포장", "테이크아웃", "딜리버리"]):
                special_keywords.append("배달맛집")
            
            # 단체 모임/회식
            if any(x in info_lower for x in ["회식", "단체", "모임", "룸", "대형테이블"]):
                special_keywords.append("단체모임")
            
            # 데이트 장소
            if any(x in info_lower for x in ["데이트", "커플", "로맨틱", "분위기"]):
                special_keywords.append("데이트장소")
            
            # 가족 식당
            if any(x in info_lower for x in ["가족", "어린이", "아이", "키즈"]):
                special_keywords.append("가족식당")
            
            # 혼밥 친화적
            if any(x in info_lower for x in ["혼밥", "혼자", "1인", "개인"]):
                special_keywords.append("혼밥하기좋은")
            
            # 주차 편의
            if any(x in info_lower for x in ["주차", "주차장", "발렛"]):
                special_keywords.append("주차편한")
            
            # 음식 종류별 특화
            if any(x in info_lower for x in ["한식", "한국", "김치", "된장", "불고기"]):
                special_keywords.append("한식맛집")
            if any(x in info_lower for x in ["중식", "중국", "짜장", "짬뽕", "탕수육"]):
                special_keywords.append("중식맛집")
            if any(x in info_lower for x in ["일식", "일본", "초밥", "라멘", "우동"]):
                special_keywords.append("일식맛집")
            if any(x in info_lower for x in ["양식", "스테이크", "파스타", "피자", "이탈리안"]):
                special_keywords.append("양식맛집")
        
        return special_keywords
    
    def extract_location_features(self, business_info: str) -> Dict[str, bool]:
        """위치/환경 특성 추출"""
        info_lower = business_info.lower()
        
        features = {
            "한강_근처": "한강" in info_lower,
            "한강_직접인접": any(x in info_lower for x in ["한강변", "강변가", "한강뷰"]),
            "바다_근처": any(x in info_lower for x in ["해운대", "광안리", "해변", "바닷가"]),
            "바다_직접인접": any(x in info_lower for x in ["오션뷰", "바다뷰", "해변가", "비치"]),
            "산_근처": "산" in info_lower and "산후" not in info_lower,  # "산후"와 구분
            "주차_불가": any(x in info_lower for x in ["주차불가", "주차장없음", "주차어려움"]),
        }
        
        return features
    
    def get_forbidden_keywords(self, features: Dict[str, bool]) -> Set[str]:
        """위치/시설 기반 금지 키워드 생성"""
        forbidden = set()
        
        # 한강 관련 검증
        if features.get("한강_근처") and not features.get("한강_직접인접"):
            forbidden.update(["한강뷰", "리버뷰", "강이보이는", "한강보이는", "강변뷰"])
        
        # 바다 관련 검증
        if features.get("바다_근처") and not features.get("바다_직접인접"):
            forbidden.update(["바다뷰", "오션뷰", "바닷가보이는", "바다보이는", "해변뷰"])
        
        # 주차 관련 검증
        if features.get("주차_불가"):
            forbidden.update(["주차편한", "주차장넓은", "주차하기좋은", "주차여유로운"])
        
        return forbidden
    
    def recommend_keywords(self, business_info: str, count: int = 20) -> Dict:
        """메인 추천 함수"""
        
        # 1. 업종 감지
        business_type = self.detect_business_type(business_info)
        
        # 2. 특별한 강점 추출
        special_features = self.extract_special_features(business_info, business_type)
        
        # 3. 위치/환경 특성 추출
        location_features = self.extract_location_features(business_info)
        
        # 4. 금지 키워드 생성
        forbidden = self.get_forbidden_keywords(location_features)
        
        # 5. 업종별 키워드 풀 가져오기
        keyword_pool = self.keyword_db.get(business_type, self.keyword_db["범용"])
        
        # 범용 업종이 아닌 경우 범용 키워드와 조합
        if business_type != "범용":
            universal_pool = self.keyword_db["범용"]
            # 범용 키워드의 일부를 추가 (30% 비율)
            universal_ratio = 0.3
            for category, keywords in universal_pool.items():
                if category in keyword_pool:
                    # 기존 키워드에 범용 키워드 일부 추가
                    additional_count = max(1, int(len(keywords) * universal_ratio))
                    additional_keywords = random.sample(keywords, min(additional_count, len(keywords)))
                    keyword_pool[category].extend(additional_keywords)
                else:
                    # 새로운 카테고리면 범용 키워드 추가
                    keyword_pool[category] = keywords[:]
            
            # 하이브리드 로직: 식당으로 감지되었지만 술집 키워드가 많으면 술집 특화 키워드 추가
            # 단, 카페/베이커리는 제외 (상충되는 업종)
            if business_type == "식당":
                pub_keyword_dict = self.business_type_keywords["술집"]
                # 핵심 키워드 가중치 3, 연관 키워드 가중치 1
                pub_score = (
                    sum(3 for keyword in pub_keyword_dict["core"] if keyword in business_info.lower()) +
                    sum(1 for keyword in pub_keyword_dict["related"] if keyword in business_info.lower())
                )

                # 술집 점수가 5점 이상일 때만 하이브리드 적용 (엄격하게)
                if pub_score >= 5:
                    pub_pool = self.keyword_db["술집"]
                    # 술집 특화 키워드 일부 추가 (20% 비율)
                    pub_ratio = 0.2
                    for category, keywords in pub_pool.items():
                        if category in keyword_pool:
                            additional_count = max(1, int(len(keywords) * pub_ratio))
                            additional_keywords = random.sample(keywords, min(additional_count, len(keywords)))
                            keyword_pool[category].extend(additional_keywords)
                        else:
                            # 새로운 카테고리면 술집 키워드 추가
                            keyword_pool[category] = keywords[:]
        
        # 6. 모든 키워드 수집
        all_keywords = []
        for category, keywords in keyword_pool.items():
            all_keywords.extend(keywords)
        
        # 7. 금지 키워드 필터링
        filtered_keywords = [
            kw for kw in all_keywords 
            if not any(forbidden_word in kw for forbidden_word in forbidden)
        ]
        
        # 8. 중복 제거
        filtered_keywords = list(set(filtered_keywords))
        
        # 9. 키워드 선택 (카테고리별 균형)
        selected_keywords = []
        keywords_per_category = max(1, count // len(keyword_pool))
        
        for category, keywords in keyword_pool.items():
            available = [kw for kw in keywords if kw in filtered_keywords]
            selected = random.sample(available, min(keywords_per_category, len(available)))
            selected_keywords.extend(selected)
        
        # 10. 부족한 수량 채우기
        if len(selected_keywords) < count:
            remaining = [kw for kw in filtered_keywords if kw not in selected_keywords]
            if remaining:
                additional = random.sample(remaining, min(count - len(selected_keywords), len(remaining)))
                selected_keywords.extend(additional)
        
        # 11. 정확히 count 개수로 조정
        selected_keywords = selected_keywords[:count]
        
        # 하이브리드 정보 추가
        hybrid_info = ""
        if business_type == "식당":
            pub_keywords = self.business_type_keywords["술집"]
            pub_score = sum(1 for keyword in pub_keywords if keyword in business_info.lower())
            if pub_score > 0:
                hybrid_info = f"식당+술집 하이브리드 (술집 키워드 {pub_score}개 감지)"
        
        return {
            "업종": business_type,
            "추천키워드": selected_keywords,
            "추천개수": len(selected_keywords),
            "차단된키워드": list(forbidden),
            "특별강점": special_features,
            "감지된특성": {k: v for k, v in location_features.items() if v},
            "하이브리드정보": hybrid_info
        }


def main():
    """테스트 실행"""
    recommender = KeywordRecommenderV2()
    
    # 테스트 케이스들
    test_cases = [
        {
            "name": "한의원 테스트",
            "info": """'몸과 마음을 함께 치유하는' 나비한의원은 내원하시는 모든 분들의 건강과 행복을 기원합니다. 
세밀한 진단과 체질별 원인 파악을 통해 개인별 맞춤진료를 진행합니다. 
매주 월~목 밤 8시 30분까지 야간진료하는 한의원입니다. 

<진료과목> 
1. 한방비만클리닉 - 많이 힘들이지 않고 꾸준히 할 수 있는 다이어트 지향
2. 한방 탈모클리닉 - 탈모질환은 대부분 내 몸에 원인이 있습니다.
3. 한방피부클리닉 - 여드름, 아토피, 지루성피부염
4. 한약/보약 처방 - 공진단 / 경옥고
5. 통증클리닉 - 목디스크, 허리디스크, 만성통증, 추나요법
6. 교통사고후유증 - 토/일요일 진료
7. 여성질환클리닉 - 난임/불임, 산전.산후관리, 생리불순
8. 소아/청소년클리닉 - 성장, 감기, 비염
9. 비염클리닉
10. 특수약침치료 - 수면약침, 안심약침, 속편한약침"""
        },
        {
            "name": "헬스장 테스트",
            "info": """프리미엄 피트니스센터입니다. 최신 운동기구와 전문 트레이너가 상주하고 있습니다.
개인 PT, 그룹 레슨, 요가, 필라테스 등 다양한 프로그램을 제공합니다.
주차장 완비, 샤워시설 완비, 24시간 운영합니다."""
        },
        {
            "name": "확장된 식당 테스트 (다양한 특징)",
            "info": """20년 전통의 가족식당입니다. 손님 한 분 한 분 정성을 다해 음식을 만듭니다.
신선한 재료로 정갈한 한식을 제공하며, 가족 단위 손님들이 많이 찾는 맛집입니다.
주차 가능, 룸 있음, 단체 예약 환영합니다. 배달 서비스도 제공하며, 야식도 맛있습니다."""
        },
        {
            "name": "술집 하이브리드 테스트",
            "info": """분위기 좋은 술집입니다. 다양한 안주와 수입맥주를 제공합니다.
회식장소로 인기있고, 데이트하기에도 좋은 곳입니다.
늦은밤까지 영업하며 야식도 맛있습니다."""
        },
        {
            "name": "인테리어 업체 테스트",
            "info": """20년 경력의 전문 인테리어업체입니다. 맞춤 디자인과 정교한 시공으로 고객 만족을 추구합니다.
리모델링, 가구 제작, 조명 설계 등 원스톱 서비스를 제공합니다.
무료 상담, 투명한 견적, 완벽한 A/S를 약속합니다."""
        },
        {
            "name": "범용 업종 테스트 (감지되지 않는 업종)",
            "info": """우리 회사는 고객 만족을 최우선으로 하는 전문 서비스 업체입니다.
친절한 직원들과 깨끗한 환경에서 최고의 서비스를 제공합니다.
합리적인 가격과 신속한 서비스로 고객님께 만족을 드립니다."""
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"테스트 {i}: {test_case['name']}")
        print("="*80)
        print(f"📥 입력 정보 (일부): {test_case['info'][:100]}...\n")
        
        result = recommender.recommend_keywords(test_case['info'])
        
        print(f"🏢 감지된 업종: {result['업종']}")
        
        if result['특별강점']:
            print(f"\n⭐ 특별 강점:")
            for feature in result['특별강점']:
                print(f"  - {feature}")
        
        print(f"\n✅ 추천 키워드 ({result['추천개수']}개):")
        for idx, keyword in enumerate(result['추천키워드'], 1):
            print(f"  {idx:2d}. {keyword}")
        
        if result['차단된키워드']:
            print(f"\n🚫 차단된 키워드: {', '.join(result['차단된키워드'])}")
        
        if result['감지된특성']:
            print(f"\n🔍 감지된 특성:")
            for feature in result['감지된특성'].keys():
                print(f"  - {feature}")
        
        print(f"\n💡 하이브리드 방식 적용:")
        if result['업종'] == "범용":
            print("  - 범용 키워드 풀 사용 (업종 감지 실패 시)")
        else:
            print(f"  - {result['업종']} 전용 키워드 + 범용 키워드 조합 (30% 비율)")
            if result.get('하이브리드정보'):
                print(f"  - {result['하이브리드정보']}")


if __name__ == "__main__":
    main()
