# blood_report_analyser

## Purpose

The **blood_report_analyser** use case processes a blood test report and generates a **structured medical summary** highlighting key biomarkers and potential health indicators.

This use case standardizes how blood reports are interpreted so that the output is consistent and easy to understand.

---

## Inputs

The use case expects the following input:

* **Blood Test Report**

  * Format: PDF or extracted text
  * Content: Lab test values and reference ranges

Optional inputs:

* Patient age
* Patient gender
* Additional clinical context (if available)

---

## Outputs

The use case produces a **structured medical summary** that includes:

* Extracted biomarker values
* Comparison against reference ranges
* Identification of abnormal markers
* Categorized results (normal / high / low)
* Basic health observations based on the results

The final output is stored in:

```
executions/blood_report_analyser/<execution_id>/
```

---

## Execution Steps

1. **Load the Blood Report**

   * Accept the blood report file or text input.

2. **Extract Test Values**

   * Identify biomarkers, measured values, and reference ranges from the report.

3. **Analyze Biomarkers**

   * Compare extracted values against the provided reference ranges.
   * Determine whether values are normal, high, or low.

4. **Generate Summary**

   * Produce a structured summary containing:

     * Key biomarker results
     * Highlighted abnormalities
     * Brief health insights

5. **Store the Output**

   * Save the generated analysis in the execution directory.

---

## Example Usage

### User Request

```
Analyze this blood test report and summarize key health indicators.
```

### System Action

```
Execute blood_report_analyser use case
```

### Expected Output

A structured summary including:

* Hemoglobin status
* Cholesterol levels
* Blood sugar indicators
* Abnormal markers highlighted
* Brief medical observations

---

## Notes

* This use case provides **informational insights only** and should not replace professional medical advice.
* Output should remain **structured and consistent** across executions.

---
