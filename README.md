# PrestaShop Demo Testing Project

### Overview
This repository contains the deliverables for a Software Testing project conducted as part of the Software Testing course. The project involved comprehensive manual and automated testing of the [PrestaShop demo e-commerce platform](https://demo.prestashop.com).

The primary goal was to evaluate the platform’s:
- Functionality  
- Usability  
- Performance  

Scenarios tested included:
- User registration
- Product browsing
- Cart management
- Checkout processes

The team delivered:
- 71 test cases  
- Bug reports  
- Automation scripts  
- A detailed project report summarizing the process and outcomes

---

### Team Members and Contributions
- **Syed Abdul Rehman (K21-3156):** Project Leader, Test Planner, Test Case Developer, Automation Developer, All Documents Compiler
- **Asadullah Wagan (K21-4824):** Test Executor, Automation Specialist  
- **Rana Wahaj Ahmed (K21-3281):** Test Executor  
- **Syed Hadi Raza (K21-3420):** Test Executor  
- **Wara Batool (K21-3214):** Test Executor, Test Case Developer  

> Detailed contributions are outlined in the Project Report.

---

### Testing Scope

#### In-Scope
- Customer-facing features:
  - Search
  - Cart
  - Checkout
  - User management
- Admin-side features:
  - Product/inventory management
  - Order processing

#### Out-of-Scope
- Real payment gateway integration  
- Third-party API integrations  
- Long-term database checks  

#### Covered Scenarios
- User Registration & Login  
- Cart Management  
- Product Filtering  
- Contact Form & Newsletter  
- Cross-Browser UI Testing  
- Checkout Process (Guest & Logged-in User)  
- UI Responsiveness  
- Product Searching  

---

### Testing Methodology

- **Manual Testing:**
  - 71 test cases executed using structured test plans and exploratory testing  
  - Results documented in `Test_Cases.xlsx` and `Manual_Execution_Report.pdf`  

- **Automation Testing:**
  - 15 critical test cases automated using Selenium WebDriver (Python)  
  - Scripts are located in the `scripts/automation/` directory  

- **Tools Used:**
  - Selenium WebDriver  
  - Python `unittest`  
  - Browser DevTools  
  - Excel  

---

### Test Environment

- **URL:** [https://demo.prestashop.com](https://demo.prestashop.com)
- **Browsers:** 
  - Chrome v115  
  - Firefox v110  
  - Edge v114  
  - Opera v99  
- **Devices:** 
  - Desktop (1920x1080)  
  - Mobile (360x640)  
  - Tablet (768x1024)  
- **Operating Systems:** 
  - Windows 11  
  - macOS Ventura  

---

### Key Findings

- **Total Test Cases:** 71  
- **Passed:** 64 (90.1%)  
- **Failed:** 7 (9.9%)  

#### Critical Defects
- **BUG_002:** Login failure on Microsoft Edge  
- **BUG_005:** Checkout allowing orders without T&C agreement  
- **BUG_007:** Search returns unrelated products for invalid terms  

> See `Bug_Report.xlsx` for detailed defect analysis and `Project_Report.pdf` for root causes, risk assessment, and recommendations.

---

### Setup and Usage

#### Prerequisites
- Python 3.8+  
- Selenium WebDriver (`pip install selenium`)  
- WebDriver for Chrome/Edge/Firefox  

#### Steps to Run Automation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/prestashop-demo-testing.git
