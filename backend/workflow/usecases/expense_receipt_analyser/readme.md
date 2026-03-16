
# expense_receipt_analyser

## Purpose
Analyze a purchase receipt and convert it into structured expense data.

The goal is to extract purchased items, validate totals, categorize expenses, and produce a clean structured summary suitable for accounting or expense tracking.

---

## Inputs
The use case expects one of the following:

- Receipt Image or PDF
- Extracted receipt text

Typical receipt information includes:

- merchant name
- purchase date
- item list
- quantity
- unit price
- item total
- tax
- grand total

Optional:

- payment method
- receipt number

---

## Outputs

Execution folder:

executions/expense_receipt_analyser/<execution_id>/

### analysis.json

Structured machine-readable expense data.

Example:

{
  "merchant": "SuperMart Grocery",
  "purchase_date": "2026-03-10",
  "items": [
    {
      "description": "Milk",
      "quantity": 2,
      "unit_price": 60,
      "total": 120,
      "category": "groceries"
    }
  ],
  "subtotal": 450,
  "tax": 22.5,
  "total": 472.5,
  "calculated_total": 472.5,
  "total_matches": true
}

### analysis.md

Human-readable explanation containing:

- receipt summary
- categorized expenses
- validation of totals
- observations

---

## Execution Steps

### 1. Load Receipt
Accept receipt input as:

- image
- PDF
- extracted text

If PDF is provided, extract text using available utilities.

### 2. Extract Line Items
Identify:

- item description
- quantity
- unit price
- item total

Store each item in structured format.

### 3. Categorize Items
Assign categories such as:

- groceries
- electronics
- office_supplies
- food
- transportation
- miscellaneous

### 4. Validate Totals

sum(line_items) -> calculated_subtotal
calculated_subtotal + tax -> calculated_total

Compare calculated totals with receipt totals and flag mismatches.

### 5. Generate Insights

Highlight:

- most expensive item
- largest category spend
- inconsistencies in totals

---

## Example User Request

Analyze this receipt and convert it into structured expense data.

---

## Notes

- Receipts may contain OCR errors.
- Assume quantity = 1 if not specified.
- Always recompute totals rather than trusting printed totals.
