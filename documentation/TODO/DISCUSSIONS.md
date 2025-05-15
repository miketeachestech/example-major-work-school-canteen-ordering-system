## Discussion of Methods Used to Plan, Develop and Engineer the Solution

### Identified Need and Solution Overview

The CanteenEats system was developed in response to a clearly defined problem: school canteen operations were manual, time-consuming, and dependent on physical cash and paper-based order tracking. These limitations led to long queues, errors in orders, difficulty in refunding transactions, and a lack of historical order data for both students and staff.

The software engineering solution aimed to digitize this process by creating a web-based platform that allowed students to browse available items, place orders using credit, and monitor their order status. Meanwhile, staff would gain administrative tools to manage stock, process orders, and handle credit balances efficiently. This addressed the core need for speed, accuracy, transparency, and scalability in school canteen operations.

### Planning and Development Methodology

TO DO

### Requirement Definition and Analysis

Requirements were drawn from a combination of observed inefficiencies in current canteen operations and explicitly defined business rules from interviews with stakeholders. Functional requirements included user roles, credit use, item visibility, order placement, and staff controls. Non-functional requirements included security (e.g., password hashing, CSRF protection), usability (clean UI, responsive design), and data integrity (e.g., transactional credit/order updates).

Analysis of these requirements shaped decisions such as:
- Using decimal fields for accurate financial data
- Preventing orders when quantity or credit is insufficient
- Restricting students from modifying protected data (e.g., email, credit)
- Allowing staff to promote users or cancel orders with automatic refund logic

### Engineering Justification

Flask was chosen as the web framework for its simplicity and modular design. Engineering decisions emphasized security (hashed passwords, role checks), maintainability (modular routes and forms), and performance (query filtering, pagination). Images were handled safely with upload validation, auto-renaming, and cleanup on item deletion.

WTForms was used to enforce frontend and backend validation, reducing error-prone logic. SQLAlchemy provided a declarative and readable database layer, streamlining development while ensuring referential integrity and transaction safety.

Overall, the combination of agile planning, focused modelling, and robust engineering practices resulted in a reliable, secure, and user-friendly solution tailored to the identified school environment.

## Discussion of the Selection and Use of Tools/Resources

### Allocation of Resources

The development of CanteenEats required the careful allocation of time, software tools, and frameworks that support rapid development, maintainability, and scalability. Python was selected as the primary programming language due to its simplicity and widespread use in educational and enterprise systems. Flask, a lightweight web framework, was chosen for its flexibility and ease of integration with extensions such as Flask-WTF, Flask-SQLAlchemy, and Flask-Login — each essential for form validation, database management, and user authentication respectively. These tools required minimal setup while providing robust security features and code clarity, enabling efficient allocation of developer time toward business logic rather than configuration.

SQLite was selected as the database for development and testing due to its simplicity and zero-configuration setup. This decision allowed for easy local testing while maintaining compatibility with more scalable production databases if needed in future deployment.

### Justification of Modelling Tools

TO DO.

### Contribution of Back-End

Back-end engineering was critical to the success and security of the project. All core functionality — from user authentication and credit deduction to role-based permissions and order state transitions — was handled securely and efficiently on the server side using Flask routes and SQLAlchemy models. Data validation occurred both at the form level (via WTForms) and in business logic, ensuring that all interactions with the system adhered to predefined rules, such as non-negative credit and quantity, or valid order statuses.

The back-end architecture also enabled modular development. Separate routes, templates, and forms were defined for each feature, such as ordering, credit management, and item control. This modularity improved maintainability and reduced coupling, making it easier to test and debug.

### Testing and Evaluation Methodologies

During development, rigorous manual testing was conducted using realistic test users and seeded database entries. Flask’s development server allowed for hot-reloading and real-time testing of forms, routes, and edge cases. Logical constraints were continuously verified by attempting invalid actions (e.g., over-ordering, insufficient credit, duplicate emails), and validation errors were observed and improved.

Code quality was further evaluated through structured walkthroughs of feature flows and testing each route’s behavior for different user roles. Realistic test scenarios (e.g., refund workflows, image uploads, item editing) were run repeatedly to ensure consistent database updates and visual feedback.

Performance was optimized by indexing relationships via SQLAlchemy and minimizing unnecessary queries. Pagination was implemented for large datasets (e.g., orders), and reusable components reduced redundancy.

## Evaluation of Data Safety and Security

### Secure Code Design and Development

The CanteenEats application demonstrates a strong emphasis on secure coding practices throughout its architecture. User authentication is handled securely using Flask-Login, with passwords stored using robust hashing via Werkzeug’s generate_password_hash function. Forms leverage Flask-WTF and WTForms validators to prevent malformed inputs, including Email() validation and minimum password lengths. Cross-site request forgery (CSRF) protection is enforced automatically via Flask-WTF.

Access control is correctly enforced by role-based checks (e.g., @login_required and current_user.is_staff) across staff-only routes such as credit management, item control, and user promotion. Students are prevented from accessing sensitive features such as altering other users, changing their email, or accessing the order management system.

Additionally, data integrity is preserved during order creation and cancellation — ensuring stock levels and user credit are updated atomically, with refund logic tied to order status. Uploaded images are validated and renamed to prevent filename conflicts or path traversal attacks, and unused images are deleted when items are removed.

### Impact of Safe and Secure Software

The secure software design has a direct impact on the system’s reliability and trustworthiness. By eliminating cash handling and digitizing transactions, CanteenEats reduces the risk of fraud or theft. Students’ credit balances are stored as decimal fields, preserving accuracy in financial calculations. Role restrictions and validation guard against privilege escalation and data tampering.

Overall, the secure handling of data throughout CanteenEats fosters a safe environment for both staff and students, reducing administrative overhead, maintaining user privacy, and ensuring the platform can be safely scaled for real-world use in school environments.