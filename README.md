# KillTheElectricBill
Python job that gathers info from the Nest and Weather APIs to save for analysis

I have this project currently running as a CRON job to save the data every 5 minutes. You will need to create a `access_token.txt` and `refresh_token.txt` file containing these initial values. The script will update them each run to stay fresh.

It is doesn't work for over an hour, you need a fresh access token. Next time this happens to me, I'll implement that as well.

```sql
-- create the sql tables to hold the data
create table nest_data (
    [id] int identity(1,1) not null primary key,
    [create_date] datetime2 not null default GETDATE(),
    humidity float null,
    temperature float null,
    fan varchar(25) null,
    mode varchar(25) null,
    eco varchar(25) NULL,
    hvac varchar(25) null,
    setpoint float null
)

create table weather_data (
    [id] int identity(1,1) not null primary key,
    [create_date] datetime2 not null default getdate(),
    [forecast_updated] datetime2 null,
    forecast_for varchar(50) null,
    temp float,
    wind_speed varchar(10),
    wind_direction varchar(25),
    icon varchar(150),
    short_forecast varchar(200),
    detailed_forecast varchar(250)
)
```