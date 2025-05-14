# CanteenEats

To be added.

## To Do

### Model Enhancements
- [x] Add `Item` model
- [x] Add `Order` model
- [x] Add `credit` field to `User` model
- [ ] Create order status constants or enum for consistency

### Student Features
- [ ] Store page to display all available items (quantity > 0) with filters:
  - Name
  - Price
  - Quantity
  - Vegetarian flag
- [ ] Place order functionality:
  - Select item and quantity
  - Deduct credit
  - Check stock
  - Create order with status "Awaiting Confirmation"
- [ ] View orders page showing only the student's own orders and their statuses
- [ ] Prevent order placement if user lacks sufficient credit

### Staff Features
- [ ] Item management:
  - Add new items
  - Edit existing items
  - Delete items
  - Validate price and quantity
- [ ] Credit management:
  - Add funds to student accounts
  - Only allow positive credit additions
- [ ] Order management:
  - View all student orders
  - Update order status through full status flow
  - Cancel order (refund credit and restore item quantity)
- [ ] Promote student accounts to staff

### Forms
- [ ] `ItemForm` for staff to manage items
- [ ] `CreditForm` for staff to top up student credit
- [ ] `OrderForm` for students to place orders
- [ ] `OrderStatusForm` for staff to update order status

### Business Rule Enforcement
- [x] Students cannot access `/users` or promote other accounts
- [ ] Students cannot change their email (currently allowed)
- [ ] Orders must contain only one item and valid quantity
- [ ] Cancelled orders should trigger credit refund and restock item

### Frontend Improvements
- [ ] Storefront layout with filters and item cards or table
- [ ] Order status indicators (e.g., color-coded badges)
- [ ] Confirmation dialogs for destructive actions (e.g., cancel)
- [ ] Flash messages for actions like placing orders, adding credit, etc.

### Testing & Validation
- [ ] Validate all forms (e.g., non-negative prices, required fields)
- [ ] Handle edge cases (e.g., ordering with zero stock or no credit)
- [ ] Test full user journey for both roles

### Future Features (Out of Scope)
- [ ] Estimated wait times for orders
- [ ] Cart system for multi-item orders
- [ ] Exportable reports (CSV or PDF)

## Suggested Implementation Order
1. Finalize models and database setup
2. Implement store view and student order placement
3. Add item and order management for staff
4. Enforce all business rules
5. Finalize forms and frontend UI
6. Conduct thorough testing and cleanup
