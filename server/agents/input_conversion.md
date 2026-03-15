# input_conversion.md

## Purpose

`input_conversion.md` defines how an `input.md` specification should be converted into a dynamic HTML form (`input.html`) that will be rendered in the UI. The generated form allows users to provide all required inputs before triggering the agent execution.

The goal is **consistent design, predictable structure, and deterministic rendering** so that any `input.md` can be automatically converted into a uniform UI.

---

# Overall Conversion Flow

1. **Input Source**

   * `input.md` contains the structured definition of parameters required by the agent.

2. **Conversion Step**

   * A converter reads `input.md`
   * It maps each input definition into a corresponding **HTML form component**

3. **Generated Output**

   * `input.html`
   * A fully structured HTML form used by the frontend to render the UI

4. **User Interaction**

   * User fills the form
   * Form submission sends a JSON payload to the agent runtime

---

# Standard HTML Structure

All generated forms must follow this structure to ensure consistency across agents.

```html
<form id="agent-input-form">

  <div class="form-section">
    <h2>Section Title</h2>

    <div class="form-field">
      <label for="field_id">Field Label</label>
      <!-- input element -->
      <small class="description">Help text</small>
    </div>

  </div>

  <div class="form-actions">
    <button type="submit">Run Agent</button>
  </div>

</form>
```

---

# Layout Rules

### Form Container

* Use a single `<form>` wrapper
* Group related inputs inside **sections**

```
.form-section
```

### Field Container

Each field must be wrapped inside:

```
.form-field
```

Structure:

```html
<div class="form-field">
  <label for="field_id">Label</label>
  <input ... />
  <small>Description text</small>
</div>
```

---

# Field Specification

Each parameter defined in `input.md` must specify:

| Property | Description       |
| -------- | ----------------- |
| id       | unique identifier |
| label    | display name      |
| type     | input type        |
| required | boolean           |
| default  | default value     |
| help     | help text         |

Example in `input.md`:

```
name: project_name
type: text
label: Project Name
required: true
help: Name of the project
```

---

# Supported Input Types

The following input types must be supported.

---

# 1. Text Input

Use for short strings.

```html
<input
  type="text"
  id="project_name"
  name="project_name"
  placeholder="Enter project name"
/>
```

Rules

* max length: 255
* supports placeholder
* supports default value

---

# 2. Multiline Text (Textarea)

Use for long descriptions.

```html
<textarea
  id="description"
  name="description"
  rows="4"
></textarea>
```

Rules

* default rows = 4
* expandable

---

# 3. Number Input

For numeric values.

```html
<input
  type="number"
  id="max_iterations"
  name="max_iterations"
  min="0"
  step="1"
/>
```

Options

* `min`
* `max`
* `step`

---

# 4. Dropdown (Select)

Use when options are predefined.

```html
<select id="model" name="model">
  <option value="gpt-4">GPT-4</option>
  <option value="gpt-4o">GPT-4o</option>
  <option value="gpt-5">GPT-5</option>
</select>
```

Rules

* Always include placeholder option if optional

```
<option value="">Select an option</option>
```

---

# 5. Radio Buttons

Used when **only one option must be selected and options should be visible**.

```html
<label>
  <input type="radio" name="mode" value="fast">
  Fast
</label>

<label>
  <input type="radio" name="mode" value="accurate">
  Accurate
</label>
```

---

# 6. Checkbox

Used for boolean values.

```html
<input
  type="checkbox"
  id="enable_logging"
  name="enable_logging"
/>
```

Returns

```
true | false
```

---

# 7. Multi Select

Used when multiple options may be selected.

```html
<select id="tools" name="tools" multiple>
  <option value="search">Search</option>
  <option value="code">Code</option>
  <option value="analysis">Analysis</option>
</select>
```

Return format

```
array<string>
```

---

# 8. File Upload

Used when the agent requires user-provided files.

```html
<input
  type="file"
  id="dataset"
  name="dataset"
/>
```

Optional constraints

```
accept=".csv,.json"
```

Example:

```html
<input
  type="file"
  id="dataset"
  name="dataset"
  accept=".csv,.json"
  multiple
/>
```

Options

| Property | Description            |
| -------- | ---------------------- |
| accept   | file types             |
| multiple | allow multiple uploads |
| max_size | maximum size           |

---

# 9. Date Input

```html
<input
  type="date"
  id="start_date"
  name="start_date"
/>
```

---

# 10. Hidden Input

Used for metadata.

```html
<input
  type="hidden"
  name="agent_id"
  value="research_agent"
/>
```

---

# Required Field Handling

Required fields must include

```html
required
```

Example

```html
<input
  type="text"
  id="project_name"
  name="project_name"
  required
/>
```

---

# Help Text

Each field may contain optional help text.

Example

```html
<small class="description">
Provide a short name for your project
</small>
```

---

# Validation Rules

Validation should be applied both:

* frontend
* backend

Supported validations

| Type      | Example             |
| --------- | ------------------- |
| required  | must not be empty   |
| min       | numeric lower bound |
| max       | numeric upper bound |
| regex     | pattern validation  |
| file type | allowed extensions  |
| file size | upload limit        |

Example

```html
<input
  type="text"
  pattern="[A-Za-z0-9_-]+"
/>
```

---

# Form Submission

The form submission must convert the values into a JSON payload.

Example payload

```json
{
  "project_name": "AI Agent",
  "model": "gpt-5",
  "max_iterations": 5,
  "enable_logging": true
}
```

Submission endpoint

```
POST /run-agent
```

---

# UI Consistency Rules

To maintain uniform UI across agents:

1. Always use `form-section`
2. Always wrap inputs with `form-field`
3. Always include labels
4. Always include help text if available
5. Use consistent naming (`snake_case`)

---

# Example Generated HTML

```html
<form id="agent-input-form">

  <div class="form-section">
    <h2>Project Settings</h2>

    <div class="form-field">
      <label for="project_name">Project Name</label>
      <input type="text" id="project_name" name="project_name" required />
      <small>Name of the project</small>
    </div>

    <div class="form-field">
      <label for="model">Model</label>
      <select id="model" name="model">
        <option value="">Select model</option>
        <option value="gpt-4">GPT-4</option>
        <option value="gpt-5">GPT-5</option>
      </select>
    </div>

    <div class="form-field">
      <label for="dataset">Dataset</label>
      <input type="file" id="dataset" name="dataset" accept=".csv,.json" />
    </div>

  </div>

  <div class="form-actions">
    <button type="submit">Run Agent</button>
  </div>

</form>
```

---

# Summary

The conversion system must:

1. Parse `input.md`
2. Map each input definition to a standardized HTML component
3. Produce a consistent `input.html`
4. Ensure predictable structure for frontend rendering
5. Support all common input types (text, dropdown, file upload, etc.)

This ensures that every agent can automatically generate a consistent UI without custom frontend development.
