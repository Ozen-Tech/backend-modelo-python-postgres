# app/schemas/dashboard.py
from pydantic import BaseModel

class DashboardStats(BaseModel):
    criticos: int
    fatais: int
    proximos: int
    status_counts: dict[str, int]