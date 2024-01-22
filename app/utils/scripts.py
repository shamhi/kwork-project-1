import random
import string


def get_unique_code(all_codes: list[str]) -> str:
    letters = string.ascii_uppercase

    while True:
        code = (f"{''.join([str(random.randint(0, 9)) for _ in range(3)])}_"
                f"{''.join([random.choice(letters) for _ in range(3)])}")

        if code not in all_codes:
            break

    return code
