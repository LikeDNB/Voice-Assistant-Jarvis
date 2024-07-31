import re


def extract_yt_term(command):
    # Define Regual expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match on the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name,
    # otherwise, return None
    return match.group(1) if match else None
