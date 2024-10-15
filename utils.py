import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

def is_strong_pass(password):
    return len(password) > 11

def send_email(subject, body, to_email):
    from_email = "neuronbytes01@gmail.com"
    from_password = "qsre hstj xzfr nlbg"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)

        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_email_thread(subject, body, to_email):
    threading.Thread(target=send_email, args=(subject, body, to_email)).start()

def pie_values(data):
    maintenance= 0
    available = 0
    borrowed = 0
    for row in data:
        maintenance += int(row[9])
        borrowed += int(row[8])
        available += int(row[7]) - int(row[9]) - int(row[8])
    return available, borrowed, maintenance

def bar_values(data, categories):
    diff_cat = {key: 0 for key in categories}
    for row in data:
        try:
            diff_cat[row[5]] += 1
        except KeyError:
            pass
    return list(diff_cat.values())

def line_chart_values(data, dates):
    data_dict = {date.strftime('%d-%m-%Y'): 0 for date in dates}
    for row in data[::-1]:
        try:
            data_dict[row[3]] += 1
        except KeyError:
            break
    return data_dict.values()

def sort_lib(key, books, striped_books):
    sorted_lib = []
    for index, book in enumerate(striped_books):
        if key in book[0] or key in book[1]:
            sorted_lib.append(books[index])
    return sorted_lib

def already_borrowed(user, book, register):
    for row in register:
        if row[1] == book and row[2] == user and row[4] == '-':
            return True
    return False
