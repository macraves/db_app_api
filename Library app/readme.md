# Flask Database and CRUD:

The aim of this work is to establish a database from scratch, prioritizing the creation of the 'users' table first, followed by 'books' and 'blog_post' tables. Through connecting to this database via SQLAlchemy, the goal is to perform CRUD operations using a Flask app through the designed frontend server. This project has followed the Flask and database relationship tutorials on the Codecademy.com YouTube channel. I would like to express my gratitude to Mr. John for his informative videos in this regard.

In terms of HTML design, the WTForms package is an essential tool that significantly enhances the design using templates obtained from https://getbootstrap.com. Although I don't focus much on the frontend, these packages in the requirements.txt file address any potential gaps to improve the project. Make sure to explore their documentation, as they are packages that simplify the process.

# Walkthroug:

The ability of each user to change the book and block fields they added was mostly done with Jinja2 template applications so far. This application based on html code and aims to improve html skills.

# PS Caution:

There are a few points to consider while working with databases. Initially starting with simple tables and smoothly upgrading them with the migrate method works well. However, after setting up instances for Users, Books, and BlogPost, a major issue may arise during foreign key assignment to all three tables. Based on my observation, it is crucial to make the tablename assignment first for each table. Installation should proceed one table at a time, meaning after performing the migration and upgrade process for the first table, move on to the second table, and so on. Foreign key assignment for the second and subsequent tables should be done after completing the installation of the previous table.

Tools and documents that can perform this operation at once will be examined, and the solution found will be added to this repository in a new branch.
