import json
import logging
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class FollowUpType(Enum):
    PROJECT = auto()
    TASK = auto()
    INITIATIVE = auto()
    PROGRAM = auto()


class SessionType(Enum):
    TECHNICAL_RETROSPECTIVE = auto()
    PROCESS_IMPROVEMENT = auto()
    TEAM_WELLBEING = auto()
    STAKEHOLDER_REVIEW = auto()
    LESSONS_LEARNED = auto()


@dataclass
class UpdateArea:
    area: str
    priority: int
    responsible: str
    status: str = "Pending"
    notes: Optional[str] = None


@dataclass
class Session:
    type: SessionType
    date: datetime
    duration: timedelta
    facilitator: str
    status: str = "Scheduled"
    attendees: List[str] = field(default_factory=list)
    outcomes: Optional[str] = None


@dataclass
class Stakeholder:
    name: str
    role: str
    contact: str
    influence_level: str = "Medium"
    engagement_strategy: Optional[str] = None


@dataclass
class Resource:
    name: str
    type: str
    allocation: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> str:
        pass


class TextReportGenerator(ReportGenerator):
    def generate(self, data: Dict[str, Any]) -> str:
        """
        Generates a plain text report from the data.

        Args:
            data (Dict[str, Any]): The follow-up specification data.

        Returns:
            str: The generated plain text report.
        """
        report_lines = []
        report_lines.append(f"Follow-Up Specification: {data['name']}\n")
        report_lines.append("Updates:")
        for update in data["updates"]:
            report_lines.append(f" - {update['area']} (Priority: {update['priority']})")

        report_lines.append("\nSessions:")
        for session in data["sessions"]:
            report_lines.append(
                f" - {session['type']} on {session['date']} for {session['duration']} minutes"
            )

        report_lines.append("\nDebrief Details:")
        for key, value in data["debrief"].items():
            report_lines.append(f" {key}: {value}")

        report_lines.append("\nPlan Details:")
        for key, value in data["plan"].items():
            report_lines.append(f" {key}: {value}")

        report_lines.append("\nStakeholders:")
        for stakeholder in data["stakeholders"]:
            report_lines.append(f" - {stakeholder['name']} ({stakeholder['role']})")

        report_lines.append("\nMetrics:")
        for key, value in data["metrics"].items():
            report_lines.append(f" {key}: {value}")

        report_lines.append("\nTimeline:")
        for key, value in data["timeline"].items():
            report_lines.append(f" {key}: {value}")

        report_lines.append("\nResources:")
        for resource in data["resources"]:
            report_lines.append(
                f" - {resource['name']} ({resource['type']}): {resource['allocation']}%"
            )

        return "\n".join(report_lines)


class HTMLReportGenerator(ReportGenerator):
    def generate(self, data: Dict[str, Any]) -> str:
        """
        Generates an HTML report from the data.

        Args:
            data (Dict[str, Any]): The follow-up specification data.

        Returns:
            str: The generated HTML report.
        """
        html_content = f"<h1>Follow-Up Specification: {data['name']}</h1>"

        html_content += "<h2>Updates</h2><ul>"
        for update in data["updates"]:
            html_content += (
                f"<li>{update['area']} (Priority: {update['priority']})</li>"
            )
        html_content += "</ul>"

        html_content += "<h2>Sessions</h2><ul>"
        for session in data["sessions"]:
            html_content += f"<li>{session['type']} on {session['date']} for {session['duration']} minutes</li>"
        html_content += "</ul>"

        html_content += "<h2>Debrief Details</h2><ul>"
        for key, value in data["debrief"].items():
            html_content += f"<li><strong>{key}:</strong> {value}</li>"
        html_content += "</ul>"

        html_content += "<h2>Plan Details</h2><ul>"
        for key, value in data["plan"].items():
            html_content += f"<li><strong>{key}:</strong> {value}</li>"
        html_content += "</ul>"

        html_content += "<h2>Stakeholders</h2><ul>"
        for stakeholder in data["stakeholders"]:
            html_content += f"<li>{stakeholder['name']} ({stakeholder['role']})</li>"
        html_content += "</ul>"

        html_content += "<h2>Metrics</h2><ul>"
        for key, value in data["metrics"].items():
            html_content += f"<li><strong>{key}:</strong> {value}</li>"
        html_content += "</ul>"

        html_content += "<h2>Timeline</h2><ul>"
        for key, value in data["timeline"].items():
            html_content += f"<li><strong>{key}:</strong> {value}</li>"
        html_content += "</ul>"

        html_content += "<h2>Resources</h2><ul>"
        for resource in data["resources"]:
            html_content += f"<li>{resource['name']} ({resource['type']}): {resource['allocation']}%</li>"
        html_content += "</ul>"

        return html_content


class FollowUpSpecification:
    # A comprehensive class designed to encapsulate and manage the necessary follow-up actions
    # after the completion of a project, task, or initiative. This class facilitates a structured,
    # professional, and thorough approach to post-completion activities, ensuring all aspects
    # of follow-up are addressed systematically.

    def __init__(self, name: str, follow_up_type: FollowUpType = FollowUpType.PROJECT):
        # Initializes the follow-up specifications with detailed information.
        #
        # Parameters:
        # - name (str): The name of the project, task, or initiative.
        # - follow_up_type (FollowUpType): The type of follow-up, defaulting to PROJECT.
        self.name: str = name
        self.follow_up_type: FollowUpType = follow_up_type
        self.update_areas: List[UpdateArea] = []
        self.sessions: List[Session] = []
        self.debrief_details: Dict[str, Any] = {}
        self.plan_details: Dict[str, Any] = {}
        self.stakeholders: List[Stakeholder] = []
        self.metrics: Dict[str, Any] = {}
        self.timeline: Dict[str, datetime] = {}
        self.resources: List[Resource] = []
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        # Sets up and returns a logger for the class.
        logger = logging.getLogger(f"{self.__class__.__name__}_{self.name}")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def add_update_area(
        self, area: str, priority: int, responsible: str, notes: Optional[str] = None
    ) -> None:
        # Adds an area to the list of areas that require updates, with additional metadata.
        #
        # Parameters:
        # - area (str): The area to be updated.
        # - priority (int): The priority level of the update (1-5, with 1 being highest).
        # - responsible (str): The person or team responsible for the update.
        # - notes (Optional[str]): Additional notes or context for the update area.
        if not any(a.area == area for a in self.update_areas):
            self.update_areas.append(
                UpdateArea(
                    area=area,
                    priority=max(
                        1, min(5, priority)
                    ),  # Ensure priority is between 1 and 5
                    responsible=responsible,
                    notes=notes,
                )
            )
            self.logger.info(f"Added update area: {area}")
        else:
            self.logger.warning(f"Update area '{area}' already exists.")

    def add_session(
        self,
        session_type: SessionType,
        date: datetime,
        duration: timedelta,
        facilitator: str,
        attendees: List[str] = [],
    ) -> None:
        # Adds a session to the list of sessions to be conducted, with comprehensive details.
        #
        # Parameters:
        # - session_type (SessionType): The type of session to be conducted.
        # - date (datetime): The scheduled date and time for the session.
        # - duration (timedelta): The planned duration of the session.
        # - facilitator (str): The name of the session facilitator.
        # - attendees (List[str]): List of attendees for the session.
        if not any(s.type == session_type for s in self.sessions):
            self.sessions.append(
                Session(
                    type=session_type,
                    date=date,
                    duration=duration,
                    facilitator=facilitator,
                    attendees=attendees,
                )
            )
            self.logger.info(f"Added session: {session_type.name}")
        else:
            self.logger.warning(f"Session type '{session_type.name}' already exists.")

    def set_debrief_details(
        self,
        date: datetime,
        participants: List[str],
        agenda: List[str],
        expected_outcomes: List[str],
    ) -> None:
        # Sets or updates the details for the debrief session with comprehensive information.
        #
        # Parameters:
        # - date (datetime): The scheduled date and time for the debrief.
        # - participants (List[str]): List of participants for the debrief session.
        # - agenda (List[str]): Detailed agenda items for the debrief.
        # - expected_outcomes (List[str]): Expected outcomes from the debrief session.
        self.debrief_details = {
            "date": date,
            "participants": participants,
            "agenda": agenda,
            "expected_outcomes": expected_outcomes,
            "status": "Planned",
        }
        self.logger.info("Updated debrief details.")

    def set_plan_details(
        self,
        plan_type: str,
        frequency: str,
        responsible_team: str,
        key_activities: List[str],
        success_criteria: List[str],
    ) -> None:
        # Sets or updates the details for the maintenance or action plan with comprehensive information.
        #
        # Parameters:
        # - plan_type (str): The type of plan (e.g., "Maintenance", "Action", "Improvement").
        # - frequency (str): The frequency of plan execution (e.g., "Weekly", "Monthly", "Quarterly").
        # - responsible_team (str): The team responsible for executing the plan.
        # - key_activities (List[str]): List of key activities included in the plan.
        # - success_criteria (List[str]): Criteria for determining the success of the plan.
        self.plan_details = {
            "type": plan_type,
            "frequency": frequency,
            "responsible_team": responsible_team,
            "key_activities": key_activities,
            "success_criteria": success_criteria,
            "status": "Draft",
        }
        self.logger.info(f"Updated {plan_type} plan details.")

    def add_stakeholder(
        self,
        name: str,
        role: str,
        contact: str,
        influence_level: str = "Medium",
        engagement_strategy: Optional[str] = None,
    ) -> None:
        # Adds a stakeholder to the list of involved parties.
        #
        # Parameters:
        # - name (str): The name of the stakeholder.
        # - role (str): The role or position of the stakeholder.
        # - contact (str): Contact information for the stakeholder.
        # - influence_level (str): The level of influence the stakeholder has (e.g., "High", "Medium", "Low").
        # - engagement_strategy (Optional[str]): The strategy for engaging with this stakeholder.
        if not any(s.name == name for s in self.stakeholders):
            self.stakeholders.append(
                Stakeholder(
                    name=name,
                    role=role,
                    contact=contact,
                    influence_level=influence_level,
                    engagement_strategy=engagement_strategy,
                )
            )
            self.logger.info(f"Added stakeholder: {name}")
        else:
            self.logger.warning(f"Stakeholder '{name}' already exists.")

    def set_metrics(
        self,
        success_criteria: Dict[str, Any],
        kpis: Dict[str, Any],
        measurement_frequency: str,
    ) -> None:
        # Sets the metrics for evaluating the success of the follow-up activities.
        #
        # Parameters:
        # - success_criteria (Dict[str, Any]): The criteria for determining success.
        # - kpis (Dict[str, Any]): Key Performance Indicators to be tracked.
        # - measurement_frequency (str): How often the metrics will be measured and reported.
        self.metrics = {
            "success_criteria": success_criteria,
            "kpis": kpis,
            "measurement_frequency": measurement_frequency,
        }
        self.logger.info("Updated metrics and KPIs.")

    def set_timeline(
        self,
        start_date: datetime,
        end_date: datetime,
        milestones: Dict[str, datetime],
        dependencies: Dict[str, List[str]],
    ) -> None:
        # Sets the timeline for the follow-up activities.
        #
        # Parameters:
        # - start_date (datetime): The start date of the follow-up period.
        # - end_date (datetime): The end date of the follow-up period.
        # - milestones (Dict[str, datetime]): Key milestones and their target dates.
        # - dependencies (Dict[str, List[str]]): Dependencies between milestones.
        self.timeline = {
            "start_date": start_date,
            "end_date": end_date,
            "milestones": milestones,
            "dependencies": dependencies,
        }
        self.logger.info("Updated timeline and milestones.")

    def add_resource(
        self,
        name: str,
        type: str,
        allocation: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> None:
        # Adds a resource required for the follow-up activities.
        #
        # Parameters:
        # - name (str): The name of the resource.
        # - type (str): The type of resource (e.g., "Human", "Financial", "Technical").
        # - allocation (float): The allocation percentage or amount for this resource.
        # - start_date (Optional[datetime]): The start date of the resource allocation.
        # - end_date (Optional[datetime]): The end date of the resource allocation.
        if not any(r.name == name for r in self.resources):
            self.resources.append(
                Resource(
                    name=name,
                    type=type,
                    allocation=allocation,
                    start_date=start_date,
                    end_date=end_date,
                )
            )
            self.logger.info(f"Added resource: {name}")
        else:
            self.logger.warning(f"Resource '{name}' already exists.")

    def validate_metrics(self) -> None:
        """
        Validates that all required metrics are set.

        Raises:
            ValueError: If any of the required metrics are missing.
        """
        required_metrics = ["success_criteria", "kpis", "measurement_frequency"]
        for metric in required_metrics:
            if metric not in self.metrics:
                self.logger.error(f"Missing required metric: {metric}")
                raise ValueError(f"Missing required metric: {metric}")

    def generate_followup_specification(self) -> Dict[str, Any]:
        # Generates a comprehensive and structured follow-up specification, encapsulating all aspects of post-completion activities.
        #
        # Returns:
        # Dict[str, Any]: A dictionary containing the detailed follow-up specification.
        self.validate_metrics()
        specification = {
            "name": self.name,
            "type": self.follow_up_type.name,
            "updates": [asdict(update) for update in self.update_areas],
            "sessions": [asdict(session) for session in self.sessions],
            "debrief": self.debrief_details,
            "plan": self.plan_details,
            "stakeholders": [asdict(stakeholder) for stakeholder in self.stakeholders],
            "metrics": self.metrics,
            "timeline": {
                k: v.isoformat()
                if isinstance(v, datetime)
                else {mk: mv.isoformat() for mk, mv in v.items()}
                if k == "milestones"
                else v
                for k, v in self.timeline.items()
            },
            "resources": [asdict(resource) for resource in self.resources],
        }
        self.logger.info("Generated comprehensive follow-up specification.")
        return specification

    def export_to_json(self, filename: str) -> None:
        # Exports the follow-up specification to a JSON file.
        #
        # Parameters:
        # - filename (str): The name of the file to export to.
        with open(filename, "w") as f:
            json.dump(self.generate_followup_specification(), f, indent=4, default=str)
        self.logger.info(f"Exported follow-up specification to {filename}")

    def import_from_json(self, filename: str) -> None:
        """
        Imports a follow-up specification from a JSON file.

        Parameters:
            filename (str): The name of the file to import from.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file content is not valid JSON.
            KeyError: If required keys are missing in the JSON data.
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            self.name = data["name"]
            self.follow_up_type = FollowUpType[data["type"]]
            self.update_areas = [UpdateArea(**update) for update in data["updates"]]
            self.sessions = [
                Session(
                    **{
                        **session,
                        "type": SessionType[session["type"]],
                        "date": datetime.fromisoformat(session["date"]),
                        "duration": timedelta(seconds=session["duration"]),
                    }
                )
                for session in data["sessions"]
            ]
            self.debrief_details = {
                **data["debrief"],
                "date": datetime.fromisoformat(data["debrief"]["date"]),
            }
            self.plan_details = data["plan"]
            self.stakeholders = [
                Stakeholder(**stakeholder) for stakeholder in data["stakeholders"]
            ]
            self.metrics = data["metrics"]
            self.timeline = {
                k: datetime.fromisoformat(v)
                if k in ["start_date", "end_date"]
                else {mk: datetime.fromisoformat(mv) for mk, mv in v.items()}
                if k == "milestones"
                else v
                for k, v in data["timeline"].items()
            }
            self.resources = [
                Resource(
                    **{
                        **resource,
                        "start_date": datetime.fromisoformat(resource["start_date"])
                        if resource["start_date"]
                        else None,
                        "end_date": datetime.fromisoformat(resource["end_date"])
                        if resource["end_date"]
                        else None,
                    }
                )
                for resource in data["resources"]
            ]

            self.logger.info(f"Imported follow-up specification from {filename}")
        except FileNotFoundError as fnf_error:
            self.logger.error(f"File not found: {filename}")
            raise fnf_error
        except json.JSONDecodeError as json_error:
            self.logger.error(f"Invalid JSON format in file: {filename}")
            raise json_error
        except KeyError as key_error:
            self.logger.error(f"Missing key in JSON data: {key_error}")
            raise key_error

    def generate_report(self, report_generator: ReportGenerator) -> str:
        # Generates a formatted report of the follow-up specification using the provided report generator.
        #
        # Parameters:
        # - report_generator (ReportGenerator): The report generator to use for creating the report.
        #
        # Returns:
        # str: A formatted string containing the report.
        data = self.generate_followup_specification()
        report = report_generator.generate(data)
        self.logger.info("Generated follow-up report.")
        return report
