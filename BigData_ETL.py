#!/usr/bin/env python
# coding: utf-8

import h5pyd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def plot_ghi_at_time(country_meta, time_index, dset, specific_time, output_folder, country):
    # Find the index for the specific time
    timestep = np.where(time_index == specific_time)[0][0]
    
    # Extract GHI data for the specific time
    ghi_data = dset[timestep][country_meta.index]

    # Generate and save plot
    plt.figure()
    plt.scatter(country_meta['longitude'], country_meta['latitude'], c=ghi_data, cmap='YlOrRd')
    plt.colorbar(label='GHI')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'GHI for {country} at {specific_time}')
    plt.savefig(f'{output_folder}{country}_ghi_{specific_time}.png')
    plt.close()

def main():
    # Open HDF5 file
    f = h5pyd.File("/nrel/nsrdb/meteosat/meteosat_2019.h5", 'r')
    dset = f['ghi']
    meta = pd.DataFrame(f['meta'][...])
    meta['country'] = meta['country'].apply(lambda x: x.decode('utf-8'))

    # Efficiently load time_index
    time_index = pd.to_datetime(f['time_index'][...].astype(str))

    # Specific time for GHI data
    specific_time = '2019-12-31 12:00:00'

    # Save time_index
    output_folder = 'output/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    time_index_df = pd.DataFrame(time_index, columns=['time'])
    time_index_df.to_csv(f'{output_folder}time_index.csv', index=False)

    # Process countries
    countries = ['India', 'Indonesia', 'China', 'South Africa']
    for country in countries:
        # Filter metadata for the current country
        country_meta = meta.loc[meta['country'] == f'{country}']
    
        # Define the filename for the CSV
        csv_filename = f'{output_folder}{country}_ghi.csv'
    
        # Save the filtered metadata to CSV
        country_meta.to_csv(csv_filename, index=False)
        
        # Plot GHI data for the specific time
        plot_ghi_at_time(country_meta, time_index, dset, specific_time, output_folder, country)


    print("CSVs and PNG maps created successfully.")

if __name__ == "__main__":
    main()