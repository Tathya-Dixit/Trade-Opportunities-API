from fastapi import Request, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, requests_per_hour: int = 10):
        self.requests_per_hour = requests_per_hour
        self.request_history = defaultdict(list)

    async def check_rate_limit(self, username: str):
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)

        user_requests = self.request_history[username]

        user_requests = [req_time for req_time in user_requests if req_time > one_hour_ago]

        self.request_history[username] = user_requests

        if len(user_requests) >= self.requests_per_hour:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {self.requests_per_hour} requests per hour."
            )

        user_requests.append(now)
        self.request_history[username] = user_requests

        logger.info(f"User {username} has made {len(user_requests)} requests in the last hour")


rate_limiter = RateLimiter(requests_per_hour=10)
