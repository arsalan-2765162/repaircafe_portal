### **Repairer Workflow**

- **Views**: 
  - Location: `RepairCafe/RepairCafe/views.py`
  - Contains the views that handle the logic for repairer-related actions.

- **Templates**: 
  - Location: `RepairCafe/templates/RepairCafe`
  - Contains the HTML templates for the repairer pages.

#### 1. **Enter Password**
- **View**: `enter_password`
- **Template**: `enter_password.html`
- Repairers must first enter the **repairer password** on the **Enter Password page**.

#### 2. **Login**
- **View**: `repairer_login`
- **Template**: `repairer_login.html`
- After entering the password, repairers can **log in** using their **name** and **photo**.

#### 3. **View Repair Queue**
- **View**: `main_queue`
- **Template**: `main_queue.html`
- Once logged in, repairers will be directed to the **Repairer Queue** where they can view all items to be repaired.

#### 4. **Filter Items**

- At the top of the page, there’s a **filter** to organize items by:
  - **Repair status**
  - **Item category**

- **Colour-coded items**:
  - Items that have been waiting for **more than 30 minutes**: **Bright red**
  - Items that have been waiting for **more than 15 minutes**: **Slightly reddish-orange**
  - Items that have been waiting for **less than 15 minutes**: **Orange**

- To view items that need **PAT testing**, use the **"Needs PAT tested"** filter.

#### 5. **Accept Repair Item**
- To repair an item, click on the **"Accept Repair"** button for the item in the queue.
- The **visitor** will be notified with a prompt that includes:
  - **Your name**
  - **Your photo**
  - A message to **meet you**.

#### 6. **Complete or Incomplete Item**
- **View**: `repair_item`
- **Template**: `repair_item.html`
- After repairing, mark the item as:
  - **Complete**, or
  - **Incomplete** with a **reason** for incompletion.

#### 7. **Provide Feedback**
- **View**: `ticket_feedback`
- **Template**: `ticket_feedback.html`
- Once the item is marked as complete or incomplete, the repairer will be prompted to **provide feedback** on the ticket.

#### 8. **Redirect to Repair Queue**
- After feedback is given, the repairer will be redirected back to the **Repair Queue**.

#### 9. **Logout**
- **View**: ``
- **Template**: ``
- To log out, navigate to the **Logout page** via the **sidebar**.