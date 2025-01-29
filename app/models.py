from pydantic import BaseModel, Field, field_validator


class FinancesMetrics(BaseModel):
    balance: float = Field(0.0, description="Current account balance")
    hours_left: float = Field(0.0, description="Remaining hours of service")
    monthly_cost: float = Field(0.0, description="Projected monthly cost of services")
    monthly_fee: float = Field(0.0, description="Fixed monthly subscription fee")
    hourly_cost: float = Field(0.0, description="Cost per hour of service usage")
    hourly_fee: float = Field(0.0, description="Fixed hourly fee for services")
    fetch_failed: bool = Field(False, description="Indicates if fetching metrics failed")

    @field_validator('hours_left', mode="before")
    def set_hours_left(cls, v):
        if v is None:
            return float('inf')
        return v
