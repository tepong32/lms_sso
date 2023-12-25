Django Leave Management System

Features:
Custom user registration/authentication
  - uses <staff_id> as the main identifier for each User class
  - a fully-functional password-reset email system but credentials (of course...) are using env variables (gmail account)
      - Google now do not recommend using Gmail accounts to be used as the server-email-address (...or maybe just for test environments? idk)
  (not yet implemented:)
  - is_active status upon User registration should be set to False by default. Manual intervention from admins or users with specific permissions is needed for new accounts to be able to log in (to avoid having too many accounts and/or to ensure that details of each employee matches with company records)
  - tbc

Leave models:
  Leave Types:
    - Dynamic options: Admins can add whatever type of leave the users can choose (dropdown) when filing for leave requests.

  Leave Counter:
    - Set a default max_instances_per_year and _per_quarter counters for each profile (currently: user.profile) that prevents over-filing of leave requests
    - Implemented automatic reset dates for these yearly and quarterly counters, as well
    - Users' leave credit counts updates only when their leave requests are tagged as "approved". 
      - avoided exploitation of leave credits count by not adjusting the counter when an already-approved leave request was changed to another status (i.e. pending, rejected)
    - A special view for admins, team leaders and operations mgrs to adjust the leave counters (see localhost:8000/increase_max_instances)
    (not yet implemented)
    - carry-over system for unused leave credits count per quarter (special instances)

Django REST Framework:
  - added the localhost:8000/api url as an extra option for the web app. Working with a front-end dev for options of which side to display to the users.

 (not yet fully-functional)
  - api for user authentication (login/logout pages)
  - urls for item-specific pages (such as users) are using <pk> as the argument and not <staff_id>
  - tbc
    
