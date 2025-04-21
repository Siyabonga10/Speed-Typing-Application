# Speed Typing Application

A speed typing application written in Python to help you improve your typing speed and accuracy. The app displays a passage of text, and the user types it out as quickly and accurately as possible. Correctly typed letters are shown in white, while incorrect ones are highlighted in red. At the end of the test, the app calculates and displays the user's Words Per Minute (WPM) and accuracy. The app features a clean and minimalistic user interface.

![Demo Screenshot](./assets/demo/gameplay.png)

---

## Features

- **Typing Test**: Displays a passage for the user to type and provides real-time feedback on accuracy.
- **Performance Metrics**: Calculates WPM and accuracy based on the test results.
- **Time Modes**: Choose between 1-minute, 3-minute, or 5-minute tests.
- **Custom Menus**: A versatile menu system for easy navigation.
- **Database Integration**: Passages are stored in a local SQL database for quick access.

---

## Why I Built This

I wanted to improve my own typing skills and decided to create a tool tailored to my needs. This project also served as a way to enhance my coding abilities. While the app is simple, there are plans for future improvements.

---

## Installation

Follow these steps to set up and run the application:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/speed-typing-application.git
   cd speed-typing-application

## Modes
The app offers three time modes to suit different comfort levels:

1 Minute Mode: Short and quick.
3 Minute Mode: A balanced challenge.
5 Minute Mode: For those who want a longer test.
Each mode uses passages of similar lengths to ensure consistency.

## Database
The passages are stored in a local SQL database. You can add new passages via the command line, and they will automatically appear in the app. In the future, the app will include a feature to add passages directly from the interface.

## Menus
The app uses a custom-built menu class. Menus are created by passing a set of options as strings and a list of return values. When the user selects an option, the associated return value is passed back to the parent, making the menus versatile and easy to integrate.

Libraries and Modules Used
The app relies on the following libraries:

### Pygame: For graphics and UI.
### SQLAlchemy: For database interactions.
### Install these libraries using:

Demo
Here are some screenshots of the application in action:
![Demo Screenshot](./assets/demo/gameplay.png)
![Demo Screenshot](./assets/demo/gameplay.png)

Typing Test Results Screen

Future Improvements
Add the ability to input new passages directly from the app.
Introduce more customization options for the typing test.
Improve the UI for a more modern look.
Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

