import csv


class DataBase:
    def __init__(self):
        with open("db\\users.csv", mode='r', newline='') as file:
            self.users = list(csv.reader(file))[1:]
        with open("db\\library.csv", mode='r', newline='') as file:
            data = list(csv.reader(file))
            self.library = data[1:]
            self.l_header = data[0]
        with open("db\\register.csv", mode='r', newline='') as file:
            data = list(csv.reader(file))
            self.register = data[1:]
            self.r_header = data[0]
        with open("db\\admin.csv", mode='r', newline='') as file:
            temp = list(csv.reader(file))[1:]
            self.a_email = temp[0][0]
            self.a_pass = temp[0][1]
        self.u_email = [row[2] for row in self.users]
        self.l_ids = [row[1] for row in self.library]
        self.users_dict = {row[0]: {"Name": row[1], "Email": row[2], "Password": row[3]} for row in self.users}
        self.lib_dict = {row[1]: {"ISBN": row[0],"Title": row[2],"Author": row[3],"Publisher": row[4],"Genre": row[5],"Language": row[6],"Copies": row[7],"Borrowed": row[8],"Maintenance": row[9]} for row in self.library}


    def update_library(self):
        with open('db\\library.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([self.l_header] +self.library)

    def update_register(self):
        with open('db\\register.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([self.r_header] + self.register)

    def add_user(self, data):
        try:
            uid_num = int(self.users[-1][0][1:]) + 1
            uid = '#' + '0'*(5 - len(str(uid_num))) + str(uid_num)
        except IndexError:
            uid = "#00001"
        with open("db\\users.csv", mode='a', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([uid] + data)
        return uid

    def lib_books(self):
        return [(row[1], row[2], row[3], int(row[7])- int(row[8]) - int(row[9])) for row in self.library]

    def reg_info(self):
        data = []
        u_ids = [row[0] for row in self.users]
        for row in self.register:
            l_index = self.l_ids.index(row[1])
            u_index = u_ids.index(row[2])
            data.append((row[1], self.library[l_index][2], self.users[u_index][1], row[3], row[4]))
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



if __name__ == "__main__":
    db = DataBase()
    print(db.library)
