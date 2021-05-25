#!usr/bin/#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Homebrew Temperature Messaging Service

Checks temperature data from a Tilt Wireless Hydrometer during fermentation and
sends a text message to the user to alert of temperature fluctuations.

Hector A Zambrano
May 2021

"""

__author__ = 'Hector A Zambrano'
__email__ = 'hector.a.zambrano@gmail.com'
__status__ = 'dev'

import os
from twilio.rest import Client

import pickle
import os.path

import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler


sheet_name = input("Enter spreadsheet ID: ")
low_alert = input("Enter low temperature alert: ")
high_alert = input("Enter high temperature alert: ")
personal_number = input("Enter personal phone number: ")
twilio_number = input("Enter Twilio phone number: ")

# Find your Account SID and Auth Token at twilio.com/console
# See http://twil.io/secure

account_sid = input("Enter Twilio Account SID: ")
auth_token = input("Enter Twilio Auth Token: ")
client = Client(account_sid, auth_token)

# Follow readme instructions to set up Google API credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def temp_check():   #function to run every 1 hour

    # Function to obtain Google API credentials
    def gsheet_api_check(SCOPES):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES) # user needs to save json file in working directory after setting up credentials
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    # Function to call Google API and copy data from spreadsheet

    from googleapiclient.discovery import build
    def pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL):
        creds = gsheet_api_check(SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=DATA_TO_PULL).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                      range=DATA_TO_PULL).execute()
            data = rows.get('values')
            print("COMPLETE: Data copied")
            return data

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    DATA_TO_PULL = 'Data'
    SPREADSHEET_ID = sheet_name
    data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL)

    column_names = ["Timestamp", "Timepoint", "SG", "Temperature", "Color", "Beer", "Comment"]
    df = pd.DataFrame(data, columns=column_names)
    df = df.drop(df.index[0])
    df = df.set_index('Timestamp')
    df = df.sort_values(by='Timestamp', ascending = False) # sorts by most recent Tilt Hydrometer reading

    # print(df)

    current_temp = df.iloc[0,2]
    # print(current_temp)

    if current_temp <= low_alert:
        message = client.messages \
                    .create(
                         body="Low fermentation temperature. Currently " + current_temp + " degF.",
                         from_= twilio_number,
                         to= personal_number
                     )

    if current_temp >= high_alert:
        message = client.messages \
                    .create(
                         body="High fermentation temperature. Currently " + current_temp + " degF.",
                         from_= twilio_number,
                         to= personal_number
                     )

scheduler = BlockingScheduler()
scheduler.add_job(temp_check, 'interval', hours=1)
scheduler.start()
