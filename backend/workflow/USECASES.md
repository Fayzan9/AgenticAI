# USECASES.md

A Use Case represents a predefined workflow for handling a specific type of request.
It defines how a particular task should be performed, including the steps, tools, inputs, and expected outputs.

When a user request matches a known pattern (for example: analyzing a report, extracting structured data, or performing a specific task), the system should identify the appropriate use case and execute it according to its documented process.

Use cases ensure that similar requests are handled consistently and predictably.

------------------------------------------------------------------------
## How to Execute a Use Case

1. **Identify the Use Case**
   Check if the user request matches an existing use case. If it does, select that use case for execution.

2. **Read the Documentation**
   Review the use case documentation located at:
   `usecases/<usecase_name>/readme.md`
   This file explains the purpose, inputs, outputs, and execution steps.

3. **Execute the Workflow**
   Perform the required steps defined in the documentation.
   This may include processing data, using utilities, running tools, or generating structured outputs.

4. **Store the Output**
   Save the final result of the execution in:
   `executions/<usecase_name>/<execution_id>`
   Each execution should use a unique run folder.

------------------------------------------------------------------------

# 📋 Available Use Cases

## blood_report_analyser
**Purpose:** Processes a blood test report and generates a structured medical summary with key biomarkers analysis.
**Location:** `usecases/blood_report_analyser/`

## expense_receipt_analyser
**Purpose:** Extracts and summarizes key information from expense receipts, such as vendor, date, total amount, and itemized expenses, to facilitate expense tracking and reporting.  
**Location:** `usecases/expense_receipt_analyser/`

## hospital_bill_analyser
**Purpose:** Analyzes hospital bills to extract patient details, services rendered, charges, and payment information, providing a structured summary for record-keeping or insurance claims.  
**Location:** `usecases/hospital_bill_analyser/`
