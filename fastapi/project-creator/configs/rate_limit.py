"""
Rate limiting decorator using Redis.
Provides flexible rate limiting based on request IP and configurable periods.
Supports multiple limits per endpoint.
"""

from functools import wraps
from typing import Any, Callable, List, Tuple

from config.cache import get_redis
from fastapi import HTTPException, Request


def rate_limit(limits: List[Tuple[int, str]]):
    """
    Decorator to limit the number of requests per multiple periods.

    Args:
        limits (List[Tuple[int, str]]): A list of (rate, period) tuples.
            Periods: 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days).

    Returns:
        Callable: The decorated function with rate limiting logic.

    Example:
        # Usage:
        # @rate_limit(limits=[(2, "m"), (8, "h"), (20, "d")])
        # async def my_endpoint(request: Request): ...
    """
    period_seconds_map = {"s": 1, "m": 60, "h": 3600, "d": 86400}

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Find the request object in args or kwargs
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not request:
                # If no request object found, we can't rate limit by IP
                return await func(*args, **kwargs)

            client_ip = request.client.host
            redis = get_redis()

            # Check all limits before incrementing
            for rate, period in limits:
                key = f"rate_limit:{func.__name__}:{client_ip}:{period}"

                current_count = await redis.get(key)
                if current_count and int(current_count) >= rate:
                    raise HTTPException(
                        status_code=429, detail=f"Rate limit exceeded: {rate} per {period}"
                    )

            # If all checks pass, increment all keys
            for rate, period in limits:
                period_seconds = period_seconds_map.get(period, 60)
                key = f"rate_limit:{func.__name__}:{client_ip}:{period}"

                current_count = await redis.get(key)
                if not current_count:
                    await redis.set(key, 1, expire=period_seconds)
                else:
                    await redis.client.incr(key)

            return await func(*args, **kwargs)

        return wrapper

    return decorator
