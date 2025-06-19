"""
Get Working Day Checker
----------------------
This script determines if today is the Nth working day of the month, considering weekends and region-specific public holidays.

Features:
- Automatically detects your system's region/country code.
- Uses the 'holidays' package to fetch public holidays for your country.
- Skips weekends and public holidays when counting working days.

How to Run:
-----------
1. Ensure you have Python 3.7+ installed.
2. Install required packages (if not already installed):
   pip install holidays tzlocal babel
3. Run the script:
   python GedDay/Get_workingday.py

You can change the value of 'nth_day_to_check' in the script to check for a different working day.

Author: [Srimanta Pal]
Date: 2025-06-19
"""

import datetime
import holidays as holidays_lib
import locale
from babel import Locale
from tzlocal import get_localzone

def is_nth_working_day(check_date, n, holiday_dates=None):
    """
    Checks if the given 'check_date' is the nth working day of its month,
    considering weekends and a provided set of public holidays.
    """
    if holiday_dates is None:
        holiday_dates = set()

    count = 0
    day = datetime.date(check_date.year, check_date.month, 1)
    while day <= check_date:
        if day.weekday() < 5 and day not in holiday_dates:
            count += 1
        if count == n and day == check_date:
            return True
        day += datetime.timedelta(days=1)
    return False

def get_region_holidays(year, country_code):
    """
    Returns a set of public holidays for the given year and country code using the 'holidays' package.
    """
    try:
        return set(holidays_lib.country_holidays(country_code, years=[year]).keys())
    except Exception as e:
        print(f"Could not fetch holidays for region {country_code}: {e}")
        return set()

def get_system_country_code():
    """
    Attempts to determine the system's country code using locale and timezone.
    Returns a 2-letter country code (e.g., 'US', 'IN'), or 'US' as fallback.
    """
    try:
        # Try to get from locale
        loc = locale.getdefaultlocale()[0]
        if loc:
            parts = loc.split('_')
            if len(parts) == 2:
                return parts[1].upper()
        # Try to get from timezone
        tz = get_localzone()
        loc = Locale.parse(locale.getdefaultlocale()[0])
        if loc.territory:
            return loc.territory.upper()
    except Exception as e:
        print(f"Could not determine system region: {e}")
    return 'US'  # Default fallback

# Example usage
if __name__ == "__main__":
    today = datetime.date.today()
    region_code = get_system_country_code()
    print(f"Detected system region: {region_code}")
    public_holidays = get_region_holidays(today.year, region_code)
    nth_day_to_check = 14
    if is_nth_working_day(today, nth_day_to_check, public_holidays):
        print(f"{today} is the {nth_day_to_check}th working day of the month (considering {region_code} holidays).")
    else:
        print(f"{today} is NOT the {nth_day_to_check}th working day of the month (considering {region_code} holidays).")