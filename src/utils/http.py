"""Safe, bounded HTTP helpers for all third-party integrations."""
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter
from config import settings

RETRYABLE = (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.RemoteProtocolError)

@retry(retry=retry_if_exception_type(RETRYABLE), stop=stop_after_attempt(3), wait=wait_exponential_jitter(initial=0.5, max=8), reraise=True)
def request(method: str, url: str, **kwargs) -> httpx.Response:
    """Issue an outbound request with a timeout; retry only transient transport failures."""
    timeout = kwargs.pop("timeout", settings.request_timeout_seconds)
    with httpx.Client(timeout=timeout, follow_redirects=False) as client:
        return client.request(method, url, **kwargs)
