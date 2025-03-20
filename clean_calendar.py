import os
import requests
import re
from icalendar import Calendar, Event

# Fetch the ICS URL from environment variables
ICS_URL = os.environ.get('ICS_URL')

def clean_event_summary(summary):
    """
    Extract only the text within 'Moment:' from the event summary.
    """
    # Regex to extract text after 'Moment:' and exclude the label itself
    moment_pattern = r'Moment:([^:]+)'  # Captures everything after 'Moment:' until the next colon or end of line
    match = re.search(moment_pattern, summary)
    
    if match:
        return match.group(1).strip()  # Return only the extracted text, trimmed of whitespace
    else:
        return "Untitled Event"  # Default title if no 'Moment:' is found

def clean_calendar():
    """
    Fetch and clean the calendar by extracting only relevant information.
    """
    # Fetch the original calendar data from the ICS URL
    response = requests.get(ICS_URL)
    original_cal = Calendar.from_ical(response.text)
    
    # Create a new calendar for cleaned events
    clean_cal = Calendar()
    clean_cal.add('prodid', '-//Cleaned HKR Calendar//EN')
    clean_cal.add('version', '2.0')
    
    for component in original_cal.walk():
        if component.name == "VEVENT":  # Process only events
            clean_event = Event()
            # Extract and clean relevant fields
            clean_event.add('summary', clean_event_summary(component.get('summary')))
            clean_event.add('dtstart', component.get('dtstart'))
            clean_event.add('dtend', component.get('dtend'))
            clean_event.add('location', component.get('location', ''))
            clean_event.add('description', component.get('description', ''))
            
            # Add cleaned event to the new calendar
            clean_cal.add_component(clean_event)
    
    return clean_cal.to_ical()

if __name__ == "__main__":
    # Clean calendar and print output (for debugging or local testing)
    cleaned_ical = clean_calendar()
    print(cleaned_ical.decode('utf-8'))
