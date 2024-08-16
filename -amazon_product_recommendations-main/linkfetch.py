import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep

def get_customer_reviews(driver, product_url):
    driver.get(product_url)
    customer_review_ids = []
    reviews = []
    sleep(7)
    
    try:
        element_xpath = '//*[@id="cm-cr-dp-review-list"]'
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, element_xpath))
        review_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )

        review_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cm-cr-dp-review-list"))
        )
        
        review_elements = review_list.find_elements(By.XPATH, './/div[starts-with(@id, "customer_review-")]')
        
        for i, review in enumerate(review_elements, 1):
            try:
                review_id = review.get_attribute('id')
                customer_review_ids.append(review_id)
                
                review_text_xpath = f'//*[@id="{review_id}"]/div[4]/span/div/div[1]'
                review_text = review.find_element(By.XPATH, review_text_xpath).text.strip()
                reviews.append(review_text)
                
                print(review_text)
                print()
                
            except NoSuchElementException:
                print(f"Couldn't fetch review text for ID: {review_id}")
            except Exception as e:
                print(f"Error fetching review {i}: {str(e)}")
            
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Couldn't fetch reviews for {product_url}: {str(e)}")
    
    return reviews

def fetch_reviews_for_products():
    with open("product_details.json", "r") as f:
        products = json.load(f)
    
    driver = webdriver.Chrome()
    
    try:
        for product in products:
            product['reviews'] = get_customer_reviews(driver, product['url'])
    
    finally:
        driver.quit()
    
    with open("product_details_with_reviews.json", "w") as f:
        json.dump(products, f, indent=2)
    
    print("Product details with reviews have been saved to product_details_with_reviews.json")

    # Print the results
    for i, product in enumerate(products, 1):
        print(f"Product {i}:")
        print(f"Title: {product['title']}")
        print(f"Price: ₹{product['price']}")
        print(f"Rating: {product['rating']}")
        print(f"URL: {product['url']}")
        print("Reviews:")
        for j, review in enumerate(product['reviews'], 1):
            print(f"  {j}. {review[:100]}...") 
        print()

fetch_reviews_for_products()