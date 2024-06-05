# CarLoanCalculator
Welcome to CarLoanCalculator, your one-stop solution for evaluating the financial aspects of owning a vehicle. This repository provides a comprehensive toolset to assist users in making informed decisions regarding car ownership costs. Leveraging web scraping techniques and currency conversion APIs, CarLoanCalculator ensures accurate and reliable data for precise calculations.

## Features
### Loan Calculation
Calculate the estimated monthly loan payments based on the principal amount, interest rate, and loan term.

### Gas Cost Calculation
Estimate the monthly or yearly fuel expenses by inputting the vehicle's fuel efficiency and current gas prices.

### Repair and Maintenance Cost Calculation
Anticipate the annual maintenance and repair costs by considering factors such as vehicle make, model, and mileage.

### Compare Overall Costs of Two Vehicles
Compare the total ownership costs of two vehicles side by side and receive recommendations based on the analysis.

## Demo
![Demo Showcase](https://github.com/MarnoShepherd/CarLoanCalculator/blob/main/docs/Showcase%20Demo.gif)

## Flowchart
![Flowchart](https://github.com/MarnoShepherd/CarLoanCalculator/blob/main/docs/FlowChart.png)

Here is a flowchart that illustrates the basic steps involved in using the project :

## Technologies

The project is built using :

* Python
* Git
* Key detection & Screen cleaning
* Webscraping with BeautifulSoup
* Exchange Rate API

## Getting Started

### Clone the Repository

To get started with the project, clone the repository to a local machine using the following command :

```git
git clone https://github.com/MarnoShepherd/CarLoanCalculator.git
```
### Install Dependencies

Once you've cloned the repository, navigate to the project directory and install the dependencies using the following command :
```git
pip install -r requirements.txt
```
This will install all the dependencies listed in the `requirements.txt` file.

### Running the Project

To run the project, use the following command :
```git
python car_loan_calculator.py
```
You can then interact with the project via the command-line interface.

## Fixed Bugs :
### Problem :
- Program couldn't get mid-grade gas prices, checked scraper.py and scraper is retrieving the data correctly from the website, 
however whenever user tries to get mid-grade gas price no matter what state, it fails, this is only the case with mid-grade
### Solution :
- Had a .capitalize() after getting Gas Grade; however, since I was using enumerate to retrieve the data, it was not necessary. I removed this and the data was loading correctly

## Testing :
- Code was tested manually

## Existing bugs :
- Doesn't contain any known bugs

## Future Features :
- Scrape vehicle makes and models directly from the web instead of reading from a JSON file. I wanted to implement this, but couldn't do it due to the website loading models dynamically
- Implement automated testing

## Links

For more information about the project, visit the [GitHub repository](https://github.com/MarnoShepherd/CarLoanCalculator).
