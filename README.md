# prestashop-demo-testingPrestaShop Demo Testing Project

Overview
This repository contains the deliverables for a Software Testing project conducted as part of the Software Testing course. The project involved comprehensive manual and automated testing of the PrestaShop demo e-commerce platform (https://demo.prestashop.com). The goal was to evaluate the platform's functionality, usability, and performance across various customer-facing scenarios, including user registration, product browsing, cart management, and checkout processes.

The testing was performed by a team of five members, with roles ranging from test planning and execution to automation and reporting. The project includes 71 test cases, bug reports, automation scripts, and a detailed project report summarizing the testing process and outcomes.

Team Members and Contributions
Syed Abdul Rehman (K21-3156): Project Leader, Test Planner, Automation Developer, Report Compiler
Asadullah Wagan (K21-4824): Test Executor, Automation Specialist
Rana Wahaj Ahmed (K21-3281): Test Executor
Syed Hadi Raza (K21-3420): Test Executor
Wara Batool (K21-3214): Test Executor, Test Case Developer

Detailed contributions are outlined in the Project Report.

Testing Scope
The testing focused on the front office of the PrestaShop demo site, covering the following scenarios:
User Registration & Login
Cart Management
Product Filtering
Contact Form & Newsletter
Cross-Browser UI Testing
Checkout Process (Guest & Logged-in User)
UI Responsiveness
Product Searching

In-Scope
Customer-facing features (search, cart, checkout, user management)
Admin-side features (product/inventory management, order processing)

Out-of-Scope
Real payment gateway integration
Third-party API integrations
Long-term database checks

Testing Methodology
Manual Testing: 71 test cases executed using structured test cases and exploratory testing. Results documented in Test_Cases.xlsx and Manual_Execution_Report.pdf.
Automation Testing: 15 critical test cases automated using Selenium WebDriver (Python). Scripts are located in the scripts/automation/ directory.
Tools Used: Selenium WebDriver, unittest, Browser DevTools, Excel for documentation.

Test Environment:
URL: https://demo.prestashop.com
Browsers: Chrome v115, Firefox v110, Edge v114, Opera v99
Devices: Desktop (1920x1080), Mobile (360x640), Tablet (768x1024)
OS: Windows 11, macOS Ventura

Key Findings
Total Test Cases: 71
Passed: 64 (90.1%)
Failed: 7 (9.9%)

Critical Defects:
Login failure on Microsoft Edge (BUG_002)
Checkout allowing orders without T&C agreement (BUG_005)
Search returning unrelated products for invalid terms (BUG_007)

See Bug_Report.xlsx for detailed defect analysis and Project_Report.pdf for root causes, risk assessment, and recommendations.

Setup and Usage
To run the automation scripts:

Prerequisites:
Python 3.8+
Selenium WebDriver (pip install selenium)
WebDriver for Chrome/Edge/Firefox

Steps:
Clone the repository: git clone https://github.com/<your-username>/prestashop-demo-testing.git
Navigate to the scripts/automation/ directory: cd prestashop-demo-testing/scripts/automation
Run a script: python registration_tests.py

Notes:
Ensure the PrestaShop demo site is accessible.
Update WebDriver paths in scripts if necessary.

Recommendations
Fix high-priority bugs (e.g., Edge login, T&C enforcement).
Enhance form validations and search functionality.
Expand automation to cover 100% of regression scenarios.
Conduct a security review for sensitive forms.

Conclusion
The testing process successfully identified critical functional and usability issues in the PrestaShop demo site. The deliverables in this repository provide a comprehensive view of the testing efforts and actionable recommendations for improving the platform.

Instructor: Sir Syed Areeb Jafri
Course: Software Testing
