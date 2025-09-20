from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from unittest.mock import patch
from .base import RecipeBaseFunctionalTest
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipe found here 😢', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        #Usuário abre a página:
        self.browser.get(self.live_server_url)

        self.sleep(6)
        
        # Vê um campo de busca com o texto "Search for a recipe":
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Search for a recipe..."]')

        #Clica  neste input e digita o termo de busca:
        # para encontrar a receita com  titulo desejado"
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # O usuario vê  o que estava procurando na pagina:
        self.assertIn(title_needed, self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,)
        
        self.sleep(6)

        
        


