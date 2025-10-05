from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Any, Optional, Union, Type
import pandas as pd
import sqlite3

def sanitize_column_name(col):
    """Convert Excel columns to SQLite-safe names"""
    col = str(col).strip()
    col = col.replace(' ', '_')
    col = col.replace('-', '_')
    col = col.replace('%', 'pct')
    col = col.replace('(', '').replace(')', '')
    col = col.replace('/', '_')
    col = col.replace('.', '_')
    if col and col[0].isdigit():
        col = '_' + col
    return col.lower()

class ExcelToSQLiteInput(BaseModel):
    file_path: str = Field(..., description="Path to the Excel file")
    sheet_name: Optional[Union[str, int]] = Field(
        None, description="Name or index of the sheet to read (optional)"
    )
    db_path: str = Field(..., description="Path to the SQLite database file")
    table_name: Optional[str] = Field(
        None, description="Table name to write to (optional, defaults to sanitized sheet name)"
    )

class ExcelToSQLiteTool(BaseTool):
    name: str = "ExcelToSQLiteTool"
    description: str = (
        "Load data from an Excel file and write it to a local SQLite3 database table in one step."
    )
    args_schema: Type[BaseModel] = ExcelToSQLiteInput

    def _run(
        self,
        file_path: str,
        sheet_name: Optional[Union[str, int]] = None,
        db_path: str = None,
        table_name: Optional[str] = None,
    ) -> dict[str, Any] | str:
        try:
            skip_rows = 0
            if sheet_name == "Investors Summary":
                skip_rows = 2
            elif sheet_name == "Holdings":
                skip_rows = 1

            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                skiprows=skip_rows,
            )
            df.columns = [sanitize_column_name(col) for col in df.columns]
            df = df.loc[:, ~df.columns.str.lower().str.startswith('unnamed')]

            # Use sanitized sheet name as table name if not provided
            if not table_name:
                table_name = sanitize_column_name(sheet_name if sheet_name else "sheet1")

            with sqlite3.connect(db_path) as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)

            return {
                "status": "success",
                "sheet_name": sheet_name,
                "db_path": db_path,
                "table_name": table_name,
                "row_count": len(df),
                "columns": df.columns.tolist(),
            }
        except Exception as e:
            return {"error": f"Error loading Excel and writing to SQLite: {e}"}