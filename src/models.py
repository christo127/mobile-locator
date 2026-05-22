"""Data models for Mobile Locator Agent"""

from typing import Optional
from pydantic import BaseModel, Field


class LocationResult(BaseModel):
    """Result model for phone number location"""
    
    phone_number: str = Field(..., description="Formatted phone number")
    country: str = Field(..., description="Country name")
    country_code: str = Field(..., description="ISO country code")
    region: str = Field(..., description="Region/State")
    city: str = Field(..., description="City name")
    carrier: str = Field(..., description="Mobile carrier name")
    carrier_type: str = Field(..., description="Type of carrier (mobile, landline, etc)")
    timezone: str = Field(default="Unknown", description="Timezone")
    valid: bool = Field(default=True, description="Whether phone number is valid")
    
    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "phone_number": "+1-415-555-2671",
                "country": "United States",
                "country_code": "US",
                "region": "California",
                "city": "San Francisco",
                "carrier": "AT&T",
                "carrier_type": "mobile",
                "timezone": "America/Los_Angeles",
                "valid": True
            }
        }


class PhoneNumber(BaseModel):
    """Parsed phone number model"""
    
    country_code: int = Field(..., description="International calling code")
    national_number: int = Field(..., description="National phone number")
    region_code: str = Field(..., description="ISO country code")
    formatted: str = Field(..., description="Formatted phone number")
    valid: bool = Field(default=True, description="Whether phone number is valid")
    
    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "country_code": 1,
                "national_number": 4155552671,
                "region_code": "US",
                "formatted": "+1-415-555-2671",
                "valid": True
            }
        }


class CarrierInfo(BaseModel):
    """Carrier information model"""
    
    name: str = Field(..., description="Carrier name")
    type: str = Field(..., description="Carrier type (mobile, landline, etc)")
    country_code: int = Field(..., description="Country code")
    area_code: str = Field(..., description="Area code")


class LocationInfo(BaseModel):
    """Location information model"""
    
    country: str = Field(..., description="Country name")
    country_code: str = Field(..., description="ISO country code")
    region: str = Field(..., description="Region/State name")
    city: str = Field(..., description="City name")
    timezone: str = Field(default="Unknown", description="Timezone")
