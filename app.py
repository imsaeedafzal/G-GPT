import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# FastAPI endpoint URL
BACKEND_URL = "https://ai-golfguiders.vercel.app/golf/query"


# Initialize saved chats in the session state if not already done
if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = []


def get_golf_response(query):
    try:
        headers = {"x-api-key": os.environ.get("ACCESS_API")}
        payload = {"query": query}
        response = requests.post(BACKEND_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    st.markdown(
        "<h1 style='text-align: center; font-size: 50px;'>GolferGPT</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 style='text-align: center; font-size: 17px;'>Your Own AI Golf Assistant by <u>GolfGuiders</u></h1>",
        unsafe_allow_html=True,
    )

    query = st.text_area("Enter your question here:")

    if st.button("Send"):
        if query.strip():
            with st.spinner("Generating response..."):
                response = get_golf_response(query)
                st.markdown("### Generated Response:")
                st.write(response)

                # Save the chat to the list
                st.session_state.saved_chats.append(
                    {"question": query, "response": response}
                )
        else:
            st.error("Please enter your query.")

    # Display saved chats in the sidebar
    st.sidebar.markdown("### Saved Chats")
    for i, chat in enumerate(st.session_state.saved_chats):
        with st.sidebar.expander(f"Chat {i + 1}"):
            st.markdown(f"**Q:** {chat['question']}")
            st.markdown(f"**A:** {chat['response']}")


if __name__ == "__main__":
    main()
