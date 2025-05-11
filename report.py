# report.py
import os
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Initialize the LangChain ChatOpenAI model
chat = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    openai_api_key= "shashi",
)

def generate_report(
    fmea_df: pd.DataFrame,
    sim_df: pd.DataFrame,
    mtbf: float,
    beta: float,
    eta: float
) -> str:
    # 1. Serialize inputs
    fmea_text = fmea_df.to_csv(index=False)
    sim_summary = (
        f"Total Records: {len(sim_df)}\n"
        f"Devices: {sim_df.dev.nunique()}\n"
        f"Failure Rate: {sim_df['status'].value_counts(normalize=True).get('FAIL',0):.2%}"
    )
    analysis_text = (
        f"MTBF (hours): {mtbf:.2f}\n"
        f"Weibull shape (β): {beta:.2f}\n"
        f"Weibull scale (η): {eta:.2f}"
    )

    # 2. Build LangChain messages
    messages = [
        SystemMessage(content="You are an expert reliability engineer."),
        HumanMessage(
            content=(
                "Using the data below, write a detailed reliability analysis report with:\n"
                "1. Introduction\n"
                "2. Methodology (describe FMEA, simulation setup, analysis)\n"
                "3. Results (highlight MTBF, Weibull)\n"
                "4. Discussion\n"
                "5. Conclusion\n\n"
                f"FMEA Table:\n{fmea_text}\n\n"
                f"Simulation Summary:\n{sim_summary}\n\n"
                f"Analysis Metrics:\n{analysis_text}"
            )
        )
    ]

    # 3. Invoke the LLM via LangChain
    response = chat(messages)
    return response.content