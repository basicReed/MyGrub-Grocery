# MyGrub Grocery

<img width="1405" alt="MyGrub Home" src="https://user-images.githubusercontent.com/109553225/204412556-0c2767b4-614d-464f-8864-4a891ef2ca86.png">

## Demo

A demo is available at https://mygrub.herokuapp.com/.

## Desciption

This application serves as my first capstone for Springboard's Software Engineering Career Track. MyGrub is a space to search for recipes while filtering out allergies and other ingredients.  Users can save recipes to account favorites or add ingredients to their shopping list if it's not already in it. 

## Features

This application is for searching recipes from API's while filtering the needs of the user.  The following features are supported:

- Account creation to save user data 
- Edit user account from user page
- Seach for recipes from API while filtering out selected intoleraces.
- Display 12 searched recipes (limited by free API tier)
- Favorite recipes to user profile
- View recipe details while listing out instructions and ingredients
- Add and remove items to and from grocery list 

## User Flow

## Technologies Used
The project is mostly written in Python while using JavaScript for some client facing fucntionality.  It's also using Flask as a framework, SQLAlchemy as an ORM, and backed by a PostgresSQL database.


## APIs

I utilized Spoonaculars free recipe and ingredients API for the search and filtering features.  Docs and other info can be found here: https://spoonacular.com/food-api/docs

## Testing

Requires a postgres database named mygrub_test. In the top-level directory, run: 
python3 -m unittest

## Looking Forward

While the project meets the requirements for a capstone submittion, it's far from the posibilities of completion.  Some features are limited by the API free tier.  Possible future addition iclude the following:

- Google and Apple Sign-in option
- Options for grocery items to have unit of measurements and amount needed (available with a higher     API call limit)
- Pagination/more search results (limited by API call limit)
- Print/Email of user grocery list
- Further customized UI for better flow and usibility

