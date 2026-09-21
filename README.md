# SK하이닉스 DART 재무분석

SK하이닉스(000660)의 OpenDART 공시를 기반으로 2016~2025년 10개년 연결 재무데이터를 수집하고 재무비율을 분석합니다.

## 분석 기준
첨부된 「재무제표 및 재무비율 실무 가이드」를 기준으로 성장성, 수익성, 현금흐름, 재무안정성, 활동성, 자본효율 및 시장가치 지표를 계산합니다.

## 데이터 출처
- 금융감독원 DART / OpenDART
- 회사 고유번호: `00164779`
- 종목코드: `000660`

## 실행
1. GitHub Actions Secret에 `DART_API_KEY` 등록
2. `python scripts/fetch_dart.py`
3. `python scripts/calculate_ratios.py`

API 키는 저장소에 직접 저장하지 않습니다.
