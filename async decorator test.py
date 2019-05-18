import asyncio


def error_check(func):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except (ZeroDivisionError):
            return -1
    return wrapper


@error_check
async def function1(i):
    await asyncio.sleep(2)
    return 5 / i


async def main():
    print("Main func")
    print(await function1(4))
    print(await function1(2))
    print(await function1(0))


asyncio.run(main())
print("Completed")
