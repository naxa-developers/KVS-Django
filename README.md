## KVS

### Setting up a development environment
#### 1. Clone the repository.
```
 git clone https://github.com/naxa-developers/KVS-Django.git
```
#### 2. Rename .env_sample to .env and change it settings accordingly for the project
> Make sure you create the database with correct privileges

#### 3. Build Docker Environment

```
docker-compose build
```
#### 4. Run the Docker Containers

```
docker-compose up
```

#### 4. Load Initial Data from fixtures

```
python manage.py loaddata fixtures/province.json
```
 ##### Similarly load data for tables District, Municipality, Theme, Category, Question and Answer, from respective json files in fixtures.

#### 6. Launch Browser
Launch browser to http://localhost:8021/api/v1/ to launch the API Explorer