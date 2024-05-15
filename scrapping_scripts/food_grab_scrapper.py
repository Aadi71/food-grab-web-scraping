import time
import csv
import json
from seleniumwire import webdriver
from seleniumwire.utils import decode as sw_decode
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GrabFoodScraper:
    def __init__(self, url, location):
        self.url = url
        self.location = location
        self.driver = self._initialize_driver()
        self.restaurants_response_data = []
        self.delivery_fee = 0
        self.total_delivery_fee_accounted = 0
        self.estimated_delivery_time = 0
        self.total_delivery_time_accounted = 0

    def _initialize_driver(self):
        # PROXY = "50.223.239.166"
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=%s' % PROXY)
        options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept")]'))).click()
        except TimeoutException:
            pass
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-layout")))
        return driver

    def _enter_location_and_submit(self):
        location_input = self.driver.find_element(By.ID, 'location-input')
        location_input.click()
        time.sleep(2)
        location_input.clear()
        location_input.send_keys(self.location)

        submit_button = self.driver.find_element(By.CSS_SELECTOR, '.ant-btn.submitBtn___2roqB.ant-btn-primary')
        submit_button.click()

        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-layout")))

    def _scroll_to_bottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _capture_restaurant_data(self):
        for req in self.driver.requests:
            if req.method == 'POST' and req.url == "https://portal.grab.com/foodweb/v2/search":
                print(req.response.status_code)
                data = sw_decode(req.response.body,
                                 req.response.headers.get('Content-Encoding', 'identity'))  # decode the response
                data = data.decode("utf8")  # decode the response
                self.restaurants_response_data.append(json.loads(data))

    def _extract_restaurant_info(self):
        print(self.restaurants_response_data)
        unique_restaurants = {}

        for restaurant_data in self.restaurants_response_data:
            restaurant_data = restaurant_data["searchResult"]["searchMerchants"]
            for restaurant in restaurant_data:
                promotional_offers = None
                if "sideLabels" in restaurant:
                    side_labels_data = restaurant["sideLabels"].get("data", [])
                    if side_labels_data:
                        promotional_offers = [label.get("type") for label in side_labels_data]
                        restaurant["merchantBrief"]["hasPromo"] = True

                restaurant_id = restaurant["id"]

                if restaurant_id not in unique_restaurants:
                    current_delivery_fee = restaurant["estimatedDeliveryFee"].get(
                        "price", None
                    ) if "estimatedDeliveryFee" in restaurant else None

                    if current_delivery_fee:
                        self.delivery_fee += current_delivery_fee
                        self.total_delivery_fee_accounted += 1

                    current_delivery_time = restaurant.get("estimatedDeliveryTime")

                    if current_delivery_time:
                        self.estimated_delivery_time += restaurant.get("estimatedDeliveryTime")
                        self.total_delivery_time_accounted += 1

                    unique_restaurants[restaurant_id] = {
                        "Restaurant Name": restaurant["address"]["name"],
                        "Restaurant Cuisine": ", ".join(restaurant["merchantBrief"]["cuisine"]),
                        "Restaurant Rating": restaurant["merchantBrief"].get("rating", None),
                        "Estimate time of Delivery": current_delivery_time,
                        "Restaurant Distance from Delivery Location": restaurant["merchantBrief"].get("distanceInKm",
                                                                                                      None),
                        "Is promo available": restaurant["merchantBrief"].get("hasPromo", False),
                        "Restaurant latitude": restaurant["latlng"]["latitude"],
                        "Restaurant longitude": restaurant["latlng"]["longitude"],
                        "Estimate Delivery Fee": current_delivery_fee,
                        "Restaurant Image Link": restaurant["merchantBrief"].get("photoHref", False),
                        "Promotional Offers": promotional_offers,
                    }
        return unique_restaurants

    def scrape_and_save(self, output_csv):
        self._enter_location_and_submit()
        self._scroll_to_bottom()
        self._capture_restaurant_data()
        unique_restaurants = self._extract_restaurant_info()

        fieldnames = ["Restaurant ID"] + list(list(unique_restaurants.values())[0].keys())

        with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for restaurant_id, restaurant_data in unique_restaurants.items():
                row = { "Restaurant ID": restaurant_id, **restaurant_data }
                writer.writerow(row)

        print("Extraction and saving completed successfully.")
        self.driver.quit()

    def get_average_delivery_time(self):
        print("Average Delivery Time: ", self.estimated_delivery_time / self.total_delivery_time_accounted, "\n")

    def get_average_delivery_fee(self):
        print("Average Delivery Fee: ", self.delivery_fee / self.total_delivery_fee_accounted)


if __name__ == "__main__":
    url = "https://food.grab.com/sg/en/"
    location = "PT Singapore - Choa Chu Kang North 6, Singapore, 689577"
    output_csv = "aadi_unique_restaurant_data.csv"

    scraper = GrabFoodScraper(url, location)
    scraper.scrape_and_save(output_csv)
    scraper.get_average_delivery_time()
    scraper.get_average_delivery_fee()
