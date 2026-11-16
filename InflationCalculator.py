'''
FINE 3300 - Assignment 2
Name: Eden Johannes
Student number: 221214440
Date: November 16, 2026

'''
#importing the needed packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Reading the csv file using pandas to get the into on the CPI's
cpi_data = pd.read_csv(
    "STATIC_INFLATIONCALC.csv",
    skiprows=8, #To skip the unnecessary section since we only need the data table
    header=0,
    usecols=[0, 1],
    names=["date", "CPI"]
)

#Converts the date column into a datetime format.
cpi_data["date"] = pd.to_datetime(cpi_data["date"])

#Converts the CPI values into numeric values.
cpi_data["CPI"] = pd.to_numeric(cpi_data["CPI"])

#Removes any rows with missing values.
cpi_data = cpi_data.dropna()

#Sorts the data by date.
cpi_data = cpi_data.sort_values("date")

#creates the annual inflation column by finding the percentage change 
cpi_data["Annual Inflation (%)"] = (
    cpi_data["CPI"].pct_change(periods=12) * 100 #period = 12 because it's monthly, so it compares each month with the same month in the previous year.
)

#Creating a graph with two vertical axes.
fig, ax1 = plt.subplots(figsize=(12, 6))

#Plots the CPI on the left axis (aka ax1).
ax1.plot(
    cpi_data["date"], #x-axis
    cpi_data["CPI"], #1st y-axis is the CPI
    label="Consumer Price Index (CPI)", 
    linewidth=2
)

ax1.set_xlabel("Date") #To add the label for the x-axis
ax1.set_ylabel("Consumer Price Index") #To add the label on the 1st y-axis
ax1.set_title("Canadian Consumer Price Index and Annual Inflation Rate") #To add the title

#Adds a dotted horizontal line at the CPI base level, which is 100.
ax1.axhline(
    y=100,
    linestyle=":",
    label="CPI Base Level (100)"
)

ax1.grid(True) #Creates the grid to better visualize

#Plots a second axis for annual inflation.
ax2 = ax1.twinx()

ax2.plot(
    cpi_data["date"],
    cpi_data["Annual Inflation (%)"],
    label="Annual Inflation Rate (%)",
    linestyle="--", #a different linestyle to differentiate
    linewidth=1.5
)

ax2.set_ylabel("Annual Inflation Rate (%)") #To add the label on the 2nd y-axis

#Combines the legends from both axes.
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc="upper left" #Placement of the legend
)

# Adjust the graph layout and save it.
fig.tight_layout()
fig.savefig("cpi_graph.png", dpi=300)

plt.show() #To show the graph


#This method gets the user to enter a date
def get_date(prompt):
    date_input = input(prompt)
    return pd.to_datetime(date_input, format="%Y-%m")



#This method calculates the inflation, eqivalent price, price difference, percentage change, and annualized inflation rate
def inflation_calculator():

    print("------------------------------------")
    print("------CPI INFLATION CALCULATOR------") #To make the title look good

    #Allows the user to input the original price 
    original_price = float(input("Enter the original price ($): "))

    #Allows the user to input the start and end date
    start_date = get_date("Enter the starting date (YYYY-MM): ")
    end_date = get_date("Enter the ending date (YYYY-MM): ")

    #To find the CPI values for both selected dates.
    start_cpi = cpi_data.loc[
        cpi_data["date"] == start_date, "CPI"
    ].iloc[0]

    end_cpi = cpi_data.loc[
        cpi_data["date"] == end_date, "CPI"
    ].iloc[0]

    #Calculates the equivalent price using the CPI ratio.
    equivalent_price = original_price * (end_cpi / start_cpi)

    #Calculates the difference in price.
    price_difference = equivalent_price - original_price

    #Calculates the percentage change.
    percentage_change = ((end_cpi / start_cpi) - 1) * 100

    #Calculates the number of months and years between the two dates.
    months_difference = ((end_date.year - start_date.year) * 12 + (end_date.month - start_date.month))
    years_difference = months_difference / 12

    #Calculates the annualized inflation rate.
    annual_rate = (np.power(end_cpi / start_cpi, 12 / months_difference) - 1) * 100
    
    #To display the calculation results
    print("--------CALCULATION RESULTS---------")

    print(f"Original price: ${original_price:,.2f}")
    print(f"Starting date: {start_date.strftime('%B %Y')}")
    print(f"Ending date: {end_date.strftime('%B %Y')}")
    print(f"Starting CPI: {start_cpi:.2f}")
    print(f"Ending CPI: {end_cpi:.2f}")
    print("------------------------------------")
    print(f"Equivalent price: ${equivalent_price:,.2f}")
    print(f"Difference in price: ${price_difference:,.2f}")
    print(f"Overall percentage change: {percentage_change:.2f}%")
    print(f"Time difference: {years_difference:.2f} years")
    print(f"Annualized inflation rate: {annual_rate:.2f}%")
    print("------------------------------------")

inflation_calculator()
