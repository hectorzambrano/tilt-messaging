# tilt-messaging
Homebrew Temperature Messaging Service: Checks temperature data from a Tilt Wireless Hydrometer during fermentation and sends a text message to the user to alert of temperature fluctuations.

This program uses Google's API and the Twilio text messaging platform. The user will need to have accounts for both.

**Tilt Hydrometer Set-Up**

The Tilt Hydrometer is a free floating thermometer and hydrometer designed for homebrewing. It provides real-time monitoring of temperature and specific gravity of the fermenting beer while it is in the fermentation vessel. The hydrometer connects to most Bluetooth 4.0 devices and can be read through the downloadable Tilt App or a Raspberry Pi. The user can then optionally log data to the cloud using Google Sheets at a desired time interval (default is 15 minutes).

Instructions: Connect your Tilt Hydrometer in the Tilt App and go to settings. Enter your Gmail email, use the default clould URL and then start a new log. You should receive an email with the link to the Google Sheets.

**Make note of the text in the URL of the Google Sheet after the "d/". The program will ask for this as an input**

![image](https://user-images.githubusercontent.com/65422369/118894555-1333d280-b8ca-11eb-9105-d7891714527f.png)

**Google API Set-Up**

1. Log into your Google account.
2. Visit: https://developers.google.com/workspace/guides/create-project and follow the instructions to create a project and enable an API.
3. Visit: https://developers.google.com/workspace/guides/create-credentials to create OAuth Credentials and then create Desktop Application credentials:

![image](https://user-images.githubusercontent.com/65422369/118862753-b2919f00-b8a3-11eb-8273-ccdf6513f285.png)

4. Save the renamed credentials.json file to the working directory you will be running the program from.
5. Make sure you have Python 2.6 or greater installed and the pip package management tool.
6. Intall the Google Client Library by running the following command:

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

**Twilio Account Set-Up**

1. Sign up for a free Twilio trial account using the personal phone number that you want to receive text messages at: https://www.twilio.com/try-twilio
2. Once your personal phone number is verified and your account is created, navigate to Phone Numbers tab in the Twilio Console on the left side of your screen.
3. Click on "Get your first Twilio number".
4. If you don't like the number Twilio selected for you, you can search for a different number instead.

![image](https://user-images.githubusercontent.com/65422369/118865755-e9b57f80-b8a6-11eb-9da8-47712d0de853.png)

**5. Make note of your "Account SID", "Auth Token", and "Twilio Phone Number". The program will ask for these as inputs.**
