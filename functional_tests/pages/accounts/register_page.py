from enum import Enum, unique

from functional_tests.pages.page import Page


@unique
class RegisterFields(Enum):
    username = 'id_username'
    password1 = 'id_password1'
    password2 = 'id_password2'


class RegisterPage(Page):

    title = 'CTFman - Register'
    name = 'register'

    def register(self, name, password):
        self.get_id(RegisterFields.username.value).send_keys(name)
        self.get_id(RegisterFields.password1.value).send_keys(password)
        self.get_id(RegisterFields.password2.value).send_keys(password)

        self.test.browser.find_element_by_id('btn_submit').click()
        return self


