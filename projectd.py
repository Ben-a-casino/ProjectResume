import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
"""
This is the Harvard Forest Data and is read from the CVS file.
Parameters:
This parameters are a filename(str): the path to the CSV data file.
Returns:
This returns a n.arrary: A numpy array containing all data from the CSV file.
    """
def readdata(filename):
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)
    return data
"""
This calculates a summary staatics and create a visualization of the C02 flux data as
time series.
Parameters:
The parameters are a hf (np.ndarray): The numpy array containing the 
Harvard Forest data.
Returns:
This returns a np.ndarray: An array containing the number of 
observations, mean, 25th quantile, and 75th quantile.
"""
def summarizedata(hf):

    plt.scatter(hf[:, 0] + (hf[:, 1]-1)/12, hf[:, 3], color='blue')
    plt.xlabel('Year')
    plt.ylabel('CO2 flux')
    plt.title('Time Series of CO2 Flux')
    #plt.show()

    data_points = hf.shape[0]
    mean_flux = np.mean(hf[:, 3])
    percentile_25 = np.percentile(hf[:, 3], 25)
    percentile_75 = np.percentile(hf[:, 3], 75)

    return data_points, round(mean_flux, 3), round(percentile_25, 3), round(percentile_75, 3)
"""
This calculates the percentage of missing data poitns in each year
and plots the results and checks if the given year is a leap year.
Parameters:
The parameters are that hf (np.ndarray): The numpy array containing 
the Harvard Forest data. We also assume the first column is the year.
Returns:
It returns a np.ndarray: An array containing the percentage of 
points missing in each year.
    """
def missingdata(hf):
    years = hf[:, 0]
    years_unique = np.unique(years)
    min_year = int(np.min(years_unique))
    max_year = int(np.max(years_unique))
    
    missing_percentages = []
    
    for y in range(min_year, max_year + 1):
        indices = (hf[:, 0] == y)
        days_recorded = np.sum(indices) 
        is_leap_year = (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0))
        expected_days = 366 if is_leap_year else 365
        
        if days_recorded == 0:
            missing_percentages.append(100.0)  
        else:
            missing_percentage = (expected_days - days_recorded) / expected_days * 100
            missing_percentages.append(round(missing_percentage, 3))

    plt.figure(figsize=(10, 6))
    years_range = np.arange(min_year, max_year + 1)
    plt.bar(years_range, missing_percentages, color="skyblue")
    plt.title('Percentage of Missing Data per Year')
    plt.xlabel('Year')
    plt.ylabel('Percentage of Missing Data')
    plt.xticks(years_range)
    plt.grid(axis='y')
    plt.show()
    
    return missing_percentages 

"""
This calculates the average CO2 fluxes for each month in each year and plot selected years.
Parameters:
The parameters aare hf (np.ndarray): The numpy array 
containing the Harvard Forest data. We assumes the first column is the year, 
second column is the month, and third column is the CO2 flux.
Returns:
This returns a np.ndarray: An array where rows correspond to years and 
columns to months, containing average CO2 fluxes.
    """

def seasonalcycle(hf):
    years = hf[:, 0].astype(int)
    months = hf[:, 1].astype(int)
    flux = hf[:, 3]

    min_year = np.min(years)
    max_year = np.max(years)
    month_range = range(1, 13)

    all_year_month = pd.MultiIndex.from_product([range(min_year, max_year + 1), month_range], names=['year', 'month'])
    df_full = pd.DataFrame(index=all_year_month).reset_index()
    df = pd.DataFrame({'year': years, 'month': months, 'flux': flux})
    df_avg = df.groupby(['year', 'month'])['flux'].mean().reset_index()
    df_final = pd.merge(df_full, df_avg, how='left', on=['year', 'month'])
    result = df_final.pivot(index='year', columns='month', values='flux').reindex(range(min_year, max_year + 1))

    plt.figure(figsize=(12, 6))
    for idx, year in enumerate(result.index):
        plt.plot(month_range, result.loc[year, :], marker='o', label=f'Year {year}')
    plt.title('Seasonal CO2 Flux Cycle at Harvard Forest')
    plt.xlabel('Month of the Year')
    plt.ylabel('Average CO2 Flux')
    plt.xticks(month_range, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend()
    plt.grid(True)
    plt.show()

    return result

"""
This estimates regression coeffcients for prediciting CO2 fluxes based on enviromental factors
and visualizes the actual and predicted CO2 fluxes as well as the contriubtions of each predictor.
Parameters:
The parameters are the hf (np.ndarray): The numpy array containing 
the Harvard Forest data. Furthermore, columns should be ordered as: [CO2 flux, net radiation, 
air temperature, water vapor, wind speed]
Returns:
This returns a tuple: A tuple containing the regression coefficients 
and the modeled CO2 flux estimates.
    """
def HFregression(hf):
    try:
        X = np.column_stack((np.ones(len(hf)), hf[:, 4:8]))
        y = hf[:, 3]
        betas = np.linalg.inv(X.T @ X) @ X.T @ y

        y_pred = X @ betas
        plt.plot(hf[:, 0] + (hf[:, 1]-1)/12, y, 'b-', label='Actual')
        plt.plot(hf[:, 0] + (hf[:, 1]-1)/12, y_pred, 'r--', label='Predicted')
        plt.xlabel('Year')
        plt.ylabel('CO2 Flux')
        plt.title('Regression Model Fit')
        plt.legend()
        #plt.show()

        return betas, y_pred  # Ensure to return both the coefficients and predictions
    except Exception as e:
        print(f"Error in regression analysis: {e}")
        return None, None


    """
This calculates and visualizes the average modeled CO2 flux for each year at Harvard Forest.
Parameters:
The parameters are hf (np.ndarray): The numpy array containing the Harvard Forest data, 
with years in the first column. Furthermore the modelest (np.ndarray) us the modeled CO2 flux
estimates corresponding to the entries in hf.
Returns:
This returns a list: list of averages of modeled CO2 flux for each year, 
rounded to three decimal places.
    """
def averagecarbon(hf, modelest):
    years=[]
    average_flux_per_year =[]
    
    min_year= int(np.min(hf[:, 0]))
    max_year= int(np.max(hf[:, 0]))
    
    for x in range(min_year, max_year+1, 1):
        x-= min_year
        years.append(min_year+x)
        
    for year in years:
        year_fluxes =[]
        
        for i in range(len(hf)):
            if hf[i][0]== year:
                year_fluxes.append(modelest[i])
        if len(year_fluxes) >0:
            total_flux =sum(year_fluxes)
            average_flux =round(total_flux/ len(year_fluxes),3)
        else:
            average_flux=np.nan
        average_flux_per_year.append(average_flux)
        
    plt.figure(figsize=(10, 6))
    plt.scatter(years, average_flux_per_year, color='blue')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title('Annual Average Modeled CO2 Flux at Harvard Forest')
    plt.xlabel('Year')
    plt.ylabel('Average CO2 Flux (modeled)')
    plt.grid(True)
    
    return average_flux_per_year


    """
This excutes the functions above so it reads the data from the CSV
file. It calculates the summary statics and creats the C02 flux data time series graph
It calulates the percentage of the missing data entries and creates the bar graph.
Its computes and plots the seasonal cycle of C02 flux data. It performs regression analysis 
C02 fluxes. It caculates the average model c02 flux for each year. 
Parameters:
The Parameters are the CSV file containg the Harvard Forest data. 
Returns:
This returns number of data points as n data, the mean, 25th and 75th percentile of C02 flux. It also lists 
the percentages of missing data per year. It also returns a datafrom containing the averaage C02 flux per 
month for each year. It also returns regression coefficients from the C02 flux prediction
model. Its models the estimates of c02 flux and lissts the average modeeled C02 flux per year. 
    """
    
if __name__ == "__main__":
    filename = 'harvard_forest.csv'
    hf = readdata(filename)
    ndata, hfmean, hf25, hf75 = summarizedata(hf)
    missing_data = missingdata(hf)
    month_means = seasonalcycle(hf)
    betas, modelest = HFregression(hf)
    means = averagecarbon(hf, modelest)
    print("Summary Statistics:", ndata, hfmean, hf25, hf75)
    print("Missing Data Percentages:", missing_data)
    print("Monthly Means:", month_means)
    print("Regression Coefficients:", betas)
    print("Average Modeled CO2 Fluxes:", means)
    
    