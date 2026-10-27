Nagar Nirikshan

Municipal Infrastructure Failure & Root-Cause Intelligence System

Nagar Nirikshan is a student DBMS project designed to monitor and manage municipal streetlight infrastructure across ward areas of Pune, Maharashtra. It organizes infrastructure data, highlights streetlight failures, calculates risk scores, and helps prioritize maintenance, repair, and replacement activities.

«Disclaimer: This is an academic project inspired by Indian government portal designs. It is not an official website of the Pune Municipal Corporation (PMC). Ward data is based on the provided dataset and is not verified live municipal data.»

Live Demo

GitHub Pages: "https://<username>.github.io/<repo>/"

Replace "<username>" and "<repo>" with your actual GitHub username and repository name.

Project Objectives

- Organize ward-wise streetlight infrastructure data for Pune.
- Display infrastructure statistics through an interactive dashboard.
- Present zone-wise and ward-wise streetlight information.
- Demonstrate streetlight failure tracking and maintenance management.
- Calculate risk scores using predefined project rules.
- Help identify streetlights that may require repair, inspection, or replacement.
- Demonstrate DBMS concepts using SQL, Oracle Database, and PL/SQL.

Key Features

1. Interactive Dashboard

- Displays important infrastructure statistics.
- Shows zone-wise and ward-wise streetlight data.
- Presents charts, summary cards, and smart insights.
- Provides a simple and user-friendly interface.

2. Infrastructure Dataset Viewer

- Displays ward-wise infrastructure data in a table.
- Includes details about poles, LED bulbs, conventional lights, and road length.
- Supports CSV data download.
- Provides English and Marathi language options.

3. Streetlight Failure and Risk Analysis

- Demonstrates streetlight failure tracking.
- Calculates risk scores using project-defined rules.
- Categorizes assets as Critical, High, Medium, or Low risk.
- Suggests maintenance actions based on the calculated risk.

4. Repair and Replacement Recommendations

- Identifies assets that may need priority repair.
- Flags assets for replacement review when defined conditions are met.
- Demonstrates how failure history, repair costs, asset age, and inspection condition can support maintenance decisions.

5. User Interface Features

- English and Marathi language options.
- Theme selection.
- Text-size adjustment.
- Responsive dashboard layout.

Note: Some operational and risk-analysis features use sample records. They do not represent live municipal operations or real-time streetlight conditions.

Technology Stack

Technology| Purpose
HTML| Structures the website content
CSS| Controls the visual design and layout
JavaScript| Handles interactions and dashboard data presentation
Python| Supports backend and data-processing scripts
Flask| Provides the web application backend and API routes
Oracle Database| Stores structured infrastructure and operational data when configured
SQL| Creates tables and manages database operations
PL/SQL| Implements procedures, functions, and triggers
python-oracledb| Connects Python applications to Oracle Database
Git and GitHub| Version control and source-code hosting
GitHub Pages| Hosts the standalone static dashboard

Project Structure

NagarNirikshan/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── build_demo.py
├── templates/
│   └── app.html
├── static/
│   ├── app.css
│   ├── app.js
│   ├── nn.js
│   └── demo-data.js
├── docs/
│   └── index.html
└── sql/
    ├── schema.sql
    ├── generate_seed.py
    ├── build_demo.py
    └── dataset.csv

The structure above represents the intended project layout. Update it if your repository contains different files.

Database Design

The Oracle database schema is designed to organize information related to municipal streetlight infrastructure and maintenance.

The database design includes tables for:

- Ward infrastructure
- Locations
- Streetlights
- Failures
- Inspections
- Contractors
- Maintenance
- Expenditure
- Audit logs

The project also demonstrates important DBMS concepts, including:

- Primary keys and foreign keys
- Data integrity constraints
- SQL queries
- Views
- Sequences
- PL/SQL functions and procedures
- Triggers for status updates and audit logging

These components demonstrate how relational databases can organize information and support maintenance-related analysis. Oracle execution and application integration must be verified separately.

Risk Scoring Logic

The project uses a rule-based approach to calculate streetlight risk scores. Factors include failure frequency, repair cost, open failures, asset age, and inspection condition.

Risk Score| Risk Level| Suggested Action
70–100| Critical| Priority attention
50–69| High| Priority repair
30–49| Medium| Schedule inspection
0–29| Low| Routine monitoring

The replacement-review rule flags an asset when it has at least three recorded failures and repair costs of ₹5,000 or more.

These thresholds are defined for this academic project and are not official PMC maintenance standards.

Dataset Information

The project uses "sql/dataset.csv", which contains ward-wise streetlight infrastructure information for Pune.

The dataset includes:

- City name
- Zone name
- Ward name
- Number of poles
- Number of LED bulbs
- Number of conventional or non-LED lights
- Total road length in kilometres
- Streetlight-related infrastructure density
- Total number of streets
- Number of streets with adequate streetlighting facilities

The provided dataset contains 15 ward records across five zones. Some fields contain "NA", indicating that values were not available in the source dataset.

Installation and Local Setup

Prerequisites

- Python 3
- Oracle Database access
- Oracle SQL Developer or SQL*Plus

Step 1: Clone the Repository

git clone https://github.com/<username>/<repo>.git
cd <repo>

Step 2: Install Dependencies

pip install -r requirements.txt

Step 3: Configure Database Credentials

Copy ".env.example" to ".env" and enter your Oracle connection details.

DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_DSN=your_oracle_connection_string

Keep your actual ".env" file private. Never upload database passwords to GitHub.

Step 4: Execute the Database Script

Open Oracle SQL Developer or SQL*Plus, connect to your Oracle schema, and execute:

sql/schema.sql

Check the execution results to confirm that the database objects have been created successfully.

Step 5: Run the Flask Application

python app.py

Open the application in your browser:

"http://127.0.0.1:5000"

A successful application launch does not automatically confirm that Oracle connectivity and all API features are working. Test these separately.

API Endpoints

The Flask application is designed to provide the following endpoints:

Endpoint| Method| Purpose
"/api/bootstrap"| GET| Retrieve initial application data
"/api/failures"| POST| Submit a streetlight failure
"/api/failures/<id>/resolve"| POST| Resolve a recorded failure
"/api/run-review"| POST| Run the review logic
"/dataset.csv"| GET| Download the dataset

Endpoint behaviour depends on the implemented Flask routes and configured database connection.

GitHub Pages Deployment

The standalone dashboard is available through "docs/index.html".

1. Open your repository on GitHub.
2. Navigate to Settings → Pages.
3. Select deployment from a branch.
4. Choose the "main" branch and "/docs" folder.
5. Click Save.
6. Wait for deployment and open the URL provided by GitHub Pages.

Important: GitHub Pages hosts static files only. It cannot run Flask or connect directly to Oracle Database. Backend-dependent functionality requires a separately hosted backend and a properly configured API connection.

Testing and Verification

Before presenting or deploying the project, verify that:

- The dataset loads correctly.
- Dashboard statistics match the provided dataset.
- Oracle tables and other database objects execute successfully.
- The Flask application starts without errors.
- Database connectivity works with valid credentials.
- API endpoints return the expected responses.
- Risk scores follow the documented rules.
- CSV download and dashboard controls work correctly.

Clearly distinguish verified features from sample demonstrations and functionality that is still under development.

Limitations

- This is an academic prototype, not an official municipal system.
- The dataset is not guaranteed to represent current municipal conditions.
- Some failure and maintenance records may be sample data.
- Risk scores use project-defined rules.
- GitHub Pages supports only the static dashboard.
- Complete frontend, Flask, and Oracle integration requires configuration and testing.

Future Scope

- Integration with verified municipal data.
- Secure authentication and role-based access.
- Real-time streetlight failure reporting.
- Map-based streetlight locations.
- Automated maintenance alerts.
- Historical failure and expenditure analysis.
- Improved energy-saving and replacement-cost estimates.
- Secure hosting of the backend and database.

Academic Propose

Nagar  demonstrates how DBMS concepts and web technologies can be applied to a municipal infrastructure monitoring problem. The project combines structured datasets, relational database design, SQL/PLSQL concepts, dashboard visualization, and rule-based risk analysis to support maintenance planning.

License

This project is licensed under the MIT License. See the "LICENSE" file for details.

---

Nagar Nirikshan — Organizing Streetlight Data for Smarter Maintenance Planning.
