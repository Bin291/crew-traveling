import os
import yaml
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

def load_yaml_config(filename):
    path = os.path.join(os.path.dirname(__file__), "config", filename)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@CrewBase
class TravelPlanner:
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.agents_config = load_yaml_config("agents.yaml")
        self.tasks_config = load_yaml_config("tasks.yaml")

    @agent
    def preference_analyzer(self) -> Agent:
        return Agent(config=self.agents_config["preference_analyzer"], verbose=True)

    @agent
    def destination_presenter(self) -> Agent:
        return Agent(config=self.agents_config["destination_presenter"], verbose=True)

    @agent
    def cultural_advisor(self) -> Agent:
        return Agent(config=self.agents_config["cultural_advisor"], verbose=True)

    @agent
    def weather_forecaster(self) -> Agent:
        return Agent(config=self.agents_config["weather_forecaster"], verbose=True)

    @agent
    def itinerary_planner(self) -> Agent:
        return Agent(config=self.agents_config["itinerary_planner"], verbose=True)

    @agent
    def cost_estimator(self) -> Agent:
        return Agent(config=self.agents_config["cost_estimator"], verbose=True)

    @agent
    def transport_advisor(self) -> Agent:
        return Agent(config=self.agents_config["transport_advisor"], verbose=True)

    @agent
    def accommodation_advisor(self) -> Agent:
        return Agent(config=self.agents_config["accommodation_advisor"], verbose=True)

    @agent
    def feasibility_analyst(self) -> Agent:
        return Agent(config=self.agents_config["feasibility_analyst"], verbose=True)

    def preference_task(self):
        config = self.tasks_config["preference_task"].copy()
        config["agent"] = self.preference_analyzer()
        return Task(config=config)

    # Add similar methods for other tasks as needed, e.g.:
    def intro_task(self):
        config = self.tasks_config["intro_task"].copy()
        config["agent"] = self.destination_presenter()
        return Task(config=config)

    def culture_task(self):
        config = self.tasks_config["culture_task"].copy()
        config["agent"] = self.cultural_advisor()
        return Task(config=config)

    def weather_task(self):
        config = self.tasks_config["weather_task"].copy()
        config["agent"] = self.weather_forecaster()
        return Task(config=config)

    def itinerary_task(self):
        config = self.tasks_config["itinerary_task"].copy()
        config["agent"] = self.itinerary_planner()
        return Task(config=config)

    def cost_task(self):
        config = self.tasks_config["cost_task"].copy()
        config["agent"] = self.cost_estimator()
        return Task(config=config)

    def transport_task(self):
        config = self.tasks_config["transport_task"].copy()
        config["agent"] = self.transport_advisor()
        return Task(config=config)

    def accommodation_task(self):
        config = self.tasks_config["accommodation_task"].copy()
        config["agent"] = self.accommodation_advisor()
        return Task(config=config)

    def feasibility_task(self):
        config = self.tasks_config["feasibility_task"].copy()
        config["agent"] = self.feasibility_analyst()
        return Task(config=config)

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )