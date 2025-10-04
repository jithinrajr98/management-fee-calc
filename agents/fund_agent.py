from crewai import Agent

data_agent = Agent(
    role = "Data Loader",
    goal = "load excel data and read/write to sqlite3 database",
)