
import streamlit as st
from pytube import YouTube
import io
import re


st.header("YouTube downloader")

# tweet url needs to have the id number at the end (you can see this url by clicking on the date of the tweet)
url = st.text_input("")

st.write("Paste the video URL in the box. NB A 60min video makes an mp4 of about 330MB.")

# Waits for an input with a tweet 
if url and ".com" in url:
    with st.spinner("Downloading now... Won't be long!"):
        yt = YouTube(url)
        video_title = yt.title
        data = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

         # Sanitize the title to be used as a file name
        safe_title = re.sub(r'[\\/*?:"<>|]', "", video_title)  # Remove disallowed characters in file names
        safe_title = safe_title.replace(' ', '_')  # Replace spaces with underscores


        # Download the stream to a buffer (in-memory file)
        buffer = io.BytesIO()
        data.stream_to_buffer(buffer)

        # Reset buffer pointer to the start
        buffer.seek(0)

        # Use the buffer in your download button
        st.download_button(
            label="Download mp4 file",
            data=buffer,
            mime='video/mp4',
            file_name=f"{safe_title}.mp4"
        )
        st.success("Your video is ready!")