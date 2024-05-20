from asyncio import run, TimeoutError
from bot import *

if __name__ == "__main__":
    while True:
        try:
            run(main())
        except TimeoutError:
            run(main())