# Mobile Locator Agent

A Python agent for locating mobile phone numbers with geolocation data and carrier information using a local database.

## Features

- **Country/Region Identification**: Identify the country and region of a phone number
- **City-Level Location**: Provide city-level location data
- **Carrier Information**: Include carrier/operator details
- **Local Database**: Fast, offline lookups without external API calls
- **Batch Processing**: Process multiple phone numbers efficiently
- **Extensible**: Easy to add custom phone data and carriers

## Installation

1. Clone the repository:
```bash
git clone https://github.com/christo127/mobile-locator.git
cd mobile-locator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

```python
from src.agent import MobileLocatorAgent

# Initialize the agent
agent = MobileLocatorAgent()

# Locate a mobile number
result = agent.locate("+14155552671")

print(result)
# Output:
# LocationResult(
#     country='United States',
#     country_code='US',
#     region='California',
#     city='San Francisco',
#     carrier='AT&T',
#     phone_number='+1-415-555-2671',
#     timezone='America/Los_Angeles',
#     valid=True
# )
```

## API Reference

### MobileLocatorAgent

#### `locate(phone_number: str) -> LocationResult | None`
Locate a mobile number and return geolocation and carrier information.

#### `locate_batch(phone_numbers: List[str]) -> List[dict]`
Locate multiple phone numbers in batch.

#### `validate_phone(phone_number: str) -> bool`
Validate if a phone number is valid.

#### `get_carrier_info(phone_number: str) -> dict | None`
Get carrier information for a phone number.

#### `get_location_info(phone_number: str) -> dict | None`
Get location information for a phone number.

## Testing

```bash
pytest tests/
```

## License

MIT License
