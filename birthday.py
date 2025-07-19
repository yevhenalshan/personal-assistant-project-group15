from datetime import datetime, date, timedelta

def get_upcoming_birthdays(book, days=7):
    if days < 1:
        raise ValueError("Number of days must be positive")
    congratulate_users = []
    today = date.today()
    for name, record in book.items():
        if not record.birthday:
            continue
        birthday = datetime.strptime(str(record.birthday), "%d.%m.%Y").date()
        birthday_this_year = date(today.year, birthday.month, birthday.day)
        if birthday_this_year - today <= timedelta(days=days):
            if birthday_this_year < today:
                birthday_this_year = date(birthday_this_year.year + 1, birthday.month, birthday.day)
            if birthday_this_year.weekday() == 5:
                birthday_this_year = birthday_this_year + timedelta(days=2)
            elif birthday_this_year.weekday() == 6:
                birthday_this_year = birthday_this_year + timedelta(days=1)
            birthday_this_year = birthday_this_year.strftime("%d.%m.%Y")
            congratulate_users.append({name: birthday_this_year})
    return congratulate_users
