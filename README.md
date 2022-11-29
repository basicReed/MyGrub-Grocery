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

- A user can log in or register a new account.  Successful registration logs the user in
- The user is presented with a number random recipes and a search bar with options to search and filter out ingredients based on intoleraces selected.
- The search form, when submited, displays the top results based on search peramiters.
- If the search is empty or no results are found they will be prompted with a message relecting the issue.
- Each recipe card has an option to add them to favorites and displays them on the user favorites page.
- Choosing one of the recipe cards will diplay a recipe details page which shows instructions and a list of ingredients needed.
- Selecting from the ingredients the user can add them to theor grocery list and it will be displayed on the grocery list page.
- The side navigation button opens several options for navigation accross the users profile. The options include "Find Recipes" (which is the home page), Favorites, Groceries, and an option to Log Out.
- Navigating to the Favorites page will list all the recipes favorited by the user.  The user will have the option to un-favorite or display the recipe details (similar to the home page)
- Navigating to the Groceries page lists out current groceries needed for your desired recipes.  
- On the Groceries page there are options to remove individual ingredients or remove them all.
- If remove all is selected the user will be prompted with a confirmation.
- Selecting the user icon at the top right (on mobile located in side navigation) you will be navigated to the user details page.
- On the user details page, information about the user will be displayed as well as an option to edit user details.
- Edit user details option will take the user to a form to edit either username or email.  There is password requirement to commit the changes.

## Technologies Used
The project is mostly written in Python while using JavaScript for some client facing fucntionality.  It's also using Flask as a framework, SQLAlchemy as an ORM, and backed by a PostgresSQL database.


## APIs

I utilized Spoonaculars free recipe and ingredients API for the search and filtering features.  Docs and other info can be found here: https://spoonacular.com/food-api/docs

## Testing

Requires a postgres database named `mygrub_test`. In the top-level directory, run: 
```
python3 -m unittest
```

## Looking Forward

While the project meets the requirements for a capstone submittion, it's far from the posibilities of completion.  Some features are limited by the API free tier.  Possible future addition iclude the following:

- Google and Apple Sign-in option
- Options for grocery items to have unit of measurements and amount needed (available with a higher     API call limit)
- Pagination/more search results (limited by API call limit)
- Print/Email of user grocery list
- Further customized UI for better flow and usibility

