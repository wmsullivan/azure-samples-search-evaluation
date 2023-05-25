import logging
from logging import Logger
import sys
from opencensus.ext.azure.log_exporter import AzureLogHandler, AzureEventHandler


class CustomLogger:
    """This class allows the user to log events into an Azure AppInsights logging system
    """

    def __init__(self, appinsights_key: str, logger_name: str):
        """

        Args:
            appinsights_key (str): Instrumental key to the AppInsights resource
            logging_level (str): default logging level for tracking logs i.e (DEBUG,INFO)
            logger_name (str): unique logger name
        """
        self.appinsights_key = appinsights_key
        self.logger_name = logger_name
        self.default_formatter = logging.Formatter("%(message)s")
        self.custom_dimensions = dict()

    def init_custom_dimensions(self):
        # define custom dimensions - add more here
        custom_dimensions = {"custom_dimensions": {
            "PYTHON VERSION": sys.version_info}
        }
        return custom_dimensions

    def setup_azure_trace_logging(self,) -> Logger:
        """
            Adds a handler to log into the traces table in AppInsights
        Returns:
            Logger: logger containing AzureLogHandler
        """
        # should be initialized every time with clean information
        self.custom_dimensions = self.init_custom_dimensions()
        trace_logger = logging.getLogger(self.logger_name)

        try:
            azureLogHandler = AzureLogHandler(
                connection_string=f"InstrumentationKey={self.appinsights_key}"
            )
            azureLogHandler.setFormatter(self.default_formatter)
            trace_logger.setLevel(logging.INFO)
            trace_logger.addHandler(azureLogHandler)
            # Note success adding AzureLogHandler to basic logger
            trace_logger.info(
                f"{self.logger_name} initialized - python {sys.version_info}",
                extra=self.custom_dimensions,
            )

        except ValueError as e:
            trace_logger.error("Instrumentation Key invalid. " +
                               str(e), extra=self.custom_dimensions)
        return trace_logger

    def setup_azure_event_logging(self,) -> Logger:
        """
            Adds a handler to log into the customEvents table in AppInsights
        Returns:
            Logger: logger containing AzureEventHandler
        """

        event_logger = logging.getLogger(self.logger_name)

        try:
            azureEventHandler = AzureEventHandler(
                connection_string=f"InstrumentationKey={self.appinsights_key}"
            )
            azureEventHandler.setFormatter(self.default_formatter)
            event_logger.setLevel(logging.INFO)
            event_logger.addHandler(azureEventHandler)
            event_logger.info(
                f"{self.logger_name} initialized - python {sys.version_info}",
                extra=self.custom_dimensions,
            )

        except ValueError as e:
            event_logger.error("Instrumentation Key invalid. " +
                               str(e), extra=self.custom_dimensions)
        return event_logger

    def get_logging_dimensions(self, **kwargs):
        return {"custom_dimensions": {**self.custom_dimensions["custom_dimensions"], **kwargs}}
