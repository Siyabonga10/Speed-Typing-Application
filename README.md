# Speed typing application

A speed typing application written in python to help you improve your typing abilities. The app shows a passage of text to the user and the user attempts to type out what is one the screen, as they type letters typed out correctly are shown in white while those that are incorrect are shown in red. At the end the app calculates the user's wpm and accuracy based off of data accumulated throughout the test. The app then displays this information to the user. The app features a very simple and minimalistic user interface.

## Why
I am currently trying to imrpove my own typing skills and this project was a good way for me to make a tool custom to my needs while also improving my coding abilities. The app is fairly simple but some improvements are in the pipeline.

## Modes
The app has three time modes for the user depending on the how comfortable the user is, the app has a one, three and five minute mode, in each case the passages lengths are about the same length.

## The database
The passages are stored in a local `SQL` file, adding a new passage can be done quickly via the command line and these will then show up in the application. Unfortunately the passages cannot be added directly from the application, this will be a feature in future however. 

## Menus
The app makes use of a custom made menu class. The menu is created by passing in a set of options as strings and a list of return items. When the user clicks enter on an option the associated return value is given back to the parent, this gives control to the application while keeping menus versatile as they can accept anything in python.

## Libraies and modules used

The makes use of `pygame` for graphics related tasks, and `SQLalchemy` to talk to a local database. Everything else is built from scratch. Both of these modules can be installed using the resective `pip install` commands.