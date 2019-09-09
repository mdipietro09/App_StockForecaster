
name = "Stock Forecaster"

host = "0.0.0.0"

threaded = False

debug = False

## dev
#port = 5000

## prod
port = int(os.environ.get("PORT", 5000))


