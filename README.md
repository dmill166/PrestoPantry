# [PrestoPantry](https://prestopantryapp.com) [![Build Status](https://app.travis-ci.com/dmill166/PrestoPantry.svg?branch=main)](https://app.travis-ci.com/dmill166/PrestoPantry) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dmill166_PrestoPantry&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dmill166_PrestoPantry)
The PrestoPantry project started as a group project initially contributed to by Adam Wojdyla, Riley Strong, Dakota Miller, and Hector Cruz.<br>
This project was completed for the purpose of CS 4360 (Technical Software Project) as our Senior Experience course at Metropolitan State University of Denver.<br>

## Technologies Used
- Python3/HTML/CSS
- Django
- PostgreSQL (prior to AWS RDS deployment)
- AWS
  - RDS
  - S3
  - EC2
  - IAM (Group and User Management)
  - Cloudwatch
- [Figma](https://www.figma.com/file/yXShQOP8BtZpHq88UahKqI/Flavor-Town-WireFrame?node-id=0%3A1)
- [Trello](https://trello.com/b/Nb03JChw/presto-pantry)
- dbdiagram.io
- Travis CI
- Spoonacular API
- Google OAuth Sign In
- Google Custom Search API
- GitGuardian
- Radon
- Sonar Cloud

<br>

## Required Modules
To install required modules run these commands **INSIDE** of the Python virtualenv (assuming Python is installed):<br>
  - `python -m ensurepip --upgrade`<br><br>
  - `pip install -r requirements.txt`<br><br>
## Required Environment Variables
In order to use the project as we left it in May 2022, you'll need a few environment variables:<br>

- [DJANGO_SECRET_KEY](https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-SECRET_KEY): A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
- SPOON_API_KEY
- [PRESTOPANTRY_DB_NAME](https://docs.djangoproject.com/en/4.0/ref/databases/): Pending your database solution, the need for these credentials may vary. Tailor your code appropriately. (used in storing user models and ingredients models)
- PRESTOPANTRY_DB_USER: Reference link from PRESTOPANTRY_DB_NAME above for more details
- PRESTOPANTRY_DB_PASSWORD: Reference link from PRESTOPANTRY_DB_NAME above for more details
- PRESTOPANTRY_DB_HOST: Reference link from PRESTOPANTRY_DB_NAME above for more details
- PRESTOPANTRY_DB_PORT: Reference link from PRESTOPANTRY_DB_NAME above for more details
- [PRESTOPANTRY_GOAUTH_CLIENT_ID](https://developers.google.com/identity/sign-in/web/sign-in): You'll need an account through the Google Developers Platform to be assigned a Client_ID and Client_Secret for using this feature (allowing users to create an account at PrestoPantry & then log in using their Google Account)
- PRESTOPANTRY_GOAUTH_CLIENT_SECRET: Reference link from PRESTOPANTRY_GOAUTH_CLIENT_ID above for more details
- [GITGUARDIAN_API_KEY](https://docs.gitguardian.com/internal-repositories-monitoring/gg_shield/getting_started): This solution was used to ensure as we pushed commits to the remote repository that we were not pushing secrets (such as API Keys)
- [PRESTOPANTRY_GCS_DEVELOPER_KEY](https://developers.google.com/custom-search/v1/introduction): Use of Google Custom Search imported images for recipe ingredients to display while searching for ingredients (can help a user validate they are adding the correct ingredient to their pantry)
- PRESTOPANTRY_GCS_CX: Reference link from PRESTOPANTRY_GCS_DEVELOPER_KEY above for more details

## Supported Modules

### Landing Page (Pre-Log In)
Features:<br>

- Sign Up / Log In buttons easily accessible
- Carousel options to provide alternate user-driven routing
- (not shown) Link to GitHub Repo at bottom of every page

![](/prestopantry_app/static/images/readme_landing_page_before.png)

### Sign Up Page
Features:<br>

- Various enforcements in place to drive stable back-end design and secure user experience
- Supplemental option available for Google OAuth account creation
- Meaningful error messaging provided to aid users in account creation
![](/prestopantry_app/static/images/readme_sign_up.png)

### Log In Page
Features:<br>

- Various enforcements in place to drive stable back-end design and secure user experience
- Supplemental option available for Google OAuth Sign In
- Meaningful error messaging provided to aid users in sign in
![](/prestopantry_app/static/images/readme_log_in.png)

### Landing Page (Post-Log In)
Features:<br>

- Successful Google OAuth Sign In illustrated
- Greeting message individualized for each user
- Carousel option currently showing placeholder for new feature (Community interactions page, TBD delivery date)
![](/prestopantry_app/static/images/readme_landing_page_after.png)

### My Account Page (Email Log In)
Features:<br>

- Enables users to edit all account details after account creation
- Meaningful error messaging provided to aid users in sign in
![](/prestopantry_app/static/images/readme_my_account_email.png)

### My Account Page (Google Log In)
Features:<br>

- Enables users to edit account details specific to PrestoPantry application after account creation
  - Other details should only be edited directly in users' Google account
- Meaningful error messaging provided to aid users in sign in
![](/prestopantry_app/static/images/readme_my_account_google.png)

### Empty Pantry Page
Features:<br>

- Prior to adding any ingredients or after removing all ingredients, a user will not have any ingredients in their pantry
![](/prestopantry_app/static/images/readme_empty_pantry.png)

### Ingredient Search Page (Finding Results)
Features:<br>

- Upon searching ingredients, users will be offered various products to add to their personal pantry for use in recipe searches
![](/prestopantry_app/static/images/readme_ingredient_search_w_results.png)

### Pantry Ingredients page
Features:<br>

- Displays current ingredients present in a user's pantry. From here, users can choose to add more ingredients, remove some or all ingredients, or begin searching recipes matching their ingredients
![](/prestopantry_app/static/images/readme_pantry_w_ingredients.png)

### Recipe Results Page
Features:<br>

- Once a user is satisfied with their pantry ingredients they've personalized, they can search recipes detailed with used ingredients, unused ingredients, and missing ingredients
![](/prestopantry_app/static/images/readme_recipe_results.png)

### Read Me Page
Features:<br>

- Introduced website vistors to site creators
  - In addition to photos and descriptions, included embedded links to GitHub/LinkedIn specific to each user
![](/prestopantry_app/static/images/readme_readme.png)
