import re
import datetime

def parse_time(time: str | None):
    if not time:
        return None
    
    re_match = re.match(r"(\d+)([a-z])", time.lower().strip())
    if re_match:
        value = int(re_match.group(1))
        unit = re_match.group(2)
    
        match unit:
            case 'm':
                time_delta = datetime.timedelta(minutes=value)
            case 'h':
                time_delta = datetime.timedelta(hours=value)
            case 'd':
                time_delta = datetime.timedelta(days=value)
            case _: 
                return None
    else:
        return None
    

    print(time_delta)
    until_date = datetime.datetime.now() + time_delta
    return until_date