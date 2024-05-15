# Grab Food Delivery Web Scraper

This project aims to develop a web scraper to extract specific information from the Grab Food Delivery platform.

### One View Objective, Approach, Challenges, and Go-to strategy look
<img width="864" alt="image" src="https://github.com/Aadi71/food-grab-web-scraping/assets/73948412/1a5876fb-b826-4d03-9ece-7f6053195769">

## Table of Contents
1. [Introduction](#introduction)
2. [Tasks](#tasks)
3. [Data Extraction](#data-extraction)
4. [Documentation](#documentation)
    - [Approach and Methodology](#approach-and-methodology)
    - [Challenges Faced](#challenges-faced)
    - [Improvements and Optimizations](#improvements-and-optimizations)
5. [Execution Steps](#execution-steps)

## Introduction
It scrapes restaurant lists, details, delivery fees, and estimated delivery times for selected locations. The scraper is implemented using Python, following object-oriented programming (OOP) concepts, and optimized for scalability and performance using multithreading.

## Tasks
The tasks performed by the web scraper include:
- Extracting restaurant lists with details.
- Creating a unique restaurant list.
- Extracting delivery fees and estimated delivery time for selected locations.

## Data Extraction
The scraper extracts the following fields/column data visible on the Grab Food Delivery website:
1. Restaurant Name
2. Restaurant Cuisine
3. Restaurant Rating
4. Estimate Time of Delivery
5. Restaurant Distance from Delivery Location
6. Promotional Offers
7. Restaurant Notice
8. Image Link of the Restaurant
9. Is Promo Available (True/False)
10. Restaurant ID
11. Restaurant Latitude and Longitude
12. Estimate Delivery Fee

## Documentation
### Approach and Methodology
1. **Scraping Logic**: The scraper navigates through the Grab Food Delivery website, parsing HTML content to extract relevant information.
2. **OOP Implementation**: The code follows object-oriented programming principles, ensuring modularity and maintainability.
3. **Optimization**: Multithreading is employed to enhance performance and scalability, enabling efficient data extraction.
4. **Data Handling**: Extracted data is saved in gzip of ndjson format for storage and analysis.

### Challenges Faced
1. **Page Structure Variability**: The scraper handles cases where data may be structured differently on different pages, ensuring robustness and reliability.
2. **Blocking and Authentication**: Measures are taken to prevent blocking and ensure compliance with the website's terms of service.

### Improvements and Optimizations
1. **Error Handling**: Implement more robust error handling mechanisms to handle edge cases gracefully.
2. **Proxy Rotation**: Introduce proxy rotation to enhance anonymity and prevent IP blocking.
3. **Dynamic Page Navigation**: Develop adaptive page navigation techniques to handle dynamic content loading.
4. **Data Validation**: Implement data validation checks to ensure the integrity and accuracy of extracted data.

## Execution Steps
```bash
# Clone this project
$ git clone https://github.com/{{YOUR_GITHUB_USERNAME}}/food-grab-web-scraping

# Access
$ cd food-grab-web-scraping

# Setup virtual environment
$ python3 -m venv venv

# Install dependencies
$ pip install -r requirements.txt

# Run the project
$ run XHR.py file
```

To execute the code locally, follow these steps:
1. Clone the repository to your local machine.
2. Install the required dependencies specified in the `requirements.txt` file.
3. Run the main script to initiate the scraping process.
4. Monitor logs for any errors or warnings.
5. Upon completion, verify the extracted data in the specified gzip of ndjson file.


#### <i>Please note, this project is developed for education and learning purposes only.</i>
