# crypto_merchant_payments

## Disclaimer : This is just for educational purpose!! use at your own risk


# My Project
Welcome to my project! Here's a video showcasing its features:
https://github.com/harshdabhi/crypto_merchant_payments/assets/109458952/ccf0bb52-e449-49a4-a8bf-098b40f6be10

## Installation process

# Step1 create a new environment
conda create --name myenv

conda activate myenv

# step2 run setup.py

pip install -r requirements.txt



# step 3
go to https://app.infura.io and generate api

put this  api into new file name as config.ini and type following inputs

[infura] 

api_url:'your api url here'

# step 4 run django to start server
python manage.py runserver 0.0.0.0:8000




