from crewai import Task
from tools import BloodTestReportTool

help_patients = Task(
    description="Analyze the patient's blood test report and provide a comprehensive health assessment based on their query: {query}",
    expected_output="""
    A detailed analysis of the blood test report including:
    - Summary of key findings
    - Interpretation of abnormal values
    - Potential health implications
    - Recommended next steps or follow-up tests
    - Answers to the patient's specific questions
    """,
    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)

nutrition_analysis = Task(
    description="Analyze the blood test results and provide personalized nutritional recommendations based on the values. Patient query: {query}",
    expected_output="""
    A nutrition plan including:
    - Foods to include/avoid based on test results
    - Recommended supplements (if medically indicated)
    - Lifestyle modifications
    - Scientific references supporting recommendations
    """,
    agent=nutritionist,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)

exercise_planning = Task(
    description="Create a safe exercise plan based on the patient's blood test results and health status. Patient query: {query}",
    expected_output="""
    An exercise prescription including:
    - Recommended types of exercise
    - Intensity and duration guidelines
    - Contraindications or precautions
    - Gradual progression plan
    """,
    agent=exercise_specialist,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)

verification = Task(
    description="Verify the validity of the uploaded blood test report and confirm it contains all necessary components",
    expected_output="""
    Verification report including:
    - Confirmation if document is a valid blood test report
    - Identification of any missing components
    - Assessment of report completeness
    - Any potential issues noted
    """,
    agent=verifier,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False
)
