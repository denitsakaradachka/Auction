# Auction

This is the final project for Python Web Framework - November 2022

## Summary

The project represent an Auction platform that connects suppliers and customers. 
A supplier can be any individual customer that want to sell it's rare item to the person
who will make the higher bid while the auction for this item is open.

## Local setup

The platform is writen in python and uses the Django Web Framework

> Note: The setup is tested in Mac OSX

### Steps

1. Clone the repository and open it on PyCharm (or you preferred IDE)
2. Open the terminal window and navigate to the project directory
3. Create and activate python virtual environment by execution the following command in terminal
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install pip dependencies. Run the following command
    ```sh
    pip3 install -r requirements.txt
    ```
5. Create database and apply your configuration in `setting.py`
6. Execute the migrations. Run the following command
    ```sh
    python3 manage.py migrate
    ```
7. Set up a superuser by executing and following the instructions of the following command
    ```sh
    python3 manage.py createsuperuser
    ```
8. Execute a custom command named `create_groups_and_permissions`. It will create new group and assign permissions to it. Run the following command
    ```sh
    python3 manage.py create_groups_and_permissions
    ```
9. Run Django server.
   ```sh
    python3 manage.py runserver --insecure
    ```

Executing all the steps will start an empty Auction platform. You can register users, add items, make auction & bids and more.
