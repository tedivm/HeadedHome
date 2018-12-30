# HeadedHome Button

The "HeadedHome" app is a simple lambda function meant to work with an AWS IoT Button. It uses the BART API to find when the next catchable trains are coming (taking into account the walk from the office), which it uses to estimate the time which I'll get home.

One a single push of the button it sends me a text message with the train depature times and the estimated time I'll be home if I left then. A double push of the button also sends my fiance a text message letting her know when I'll be home.

## Configuration

### Building

Before creating the lamdba package edit the settings on the top of `app.py` to match your specific setup.

Once done, run `make package`. You can then upload the `dist/function.zip` file using the AWS Console.


### Environmental Variables

* TWILIO_ACCOUNT
* TWILIO_TOKEN
* TWILIO_PHONE
* MY_NUMBER
* SO_NUMBER


## Lambda Settings

* Handler Function: `app.lambda_handler`
* Memory: 128mb (the minimum)
* Timeout: 10 seconds (the API calls are the biggest cost, but generally requests take less than two seconds)
