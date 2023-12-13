
# Fashion-E-Commerce-Platform

## How To Setup
Make sure you have python3 and Django installed. Also install virtualenv using `python3 -m pip install --user virtualenv` if you don't have it already.

1. Clone This Project git:
```bash
clone https://github.com/Arbaz-Khan2/Fashion-E-Commerce-Platform.git
```
2. Go to Project Directory:
```bash
cd FashionECommerce
```
3. Create and Activate the Virtual Environment:
```bash
python3 -m venv env
source env/bin/activate
```
4. Install Requirements Package:
```bash
pip install -r requirements.txt
```
5. Migrate Database:
```bash
python manage.py migrate
```
6. Finally Run The Project:
```bash
python manage.py runserver
```
Note: If you face an error related to "cors" then please install the following package
```bash
pip install django-cors-headers
```
