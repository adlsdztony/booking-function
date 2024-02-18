# booking-function
HKU booking system with Python and azure serverless function

## Setup
### clone the repository
```bash
git clone https://github.com/adlsdztony/booking-function.git
cd booking-function
```
### set environment variables
set your mogoDB connection string as MONGO_LINK on function app
```bash
func settings add MONGO_LINK <your-mongo-link>
```
### deploy to azure
```bash
func azure functionapp publish <your-function-app-name>
```
