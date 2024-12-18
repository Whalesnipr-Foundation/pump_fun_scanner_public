from datetime import datetime, timedelta,timezone


def check_creation_time(created_timestamp):
    # Convert timestamp from milliseconds to seconds
    earliest_timestamp_in_seconds = created_timestamp / 1000

    # Convert the earliest data's timestamp to an offset-aware datetime object (in UTC)
    earliest_timestamp = datetime.fromtimestamp(
        earliest_timestamp_in_seconds, tz=timezone.utc
    )

    # Get the current UTC time
    current_time = datetime.now(timezone.utc)

    # Get the date part of the earliest timestamp
    earliest_date = earliest_timestamp.date()

    # Get the current date (UTC)
    current_date = current_time.date()

    # Check if the earliest timestamp is from the same day as today
    same_day = earliest_date == current_date

    # Check if the earliest timestamp is within the last hour
    within_last_hour = (current_time - earliest_timestamp) <= timedelta(hours=2)

    return same_day
