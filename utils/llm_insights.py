
from groq import Groq
import streamlit as st

def generate_llm_insights(prod, log, inv):

    # ---------------------------------------------------
    # COMPUTE IMPORTANT METRICS
    # ---------------------------------------------------

    top_state = (
        prod.groupby("State")["Production_MT"]
        .sum()
        .idxmax()
    )

    risky_state = (
        log.groupby("State")["LogisticsRisk"]
        .mean()
        .idxmax()
    )

    vulnerable_crop = (
        inv.groupby("Crop")["StorageLoss"]
        .mean()
        .idxmax()
    )

    avg_spoilage = round(
        inv["StorageLoss"].mean(),
        2
    )

    avg_delay = round(
        log["DelayHours"].mean(),
        2
    )

    # ---------------------------------------------------
    # PROMPT
    # ---------------------------------------------------

    prompt = f"""
    You are an agricultural supply chain analyst.

    Analyze the following operational metrics and generate
    concise business insights.

    Metrics:

    - Highest production state: {top_state}
    - Highest logistics risk state: {risky_state}
    - Most vulnerable crop: {vulnerable_crop}
    - Average spoilage loss: {avg_spoilage}
    - Average logistics delay: {avg_delay}

    Generate:

    1. Key operational insights
    2. Supply chain risks
    3. Recommendations

    Keep the response concise and business-focused.
    """

    # ---------------------------------------------------
    # GROQ CLIENT
    # ---------------------------------------------------

    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )

    # ---------------------------------------------------
    # LLM RESPONSE
    # ---------------------------------------------------

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content

