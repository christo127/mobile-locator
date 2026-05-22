"""Mobile Locator Agent - Main module"""

from typing import List, Optional, Dict
from src.models import LocationResult
from src.parser import PhoneNumberParser
from src.database import PhoneDatabase


class MobileLocatorAgent:
    """Agent for locating mobile phone numbers with geolocation and carrier data"""
    
    def __init__(self, db_path: str = "data"):
        """Initialize the Mobile Locator Agent"""
        self.parser = PhoneNumberParser()
        self.db = PhoneDatabase(db_path)
    
    def locate(self, phone_number: str) -> Optional[LocationResult]:
        """Locate a mobile phone number"""
        if not self.validate_phone(phone_number):
            return None
        
        parsed = self.parser.parse(phone_number)
        if not parsed:
            return None
        
        area_code = self.parser.get_area_code(phone_number)
        if not area_code:
            return None
        
        location = self.db.get_location(parsed.country_code, area_code)
        if not location:
            return None
        
        carrier = self.db.get_carrier(parsed.country_code, area_code)
        if not carrier:
            carrier = {"name": "Unknown", "type": "unknown"}
        
        return LocationResult(
            phone_number=parsed.formatted,
            country=location["country"],
            country_code=location["country_code"],
            region=location["region"],
            city=location["city"],
            carrier=carrier["name"],
            carrier_type=carrier["type"],
            timezone=location["timezone"],
            valid=True
        )
    
    def locate_batch(self, phone_numbers: List[str]) -> List[Dict]:
        """Locate multiple phone numbers"""
        results = []
        for phone_number in phone_numbers:
            result = self.locate(phone_number)
            if result:
                results.append(result.model_dump())
            else:
                results.append({"phone_number": phone_number, "valid": False})
        return results
    
    def validate_phone(self, phone_number: str) -> bool:
        """Validate a phone number"""
        return self.parser.validate(phone_number)
    
    def get_carrier_info(self, phone_number: str) -> Optional[Dict]:
        """Get carrier information for a phone number"""
        if not self.validate_phone(phone_number):
            return None
        
        parsed = self.parser.parse(phone_number)
        if not parsed:
            return None
        
        area_code = self.parser.get_area_code(phone_number)
        if not area_code:
            return None
        
        return self.db.get_carrier(parsed.country_code, area_code)
    
    def get_location_info(self, phone_number: str) -> Optional[Dict]:
        """Get location information for a phone number"""
        if not self.validate_phone(phone_number):
            return None
        
        parsed = self.parser.parse(phone_number)
        if not parsed:
            return None
        
        area_code = self.parser.get_area_code(phone_number)
        if not area_code:
            return None
        
        return self.db.get_location(parsed.country_code, area_code)
    
    def add_phone_data(self, country_code: int, country_name: str,
                      country_iso: str, area_code: str, region: str,
                      city: str, timezone: str = "Unknown"):
        """Add phone location data to database"""
        self.db.add_phone_data(
            country_code=country_code,
            country_name=country_name,
            country_iso=country_iso,
            area_code=area_code,
            region=region,
            city=city,
            timezone=timezone
        )
    
    def add_carrier_data(self, country_code: int, area_code: str,
                        carrier_name: str, carrier_type: str = "mobile"):
        """Add carrier data to database"""
        self.db.add_carrier_data(
            country_code=country_code,
            area_code=area_code,
            carrier_name=carrier_name,
            carrier_type=carrier_type
        )
    
    def save_database(self):
        """Save databases to files"""
        self.db.save_databases()
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        return self.db.get_statistics()
