import streamlit as st

# Add PWA configuration to make it installable on mobile
st.set_page_config(
    page_title="AI Plant Doctor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add PWA meta tags
st.markdown("""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#ff006e">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="AI Plant Doctor">
</head>
""", unsafe_allow_html=True)

# Import and run the main app
exec(open('main.py').read())