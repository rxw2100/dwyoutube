import streamlit as st
import random

st.title("🎉 랜덤 추첨기 🎉")
st.write("참가자 목록을 입력하고 버튼을 누르면 랜덤으로 당첨자를 뽑습니다.")

# 참가자 입력
participants_text = st.text_area("참가자 이름을 한 줄에 하나씩 입력하세요")
participants = [p.strip() for p in participants_text.split("\n") if p.strip()]

# 추첨 인원 선택
num_winners = st.number_input("뽑을 인원 수", min_value=1, max_value=len(participants) if participants else 1, value=1, step=1)

if st.button("추첨하기"):
    if not participants:
        st.warning("참가자를 입력해주세요!")
    elif num_winners > len(participants):
        st.warning("참가자 수보다 많은 인원을 뽑을 수 없습니다.")
    else:
        winners = random.sample(participants, num_winners)
        st.success("🎉 당첨자 발표 🎉")
        for idx, winner in enumerate(winners, 1):
            st.write(f"{idx}. {winner}")
