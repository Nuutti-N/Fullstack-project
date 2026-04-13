from fastapi import HTTPException, APIRouter, Depends, status
from time import time
import threading

router = APIRouter()


class RateLimiter:
    def __init__(self, rate: int, per: int):
        """
        Rate Limiter (Token bucker algortihm)
        param rate: Maximum number of requests allowed within the time window
        param per: Time window in seconds:        
        """
