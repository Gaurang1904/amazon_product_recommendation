import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def scrape_amazon_products(search_term):
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        driver.get("https://www.amazon.in")
        
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-item"))
        )
        
        top_products = []
        while len(top_products) < 5:
            products = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item[data-component-type='s-search-result']")
            
            for product in products:
                if len(top_products) >= 5:
                    break
                
                try:
                    title = product.find_element(By.CSS_SELECTOR, "h2 a span").text.strip()
                    price = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.strip()
                    url = product.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
                    
                    try:
                        rating = product.find_element(By.CSS_SELECTOR, "span.a-icon-alt").get_attribute("textContent")
                    except NoSuchElementException:
                        rating = "No rating"
                    
                    if title and price:
                        top_products.append({
                            "title": title,
                            "price": price,
                            "rating": rating,
                            "url": url
                        })
                except NoSuchElementException:
                    continue
            
            if len(top_products) < 5:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
        
        return top_products[:5]

    finally:
        driver.quit()

# Example usage
search_term = "smartphones"
results = scrape_amazon_products(search_term)

# Save results to a JSON file
with open("product_details.json", "w") as f:
    json.dump(results, f, indent=2)

print("Product details have been saved to product_details.json")

# Print the results
for i, product in enumerate(results, 1):
    print(f"Product {i}:")
    print(f"Title: {product['title']}")
    print(f"Price: ₹{product['price']}")
    print(f"Rating: {product['rating']}")
    print(f"URL: {product['url']}")
    print()