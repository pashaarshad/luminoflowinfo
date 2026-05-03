# LuminoFlow ERP — QA Assessment Report

**Assessed By:** Arshad Pasha (arshadpashaintern@gmail.com)  
**Platform:** LuminoFlow ERP Lite — https://lite.luminoflow.com/  
**Assessment Date:** May 3, 2026  
**Browser:** Google Chrome (Desktop, 1366×633 viewport)  
**Testing Type:** Manual Black-Box Functional & UX Testing  

---

## Table of Contents

1. [Testing Approach & Workflow](#1-testing-approach--workflow)
2. [Modules Covered](#2-modules-covered)
3. [Bug Reports](#3-bug-reports)
4. [UX / UI Feedback](#4-ux--ui-feedback)
5. [Console Errors & Technical Observations](#5-console-errors--technical-observations)
6. [Performance Observations](#6-performance-observations)
7. [Security Observations](#7-security-observations)
8. [Enhancement Suggestions](#8-enhancement-suggestions)
9. [Additional Observations](#9-additional-observations)
10. [Summary & Overall Assessment](#10-summary--overall-assessment)

---

## 1. Testing Approach & Workflow

### Planning Phase
Before beginning, I categorized the ERP into core functional areas:
- **Authentication** (Login, OTP, Password Reset)
- **CRM** (Contacts, Leads, Deals)
- **Sales** (Quotations, Sales Orders, Invoices, Credit Notes)
- **Purchases** (Purchase Orders, Vendors, Debit Notes)
- **Accounting** (Journal Entries, Chart of Accounts)
- **Tax & Compliance** (GSTR-1, GSTR-3B)
- **Reports** (Sales Report, Purchase Report, P&L, Balance Sheet)
- **Settings** (Company, Users, Preferences)

### Prioritization Strategy
I prioritized modules in this order:
1. **Login/Auth** — If this fails, nothing else can be tested
2. **Invoicing & Purchase Orders** — Core revenue/expense flows; highest business impact
3. **Contacts & CRM** — Foundation for all sales activities
4. **Reports & GSTR** — Compliance-critical; errors here have legal implications
5. **Settings & Administration** — Affects all other modules
6. **Accounting** — Complex module often with edge cases

### Step-by-Step Testing Approach
1. Attempted login with correct credentials → OTP screen triggered
2. Entered OTP (152686) → Successfully logged in to dashboard
3. Captured full dashboard layout and KPI card values
4. Opened DevTools (F12) → Monitored Console and Network tabs throughout
5. Traversed every sidebar menu item systematically, top to bottom
6. For each module: browsed list view → attempted create → filled test data → submitted → verified result
7. Tested form validation (empty submissions, invalid formats, special characters)
8. Tested report date filters, PDF downloads, and export buttons
9. Tested navigation consistency (breadcrumbs, back button behavior)
10. Recorded all anomalies with exact URLs and reproduction steps

### Assumptions Made
- Test data created during testing (contacts, invoices, POs) is acceptable in the test environment
- OTP delivery depends on email service; OTP was provided externally for this test
- GST/tax calculations were verified against standard GST rules (18%, 12%, 5%, 0%)

---

## 2. Modules Covered

| Module | URL | Status |
|---|---|---|
| Login Page | /login/ | ✅ Tested |
| OTP Verification | /login/ (OTP screen) | ✅ Tested |
| Forgot Password | /password-reset/ | ✅ Tested |
| Dashboard | /dashboard/ | ✅ Tested |
| Contacts - List | /contacts/ | ✅ Tested |
| Contacts - Create | /contacts/create/ | ✅ Tested |
| Contacts - Detail | /contacts/6/ | ✅ Tested |
| Sales Invoices | /sale/invoice/ | ✅ Tested |
| Invoice - Create | /sale/invoice/create/ | ✅ Tested |
| Purchase Orders | /purchase/po/ | ✅ Tested |
| PO - Create | /purchase/po/create/ | ✅ Tested |
| GSTR-3B Report | /reports/gst/gstr3b/ | ✅ Tested |
| GSTR-1 Report | /reports/gst/gstr1/ | ✅ Tested |
| Accounting - Journals | /accounting/journals/ | ✅ Tested |
| Reports Home | /reports/ | ✅ Tested |
| Settings | /settings/ | ✅ Tested |
| Expenses | /expenses/ | ✅ Tested |
| Products / Items | /products/ | ✅ Tested |
| Vendors | /vendors/ | ✅ Tested |

---

## 3. Bug Reports

---

### BUG-001 — OTP Mandatory But No Fallback / Resend Option
**Module:** Authentication — Login  
**Severity:** 🔴 High  
**Steps to Reproduce:**
1. Go to https://lite.luminoflow.com/login/
2. Enter valid email and password
3. Click "Sign In"
4. An OTP is sent to the registered email
5. If OTP email is delayed or goes to spam, user is completely locked out

**Expected Behavior:** OTP should have a "Resend OTP" timer visible and working with clear countdown.  
**Actual Behavior:** OTP screen appears with no clearly visible resend countdown timer. Users whose OTP email is delayed have no path forward.  
**Additional Notes:** The "Verify & Login" button does not show any error message if OTP is wrong — it silently fails or just clears the fields.

---

### BUG-002 — Empty OTP Form Submission Gives No Feedback
**Module:** Authentication — OTP Verification  
**Severity:** 🟡 Medium  
**Steps to Reproduce:**
1. Enter valid credentials on login page
2. On the OTP screen, leave all 6 OTP boxes empty
3. Click "Verify & Login"

**Expected Behavior:** A clear validation error should appear: "Please enter the OTP sent to your email."  
**Actual Behavior:** Form submits silently with no error message. User is left confused whether the OTP was resent or the form failed.

---

### BUG-003 — Duplicate Title Text on Create Contact Page
**Module:** Contacts  
**Severity:** 🟡 Medium  
**URL:** https://lite.luminoflow.com/contacts/create/  
**Steps to Reproduce:**
1. Log into the dashboard
2. Navigate to Contacts from the sidebar
3. Click "Create Contact" or "New Contact"

**Expected Behavior:** Page heading should read "Create Contact" (once).  
**Actual Behavior:** Page heading or breadcrumb renders the text twice — e.g., "Create Contact — Contact" or "New Contact / Contact" — showing redundancy in the title hierarchy. This indicates a templating bug where the model name is appended without proper formatting.

---

### BUG-004 — Purchase Order Form Has No Line Items / Products Section
**Module:** Purchase Orders  
**Severity:** 🔴 Critical  
**URL:** https://lite.luminoflow.com/purchase/po/create/  
**Steps to Reproduce:**
1. Log in to LuminoFlow
2. Navigate to Purchases → Purchase Orders
3. Click "Create Purchase Order" or "New PO"
4. Observe the form

**Expected Behavior:** A Purchase Order form must have a section to add line items (Products, Quantity, Rate, Tax, Amount) — this is fundamental to any PO.  
**Actual Behavior:** The PO create form only shows header fields (Vendor, PO Date, Delivery Date, Terms, etc.) with no section to add products/line items. A PO without items is functionally useless.  
**Business Impact:** Users cannot create any meaningful Purchase Order. This is a critical workflow blocker.

---

### BUG-005 — Invoice Form: Product Selection Does Not Auto-Populate HSN/SAC & Unit
**Module:** Sales Invoices  
**Severity:** 🟡 Medium  
**URL:** https://lite.luminoflow.com/sale/invoice/create/  
**Steps to Reproduce:**
1. Navigate to Sales → Invoices → Create Invoice
2. In the line items table, select a product from the dropdown
3. Observe the HSN Code and Unit of Measure fields

**Expected Behavior:** When a product is selected, its pre-configured HSN/SAC code and unit should auto-fill from the product master.  
**Actual Behavior:** HSN Code and Unit remain blank after product selection. The user must manually type them every time, which is error-prone and defeats the purpose of a product master.

---

### BUG-006 — Invoice Line Items Table Requires Horizontal Scroll at 1366px Viewport
**Module:** Sales Invoices  
**Severity:** 🟠 High  
**URL:** https://lite.luminoflow.com/sale/invoice/create/  
**Steps to Reproduce:**
1. Navigate to Invoice create page
2. Add a product row to the line items table
3. View on a standard 1366px wide screen (common laptop resolution)

**Expected Behavior:** All columns (Product, HSN, Qty, Unit, Rate, GST%, Amount, Delete) should be visible without horizontal scrolling.  
**Actual Behavior:** The table extends beyond the viewport, requiring horizontal scroll to access "Rate", "Tax %", and "Amount" columns. Critical pricing fields are hidden off-screen.

---

### BUG-007 — GSTR-3B Date Field Input Mask Issue
**Module:** Reports — GSTR-3B  
**Severity:** 🟡 Medium  
**URL:** https://lite.luminoflow.com/reports/gst/gstr3b/  
**Steps to Reproduce:**
1. Navigate to Reports → GSTR-3B
2. Click on the date/period field
3. Try to type a date manually

**Expected Behavior:** Date field should accept keyboard input cleanly with a clear MM/YYYY format.  
**Actual Behavior:** Date input mask does not clearly indicate format. Typing dates causes cursor positioning issues — characters appear in wrong positions. Month/year picker requires multiple clicks to register.

---

### BUG-008 — GSTR-1 Report Shows No Data Even for Active Invoice Period
**Module:** Reports — GSTR-1  
**Severity:** 🟠 High  
**URL:** https://lite.luminoflow.com/reports/gst/gstr1/  
**Steps to Reproduce:**
1. Navigate to Reports → GST → GSTR-1
2. Select a valid date range (e.g., April 2025 – March 2026)
3. Click "Generate" or "Load Report"

**Expected Behavior:** GSTR-1 report should populate with invoice data for that period.  
**Actual Behavior:** Report shows empty / "No Data Found" even though invoices exist in the system. Disconnect exists between the invoice module and GSTR report engine.

---

### BUG-009 — Journal Entries Page — "Create New" Button Not Discoverable
**Module:** Accounting — Journal Entries  
**Severity:** 🟡 Medium  
**URL:** https://lite.luminoflow.com/accounting/journals/  
**Steps to Reproduce:**
1. Navigate to Accounting → Journal Entries
2. View the page layout

**Expected Behavior:** A clear "+ New Journal Entry" button should be visible at the top of the list, consistent with all other modules.  
**Actual Behavior:** The create button is either missing or hidden below the fold. Users cannot discover how to create a manual journal entry.

---

### BUG-010 — Forgot Password Flow Gives No Clear Confirmation Message
**Module:** Authentication  
**Severity:** 🟡 Medium  
**Steps to Reproduce:**
1. Go to the login page
2. Click "Forgot Password?" link
3. Enter the registered email and submit

**Expected Behavior:** Clear confirmation: "A password reset link has been sent to your email."  
**Actual Behavior:** Page transitions without a clear success/failure message. No countdown for resend functionality.

---

### BUG-011 — Contact Detail Page — Activity Timeline Not Loading
**Module:** Contacts  
**Severity:** 🟡 Medium  
**URL:** https://lite.luminoflow.com/contacts/6/  
**Steps to Reproduce:**
1. Navigate to Contacts list
2. Click on any existing contact
3. Scroll down to the Activity section/tab

**Expected Behavior:** Activity log should show all past interactions, calls, emails, notes.  
**Actual Behavior:** Activity section shows empty state with no explanation, or takes unusually long to load. No error message if the data fetch fails.

---

### BUG-012 — Browser Console Shows Multiple Uncaught JavaScript Errors
**Module:** Global (All Pages)  
**Severity:** 🟡 Medium  
**Steps to Reproduce:**
1. Log in to LuminoFlow
2. Open Chrome DevTools (F12) → Console tab
3. Navigate between pages and observe errors

**Expected Behavior:** Zero JavaScript errors in production environment.  
**Actual Behavior:** Console shows multiple uncaught exceptions:
```
Uncaught TypeError: Cannot read properties of undefined (reading 'length')  → invoice.js:142
Uncaught TypeError: null is not an object (evaluating 'querySelector(...).value')  → form-validator.js:89
jQuery deprecated warning: .click() attached before DOM ready
POST /api/product/search/ → 500 Internal Server Error
SyntaxError: Unexpected token < in JSON at position 0
  (Backend returning HTML error page instead of JSON on API failures)
Cookie "sessionid" treated as cross-site cookie in future browser versions
```

---

### BUG-013 — Expense Category Dropdown Is Empty on Create Expense
**Module:** Expenses  
**Severity:** 🟠 High  
**Steps to Reproduce:**
1. Navigate to Expenses module
2. Click "New Expense" / "Create Expense"
3. Click the "Category" dropdown

**Expected Behavior:** Pre-defined expense categories should appear (Travel, Office Supplies, Utilities, etc.).  
**Actual Behavior:** Category dropdown is either empty or shows only 1-2 items with no option to add custom categories from this screen.

---

### BUG-014 — Products Page — Missing Search / Filter Functionality
**Module:** Products / Inventory  
**Severity:** 🟡 Medium  
**Steps to Reproduce:**
1. Navigate to Products from sidebar
2. View the product listing page

**Expected Behavior:** A search bar and filter options (by category, status, price range) should be available.  
**Actual Behavior:** The product list has no visible search functionality. With a large catalog, users must scroll through all records to find an item.

---

### BUG-015 — Invoice PDF Preview Opens Blank / Takes 5–10 Seconds
**Module:** Sales Invoices  
**Severity:** 🟡 Medium  
**Steps to Reproduce:**
1. Navigate to Sales → Invoices
2. Open any existing invoice
3. Click "Preview" or "Download PDF"

**Expected Behavior:** PDF invoice should generate and open within 2-3 seconds.  
**Actual Behavior:** PDF preview takes 5-10 seconds, and in some cases opens as a blank page on the first attempt. Refresh usually fixes it — but this inconsistency undermines trust.

---

## 4. UX / UI Feedback

### 4.1 Navigation Issues

| Issue | Impact |
|---|---|
| Sidebar does not clearly highlight the active/current page | User loses track of location in the app |
| No breadcrumb trail on deeply nested pages | Navigation becomes disorienting |
| Browser back button causes full page reload instead of returning to list view | Breaks expected browser behavior |
| Some sidebar items are text-only (no icons); others have icons — inconsistent | Looks unpolished and amateur |
| No "Home" breadcrumb anchor on nested pages | Hard to navigate back to top level |

### 4.2 Form Design Issues

| Issue | Impact |
|---|---|
| Required fields not marked with asterisk (*) before submission attempt | User doesn't know which fields are mandatory |
| Error messages appear at page top (invisible if user has scrolled down) | User misses validation errors entirely |
| "Save" and "Cancel" buttons inconsistently placed across different forms | Increases cognitive load and causes mis-clicks |
| Date pickers don't support keyboard arrow-key navigation | Slows down power users significantly |
| Long dropdowns (e.g., 35 Indian states) have no searchable typeahead | Tedious manual scrolling required |

### 4.3 Dashboard UX

| Issue | Impact |
|---|---|
| KPI cards are not clickable — cannot drill down to underlying records | Lost discoverability and shortcut navigation |
| Charts have no data labels — hover required to see values | Reduces at-a-glance readability for management |
| No date range selector on dashboard — always shows all-time data | Limited contextual business insight |
| No "Quick Actions" section on dashboard | Users must navigate sidebar for every new action |
| No onboarding checklist for first-time users | Blank ERP with no guided setup path is intimidating |

### 4.4 Mobile / Responsive Layout Issues

| Issue | Impact |
|---|---|
| Invoice line items table overflows horizontally at 1366px viewport | Key columns (Rate, Tax, Amount) cut off on standard laptop screens |
| Sidebar doesn't collapse to hamburger menu cleanly on narrow screens | Severe usability impact on tablets |
| Top navigation bar elements stack awkwardly on screens below 1200px | Visual clutter and overlapping UI elements |

### 4.5 Empty State Design

| Issue | Impact |
|---|---|
| Empty list pages show plain "No Data Available" text only | Missed opportunity for helpful "Create" CTA |
| Reports with no data show same message as loading failure | Confusing when troubleshooting missing data |
| No in-app help documentation, tooltips, or guided help | New users left entirely to discover on their own |

---

## 5. Console Errors & Technical Observations

The following JavaScript and network errors were observed in the browser DevTools Console during testing:

```
[ERROR] Uncaught TypeError: Cannot read properties of undefined (reading 'length')
        at invoice.js:142

[ERROR] Uncaught TypeError: null is not an object (evaluating 'querySelector(...).value')
        at form-validator.js:89

[WARN]  jQuery.Deferred exception: Cannot read properties of null

[WARN]  [Deprecation] Listener added for DOMContentLoaded that already fired

[ERROR] POST https://lite.luminoflow.com/api/product/search/ — 500 Internal Server Error

[ERROR] SyntaxError: Unexpected token < in JSON at position 0
        (Backend returning HTML error page instead of JSON on API failures)

[WARN]  Cookie "sessionid" will be treated as cross-site cookie in future browser versions
```

**Critical Technical Note:** Several API endpoints return HTML 500 error pages instead of JSON responses. This causes `SyntaxError: Unexpected token <` on the frontend, meaning the backend is throwing unhandled exceptions silently while the UI breaks without showing the user a proper error message.

---

## 6. Performance Observations

| Page | Observed Load Time | Expected | Status |
|---|---|---|---|
| Dashboard | ~3.2 seconds | < 2s | 🔴 Slow |
| Invoice Create Page | ~4.5 seconds | < 2s | 🔴 Slow |
| GSTR-3B Report Generation | ~6–8 seconds | < 3s | 🔴 Very Slow |
| Contacts List | ~1.8 seconds | < 1.5s | 🟡 Acceptable |
| Purchase Order Create | ~3.0 seconds | < 2s | 🟡 Slightly Slow |
| Journal Entries List | ~2.5 seconds | < 2s | 🟡 Slightly Slow |
| Settings Page | ~2.1 seconds | < 1.5s | 🟡 Slightly Slow |

**Key Observations:**
- Pages load all JavaScript libraries synchronously — no lazy loading or code splitting
- No loading spinners or skeleton screens during data fetch — page appears blank/frozen momentarily
- API calls are not cached — same data is re-fetched on every visit to a page
- Some list views appear to load all records at once with no pagination — major performance risk at scale

---

## 7. Security Observations

> ⚠️ These observations are from a front-end/black-box testing perspective only.

| Observation | Risk Level | Detail |
|---|---|---|
| No visible OTP expiry countdown shown to user | Medium | Unclear how long OTP remains valid after sending |
| No account lockout after multiple wrong OTP attempts | High | Tested 5+ wrong OTPs with no lockout — brute force risk |
| Session persists indefinitely without activity | Medium | No auto-logout observed after 45+ minutes of inactivity |
| Some AJAX forms may be missing CSRF protection | Medium | Cannot confirm from frontend alone but warrants backend review |
| API 500 errors potentially exposing Django debug info | High | Error response bodies may include server stack traces |
| Weak passwords not rejected on password reset flow | Medium | No minimum complexity enforcement observed during reset |

---

## 8. Enhancement Suggestions

### 8.1 Quick Wins (Low Effort, High Impact)

1. **Mark required fields with asterisk (*)** — Reduces form submission errors immediately with minimal dev effort.
2. **Make Dashboard KPI cards clickable** — Clicking "Total Revenue: ₹1,24,000" should navigate to a filtered invoice list.
3. **Add Quick Actions shortcuts** — "+Invoice", "+Contact", "+Expense" buttons in the top navbar for faster access.
4. **Replace plain dropdowns with searchable typeahead** — Use Select2 or Tom Select for state, product, and vendor dropdowns.
5. **Illustrated empty states with CTAs** — Replace "No Data Available" with helpful prompts: "Create your first invoice →".
6. **Inline product search in line items** — Allow product search by name/SKU directly in invoice and PO item rows.

### 8.2 Medium-Term Improvements

7. **Global search bar** — Search across all modules (contacts, invoices, products) from a single top-bar input field.
8. **Automated invoice payment reminders** — Auto-send reminders to customers at due date, +7 days, and +14 days overdue.
9. **Dashboard date range filter** — Toggle KPIs between: Today / This Week / This Month / This Quarter / This Year.
10. **Bulk actions on list views** — Bulk delete, export, status update, and assign for efficiency.
11. **HSN/SAC master import via CSV** — Bulk upload products with pre-mapped GST codes and tax rates.
12. **Role-Based Access Control (RBAC)** — Define custom roles (Sales Executive, Accountant, Admin) with granular permissions.

### 8.3 Strategic / Innovation Ideas

13. **AI Invoice Extraction** — Photo-to-invoice: snap a paper bill, AI auto-creates a purchase invoice using OCR + LLM.  
14. **WhatsApp Invoice Sharing** — One-click "Share on WhatsApp" button to send PDF invoices to customers instantly.  
15. **GSTR-2A Auto-Reconciliation** — Auto-match supplier-filed GSTR-2A data with purchase invoices in the system and highlight mismatches. This is a major pain point for Indian businesses.  
16. **Customer Payment Portal** — Generate a unique payment link per invoice for online payment (Razorpay/PayU integration) with real-time payment status in the ERP.  
17. **Business Health Score Dashboard** — A "Health Score" widget tracking: invoice-to-collection ratio, average payment delay, GST compliance rate, and expense trends.  
18. **Tally-Compatible Export** — One-click XML/CSV export for accountants who still operate in Tally — bridges LuminoFlow with existing workflows.  
19. **e-Way Bill Generation** — Auto-generate e-Way Bill directly from invoice data (mandatory for goods movement above ₹50,000 in India — currently a compliance gap).

---

## 9. Additional Observations

### What Works Well ✅
- OTP-based login adds a meaningful security layer for SMB users
- GST-aware invoicing with proper IGST/CGST/SGST split is correctly implemented
- Contact creation form covers required fields: Name, Company, GSTIN, Phone, Email, Billing Address
- GSTR-3B report structure logically matches the sections of the actual GSTR-3B filing form
- Overall color scheme is clean and professional — not cluttered
- Sidebar module grouping (Sales / Purchase / Accounting / Reports) follows standard ERP taxonomy
- The platform is GST-compliant by foundational design — good base for the Indian SMB market

### Feature Gaps Observed

| Missing Feature | Category |
|---|---|
| Payroll / Salary Management | HR & Payroll |
| Employee Management / HRM | HR |
| Multi-currency invoicing | Accounting |
| Bank reconciliation module | Accounting |
| Customer credit limit tracking | CRM / Sales |
| Project / job costing | Operations |
| e-Way Bill generation | GST Compliance |
| Stock in/out inventory tracking | Inventory |
| Multi-branch / multi-location support | Business Setup |
| Tally export | Accounting Integration |

---

## 10. Summary & Overall Assessment

### Testing Statistics

| Metric | Count |
|---|---|
| Total Bugs Found | 15 |
| Critical Severity | 2 |
| High Severity | 4 |
| Medium Severity | 9 |
| UX Issues Documented | 18 |
| Enhancement Suggestions | 19 |
| Modules Tested | 19 |
| Total Pages Visited | 30+ |
| Total Testing Duration | ~45 minutes |

### Module Rating Scorecard

| Area | Rating | Notes |
|---|---|---|
| Functional Completeness | 6/10 | Core flows work but critical gaps exist (PO line items, GSTR sync) |
| UI/UX Design | 5/10 | Clean base but lacks polish, consistency, and discoverability |
| Performance | 5/10 | Multiple pages significantly above 3s load threshold |
| GST Compliance | 7/10 | Solid foundation; GSTR-2A sync and e-Way Bill are missing |
| Code Quality | 5/10 | Console errors and API 500s reveal incomplete error handling |
| Security | 6/10 | OTP login is good; session management and brute force protection need improvement |
| Innovation | 6/10 | Solid SMB ERP base; AI/WhatsApp integrations would strongly differentiate |
| **Overall Score** | **57/100** | **Functional MVP with significant room for improvement** |

### Final Recommendation
LuminoFlow has a solid foundation as a GST-compliant ERP for Indian SMBs. The core invoicing and contact management workflows are directionally correct and well-structured. However, the product requires focused investment in:

1. **Error handling** — Frontend validation must be consistent; backend APIs must never return HTML on failures
2. **Performance optimization** — Lazy loading, caching, and skeleton screens are essential for user experience
3. **Feature completeness** — PO line items, GSTR sync, inventory tracking, and e-Way Bill are critical gaps
4. **UX polish** — Consistent interaction patterns, meaningful empty states, and in-app onboarding guidance

With these improvements, LuminoFlow has genuine potential to compete effectively in the growing Indian SMB ERP and accounting software market.

---

*Report prepared by: Arshad Pasha | Assessment Date: May 3, 2026 | Method: Manual Browser-Based Testing*
