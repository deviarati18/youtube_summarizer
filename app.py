import streamlit as st
import base64  # Make sure to import base64
from scrape_youtube import extract_video_id, get_transcript, extract_metadata, download_thumbnail
from summarize_text import summarize_text
import os

def get_image_base64(image_path):
    """Convert the image to base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def main():       
    # Define the title text and local image path
    title_text = "SunTec Video Summarizer"
    image_path = "suntec_6.png"  # Replace with the actual path to your local image

    # Use HTML and CSS to style the title and image
    html_code = f"""
    <div style="display: flex; align-items: center; margin-bottom: 30px;">
        <img src="data:image/png;base64,{get_image_base64(image_path)}" alt="Local Image" style="width: 50px; height: 50px; margin-right: 15px;">
        <h3 style="font-size: 45px;">{title_text}</h3>
    </div>
    """

    # Display the HTML code using markdown
    st.markdown(html_code, unsafe_allow_html=True)
    
    def get_thumbnail_from_url(url):
        video_id = extract_video_id(url)
        download_thumbnail(video_id)
    
    # Function to get transcript from URL
    def get_transcript_from_url(url):
        video_id = extract_video_id(url)
        transcript = get_transcript(video_id)
        return transcript

    # Function to summarize text
    def summarize_transcript(transcript, lang):
        summary = summarize_text(transcript, lang=lang)
        return summary

    # Interface components
    st.subheader("Enter video URL:")
    st.write("Paste a video link to summarize its content (must have a transcript available)")
    url = st.text_input("URL")

    if st.button("Summarize"):
        if url:
            # After Button is Clicked
            # Display Title and Channel Names
            title, channel = extract_metadata(url)
            st.subheader("Title:")
            st.write(title)
            st.subheader("Channel:")
            st.write(channel)
            
            # Display Thumbnail
            get_thumbnail_from_url(url)
            st.image(os.path.join(os.getcwd(), "thumbnail.jpg"), caption='Thumbnail', use_column_width=True) 
            
            # Display Summary
            transcript = get_transcript_from_url(url)
            summary = summarize_transcript(transcript, 'English')
            st.subheader("Video Summary:")
            st.write(summary)
        else:
            st.warning("Please enter a YouTube URL.")

if __name__ == "__main__":
    main()
