"""This file holds the retry logic"""

class RetryPolicy:
    """
    This class holds the retry logic.
    """
    def __init__(
            self,
            max_retries: int = 0,
            retry_on: tuple[type[Exception], ...] = (),
            backoff=None ):
        """Initializing the retry attributes."""
        self.max_retries = max_retries
        self.retry_on = retry_on
        self.backoff = backoff

    def should_retry(self, exception: Exception, attempt: int) -> bool:
        """This method returns a bool value when it concludes that we have to retry or not."""
        if attempt > self.max_retries:
            return
        return isinstance(exception, self.retry_on)

    def get_delay(self, attempt: int) -> float:
        """This method returns a float as per the backoff that you have told them - fixed backoff or exponential backoff."""
        return self.backoff(attempt)