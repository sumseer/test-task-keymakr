class BaseAPIError(Exception):
    """Base class for all API-related errors."""

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred during the API request."
        super().__init__(message)


class APIInvalidURLError(BaseAPIError):
    """Raised when the API URL is invalid."""

    def __init__(self, message="The API URL provided is invalid."):
        super().__init__(message)


class APIConnectionError(BaseAPIError):
    """Raised when there is an issue connecting to the API."""

    def __init__(self, message="Failed to establish a connection to the API."):
        super().__init__(message)


class APIRequestTimeoutError(BaseAPIError):
    """Raised when the request times out."""

    def __init__(self, message="The API request timed out."):
        super().__init__(message)


class APIRequestResponseError(BaseAPIError):
    """Raised when an API response is invalid or unexpected."""

    def __init__(self, status_code: int, message=None):
        if message is None:
            message = f"Unexpected API response: {status_code}"
        super().__init__(message)
        self.status_code = status_code
