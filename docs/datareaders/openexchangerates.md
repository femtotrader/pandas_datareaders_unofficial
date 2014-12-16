#Open Exchange Rates

[Open Exchange Rates](https://openexchangerates.org/) provides an API to fetch currency rates.

You need to signup to get an API key (named `app_id`)

    from pandas_datareaders import DataReader
    dr = DataReader("OpenExchangeRates", expire_after=5*60, app_id='...')
    currencies = ["EUR", "GBP", "CHF", "USD", "AUD", "CAD", "JPY"]
    data = dr.get(currencies) # or data = dr.get() # to get all available currencies

You can display conversion rates matrix using:

    data["matrix"]


You should see conversion rates matrix (as DataFrame)

               EUR       GBP       CHF       USD
    EUR          1  0.796835  1.201372  1.247038
    GBP   1.254965         1  1.507679  1.564989
    CHF  0.8323818  0.663271         1  1.038012
    USD     0.8019  0.638982   0.96338         1

You can use this conversion matrix to convert amount:

    dr.convert(100, "EUR", "GBP")

should display:

    79.68350168350169

It means that 100 EUR are worth 79.68 GBP (at this date: 2014-12-16 10:45).

Caution! use this at your own risk. That's still very experimental.
