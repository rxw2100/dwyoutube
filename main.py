import streamlit as st
from googleapiclient.discovery import build
import pandas as pd

# -----------------------------
# 유튜브 API 설정
# -----------------------------
api_key = "YOUR_YOUTUBE_API_KEY"  # 여기에 발급받은 API 키 입력
youtube = build('youtube', 'v3', developerKey=api_key)

# -----------------------------
# 댓글 가져오기 함수
# -----------------------------
def get_comments(video_id, max_results=100):
    comments = []
    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        ).execute()

        while response:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            if 'nextPageToken' in response:
                response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=max_results,
                    pageToken=response['nextPageToken'],
                    textFormat="plainText"
                ).execute()
            else:
                break
    except Exception as e:
        st.error(f"댓글 가져오기 오류: {e}")
    return comments

# -----------------------------
# 스트림릿 UI
# -----------------------------
st.title("유튜브 댓글 필터링 사이트")
st.write("유튜브 URL과 찾고 싶은 단어를 입력하면, 해당 단어가 포함된 댓글만 보여줍니다.")

# 유튜브 URL 입력
video_url = st.text_input("유튜브 영상 URL 입력")
keyword = st.text_input("검색할 단어 입력")

if st.button("댓글 검색"):
    if not video_url or not keyword:
        st.warning("유튜브 URL과 검색할 단어를 모두 입력해주세요.")
    else:
        # URL에서 videoId 추출
        import re
        match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", video_url)
        if match:
            video_id = match.group(1)
            st.info("댓글을 불러오는 중입니다...")
            comments = get_comments(video_id, max_results=100)
            filtered_comments = [c for c in comments if keyword.lower() in c.lower()]
            st.success(f"{len(filtered_comments)}개의 댓글을 찾았습니다.")
            
            # 결과 표시
            for idx, comment in enumerate(filtered_comments, 1):
                st.write(f"{idx}. {comment}")
        else:
            st.error("유효하지 않은 유튜브 URL입니다.")
