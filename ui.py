import glob
import json
import os
from collections import Counter, defaultdict
from typing import List, Text

import streamlit as st

# files = glob.glob("./ml/data/tmp_insights/*")
# counter = Counter()
# _data_ = {}


def add_query_to_url(url: Text, query: Text) -> Text:
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{query}"


def add_timestamp_to_url(url: Text, start: float) -> Text:

    if "youtube" not in url:
        start = start / 1000

    start = int(start)
    if "granicus.com" in url:
        return add_query_to_url(url, f"entrytime={start}")

    if "youtube.com" in url:
        return add_query_to_url(url, f"t={start}s")

    if "swagit.com" in url:
        return add_query_to_url(url, f"ts={start}")

    if "opengovideo.com" in url:
        if "iCurrentPosition" in url:
            return re.sub(r"iCurrentPosition=\d+", f"iCurrentPosition={start}", url)
        return add_query_to_url(url, f"iCurrentPosition={start}")

    return url


# for file in files:
#     data = json.load(open(file))
#     insight = data["insights"]
#     _data_[data["meeting_id"]] = (
#         data["municipality"],
#         data["date"],
#         data["title"],
#         data["source"],
#         data["meeting_id"],
#     )
#     id_idx = [
#         ("62487cba-7ed9-4a20-9ebb-b20d8fd5cedb", 1),
#         ("bE7WGmAwfnY", 2),
#         ("x6HgyvqbPgI", 1),
#         ("q7Jr2-ioV1E", 7),
#         ("q7Jr2-ioV1E", 8),
#         ("siQxuLxaO3E", 8),
#         ("w9pv0sxKZd4", 8),
#     ]
#     if (data["meeting_id"], data["index"]) in id_idx:
#         st.write(
#             data["meeting_id"],
#             data["index"],
#             data["source"],
#             data["title"],
#             data["date"],
#         )
#         # st.markdown(data["text"])
#         # st.write("---")
#         st.write(data["insights"])
#         st.write("\n\n\n")
#         st.write("---")
#         chunk_link = add_timestamp_to_url(data["source"], data["start"])
#         st.write(f"Link to the chunk = {chunk_link}")
#         st.write("---")
#         st.write(data["text"])

#         st.write("---")
#         st.write("---")
#         st.write("---")

# # st.dataframe(
# #     pd.DataFrame(
# #         list(_data_.values()),
# #         columns=["Municipality", "Date", "Title", "Source", "meeting_id"],
# #     )
# # )


# # completed meetings
# files = glob.glob("./ml/data/tmp_transcripts/*.json")
# completed_ids = [os.path.basename(x).replace(".json", "") for x in files]

# # keyword mentions of chunks
# transcripts = []
# for file in files:
#     transcript = json.load(open(file))
#     sentences = transcript["sentences"]
#     text = " ".join([x["text"] for x in sentences]).lower()
#     if "battery" in text or "lithium" in text:
#         transcripts.append(transcript)

# transcripts = json.load(open("./battery_or_litium_meetings.json", "r"))

# for transcript in transcripts:
#     st.write(transcript["meeting_id"])
#     st.write(transcript["title"])
#     st.write(transcript["date"])
#     st.write(transcript["source"])
#     st.write(transcript["municipality"])
#     st.write("\n\n\n")
#     st.write(" ".join([x["text"] for x in transcript["sentences"]]))
#     st.write("---")
#     st.write("\n\n\n")


def dummy_clean_json(text):
    new_text = text.replace("```%json", "").replace("```json", "").replace("```", "")
    return new_text


# files = glob.glob("./ml/data/tmp_total_insights/*.json")

# valid_documents = []

# for file in files:
#     data = json.load(open(file))
#     has_crapped = False
#     has_value = False
#     try:
#         insight = json.loads(dummy_clean_json(data["insights"]))
#         for key, value in insight.items():
#             if value:
#                 has_value = True
#                 break
#     except:
#         has_crapped = True
#         insight = data["insights"]
#         # has_value = True

#     if has_value:  # and data["municipality"] != "OregonDOE":
#         data["chunk_url"] = add_timestamp_to_url(data["source"], data["start"])
#         valid_documents.append(data)
#         # st.write(file)
#         # st.write(data["meeting_id"])
#         # st.write(data["index"])
#         # st.write(data["municipality"])
#         # st.write(data["date"])
#         # st.write(data["title"])
#         # st.write(add_timestamp_to_url(data["source"], data["start"]))
#         # st.write(has_crapped)
#         # st.write(insight)
#         # st.write(data["text"])
#         # st.write("---")


# # json.dump(valid_documents, open("./valid_documents_total.json", "w"), indent=4)

# # st.write(len(valid_documents))

# valid_documents = json.load(open("./valid_documents_total.json", "r"))
# counter = 0
# for i in range(0, len(valid_documents), 300):
#     tmp_data = valid_documents[i : i + 300]
#     json.dump(
#         tmp_data, open(f"./valid_documents_total_bucket_{counter}.json", "w"), indent=4
#     )
#     counter += 1

files = glob.glob("./valid_documents_total_bucket_*.json")
buckets = [f"bucket_{i}" for i in range(len(files))]

bucket_id = st.sidebar.selectbox(
    "Select a bucket of documents to view",
    buckets,
)

# Extract the number from the bucket_id
idx = int(bucket_id.split("_")[1])

file = files[idx]
st.write(idx, files[idx])

with open(file, "r") as f:
    valid_documents = json.load(f)

for data in valid_documents:
    # st.write(data["chunk_url"])
    st.write(data["meeting_id"])
    st.write(data["index"])
    st.write(data["municipality"])
    st.write(data["date"])
    st.write(data["title"])
    st.write(add_timestamp_to_url(data["source"], data["start"]))
    try:
        st.write(json.loads(dummy_clean_json(data["insights"])))
    except:
        st.write(data["insights"])
    st.write(data["text"])
    st.write("---")
