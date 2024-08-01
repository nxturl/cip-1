import glob
import json
import os
from collections import Counter, defaultdict
from typing import List, Text

import pandas as pd
import streamlit as st

# files = glob.glob("./ml/data/tmp_insights/*")
# counter = Counter()
# _data_ = {}


# def add_query_to_url(url: Text, query: Text) -> Text:
#     separator = "&" if "?" in url else "?"
#     return f"{url}{separator}{query}"


# def add_timestamp_to_url(url: Text, start: float) -> Text:
#     start = int(start)

#     if "granicus.com" in url:
#         return add_query_to_url(url, f"entrytime={start}")

#     if "youtube.com" in url:
#         return add_query_to_url(url, f"t={start}s")

#     if "swagit.com" in url:
#         return add_query_to_url(url, f"ts={start}")

#     if "opengovideo.com" in url:
#         if "iCurrentPosition" in url:
#             return re.sub(r"iCurrentPosition=\d+", f"iCurrentPosition={start}", url)
#         return add_query_to_url(url, f"iCurrentPosition={start}")

#     return url


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


# completed meetings
files = glob.glob("./ml/data/tmp_transcripts/*.json")
completed_ids = [os.path.basename(x).replace(".json", "") for x in files]

# keyword mentions of chunks
transcripts = []
for file in files:
    transcript = json.load(open(file))
    sentences = transcript["sentences"]
    text = " ".join([x["text"] for x in sentences]).lower()
    if "battery" in text or "lithium" in text:
        transcripts.append(transcript)

json.dump(transcripts, open("./battery_or_litium_meetings.json", "w"))
