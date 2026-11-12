import asyncio
import logging
from typing import Any, Dict

from aiohttp import ClientSession
from data_analysis import DataAnalyzer
from data_collection import DataCollector
from error_handling import DataAnalysisError, DataCollectionError, ReportExecutionError
from report_delivery import ReportDeliverer
from report_generation import ReportGenerator
from specify_report import (
    AnalysisMethod,
    DataSource,
    ReportSpecification,
)


class ReportExecutor:
    """
    A class responsible for executing the entire report generation process.

    This class orchestrates the data collection, analysis, report generation,
    and delivery phases of the reporting process.
    """

    def __init__(self, report_specification: ReportSpecification):
        """
        Initialize the ReportExecutor with a given report specification.

        Args:
            report_specification (ReportSpecification): The specification for the report to be executed.
        """
        self.report_specification = report_specification
        self.logger = self._setup_logger()
        self.data_collector = DataCollector()
        self.data_analyzer = DataAnalyzer()
        self.report_generator = ReportGenerator()
        self.report_deliverer = ReportDeliverer()

    def _setup_logger(self) -> logging.Logger:
        """
        Set up a logger for the ReportExecutor instance.

        Returns:
            logging.Logger: Configured logger for this ReportExecutor instance.
        """
        logger = logging.getLogger(
            f"{self.__class__.__name__}_{self.report_specification.id}"
        )
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    async def execute_report(self) -> Dict[str, Any]:
        """
        Execute the report generation process asynchronously.

        This method coordinates the entire report generation workflow, including
        data collection, analysis, report generation, and delivery.

        Returns:
            Dict[str, Any]: A dictionary containing the report execution results.

        Raises:
            ReportExecutionError: If any step of the report execution process fails.
        """
        self.logger.info(
            f"Starting execution of report: {self.report_specification.report_title}"
        )

        try:
            # Validate report specification
            if not await self.report_specification.validate():
                raise ValueError("Invalid report specification")

            # Collect data
            collected_data = await self._collect_data()

            # Analyze data
            analysis_results = await self._analyze_data(collected_data)

            # Generate report
            report = await self._generate_report(analysis_results)

            # Deliver report
            delivery_result = await self._deliver_report(report)

            self.logger.info(
                f"Report execution completed successfully: {self.report_specification.report_title}"
            )
            return {
                "report_id": self.report_specification.id,
                "report_title": self.report_specification.report_title,
                "delivery_result": delivery_result,
            }

        except Exception as e:
            self.logger.error(f"Error during report execution: {str(e)}")
            raise ReportExecutionError(f"Failed to execute report: {str(e)}") from e

    async def _collect_data(self) -> Dict[str, Any]:
        """
        Collect data from all specified data sources asynchronously.

        This method manages the concurrent collection of data from multiple sources,
        handling potential errors and ensuring all sources are attempted.

        Returns:
            Dict[str, Any]: A dictionary containing collected data from each source.

        Raises:
            DataCollectionError: If data collection fails for all sources.
        """
        self.logger.info("Starting data collection")
        collected_data = {}
        async with ClientSession() as session:
            tasks = [
                self._collect_from_source(source, session)
                for source in self.report_specification.data_sources
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for source, result in zip(self.report_specification.data_sources, results):
                if isinstance(result, Exception):
                    self.logger.error(
                        f"Data collection failed for {source.name}: {str(result)}"
                    )
                else:
                    collected_data[source.id] = result
                    self.logger.info(f"Collected data from source: {source.name}")

            if not collected_data:
                raise DataCollectionError("Failed to collect data from all sources")

        return collected_data

    async def _collect_from_source(
        self, source: DataSource, session: ClientSession
    ) -> Any:
        """
        Collect data from a single source asynchronously.

        Args:
            source (DataSource): The data source to collect from.
            session (ClientSession): The aiohttp ClientSession to use for HTTP requests.

        Returns:
            Any: The collected data from the source.

        Raises:
            DataCollectionError: If data collection fails for this source.
        """
        try:
            return await self.data_collector.collect_async(source, session)
        except Exception as exc:
            raise DataCollectionError(
                f"Failed to collect data from {source.name}: {str(exc)}"
            ) from exc

    async def _analyze_data(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze collected data using specified analysis methods asynchronously.

        This method manages the concurrent analysis of data using multiple methods,
        handling potential errors and ensuring all methods are attempted.

        Args:
            collected_data (Dict[str, Any]): The data collected from various sources.

        Returns:
            Dict[str, Any]: A dictionary containing analysis results for each method.

        Raises:
            DataAnalysisError: If data analysis fails for all methods.
        """
        self.logger.info("Starting data analysis")
        analysis_results = {}
        tasks = [
            self._analyze_with_method(method, collected_data)
            for method in self.report_specification.analysis_methods
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for method, result in zip(self.report_specification.analysis_methods, results):
            if isinstance(result, Exception):
                self.logger.error(f"Analysis failed for {method.name}: {str(result)}")
            else:
                analysis_results[method.id] = result
                self.logger.info(f"Completed analysis method: {method.name}")

        if not analysis_results:
            raise DataAnalysisError("Failed to perform any data analysis")

        return analysis_results

    async def _analyze_with_method(
        self, method: AnalysisMethod, collected_data: Dict[str, Any]
    ) -> Any:
        """
        Analyze data using a single method asynchronously.

        Args:
            method (AnalysisMethod): The analysis method to use.
            collected_data (Dict[str, Any]): The collected data to analyze.

        Returns:
            Any: The result of the analysis.

        Raises:
            DataAnalysisError: If data analysis fails for this method.
        """
        try:
            return await self.data_analyzer.analyze_async(method, collected_data)
        except Exception as exc:
            raise DataAnalysisError(
                f"Failed to analyze data with {method.name}: {str(exc)}"
            ) from exc

    async def _generate_report(self, analysis_results: Dict[str, Any]) -> Any:
        """
        Generate the report based on analysis results.

        This method coordinates the creation of the final report using the
        analyzed data and the report specification.

        Args:
            analysis_results (Dict[str, Any]): The results of data analysis.

        Returns:
            Any: The generated report object.
        """
        self.logger.info("Generating report")
        return await self.report_generator.generate_async(
            self.report_specification, analysis_results
        )

    async def _deliver_report(self, report: Any) -> Dict[str, Any]:
        """
        Deliver the generated report to the specified audience.

        This method manages the delivery of the final report according to
        the specifications in the report configuration.

        Args:
            report (Any): The generated report object.

        Returns:
            Dict[str, Any]: The result of the report delivery process.
        """
        self.logger.info("Delivering report")
        return await self.report_deliverer.deliver_async(
            report,
            self.report_specification.target_audience,
            self.report_specification.delivery_format,
        )


async def execute_report(report_specification: ReportSpecification) -> Dict[str, Any]:
    """
    Execute a report based on the given specification.

    This function serves as the main entry point for report execution,
    creating a ReportExecutor instance and managing the overall process.

    Args:
        report_specification (ReportSpecification): The specification for the report to be executed.

    Returns:
        Dict[str, Any]: The result of the report execution process.

    Raises:
        ReportExecutionError: If the report execution fails.
    """
    executor = ReportExecutor(report_specification)
    return await executor.execute_report()
