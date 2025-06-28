import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import BaseTool
from langchain.document_loaders import PDFLoader
from typing import Optional

class BloodTestReportTool(BaseTool):
    name = "Blood Test Report Reader"
    description = "Tool to read and extract data from blood test report PDF files"

    def _run(self, file_path: Optional[str] = 'data/sample.pdf') -> str:
        """Read data from a blood test report PDF file
        
        Args:
            file_path (str, optional): Path to the PDF file. Defaults to 'data/sample.pdf'.
            
        Returns:
            str: Formatted blood test report content
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found at path: {file_path}")
                
            loader = PDFLoader(file_path=file_path)
            docs = loader.load()

            full_report = ""
            for data in docs:
                content = data.page_content
                
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                    
                full_report += content + "\n\n"
                
            return full_report
            
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

class NutritionTool(BaseTool):
    name = "Nutrition Analyzer"
    description = "Tool to analyze nutrition needs based on blood test results"

    def _run(self, blood_report_data: str) -> str:
        """Analyze nutritional needs from blood test data
        
        Args:
            blood_report_data (str): Blood test report content
            
        Returns:
            str: Nutrition analysis and recommendations
        """
        processed_data = blood_report_data
        
        processed_data = ' '.join(processed_data.split())
                
        return "Nutrition analysis based on blood work:\n" + processed_data[:500] + "..."

class ExerciseTool(BaseTool):
    name = "Exercise Planner"
    description = "Tool to create exercise plans based on health status"

    def _run(self, blood_report_data: str) -> str:
        """Create exercise plan from blood test data
        
        Args:
            blood_report_data (str): Blood test report content
            
        Returns:
            str: Personalized exercise plan
        """
        return "Safe exercise plan based on current health status:\n" + blood_report_data[:500] + "..."
