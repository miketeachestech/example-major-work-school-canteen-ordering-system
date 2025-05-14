# Business Rules – School Canteen Ordering System

## General Rules

1. **User Authentication**
   - All users must log in using their school email and password.
   - Users without an account can register with their school email and password.
   - New accounts are automatically assigned the **student** role.
   - Only staff members can upgrade student accounts to staff.

2. **User Roles**
   - Two roles exist: **student** and **staff**.
   - System access and permissions are based on user role.

3. **Store Items**
   - Each item has a name, price, quantity, and is_vegetarian.
   - Quantity must be a non-negative integer.
   - Items with zero quantity are visible to all users but cannot be purchased by students.
   - An order shall only contain one item up to any valid quantity.

## Staff Rules

1. **Credit Management**
   - Staff can add credit to any student account.
   - Only positive credit amounts are allowed.

2. **Item Management**
   - Staff can add, edit, or delete items in the store.
   - Edits may include name, price, or quantity.
   - Item prices must be non-negative.

3. **Order Oversight**
   - Staff can view all orders placed by students.
   - Orders can be marked as **Awaiting Confirmation**, **Confirmed**, **Being Prepared**, **Ready For Pickup**, **Completed** or **Cancelled**.
   - Cancelling an order refunds the full cost to the student’s credit and returns quantity to the item.

4. **Account Permissions**
   - Staff can promote student accounts to staff.
   - Staff can edit their own account details (e.g., name, password).

## Student Rules

1. **Store Access**
   - Students can browse available items (quantity > 0).
   - Students should be able to filter items on name, price, quantity, and is_vegetarian. 
   - Item prices and quantities are visible to the student.
   - Students can place an order for an item on the respective item's page.

2. **Purchasing**
   - Orders are placed using available credit.
   - Credit is deducted immediately upon ordering.
   - Orders cannot be placed if the student lacks sufficient credit.

3. **Order Status**
   - Students can view their own orders.
   - Each order displays its status: **Awaiting Confirmation**, **Confirmed**, **Being Prepared**, **Ready For Pickup**, **Completed** or **Cancelled**.
   - If a student wishes to cancel an order, they should ask a staff member to do so. 

4. **Account Control**
   - Students cannot change their role or access other users' data.
   - Students cannot change their email.
   - Students can change their other account details (e.g. password).

## Additional Constraints

- **Credit Format**: All credit and item prices are stored as decimal values (e.g., 10.50).
- **Order Structure**: Each order includes item(s), quantity, total cost, timestamp, and status.
- **Order Status Flow**:
  - New orders start as **Awaiting Confirmation**.
  - Staff update status to **Confirmed**, **Being Prepared**, **Ready For Pickup**, **Completed** or **Cancelled**.
  - Refunds are only processed on cancellations.

## Out Of Scope / Future Improvements

- **Cart**: Students can add multiple items to a cart and then place one order for the cart's contents.
- **Estimated Wait Time**: Staff can provide an estimated wait time when the order is changed to **Confirmed**.
