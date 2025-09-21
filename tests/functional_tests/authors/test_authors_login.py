from .base import AuthorsBaseTest
from django.urls import reverse
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
import pytest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(username = 'my_user', password = string_password)

        # Usuário abre a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        #Usuário vê o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuario digita seu usuario e senha:
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuario envia o formulario:
        form.submit()

        self.sleep(6)

        # Usuário vê a mensagem de login com sucesso e seu nome:
        self.assertIn(f'Your are logged in with {user.username} Please,', self.browser.find_element(By.TAG_NAME, 'body').text)

        # end test
        self.sleep(6)
        



