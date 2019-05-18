import gspread


def error_check(func):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except (gspread.exceptions.APIError):
            return "ERROR"
    return wrapper