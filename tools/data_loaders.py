from crewai.tools  import BaseTool
from pydantic import BaseModel, Field
import pandas as pd

class ExcelloaderInput(BaseModel):
    file_path: str = Field(..., description="Path to the Excel file")
    sheet_name: str = Field(None, description="Name of the sheet to read (optional)")
    
class ExcelloaderTool(BaseTool):
    name = "ExcelLoader"
    description = "Load data from an Excel file and return it as a list of dictionaries."
    args_schema = ExcelloaderInput

    def _run(self, file_path: str, sheet_name: str = None) -> list:
        
        try:
            skip_rows = 0
            if sheet_name == "Investment Summary":
                skip_rows = 2
            elif sheet_name == "Holdings":
                skip_rows = 1
                
            df = pd.read_excel(file_path, 
                               sheet_name=sheet_name,
                               skiprows= skip_rows)
            return {
                'sheet_name' : sheet_name,
                'data' : df.to_dict(orient='records'),
                'columns' : df.columns.tolist(),
                'row_count' : len(df)
                }
            
        
        
        except Exception as e:
            return f"Error loading Excel file: {e}"
        
    
    
