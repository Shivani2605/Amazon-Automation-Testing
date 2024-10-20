import time
import unittest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import HtmlTestRunner

results = []

def get_test_status(flag):
    # function to return status
    status_map = {
        True: 'Pass',
        False: 'Fail'
    }
    return status_map.get(flag)

def search(search_text):
    # Wait for the search box to load and find it
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
        
    # Enter the search term 'laptop' and submit the search
    search_box.send_keys(search_text)
    search_box.send_keys(Keys.RETURN)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
driver = webdriver.Chrome(options=options)

# Open the Amazon homepage
driver.get("https://www.amazon.in/")
# Maximize Window
driver.maximize_window() 

# Object to store status of each test case
test_case_status = {
    'test_case_1':{
        'Test case': 'Search for a non-existing product (e.g., "ld345tsxslfer")',
        'expected_result': '"No results found" message should be displayed'
    },
    'test_case_2':{
        'Test case': 'Search for an existing product(e.g., "Laptop")',
        'expected_result': 'Product results should display "Laptop" on the page'
    },
    'test_case_3':{
        'Test case': 'Add a product to the cart',
        'expected_result': 'Product (Select 4th result from list) should be added to the cart with correct quantity and price details'
    },
    'test_case_4':{
        'Test case': 'Add a product to the cart, then update the quantity to 2',
        'expected_result': 'The cart should reflect the updated quantity and price'
    },
    'test_case_5':{
        'Test case': 'Remove a product from the cart',
        'expected_result': 'The cart should be empty'
    }
}





class TestAmazon(unittest.TestCase):

    def setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)
        # Maximize Window
        self.driver.maximize_window() 
        # Open the Amazon homepage
        self.driver.get("https://www.amazon.in/")
        
    def test_step1_search_non_existing_product(self):
        try:
            # Locate the category dropdown (search dropdown)
            category_dropdown = driver.find_element(By.ID, "searchDropdownBox")

            # Create a Select object to select option in the dropdown
            select = Select(category_dropdown)

            # Select the "Books" category from the dropdown - To get no result
            selected_category = "Books"
            select.select_by_visible_text(selected_category)

            # Wait for a short time to make sure the category is selected
            time.sleep(3)

            # search for ld345tsxslfer
            text_to_search = "ld345tsxslfer"
            search(text_to_search)

            # Wait for the results page to load
            time.sleep(3)

            # Verify the 'No results for ld345tsxslfer in Books.' is displayed on page
            text_to_be_displayed = 'No results for ' + text_to_search + ' in ' +  selected_category + '.'
            no_result_text=driver.find_element(By.XPATH,"(//div[@class='a-row'])[1]").text
            time.sleep(3) # Wait for a short time to make sure the text is rendered 
            status = text_to_be_displayed == no_result_text

            # to capture test result
            test_case_status['test_case_1']['actual_result'] = no_result_text
            test_case_status['test_case_1']['status'] = get_test_status(status)

            self.assertTrue(text_to_be_displayed,no_result_text)

        
        
        except Exception as e:
            print("Error in searching", e)

    def test_step2_search_existing_product(self):
        try:
            #Refetch the search input box after results are loaded
            search_box = driver.find_element(By.ID, "twotabsearchtextbox")
            search_box.clear()

            # Refetch the category dropdown
            category_dropdown = driver.find_element(By.ID, "searchDropdownBox")

            # Change the selection to "All Category" category from the dropdown - To get no result
            select = Select(category_dropdown)
            selected_category = "All Categories"
            select.select_by_visible_text(selected_category)

            #search for laptop
            search_term = "laptop"
            search(search_term)
            time.sleep(3)

            searched_term=driver.find_element(By.XPATH,"//span[@class='a-color-state a-text-bold']")
            # removing "" as check for search term -> return value: "laptop"
            searched_termUI=(searched_term.text).replace('"','')
            status = (search_term == searched_termUI)
            if status:
                test_case_status['test_case_2']['actual_result'] = 'Searched term is displayed at the top of page successfully'
            else:
                test_case_status['test_case_2']['actual_result'] = 'Searched term is not displayed at the top of page'
            test_case_status['test_case_2']['status'] = get_test_status(status)

            self.assertTrue(search_term == searched_termUI)

        except Exception as e:
            print("Error in searching", e)

    def test_step3_add_product_to_cart(self):
        try:
            # Wait for the search results to load and locate the fourth result
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
            )

            # Find the product elements
            products = driver.find_elements(By.XPATH, '//span[@class="a-size-medium a-color-base a-text-normal"]')
                
            # Check if there are at least 4 products
            if len(products) >= 4:
                # Get the 4th product name
                fourth_product = products[3]
                fourth_product_name = products[3].text
                fourth_product.click() # Click to open the product - opens in new tab
                time.sleep(3)  # Wait for the product page to load
                
                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[1])

                # Wait until the page is fully loaded
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "add-to-cart-button"))
                )


                # Change the quantity to 2
                quantity_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "(//div[@id='selectQuantity'])[1]"))
                )
                quantity_dropdown.click()  # Open the dropdown
                quantity_option = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//option[@value='2']"))
                )
                quantity_option.click()  # Select quantity 2

                # get product price from the product page
                product_price=(driver.find_element(By.XPATH,"(//span[@class='a-price aok-align-center reinventPricePriceToPayMargin priceToPay'])[1]").text).strip()

                # replace the mentioned symbol if exist [',','₹']
                symbols = [',','₹']
                for symbol in symbols:
                    product_price=product_price.replace(symbol,"")
                product_price=int(float(product_price))

                # Wait for the "Add to Cart" button to be present
                add_to_cart_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "(//input[@id='add-to-cart-button'])[2]"))
                )
                
                # Use JavaScript to click the button if it's present but not clickable
                if add_to_cart_button.is_displayed() and add_to_cart_button.is_enabled():
                    driver.execute_script("arguments[0].click();", add_to_cart_button)
                else:
                    print("Add to Cart button is not clickable.")

                time.sleep(5)  # Wait for the cart confirmation to appear


                # Navigate to the cart
                driver.get("https://www.amazon.in/gp/cart/view.html?ref_=nav_cart")

                # Wait for the cart page to load
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.ID, "sc-active-cart"))
                )

                # Extract the full product name using JavaScript
                cart_product_name = driver.execute_script("return arguments[0].textContent;", driver.find_element(By.XPATH, "//span[@class='a-truncate-full a-offscreen']"))

                # if cart_product_name in fourth_product_name:
                #     print("Product name verification passed.")
                # else:
                #     print(f"Product name verification failed: Expected '{fourth_product_name}', but got '{cart_product_name}'.")
                

                # Verify the quantity
                selected_quantity=((driver.find_element(By.XPATH,"(//span[@class='a-dropdown-prompt'])[1]")).text).strip()
                
                # if selected_quantity == '2':  # Assuming we want to verify that 2 quantity is added
                #     print("Quantity verification passed.")
                # else:
                #     print(f"Quantity verification failed: Expected '2', but got '{selected_quantity}'.")

                # Verify the price
                cart_price=driver.find_element(By.XPATH,"(//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap sc-product-price a-text-bold'])[1]")
                cart_price=int(float((cart_price.text).strip().replace(",","")))

                # if product_price == cart_price:
                #     print("Price verification passed.")
                # else:
                #     print(f"Price verification failed: Expected '{product_price}', but got '{cart_price}'.")
                
                if cart_product_name in fourth_product_name and selected_quantity == '2' and product_price == cart_price:
                    test_case_status['test_case_3']['actual_result'] = 'Product Addition to cart Verified successfully'
                    test_case_status['test_case_3']['status'] = get_test_status(True)
                else:
                    test_case_status['test_case_3']['actual_result'] = 'Product Addition to cart Verification failed'
                    test_case_status['test_case_3']['status'] = get_test_status(False)

                self.assertTrue(cart_product_name in fourth_product_name and selected_quantity == '2' and product_price == cart_price)
                
            else:
                print("Less than 4 products found.")

        
        except Exception as e:
            print("Error in searching", e)

    def test_step4_update_product_quantity(self):
        try:
            #Fetch price for selected product 
            single_product_price=driver.find_element(By.XPATH,"(//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap sc-product-price a-text-bold'])[1]")
            single_product_price_value=(single_product_price.text).strip().replace(",","")

            # Update the quantity of the product in the cart
            quantity_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-action-quantity'])[1]"))
            )
            quantity_dropdown.click()  # Open the dropdown

            # Select quantity 3
            quantity_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//option[@value='3']"))
            )
            quantity_option.click()

            time.sleep(3)

            #Update value for selected product
            total_product_price=driver.find_element(By.XPATH,"//span[@id='sc-subtotal-amount-activecart']//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap']")
            total_product_price_value=(total_product_price.text).strip().replace(",","")

            #Updated quantity of product
            selected_quantity=((driver.find_element(By.XPATH,"(//span[@class='a-dropdown-prompt'])[1]")).text).strip()

            price_calculation_flag=int(float(total_product_price_value)) ==  int(selected_quantity) * int(float(single_product_price_value))

            if price_calculation_flag:
                test_case_status['test_case_4']['actual_result'] = 'Product quantity updated successfully.'
            else:
                test_case_status['test_case_4']['actual_result'] = 'Product quanity is not updated.'
            test_case_status['test_case_4']['status'] = get_test_status(price_calculation_flag)

            self.assertTrue(price_calculation_flag)
                

        except Exception as e:
            print("Error in searching", e)

    def test_step5_remove_product_from_cart(self):
        try:
            #Remove the item from the cart
            remove_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='Delete']"))
            )
            remove_button.click()

            # Wait for removal confirmation
            time.sleep(3)

            empty_cart_text="Your Amazon Cart is empty."

            # Optionally, verify the cart is empty
            fetched_cart_message = driver.find_element(By.XPATH, "//h2[normalize-space()='Your Amazon Cart is empty.']").text
            is_cart_empty = (empty_cart_text == fetched_cart_message)

            if is_cart_empty:
                test_case_status['test_case_5']['actual_result'] = empty_cart_text
            else:
                test_case_status['test_case_5']['actual_result'] = "Cart is not empty"
            test_case_status['test_case_5']['status'] = get_test_status(is_cart_empty)

            self.assertTrue(is_cart_empty)
        
            df = pd.DataFrame(results)
            df = pd.DataFrame.from_dict(test_case_status, orient='index')
            df.to_excel("Amazon_test_report.xlsx", index=False)

            # ###############################################################################
            # Consolidate View of the test cases
            # ###############################################################################
            print("-------------------------------------------------------------------------")
            print("Consolidate View of the test cases")
            print("-------------------------------------------------------------------------")
            total_pass = 0
            for key, value in test_case_status.items():
                if value.get('status') == 'Pass':
                    total_pass += 1
                print(key + ": " + value.get('Test case')+ "(" + value.get('status') +")")
            print("Total Passed: " + str(total_pass) + '/5')
        
        except Exception as e:
            print("Error in searching", e)
    

    def teardown(self):
        self.driver.quit()     

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports', report_name='amazon_test_report.html',verbosity=2))