import re
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai
from database import Library

key = "AIzaSyDCT9vYHyCZiHewbGMDHCzta1rbq9Sdr4U"
email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
prompt = f"""
I'm working on a Library management system and Integrating you in to the user side to let him clarify his doubts about different books.
So, I'm expecting you to reply to messages that are relevant. And for others just reply with "I'm here to assist you with library related queries! You can ask me about book availability, suggestions, or library services. How can I help you with that?"
Do not use any bold text or styles in replies just reply in normal words.
You can respond to greetings and some common things if it's completely out of topic the reply similar to above not exactly. above.

Here is some data about our specifications and library:
A user can not have the book if he already have borrowed the same book and haven't returned yet.
They will be notified through emails about dues.
The user can borrow the book from the home tab.
He can see his previous borrowing history from the history tab.
The due time after borrowing is {Library.DUE_PERIOD} and fine for each excess day is {Library.FINE}.
"""


genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def is_strong_pass(password):
    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True

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
        available += int(row[7])
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

def get_gemini_response(question):
    response = chat.send_message(question)
    return response.text

