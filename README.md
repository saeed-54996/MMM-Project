# MMM-Project 🖥️ 📸

This is a Multi Media Management system written with the Python Flask framework, using a MySQL database.

## Features ✨

-   **Pictures:** Users can upload pictures with their title, description, and tags. All pictures are shown on the pictures page.
-   **Articles:** Users can write and post articles with their title, description, and keywords. All articles are shown on the articles page.
-   **Login/Signup:** The system allows users to sign up and log in easily. All login passwords are hashed with the MD5 protocol and stored in the database's users table.
-   **Admin Roles:** The website supports roles for users. Roles are stored in the users table. To make a user an admin, set their role to "admin." Admins can manage categories and import data from CSV files in the admin panel.
-   **Filtering by Category:** A filter drop-down is available on the articles and pictures pages, allowing users to filter posts by category.
-   **Easy Navigation System:** Users can use navigation links on different pages to go back, visit their profile, go to category-filtered posts, and access other sections like the admin page and the "my-profile" page.

## Usage 🚀


**Windows:**
1. Install **Python 3**:
Download and Install Python 3 From [www.python.org](https://www.python.org/downloads/)<br >

2. Clone the repository:

```bash
git clone https://github.com/saeed-54996/MMM-Project.git
```

3. Install the required dependencies:
Simply Run "**setup.bat**" to install all dependencies OR use this command:
```bash
pip install -r requirements.txt
```
4. Create "db_config.py":
for connecting database you shoud create the "db_config.py" from "db_config.py.copy" , simply fill in the requirements(server-ip,user,db name,password) to connect to the database server.

5.Run migration:
To create the tables and run the project, delete the migrations folder, and run these commands in the `my_flask_app` folder:
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

6. Run the server:
Simply use this command:
```bash
python app.py
```

Users can now see the webpage on **port 5000** (default port):
```bash
http://127.0.0.1:5000/
```


**Linux/MacOS:**

1. Clone the repository:

```bash
git clone https://github.com/saeed-54996/MMM-Project.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```
3. Create "db_config.py":
for connecting database you shoud create the "db_config.py" from "db_config.py.copy" , simply fill in the requirements(server-ip,user,db name,password) to connect to the database server.

4.Run migration:
To create the tables and run the project, delete the migrations folder, and run these commands in the `my_flask_app` folder:
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

5. Run the server:
Simply use this command:

```bash
python app.py
```


Users can now see the webpage on **port 5000** (default port):
```bash
http://127.0.0.1:5000/
```
## Dependency 📦

All dependencies are included in the **requirements.txt** file.

## Contributing 🤝

Contributions are always welcome!

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License 📄

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

## More about this project:🙏

This project was created at the end of the university semester for the database course in the spring of 2024. The participants were my teammates in the database class. This project was our first work experience with the Python Flask framework.
