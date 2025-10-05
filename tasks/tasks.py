from crewai import Crew, Task
from agents.agents import data_pipeline_agent



def LoadDataTask(file_path, sheet_name, db_path, table_name=None):
    return Task(
        description=f"""Load excel data from path {file_path} and sheet {sheet_name}.
        And write the data  it to {db_path} with table name {table_name}""",
        expected_output= "Confirmation of data written to SQLite with table details in JSON format.",
        agent=data_pipeline_agent,
        verbose=True,
    )
    

