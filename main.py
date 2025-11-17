    import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import re
import time

# -----------------------------
# 유튜브 API 설정
# -----------------------------
api_key = "YOUR_YOUTUBE_API_KEY"  # 여기에 발급받은 API 키 입력
youtube = build('youtube', 'v3', developerKey=api_key)

# -----------------------------
# 댓글 가져오기 함수
# -----------------------------
def get_comments(video_id, max_results=10000):
    comments = []
    next_page_token = None
    total_fetched = 0
    try:
        while True:
            results_to_fetch = min(max_results - total_fetched, 100)  # 한 번에 최대 100개씩
            if results_to_fetch <= 0:
                break

            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=results_to_fetch,
                pageToken=next_page_token,
                textFormat="plainText"
            ).execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
                total_fetched += 1

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
            time.sleep(0.1)  # API 제한을 피하기 위해 잠깐 대기

    except Exception as e:
        st.error(f"댓글 가져오기 오류: {e}")
    return comments

# -----------------------------
# 스트림릿 UI
# -----------------------------
st.title("유튜브 댓글 필터링 사이트")
st.write("유튜브 URL과 찾고 싶은 단어를 입력하면, 해당 단어가 포함된 댓글만 보여줍니다.")

video_url = st.text_input("유튜브 영상 URL 입력")
keyword = st.text_input("검색할 단어 입력")

if st.button("댓글 검색"):
    if not video_url or not keyword:
        st.warning("유튜브 URL과 검색할 단어를 모두 입력해주세요.")
    else:
        # URL에서 videoId 추출
        match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", video_url)
        if match:
            video_id = match.group(1)
            st.info("댓글을 불러오는 중입니다... 최대 10,000개까지 수집합니다.")
            comments = get_comments(video_id, max_results=10000)
            filtered_comments = [c for c in comments if keyword.lower() in c.lower()]
            st.success(f"{len(filtered_comments)}개의 댓글을 찾았습니다.")

            # 결과 표시
            for idx, comment in enumerate(filtered_comments, 1):
                st.write(f"{idx}. {comment}")

            # 엑셀로 저장
            if filtered_comments:
                df = pd.DataFrame(filtered_comments, columns=['댓글'])
                df.to_excel("filtered_comments.xlsx", index=False)
                st.download_button(
                    label="엑셀로 다운로드",
                    data=df.to_excel(index=False),
                    file_name="filtered_comments.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("유효하지 않은 유튜브 URL입니다.")
