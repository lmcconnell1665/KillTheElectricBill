# KillTheElectricBill
Python job that gathers info from the Nest and Weather APIs to save for analysis

I have this project currently running as a CRON job to save the data every 5 minutes. You will need to create a `access_token.txt` and `refresh_token.txt` file containing these initial values. The script will update them each run to stay fresh.

It is doesn't work for over an hour, you need a fresh access token. Next time this happens to me, I'll implement that as well.