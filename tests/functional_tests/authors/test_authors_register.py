from .base import AuthorsBaseTest
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorRegisterTest(AuthorsBaseTest):

    def fill_form_dummy_data(self,form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)
       
    def get_form(self):
        return self.browser.find_element(By.XPATH, '/html/body/main/div[2]/form')


    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)
        return form


    def test_empty_first_name_error_message(self):

        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Your First Name')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.sleep(10)
            self.assertIn('Write your first name', form.text)

        self.form_field_test_with_callback(callback)


    
    def test_empty_last_name_error_message(self):

        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Your Last Name')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.sleep(10)
            self.assertIn('Write your last name', form.text)

        self.form_field_test_with_callback(callback) 


    def test_empty_username_error_message(self):

        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your Username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.sleep(10)
            self.assertIn('This field must not be empty', form.text)

        self.form_field_test_with_callback(callback)


    def test_invalid_email_error_message(self):

        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your e-mail')
            email_field.clear()  # limpa antes de digitar
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.sleep(10)
            self.assertIn('Informe um endereço de email válido.', form.text)

        self.form_field_test_with_callback(callback)   


    def test_passwords_do_not_match(self):

        def callback(form):
            password1 = self.get_by_placeholder(form, 'Type your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password1.clear()  # limpa antes de digitar
            password2.clear()  # limpa antes de digitar
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Diff')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.sleep(10)
            self.assertIn('Password and password2 must be equal', form.text)

        self.form_field_test_with_callback(callback)         
           

    def test_user_valid_data_register_successfuly(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.get_form()

        self.get_by_placeholder(form, 'Your First Name').send_keys('First Name')
        self.get_by_placeholder(form, 'Your Last Name').send_keys('Last Name')
        self.get_by_placeholder(form, 'Your Username').send_keys('my_username')
        self.get_by_placeholder(form, 'Your e-mail').send_keys('email@valid.com')
        self.get_by_placeholder(form, 'Type your password').send_keys('P@ssw0rd1')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('P@ssw0rd1')

        form.submit()

        self.sleep(5)

        self.assertIn('Your user is created, please log in', self.browser.find_element(By.TAG_NAME, 'body').text)








