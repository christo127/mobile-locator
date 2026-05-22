"""Enhanced Mobile Locator Agent with multiple API providers"""

from typing import List, Optional, Dict
from src.models import LocationResult
from src.parser import PhoneNumberParser
from src.database import PhoneDatabase
import os


class EnhancedMobileLocatorAgent:
    """Enhanced agent supporting multiple location providers"""
    
    def __init__(self, db_path: str = "data", provider: str = "local"):
        """Initialize enhanced agent
        
        Args:
            db_path: Path to local database
            provider: Location provider ('local', 'truecaller', 'vonage', 'aws', 'opencage')
        """
        self.parser = PhoneNumberParser()
        self.db = PhoneDatabase(db_path)
        self.provider = provider
        self._init_providers()
    
    def _init_providers(self):
        """Initialize external API providers"""
        try:
            if self.provider in ["truecaller", "all"]:
                from src.truecaller_api import TrueCallerAPI
                self.truecaller = TrueCallerAPI()
        except ImportError:
            print("TrueCaller API not available")
        
        try:
            if self.provider in ["vonage", "all"]:
                from src.vonage_api import VonageAPI
                self.vonage = VonageAPI()
        except ImportError:
            print("Vonage API not available")
        
        try:
            if self.provider in ["aws", "all"]:
                from src.aws_pinpoint_api import AWSPinpointAPI
                self.aws = AWSPinpointAPI()
        except ImportError:
            print("AWS Pinpoint API not available")
        
        try:
            if self.provider in ["opencage", "all"]:
                from src.opencage_api import OpenCageAPI
                self.opencage = OpenCageAPI()
        except ImportError:
            print("OpenCage API not available")
    
    def locate(self, phone_number: str, use_external: bool = True) -> Optional[LocationResult]:
        """Locate phone number using specified provider
        
        Args:
            phone_number: Phone number in E.164 format
            use_external: Try external APIs if local lookup fails
            
        Returns:
            LocationResult with geolocation and carrier data
        """
        # First try local database
        local_result = self._locate_local(phone_number)
        if local_result:
            return local_result
        
        # If not found locally and use_external is True, try external providers
        if use_external and self.provider != "local":
            return self._locate_external(phone_number)
        
        return None
    
    def _locate_local(self, phone_number: str) -> Optional[LocationResult]:
        """Locate using local database
        
        Args:
            phone_number: Phone number in E.164 format
            
        Returns:
            LocationResult or None
        """
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
    
    def _locate_external(self, phone_number: str) -> Optional[Dict]:
        """Locate using external API providers
        
        Args:
            phone_number: Phone number in E.164 format
            
        Returns:
            Location result or None
        """
        results = {}
        
        # Try TrueCaller
        if hasattr(self, 'truecaller'):
            try:
                result = self.truecaller.search_phone_number(phone_number)
                if result:
                    results['truecaller'] = result
            except Exception as e:
                print(f"TrueCaller error: {e}")
        
        # Try Vonage
        if hasattr(self, 'vonage'):
            try:
                result = self.vonage.get_phone_details(phone_number)
                if result:
                    results['vonage'] = result
            except Exception as e:
                print(f"Vonage error: {e}")
        
        # Try AWS Pinpoint
        if hasattr(self, 'aws'):
            try:
                result = self.aws.validate_phone_number(phone_number)
                if result:
                    results['aws'] = result
            except Exception as e:
                print(f"AWS Pinpoint error: {e}")
        
        # Return best result
        if results:
            return self._merge_results(results)
        
        return None
    
    def _merge_results(self, results: Dict) -> Dict:
        """Merge results from multiple providers
        
        Args:
            results: Dictionary of results from different providers
            
        Returns:
            Merged result
        """
        # Prefer TrueCaller > Vonage > AWS
        priority = ['truecaller', 'vonage', 'aws', 'opencage']
        
        for provider in priority:
            if provider in results and results[provider]:
                return results[provider]
        
        # If no good result, return first available
        for result in results.values():
            if result:
                return result
        
        return None
    
    def locate_batch(self, phone_numbers: List[str], use_external: bool = True) -> List[Dict]:
        """Locate multiple phone numbers
        
        Args:
            phone_numbers: List of phone numbers
            use_external: Try external APIs if local lookup fails
            
        Returns:
            List of location results
        """
        results = []
        for phone_number in phone_numbers:
            result = self.locate(phone_number, use_external)
            if result:
                if isinstance(result, LocationResult):
                    results.append(result.model_dump())
                else:
                    results.append(result)
            else:
                results.append({"phone_number": phone_number, "valid": False})
        return results
    
    def validate_phone(self, phone_number: str) -> bool:
        """Validate a phone number"""
        return self.parser.validate(phone_number)
    
    def set_provider(self, provider: str):
        """Change location provider
        
        Args:
            provider: Provider name ('local', 'truecaller', 'vonage', 'aws', 'all')
        """
        self.provider = provider
        self._init_providers()
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        available = []
        
        if hasattr(self, 'truecaller'):
            available.append('truecaller')
        if hasattr(self, 'vonage'):
            available.append('vonage')
        if hasattr(self, 'aws'):
            available.append('aws')
        if hasattr(self, 'opencage'):
            available.append('opencage')
        
        available.append('local')
        return available
