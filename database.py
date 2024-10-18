import csv
import datetime


class Library:
    DUE_PERIOD = 10
    FINE = 5
    def __init__(self):
        try:
            with open("db\\books.csv", mode='r', newline='') as file:
                data = list(csv.reader(file))
                self.books = data[1:]
                self.l_header = data[0]
        except OSError as e:
            print("*********Failed to read the data from books.csv file**********", e)
            exit()

        try:
            with open("db\\logger.csv", mode='r', newline='') as file:
                data = list(csv.reader(file))
                self.register = data[1:]
                self.r_header = data[0]
        except OSError as e:
            print("*********Failed to read the data from logger.csv file**********", e)
            exit()

        self.l_ids = [row[1] for row in self.books]
        self.lib_dict = {row[1]: {"ISBN": row[0],"Title": row[2],"Author": row[3],"Publisher": row[4],"Genre": row[5],"Language": row[6],"Copies": row[7],"Borrowed": row[8],"Maintenance": row[9]} for row in self.books}

    def update_library(self):
        try:
            with open('db\\books.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([self.l_header] + self.books)
        except OSError as e:
            print("**************Failed to write to file.**********", e)

    def update_register(self):
        try:
            with open('db\\logger.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([self.r_header] + self.register)
        except OSError as e:
            print("**************Failed to write to file.**********", e)

    def lib_books(self):
        return [(row[1], row[2], row[3], int(row[7])) for row in self.books]

    def reg_info(self):
        data = []
        u_ids = [row[0] for row in UserAdminManager.USERS]
        for row in self.register[::-1]:
            l_index = self.l_ids.index(row[1])
            u_index = u_ids.index(row[2])
            data.append((row[1], self.books[l_index][2], UserAdminManager.USERS[u_index][1], row[3], row[4], row[0]))
        return data

    def borrow_hist(self, u_id):
        data = []
        for row in self.register[::-1]:
            if row[2] == u_id:
                b_id = row[1]
                title = self.lib_dict[b_id]["Title"]
                i_date = row[3]
                r_date = row[4]
                data.append([b_id, title, i_date, r_date, row[0]])
        return data

    def already_borrowed(self, user, book):
        for row in self.register:
            if row[1] == book and row[2] == user and row[4] == '-':
                return True
        return False

    def due_by(self, i_dates):
        due_info = []
        for i_date in i_dates:
            issue_date = datetime.datetime.strptime(i_date, "%d-%m-%Y")
            today_date = datetime.datetime.now()
            days_difference = (today_date - issue_date).days
            remaining_days = self.DUE_PERIOD - days_difference
            last_return_date = issue_date + datetime.timedelta(days=self.DUE_PERIOD)

            if remaining_days >= 0:
                due_info.append([False, remaining_days, last_return_date.strftime("%d-%m-%Y")])
            else:
                due_info.append([True, abs(remaining_days)])
        return due_info

class UserAdminManager:
    USERS = None
    def __init__(self):
        with open("db\\users.csv", mode='r', newline='') as file:
            UserAdminManager.USERS = list(csv.reader(file))[1:]
        with open("db\\admin.csv", mode='r', newline='') as file:
            self.admins = list(csv.reader(file))[1:]

        self.u_email = [row[2] for row in self.USERS]
        self.users_dict = {row[0]: {"Name": row[1], "Email": row[2], "Password": row[3]} for row in self.USERS}


    def add_user(self, data):
        try:
            uid_num = int(self.USERS[-1][0][1:]) + 1
            uid = '#' + '0'*(5 - len(str(uid_num))) + str(uid_num)
        except IndexError:
            uid = "#00001"
        with open("db\\users.csv", mode='a', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([uid] + data)
        UserAdminManager.USERS.append([uid] + data)
        self.u_email.append(data[1])
        self.users_dict[uid] = {"Name": data[0], "Email": data[1], "Password": data[2]}
        return uid

    def is_admin(self, email, password):
        for row in self.admins:
            if row[0] == email and row[1] == password:
                return True
        return False

    def is_user(self, email, password):
        for row in self.USERS:
            if row[2] == email and row[3] == password:
                return row[0]
        return False
