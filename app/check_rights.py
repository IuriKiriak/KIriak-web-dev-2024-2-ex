from flask_login import current_user


class CheckRights:
    def __init__(self, record):
        self.record = record

    def create(self):
        return current_user.is_admin()

    def edit(self):
        # if current_user.id == self.record.id:
        #     return True
        if current_user.is_admin():
            return current_user.is_admin()
        elif current_user.is_moder():
            return current_user.is_moder()

    def delete(self):
        return current_user.is_admin()

    def show(self):
        return True
