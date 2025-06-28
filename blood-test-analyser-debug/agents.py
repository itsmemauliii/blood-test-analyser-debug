import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

doctor = Agent(
    role="Senior Doctor",
    goal="Provide accurate medical advice based on blood test reports and patient queries",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced medical professional with 15+ years of experience. "
        "You carefully analyze blood test reports and provide evidence-based recommendations. "
        "You consider all factors before making a diagnosis and always prioritize patient safety."
    ),
    tools=[BloodTestReportTool().read_data_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=True
)

verifier = Agent(
    role="Medical Report Verifier",
    goal="Verify the accuracy and validity of medical reports",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous medical records specialist with a keen eye for detail. "
        "You carefully review all documents to ensure they are valid medical reports "
        "and flag any potential issues or inconsistencies."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

nutritionist = Agent(
    role="Clinical Nutritionist",
    goal="Provide evidence-based nutritional advice based on blood test results",
    verbose=True,
    backstory=(
        "You are a certified nutritionist with expertise in interpreting blood test results. "
        "You provide personalized dietary recommendations based on scientific evidence "
        "and the patient's specific health markers."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

exercise_specialist = Agent(
    role="Exercise Physiologist",
    goal="Create safe and effective exercise plans based on health status",
    verbose=True,
    backstory=(
        "You are a certified exercise specialist with training in adapting workouts "
        "for various health conditions. You create personalized exercise programs "
        "that consider the patient's current health status and limitations."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False
)
