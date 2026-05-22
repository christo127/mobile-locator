"""Test script to locate phone number using TrueCaller API"""

from src.truecaller_api import TrueCallerAPI
import os
import json

# Set the API key
os.environ["TRUECALLER_API_KEY"] = "a1k07--Vgdfyvv_rftf5uuudhuhnkljyvvtfftjuhbuijbhug"

def locate_phone_number(phone_number):
    """Locate a phone number using TrueCaller API"""
    
    print(f"\n{'='*70}")
    print(f"🔍 Locating Phone Number: {phone_number}")
    print(f"{'='*70}\n")
    
    try:
        # Initialize TrueCaller API
        truecaller = TrueCallerAPI()
        
        # Search for phone number
        result = truecaller.search_phone_number(phone_number)
        
        if result:
            print("✅ LOCATION FOUND!\n")
            print("📍 Location Details:")
            print(f"  Country: {result.get('country', 'N/A')}")
            print(f"  Country Code: {result.get('country_code', 'N/A')}")
            print(f"  City: {result.get('city', 'N/A')}")
            print(f"  Region/State: {result.get('region', 'N/A')}")
            print(f"  Timezone: {result.get('timezone', 'N/A')}")
            
            print("\n📱 Phone Details:")
            print(f"  Carrier: {result.get('carrier', 'N/A')}")
            print(f"  Carrier Type: {result.get('carrier_type', 'N/A')}")
            print(f"  Phone Type: {result.get('phone_type', 'N/A')}")
            print(f"  Phone Number: {result.get('phone_number', 'N/A')}")
            
            if result.get('name'):
                print(f"\n👤 Name: {result.get('name', 'N/A')}")
            
            print(f"\n{'-'*70}")
            print("Full Result (JSON):")
            print(json.dumps(result, indent=2))
            print(f"{'='*70}\n")
            
            return result
        else:
            print("❌ Phone number not found in TrueCaller database\n")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return None

if __name__ == "__main__":
    # Locate the phone number
    result = locate_phone_number("+916238501147")
