import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# ---------------------------------------------------------
# 1. Page Configuration & SpotnXt Branding Theme
# ---------------------------------------------------------
st.set_page_config(page_title="SpotnXt - Ultimate AI Performance Marketing Engine", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stApp { max-width: 1250px; margin: 0 auto; }
    .brand-header {
        background: linear-gradient(90deg, #0d253f, #01b4e4, #90aea4);
        padding: 25px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(1, 180, 228, 0.3);
    }
    .sub-tag {
        font-size: 14px;
        color: #E2E8F0;
        margin-top: 5px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.2em;
        background: linear-gradient(90deg, #01b4e4, #00d2ff);
        color: black;
        font-weight: bold;
        font-size: 16px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <h1>🚀 SpotnXt AI - Performance Marketing & Meta Ads Suite</h1>
        <div class="sub-tag">Presented by CK College of Engineering & Technology & StartupTN-CavinKare Foundation</div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Gemini API Client Initialization & Auto-Fallback
# ---------------------------------------------------------
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Gemini API Key is missing! Please set it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

def generate_content_with_fallback(contents):
    # Try models in order of best performance
    models_to_try = ['gemini-1.5-flash', 'gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    last_error = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(contents)
            return response.text
        except Exception as e:
            last_error = e
            continue
            
    raise Exception(f"All models failed. Last error: {last_error}")

# ---------------------------------------------------------
# 3. System Prompt Definition
# ---------------------------------------------------------
SPOTNXT_SYSTEM_PROMPT = """
You are SpotnXt AI, an elite AI-powered Performance Marketing Engine developed for SpotnXt (presented by CK College of Engineering & Technology & StartupTN-CavinKare Foundation). 

Your core mandate is to analyze user requests for any business, product, or shop and generate a complete, high-converting Meta Ads campaign strategy based on the Meta Ads Algorithm.

CRITICAL RULES & LANGUAGE POLICY:
1. MULTILINGUAL CAPABILITY: Automatically detect the language of the user's input (e.g., Tamil, Tanglish, English, Hindi, etc.). ALWAYS generate your entire output in the EXACT same language/style as the user's input.
2. SPOTNXT BRANDING: All recommendations and creative outputs belong to SpotnXt. Explicitly mention that posters and ad creative suggestions must include the "SpotnXt" logo as a visual watermark.
3. META ADS ALGORITHM KNOWLEDGE: Apply Meta's core ad auction principles (Total Value = Bid x Estimated Action Rate + User Value). Optimize for CTR, CPC, conversion rates, and regional user engagement trends.

WHEN A USER PROVIDES A BUSINESS / PRODUCT (e.g., "biryani shop", "skincare", "apparel brand"):
Generates a structured performance marketing proposal with the following sections:

1. 🚀 SpotnXt Campaign Strategy Overview
   - Business Category & Niche Analysis
   - Objective (Traffic, Lead Gen, Conversions, Brand Awareness)

2. 🖼️ Poster & Visual Creative Direction (Image Generation Prompt)
   - Visual Scene Description: Detailed visual storyboard for an AI image generator (e.g., DALL-E / Midjourney).
   - Hook Text Overlay: High-converting headline in the user's language.
   - Design Cues: Color palette and emotional triggers.
   - Branding Rule: Include "Overlaid with the official SpotnXt logo watermark".

3. 📍 Recommended Platforms & Format
   - Best Platforms: (e.g., Instagram Reels, Facebook Feed, Instagram Story, Carousel).
   - Reason: Why this format performs best for this specific product based on Meta Ads engagement data.

4. ⏰ Best Posting Time & Regional Schedule
   - Best Days of the Week: (e.g., Wednesday, Friday, Saturday).
   - Best Time Slots: Local region time (e.g., 6:00 PM - 9:30 PM).
   - Regional Context: Tailored to target geographic trends.

5. 🎯 Target Audience Profiling (Meta Ads Parameters)
   - Age Group: Specific range (e.g., 18 - 35 years).
   - Gender: Targeted demographic mix.
   - Detailed Targeting (Interests & Behaviors): Specific Meta Ad interest keywords.

6. ✍️ Ad Copy Copilot (High Converting Text)
   - Hook (First 3 seconds capture)
   - Main Body Text
   - Call to Action (CTA) button suggestion

7. 💡 Meta Algorithm Optimization Tips
   - Key factors influencing performance (Estimated Action Rate, Ad Relevance Diagnostics, Landing Page Speed).
   - A/B Testing recommendation.

8. 🔌 SpotnXt API Integration Note
   - A brief note explaining how this strategy integrates seamlessly with the SpotnXt Performance Marketing Engine.

Be highly professional, structured, creative, and strictly adhere to the user's input language.
"""

# ---------------------------------------------------------
# 4. Sidebar Controls & Feature Navigation
# ---------------------------------------------------------
st.sidebar.header("🎯 SpotnXt Engine Setup")

mode = st.sidebar.radio("Select SpotnXt AI Tool:", [
    "🚀 Full SpotnXt Meta Strategy (8-Section)",
    "📊 Analyze Banner & Predict CTR",
    "🧪 A/B Testing Creative Generator",
    "🛡️ Meta Ad Policy & Compliance Checker",
    "📢 Multi-Platform Campaign Converter",
    "⚔️ Competitor Spy & Counter-Strategy",
    "💰 Ad Budget & ROI Predictor"
])

# ---------------------------------------------------------
# 5. User Inputs & Execution Logic
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Input Configuration")
    
    if mode == "🚀 Full SpotnXt Meta Strategy (8-Section)":
        user_input = st.text_area(
            "Enter your Business, Shop, or Product Details:",
            placeholder="e.g., Tirupur-la oru readymade dress shop vachurukken OR Sri Krishna Sweet Stall in Chennai",
            height=120
        )
        uploaded_file = st.file_uploader("Optional: Upload Existing Ad Banner (JPG/PNG)", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Creative", use_column_width=True)

    else:
        business_type = st.text_input("🏪 Business / Product Name", placeholder="e.g. Sri Krishna Sweet Stall, Fitness Gym")
        target_aud = st.text_input("👥 Target Audience", placeholder="e.g. Sweets Lovers, Families, Youth")
        location = st.text_input("📍 Target Location", placeholder="e.g. Chennai, Tamil Nadu")

        if mode in ["📊 Analyze Banner & Predict CTR", "🛡️ Meta Ad Policy & Compliance Checker"]:
            uploaded_file = st.file_uploader("Upload Ad Banner (JPG/PNG)", type=["jpg", "png", "jpeg"])
            if uploaded_file:
                img = Image.open(uploaded_file)
                st.image(img, caption="Uploaded Creative", use_column_width=True)

        elif mode == "⚔️ Competitor Spy & Counter-Strategy":
            competitor_name = st.text_input("🕵️ Competitor Brand Name", placeholder="e.g. A2B Sweets")

        elif mode == "💰 Ad Budget & ROI Predictor":
            budget = st.number_input("💵 Daily Budget (in ₹ INR)", min_value=100, value=1000, step=100)

    action_btn = st.button("🚀 Execute SpotnXt AI Engine")

with col2:
    if action_btn:
        with st.spinner("SpotnXt AI Engine is running..."):
            try:
                if mode == "🚀 Full SpotnXt Meta Strategy (8-Section)":
                    if not user_input.strip():
                        st.warning("Please enter your business or product details!")
                    else:
                        full_prompt = f"{SPOTNXT_SYSTEM_PROMPT}\n\nUser Input Request: {user_input}"
                        if uploaded_file:
                            output = generate_content_with_fallback([img, full_prompt])
                        else:
                            output = generate_content_with_fallback([full_prompt])
                        st.subheader("📊 SpotnXt Performance Proposal")
                        st.markdown(output)

                elif mode == "📊 Analyze Banner & Predict CTR":
                    if not uploaded_file:
                        st.error("Please upload an image first!")
                    else:
                        prompt = f"{SPOTNXT_SYSTEM_PROMPT}\nAnalyze this ad banner for {business_type} targeting {target_aud} in {location}."
                        output = generate_content_with_fallback([img, prompt])
                        st.subheader("📊 Ad Analysis & CTR Prediction")
                        st.markdown(output)

                elif mode == "🧪 A/B Testing Creative Generator":
                    prompt = f"{SPOTNXT_SYSTEM_PROMPT}\nCreate 2 A/B Test Campaign Variations for {business_type} targeting {target_aud} in {location}."
                    output = generate_content_with_fallback([prompt])
                    st.subheader("🧪 A/B Testing Campaign Output")
                    st.markdown(output)

                elif mode == "🛡️ Meta Ad Policy & Compliance Checker":
                    if not uploaded_file:
                        st.error("Please upload an image!")
                    else:
                        prompt = f"{SPOTNXT_SYSTEM_PROMPT}\nAudit this ad image for {business_type} against Meta Ad policies."
                        output = generate_content_with_fallback([img, prompt])
                        st.subheader("🛡️ Meta Policy Audit Report")
                        st.markdown(output)

                elif mode == "📢 Multi-Platform Campaign Converter":
                    prompt = f"{SPOTNXT_SYSTEM_PROMPT}\nGenerate platform-specific ad copies for {business_type} targeting {target_aud}."
                    output = generate_content_with_fallback([prompt])
                    st.subheader("📢 Multi-Platform Copy Suite")
                    st.markdown(output)

                elif mode == "⚔️ Competitor Spy & Counter-Strategy":
                    prompt = f"{SPOTNXT_SYSTEM_PROMPT}\nAnalyze competitor '{competitor_name}' against {business_type} in {location}."
                    output = generate_content_with_fallback([prompt])
                    st.subheader("⚔️ Competitor Intelligence Report")
                    st.markdown(output)

                elif mode == "💰 Ad Budget & ROI Predictor":
                    prompt = f"{SPOTNXT_SYSTEM_PROMPT}\nCalculate expected metrics for Daily Budget ₹{budget} for {business_type} targeting {target_aud} in {location}."
                    output = generate_content_with_fallback([prompt])
                    st.subheader("💰 ROI & Budget Forecast")
                    st.markdown(output)

            except Exception as e:
                st.error(f"Execution Error: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8;'>Powered by SpotnXt Performance Marketing Engine | Presented by CK College of Engineering & Technology & StartupTN-CavinKare Foundation</p>", unsafe_allow_html=True)
