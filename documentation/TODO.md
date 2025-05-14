## Code To Do List

### Student Features
- [x] Store page to display all available items (quantity > 0) with filters:
  - Name
  - Price
  - Quantity
  - Vegetarian flag
- [x] Place order functionality:
  - Select item and quantity
  - Deduct credit
  - Check stock
  - Create order with status "Awaiting Confirmation"
- [x] View orders page showing only the student's own orders and their statuses
- [x] Prevent order placement if user lacks sufficient credit

### Staff Features
- [x] Item management:
  - Add new items
  - Edit existing items
  - Delete items
  - Validate price and quantity
- [x] Credit management:
  - Add funds to student accounts
  - Only allow positive credit additions
- [x] Order management:
  - View all student orders
  - Update order status through full status flow
  - Cancel order (refund credit and restore item quantity)
- [x] Promote student accounts to staff

### Forms
- [x] `ItemForm` for staff to manage items
- [x] `CreditForm` for staff to top up student credit
- [x] `OrderForm` for students to place orders
- [x] `OrderStatusForm` for staff to update order status

### Business Rule Enforcement
- [x] Students cannot access `/users` or promote other accounts
- [x] Orders must contain only one item and valid quantity
- [x] Cancelled orders should trigger credit refund and restock item

### Frontend Improvements
- [x] Storefront layout with filters and item cards or table
- [x] Order status indicators (e.g., color-coded badges)
- [x] Confirmation dialogs for destructive actions (e.g., cancel)
- [x] Flash messages for actions like placing orders, adding credit, etc.

### Testing & Validation
- [x] Validate all forms (e.g., non-negative prices, required fields)
- [x] Handle edge cases (e.g., ordering with zero stock or no credit)
- [ ] Test full user journey for both roles

