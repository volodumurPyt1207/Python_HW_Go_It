
from datetime import datetime


def get_days_from_today(date: str) -> int:
    try:

        given_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            f"Неправильний формат дати: '{date}'. Очікується формат 'РРРР-ММ-ДД'."
        )


    today = datetime.today().date()

    delta = today - given_date

    return delta.days

if __name__ == "__main__":
    today = datetime.today().date()
    print(f"Сьогодні: {today}\n")

    test_cases = [
        "2021-10-09",   
        "2020-01-01",   
        str(today),     
        "2030-12-31",   
    ]

    for date_str in test_cases:
        result = get_days_from_today(date_str)
        sign = "днів тому" if result >= 0 else "днів у майбутньому"
        print(f"get_days_from_today('{date_str}') = {result:>6}  ({abs(result)} {sign})")

