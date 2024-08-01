import requests
import streamlit as st

HOST = "http://localhost:8000"


def send_message(session_id, message):
    response = requests.post(
        f"{HOST}/chat", json={"session_id": session_id, "message": message}
    )
    return response.json()


def visualize(history):
    turns = history["turns"]
    for idx in range(len(turns) + 1):
        if idx == len(turns):
            if "new_user_input" not in st.session_state:
                st.session_state.new_user_input = ""

            st.text_area(
                "User : ",
                value=st.session_state.new_user_input,
                height=1,
                max_chars=1000,
                key="new_user_input",
                help=None,
                on_change=None,
                args=None,
                kwargs=None,
                placeholder="Enter your query here",
                disabled=False,
                label_visibility="visible",
            )
        else:
            event = turns[idx]
            if not event["is_visible"]:
                continue
            if event["role"] == "user":
                st.text_input(
                    "User : ",
                    value=event["content"],
                    # height=1,
                    # max_chars=1000,
                    key=idx,
                    help=None,
                    on_change=None,
                    args=None,
                    kwargs=None,
                    placeholder="Enter your query here",
                    disabled=True,
                    label_visibility="visible",
                )
            elif event["role"] in ["assistant", "system", "context"]:
                st.write(f"**Civic** : ")
                st.markdown(event["content"])
                st.write("---")


st.title("GatherGov")


chat_sessions = requests.get(f"{HOST}/get_sessions").json()
if not chat_sessions:
    session_id = requests.get(f"{HOST}/create_session").json()
    chat_sessions = [{"session_id": session_id}]
    st.experimental_rerun()


# get the session
session_id = st.sidebar.selectbox(
    "Select a chat session",
    [session["session_id"] for session in chat_sessions],
)


new_session = st.sidebar.button("Create new session")
if new_session:
    session_id = requests.get(f"{HOST}/create_session").json()
    st.experimental_rerun()

history = requests.get(f"{HOST}/chat_history/{session_id}").json()

visualize(history)

*_, send_column = st.columns(8)
with send_column:
    send_button = st.button(" Send", key="send", type="primary")
if send_button:
    user_input = st.session_state.new_user_input
    print(f"getting response for {user_input} with {session_id}")
    if user_input:
        history = send_message(session_id, user_input)
        if history:
            del st.session_state.new_user_input
            st.experimental_rerun()
    else:
        st.warning("Enter some text to get reply...")
