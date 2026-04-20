import json, os, pandas, random, smtplib, datetime as dt

with open("quotes.txt", "r") as f:
    quotes = f.read().split("\n")

now = dt.datetime.now()
url = os.environ.get("BIRTHDAYS_URL")
birthdays = pandas.read_csv(url)
month_name = dt.datetime.strftime(now, '%B')
day_name = dt.datetime.strftime(now, '%A')
MY_EMAIL = os.environ.get("MY_EMAIL")
EMAIL_LIST = json.loads(os.environ.get("EMAIL_LIST", "[]"))
PASSWORD = os.environ.get("MY_PASSWORD")

for _, row in birthdays.iterrows():
    if birthdays.month.item() == now.month and birthdays.date.item() == now.day:
        birthday_person_name = birthdays["name"].item()
        birthday_person_age = now.year - birthdays["year"].item()
        birthday_person_email = birthdays["email"].item()
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=birthday_person_email, msg=f"Subject: Happy Birthday {birthday_person_name}!\n\n"
                                                                                    f"Congrats on turning the big ol {birthday_person_age}!\n"
                                                                                    f"Hope you have a great day and eats lots of cake for me!\n\n"
                                                                                    f"Love,\nBubba")
        connection.close()

if day_name == "Monday":
    daily_quote = random.choice(quotes)
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        for email in EMAIL_LIST:
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=email, msg= f"Subject: Inspirational Quote For The Week\n\nDamn,"
                                                                         f" it's already monday again, here is a quote to help"
                                                                         f" you get through the week:\n{daily_quote}\n\nThis"
                                                                         f" was automatically sent by my Python script")
