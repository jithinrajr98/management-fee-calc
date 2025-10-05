from agents import data_pipeline_agent
from tasks import LoadDataTask
from crewai import Crew
from config.settings import CSV_PATH,DB_PATH


# define crew

file_path = CSV_PATH
sheet_name = "Investors Summary"
db_path = DB_PATH
table_name = "investors_summary"

crew = Crew(
    name="DataPipelineCrew",
    tasks=[LoadDataTask(file_path, sheet_name, db_path, table_name)],
    agents=[data_pipeline_agent],
    verbose=True,)

if __name__ == "__main__":
    result = crew.kickoff() 
    print(result)