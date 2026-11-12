import json
import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Enumerations for various report components
class DataSourceType(Enum):
    """Enumeration of possible data source types."""

    INTERNAL = auto()
    EXTERNAL = auto()
    PUBLIC = auto()
    PROPRIETARY = auto()
    REAL_TIME = auto()
    HISTORICAL = auto()
    SYNTHETIC = auto()
    FEDERATED = auto()


class AnalysisMethodType(Enum):
    """Enumeration of possible analysis method types."""

    QUANTITATIVE = auto()
    QUALITATIVE = auto()
    PREDICTIVE = auto()
    DESCRIPTIVE = auto()
    DIAGNOSTIC = auto()
    PRESCRIPTIVE = auto()
    EXPLORATORY = auto()
    CAUSAL = auto()


class DeliveryFormatType(Enum):
    """Enumeration of possible delivery format types."""

    PDF = auto()
    INTERACTIVE_DASHBOARD = auto()
    PRESENTATION = auto()
    API = auto()
    RAW_DATA = auto()
    ENCRYPTED_PACKAGE = auto()
    REAL_TIME_FEED = auto()
    AUGMENTED_REALITY = auto()


# Abstract base class for report components
class ReportComponent(ABC):
    """Abstract base class for all report components."""

    @abstractmethod
    def validate(self) -> bool:
        """Validate the component."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the component to a dictionary."""
        pass


@dataclass
class DataSource(ReportComponent):
    """Detailed representation of a data source."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: DataSourceType
    description: str
    limitations: str
    reliability: float  # 0.0 to 1.0
    update_frequency: str
    access_method: str
    last_updated: datetime = field(default_factory=datetime.now)
    data_schema: Optional[Dict[str, Any]] = None
    sample_data: Optional[Any] = None

    def __post_init__(self):
        if not 0 <= self.reliability <= 1:
            raise ValueError("Reliability must be between 0 and 1")

    def validate(self) -> bool:
        """Validate the data source."""
        try:
            assert self.name, "Name is required"
            assert isinstance(self.type, DataSourceType), "Invalid data source type"
            assert 0 <= self.reliability <= 1, "Reliability must be between 0 and 1"
            return True
        except AssertionError as e:
            logger.error(f"DataSource validation failed: {str(e)}")
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert the data source to a dictionary."""
        return asdict(self)


@dataclass
class AnalysisMethod(ReportComponent):
    """Detailed representation of an analysis method."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: AnalysisMethodType
    description: str
    expected_outcomes: str
    limitations: str
    required_tools: List[str]
    complexity: int = field(default=1)  # 1-5 scale
    execution_time: str = field(default="Unknown")
    validation_method: Optional[str] = None

    def __post_init__(self):
        if not 1 <= self.complexity <= 5:
            raise ValueError("Complexity must be between 1 and 5")

    def validate(self) -> bool:
        """Validate the analysis method."""
        try:
            assert self.name, "Name is required"
            assert isinstance(self.type, AnalysisMethodType), (
                "Invalid analysis method type"
            )
            assert 1 <= self.complexity <= 5, "Complexity must be between 1 and 5"
            return True
        except AssertionError as e:
            logger.error(f"AnalysisMethod validation failed: {str(e)}")
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert the analysis method to a dictionary."""
        return asdict(self)


@dataclass
class TargetAudience(ReportComponent):
    """Detailed representation of the target audience."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    expertise_level: str
    key_interests: List[str]
    preferred_formats: List[DeliveryFormatType]
    decision_making_context: str
    technical_proficiency: int = field(default=3)  # 1-5 scale
    data_literacy: int = field(default=3)  # 1-5 scale
    primary_language: str = field(default="English")

    def __post_init__(self):
        if not 1 <= self.technical_proficiency <= 5:
            raise ValueError("Technical proficiency must be between 1 and 5")
        if not 1 <= self.data_literacy <= 5:
            raise ValueError("Data literacy must be between 1 and 5")

    def validate(self) -> bool:
        """Validate the target audience."""
        try:
            assert self.name, "Name is required"
            assert 1 <= self.technical_proficiency <= 5, (
                "Technical proficiency must be between 1 and 5"
            )
            assert 1 <= self.data_literacy <= 5, "Data literacy must be between 1 and 5"
            return True
        except AssertionError as e:
            logger.error(f"TargetAudience validation failed: {str(e)}")
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert the target audience to a dictionary."""
        return asdict(self)


@dataclass
class DeliveryFormat(ReportComponent):
    """Detailed representation of the delivery format."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: DeliveryFormatType
    reasoning: str
    alternatives: List[DeliveryFormatType]
    accessibility_considerations: str
    interactivity_level: int = field(default=1)  # 1-5 scale
    update_frequency: Optional[str] = None
    version_control: bool = False

    def __post_init__(self):
        if not 1 <= self.interactivity_level <= 5:
            raise ValueError("Interactivity level must be between 1 and 5")

    def validate(self) -> bool:
        """Validate the delivery format."""
        try:
            assert isinstance(self.type, DeliveryFormatType), (
                "Invalid delivery format type"
            )
            assert 1 <= self.interactivity_level <= 5, (
                "Interactivity level must be between 1 and 5"
            )
            return True
        except AssertionError as e:
            logger.error(f"DeliveryFormat validation failed: {str(e)}")
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert the delivery format to a dictionary."""
        return asdict(self)


class ReportSection(BaseModel):
    """Pydantic model for a report section."""

    title: str
    content: str
    priority: int = Field(1, ge=1, le=10)
    subsections: List["ReportSection"] = []

    @validator("priority")
    def check_priority(cls, v):
        if not 1 <= v <= 10:
            raise ValueError("Priority must be between 1 and 10")
        return v


class ReportSpecification:
    """
    A comprehensive class designed to encapsulate and manage the specifications
    required for generating a sophisticated intelligence report.
    """

    def __init__(
        self,
        report_title: str,
        data_sources: List[DataSource],
        analysis_methods: List[AnalysisMethod],
        target_audience: TargetAudience,
        delivery_format: DeliveryFormat,
        additional_notes: Optional[str] = None,
    ):
        """
        Constructs the specifications for a sophisticated intelligence report.

        Parameters:
        - report_title (str): The title of the report.
        - data_sources (List[DataSource]): The data sources to be utilized in the report.
        - analysis_methods (List[AnalysisMethod]): The analysis methods to be applied.
        - target_audience (TargetAudience): The report's intended audience.
        - delivery_format (DeliveryFormat): The report's delivery format.
        - additional_notes (Optional[str]): Optional additional notes regarding the report specifications.
        """
        self.id = str(uuid.uuid4())
        self.report_title = report_title
        self.data_sources = data_sources
        self.analysis_methods = analysis_methods
        self.target_audience = target_audience
        self.delivery_format = delivery_format
        self.additional_notes = additional_notes
        self.sections: List[ReportSection] = []
        self.key_findings: List[str] = []
        self.recommendations: List[str] = []
        self.created_at = datetime.now()
        self.last_modified = self.created_at
        self.version = "1.0.0"

        logger.info(f"Created new ReportSpecification with ID: {self.id}")

    def add_section(
        self,
        title: str,
        content: str,
        priority: int = 1,
        parent_section: Optional[ReportSection] = None,
    ):
        """
        Adds a new section to the report specification.

        Parameters:
        - title (str): The title of the section.
        - content (str): The content of the section.
        - priority (int): The priority of the section (1-10).
        - parent_section (Optional[ReportSection]): The parent section, if this is a subsection.
        """
        new_section = ReportSection(title=title, content=content, priority=priority)
        if parent_section:
            parent_section.subsections.append(new_section)
        else:
            self.sections.append(new_section)
        self.last_modified = datetime.now()
        logger.info(f"Added new section: {title}")

    def add_key_finding(self, finding: str):
        """
        Adds a key finding to the report specification.

        Parameters:
        - finding (str): The key finding to be added.
        """
        self.key_findings.append(finding)
        self.last_modified = datetime.now()
        logger.info(f"Added new key finding: {finding[:50]}...")

    def add_recommendation(self, recommendation: str):
        """
        Adds a recommendation to the report specification.

        Parameters:
        - recommendation (str): The recommendation to be added.
        """
        self.recommendations.append(recommendation)
        self.last_modified = datetime.now()
        logger.info(f"Added new recommendation: {recommendation[:50]}...")

    def _detail_data_sources(self) -> List[Dict[str, Any]]:
        """
        Details the data sources for the report.

        Returns:
        List[Dict[str, Any]]: A list of data sources with detailed descriptions and potential limitations.
        """
        return [source.to_dict() for source in self.data_sources]

    def _detail_analysis_methods(self) -> List[Dict[str, Any]]:
        """
        Details the analysis methods for the report.

        Returns:
        List[Dict[str, Any]]: A list of analysis methods with comprehensive descriptions and expected outcomes.
        """
        return [method.to_dict() for method in self.analysis_methods]

    def _detail_target_audience(self) -> Dict[str, Any]:
        """
        Details the target audience for the report.

        Returns:
        Dict[str, Any]: Details about the target audience, including specific needs and preferences.
        """
        return self.target_audience.to_dict()

    def _detail_delivery_format(self) -> Dict[str, Any]:
        """
        Details the delivery format of the report.

        Returns:
        Dict[str, Any]: Details about the delivery format, including rationale and potential alternatives.
        """
        return self.delivery_format.to_dict()

    def compile_report_specification(self) -> Dict[str, Any]:
        """
        Compiles a comprehensive specification for the sophisticated intelligence report,
        including any additional notes, sections, key findings, and recommendations.

        Returns:
        Dict[str, Any]: The complete specifications of the report, enriched with additional insights.
        """
        report_specification = {
            "id": self.id,
            "title": self.report_title,
            "data_sources": self._detail_data_sources(),
            "analysis_methods": self._detail_analysis_methods(),
            "target_audience": self._detail_target_audience(),
            "delivery_format": self._detail_delivery_format(),
            "sections": [
                section.dict()
                for section in sorted(self.sections, key=lambda x: x.priority)
            ],
            "key_findings": self.key_findings,
            "recommendations": self.recommendations,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat(),
            "version": self.version,
        }
        if self.additional_notes:
            report_specification["additional_notes"] = self.additional_notes
        return report_specification

    def export_to_json(self, file_path: str):
        """
        Exports the report specification to a JSON file.

        Parameters:
        - file_path (str): The path where the JSON file will be saved.
        """
        with open(file_path, "w") as f:
            json.dump(self.compile_report_specification(), f, indent=4, default=str)
        logger.info(f"Exported report specification to {file_path}")

    @classmethod
    def from_json(cls, file_path: str) -> "ReportSpecification":
        """
        Creates a ReportSpecification instance from a JSON file.

        Parameters:
        - file_path (str): The path to the JSON file containing the report specification.

        Returns:
        ReportSpecification: An instance of ReportSpecification populated with data from the JSON file.
        """
        with open(file_path, "r") as f:
            data = json.load(f)

        data_sources = [DataSource(**source) for source in data["data_sources"]]
        analysis_methods = [
            AnalysisMethod(**method) for method in data["analysis_methods"]
        ]
        target_audience = TargetAudience(**data["target_audience"])
        delivery_format = DeliveryFormat(**data["delivery_format"])

        report_spec = cls(
            report_title=data["title"],
            data_sources=data_sources,
            analysis_methods=analysis_methods,
            target_audience=target_audience,
            delivery_format=delivery_format,
            additional_notes=data.get("additional_notes"),
        )

        report_spec.id = data["id"]
        report_spec.created_at = datetime.fromisoformat(data["created_at"])
        report_spec.last_modified = datetime.fromisoformat(data["last_modified"])
        report_spec.version = data["version"]

        for section_data in data["sections"]:
            section = ReportSection(**section_data)
            report_spec.sections.append(section)

        report_spec.key_findings = data["key_findings"]
        report_spec.recommendations = data["recommendations"]

        logger.info(f"Loaded ReportSpecification from {file_path}")
        return report_spec

    def validate(self) -> bool:
        """
        Validates the report specification for completeness and consistency.

        Returns:
        bool: True if the specification is valid, False otherwise.
        """
        try:
            assert self.report_title, "Report title is missing"
            assert self.data_sources, "No data sources specified"
            assert self.analysis_methods, "No analysis methods specified"
            assert self.target_audience, "Target audience is not specified"
            assert self.delivery_format, "Delivery format is not specified"
            assert self.sections, "No sections defined for the report"

            for section in self.sections:
                assert section.title and section.content, (
                    f"Section {section.title} is incomplete"
                )

            logger.info("Report specification validation passed")
            return True
        except AssertionError as e:
            logger.error(f"Validation failed: {str(e)}")
            return False

    def update_version(self, new_version: str):
        """
        Updates the version of the report specification.

        Parameters:
        - new_version (str): The new version string.
        """
        self.version = new_version
        self.last_modified = datetime.now()
        logger.info(f"Updated report specification version to {new_version}")

    def clone(self) -> "ReportSpecification":
        """
        Creates a deep copy of the current ReportSpecification instance.

        Returns:
        ReportSpecification: A new instance with the same data but a new ID.
        """
        new_spec = ReportSpecification(
            report_title=self.report_title,
            data_sources=self.data_sources.copy(),
            analysis_methods=self.analysis_methods.copy(),
            target_audience=self.target_audience,
            delivery_format=self.delivery_format,
            additional_notes=self.additional_notes,
        )
        new_spec.sections = [
            ReportSection(**section.dict()) for section in self.sections
        ]
        new_spec.key_findings = self.key_findings.copy()
        new_spec.recommendations = self.recommendations.copy()
        new_spec.version = f"{self.version}-clone"
        logger.info(f"Cloned ReportSpecification with new ID: {new_spec.id}")
        return new_spec
