## Hospital Bill Analyzer

### Purpose

Analyze hospital bills and convert them into structured cost insights.
Break down charges into categories, highlight expensive items, and estimate insurance-eligible costs.

---

### Input

Hospital bill in `PDF` or `TXT`.

---

### Processing

1. Extract line items (description, quantity, unit price, total).
2. Group charges into categories:

   * Room Charges
   * Doctor/Consultation
   * Surgery/Procedure
   * Nursing
   * Lab Tests
   * Imaging
   * Medicines/Pharmacy
   * Consumables
   * Administrative/Misc
3. Calculate totals per category.
4. Flag expensive items (≥10% of total bill).
5. Mark insurance eligibility: `eligible`, `partial`, `not_eligible`.

---

### Output (JSON)

```json
{
  "total": 18000,
  "categories": {
    "room_charges": 6000,
    "doctor_fees": 1500,
    "lab_tests": 2500,
    "medicines": 3200
  },
  "expensive_items": [
    {
      "description": "Room Charges",
      "amount": 6000,
      "percentage": 33.3
    }
  ],
  "insurance_eligible_total": 14500,
  "non_eligible_total": 3500
}
```

---
