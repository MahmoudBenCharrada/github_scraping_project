## Github Scrapping with existing Backend

The objective is to scrape a website for information, store it in a database, and provide a web
interface to that data via a REST interface.
1. Install the backend
- Extract and install the backend from the attached archive file.
- Run the backend
- Open http://localhost:8000/docs in your browser to make sure the backend runs.
- Examine the API provided by the service
2. Create a Python script that:
- Takes one or more GitHub usernames
- Gets a list of the public repositories for that user.
- Store the username and names of the repositories in the database created by the
  backend
3. Create an appealing single page application that allows retrieving the information from the
- backend server through its REST API.
- Priority would be for this to use React, but other modern and commonly used
  JavaScript frameworks could be used
- At a minimum, the UI should allow selection of a GitHub username in the database and
  display the public repositories for that username
- It should dynamically load information as needed and only keep data that is being
  displayed

*The expectation is these ‘requirements’ are just a starting point and that you will expand the
capabilities as much as you have time for and be prepared to discuss your thought process and
how you might extend the project in the future
Please make a git repository with your solution available at least two business days before the
interview, so we have time to review it.*

