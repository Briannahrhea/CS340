The artifact I have chosen to work on for enhancement two, algorithms and data
structures, is a Python-based dashboard application originally developed during my time in the
CS 340 Client/Server Development course. The initial version of this project was designed to
support an animal shelter’s operations by connecting to a MongoDB database and displaying the
data interactively using Dash, Plotly, and pandas. It included several visualization tools, such as a
searchable data table, basic filtering options, and an interactive map.

The original artifact offered a way to display and filter the animal shelter data through a
web interface; however, it lacked the complex functionality and querying capabilities to provide
purposeful data to the user. For the enhancements of this project, I wanted to incorporate more
complex filtering logic, a trend analysis graph, a bookmarking system, and additional data-driven
support tools that would increase the usability and organization of the data presented.

I am including this artifact in my CS 499 Capstone ePortfolio because it highlights a wide
range of skills I’ve developed throughout my Computer Science program. I believe this project
best demonstrates my ability to design and implement real-world, user-centered solutions that
interact with complex datasets. In the enhanced version of this project, I showcased many skills
such as the use of efficient data filtering algorithms, pandas group-by logic, and time-based data
transformations for trend analysis. I also utilized MongoDB queries using nested dictionaries and
conditional operators, and a bookmarking system that uses data modeling and CRUD operations
to manage user-selected records.

One of the first enhancements I made to demonstrate these skills was converting the
original .ipynb Jupyter Notebook into a modular Python file structure. I encountered several
issues running the application in Jupyter. I found that moving it to a standalone Python project
hosted on a local server allowed for easier updates, faster refresh capabilities, and a better
foundation for a scalable full-stack application.

The next enhancement was the implementation of a match animals feature, which allows
users to search for animals based on breed, sex upon outcome (e.g., neutered/spayed or intact),
and outcome type (e.g., adopted, transferred, euthanized, deceased). This feature uses query logic
to quickly return matched animal records based on the user’s specifications, providing the user
with the animal ID that can be used to search the data table. Using the ID, the user can further
explore more details about the animals within the organized table to make fast and efficient
decisions.

I also developed a bookmarking system to aid in the search and retrieval process that this
app aims to provide. This feature allows users to save and manage a list of animals, determined
from the table rows, for future reference. For example, if the user is querying the data table using
the IDs provided from the match animals feature, the user can save each of these animals’ IDs
for future login use.

Another enhancement involved replacing the earlier pie chart with a trend analysis line
graph, which is easier to read and interact with. This new graph includes two filters, breed and
outcome type, that aid in visualizing data trends over time through an organized layout grouped
by month and year. I think this feature helps the user to understand patterns within the data and
gives it purpose beyond just searching for animal records.

Finally, I enhanced the existing map visualization by adding a heatmap overlay that
shows the concentrations of animals based on the latitude and longitude data points provided in
the database. This feature provides insight into where most animals are located or being put up
for adoption, offering potential value for future planning or resource allocation. Again, giving the
data a purpose beyond just animal record search and query.

In implementing the project enhancements, I believe that I met each of the intended
outcomes. For the collaborative environment outcome, the design reflects the ability to create
user-facing tools that can support collaboration in a team working environment. For the
professional communication outcome, I believe that I intuitively organized the dashboard to
demonstrate my ability to deliver clear and purposeful visual communication using various UI
components with real-time feedback. I also met the algorithmic design and evaluation outcome
through the use of filtering algorithms and data grouping logic that were designed to efficiently
handle user inputs, trends, and queries. Additionally, I met the software engineering and
computing practices outcome through the use of a modular Python design and industry standard
tools such as Dash, MongoDB, and Plotly. Lastly, the security outcome was partially met, but
could be expanded upon. I implemented the MongoDB URI using secure credentials.

Working on this artifact allowed me to further explore bridging the gap between the use
of data structure logic and user experience design through applying algorithmic thinking skills to
real-time user interactions, creating tools that support dynamic querying based on multiple input
variables. One of the biggest challenges I faced was implementing the line graph and heatmap
components, as I had never used those tools before. This required research and experimentation
to understand how to format and display the data effectively. I also encountered issues with the
radio buttons not querying the database correctly, which led me to learn and apply the $regex
operator in MongoDB for better pattern matching. Additionally, I used Python’s logging module
to aid my process in debugging callback functions and tracing issues step by step. Through this
process, I strengthened my technical abilities, deepened my understanding of web-based data
applications, and gained confidence in building scalable, interactive, data-driven tools.
