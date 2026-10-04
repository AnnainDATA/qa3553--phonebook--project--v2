import logging
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener

logger = logging.getLogger(__name__)
class SeleniumEventListener(AbstractEventListener):

    def before_find(self, by, value, driver) -> None:
        logger.debug("WebDriver find: by=%s, value=%s",by,value)
        super().before_find(by, value, driver)

    def before_click(self, element, driver) -> None:
        logger.debug("WebDriver click")
        super().before_click(element, driver)

    def before_change_value_of(self, element, driver) -> None:
        logger.debug("WebDriver change value")
        super().before_change_value_of(element, driver)

    def on_exception(self, exception, driver) -> None:
        logger.error("WebDriver exception: %s", exception)
        super().on_exception(exception, driver)

