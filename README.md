# ✨ Repair Cafe Portal

## 🪄 Overview
_This project, aptly named 'Repair Cafe Portal', is a web application that is designed to streamline monthly Repair Cafe events. The app allows for online forms to be in place of paper forms; dynamic allocation of visitors to repairers; and enhanced statistical analysis tools._

## 🚀 Features
- ⭐ Updatable password entry system 
- ⭐ Check in and check out forms for visitors to fill out and send
- ⭐ Visitor waiting queue page for volunteers to accept check in forms
- ⭐ Webhooks to move visitors through appropriate waiting pages as volunteers and repairers process their item incrementally
- ⭐ Webhooks to keep repairer and volunteer queues in sync
- ⭐ A repairer login page for repairers to choose which repairer to login as,
 based via a name and photo
- ⭐ An item queue for tickets to be accepted from by repairers to repair
- ⭐ A repairer pop up displaying information about the current item being repaired along with options to mark the repair as 'complete' or 'incomplete'
- ⭐ Reason tags to add to the backend of an item ticket for if the item is marked as 'incomplete' - to be used for monitoring and statistical purposes
- ⭐ PAT testing functionality for items in repair queue to be PAT tested 
- ⭐ A check out queue for volunteers to be able to manually review and checkout visitors after reviewing the final, processed item ticket
- ⭐ A basic statistics page for volunteers and repairers to be able to see metrics from the current event - updated live as an event continues
- ⭐ A Volunteer check in page for volunteers to manually check in for visitors.
- ⭐ Ability to dynamically change passwords for all three user roles from admin page
- ⭐ Ability to see graphs showing metrics such as ticket status, repair success rate and ammount of items and carbon footprint of each subcategory, with ability to filter these metrics by time and category
- ⭐ Ability to export data to a spreadsheet between dates specified or all time
- ⭐ Ability to directly modify, add or delete records for visitors, repairers, tickets and subcategories

## 🎢 Installation
### 🔻Prerequisites
Ensure any of the following listed have been installed:
- Python 3.9
- Django 4.2.18
- Any other dependencies listed in 'requirements.txt'

### 🔻 **Setup**  
1. **Open a command prompt.**  
2. **Activate a virtual environment** (if not already activated):    

    #### Create a virtual environment (if not already created) 
    ```sh
    python -m venv venv1
    ```
    #### Activate virtual environment
    ```sh
    source venv/bin/activate  # macOS/Linux
    venv1\Scripts\activate  # Windows
    ```
3. **Navigate to the root directory of the Django project:**  
   ```sh
   cd RepairCafe/
   ```
4. **Install dependencies:**  
   ```sh
   pip install -r requirements.txt
   ```
5. **Apply database migrations:**  
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Setup site data:**  
   ```sh
   python setup.py
   ```
   Alternatively if you wish to populate the site with demo ticket, repairer and customer data, run the following command instead 
   ```sh
   python populate_RepairCafe.py
   ```
7. **Run the development server:**  
   ```sh
   python manage.py runserver
   ```

---

### 🔻 **Testing**  
Ensure you are in the Djangos projects root directory (RepairCafe)
```sh
cd RepairCafe/
```
#### ✅ Run all tests:  
```sh
pytest
```
#### ✅ Run only Django tests:  
```sh
python manage.py test
```
## 🫧 API Endpoints
| Endpoint |  Method  |Descriptions|
|----------|----------|------------|
|          |          |            |


## ☕ License 
This project is licensed under the MIT License.



