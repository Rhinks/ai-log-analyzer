def parse_log(log_content: str ) -> list[dict]:
    """
    Parses the given log content and returns a list of log entries as dictionaries.

    Each log entry is expected to be in the format:

    Jun 15 02:04:59 combo sshd(pam_unix)[20885]: authentication failure...

    Args:
        log_content (str): The content of the log file as a string.

    Returns:
        list[dict]: A list of dictionaries representing log entries.
    """
    import re
    log_entries = []
    log_pattern = re.compile(r'^(\w+ \d+ \d+:\d+:\d+) (\w+) ([^\[]+)\[(\d+)\]: (.*)$')

    for line in log_content.splitlines():
        match = log_pattern.match(line)
        if match:
            log_entry = {
                'timestamp': match.group(1),
                'hostname': match.group(2),
                'process': match.group(3),
                'pid': match.group(4),
                'message': match.group(5)
            }
            log_entries.append(log_entry)

    return log_entries

if __name__ == "__main__":
    # Example usage of the parse_log function
    print(parse_log("""Jun 15 02:04:59 combo sshd(pam_unix)[20885]: authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=192.168.100  user=root
    Jun 15 02:05:01 combo sshd[20890]: Accepted password for user from 192.168.100 port 54321 ssh2
    """))