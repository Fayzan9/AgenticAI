# Chat Interface (Light Dashboard Style) -- Requirements

## 1. Layout Structure

### 1.1 Root Layout

-   Full-width responsive layout.
-   Soft neutral page background.
-   Centered main content region.
-   No heavy gradients or visual noise.

------------------------------------------------------------------------

## 2. Top Header Bar

-   Fixed horizontal header at top.
-   Left: Sidebar toggle icon.
-   Center: Active model or chat title dropdown.
-   Right:
    -   Temporary / mode toggle button
    -   User avatar

Behavior: - Sticky on scroll. - Subtle bottom divider or light shadow. -
Compact height.

------------------------------------------------------------------------

## 3. Sidebar

### 3.1 Structure

-   Fixed vertical sidebar on left.
-   Scrollable conversation list.
-   Section grouping:
    -   Today / Yesterday
    -   Previous 7 Days
    -   Previous 30 Days

### 3.2 Items

-   Each conversation:
    -   Title text
    -   Hover state
    -   Active state highlight
-   Ellipsis menu for item actions (rename, delete).

### 3.3 Top Section

-   Product switcher (e.g., ChatGPT, DALL·E).
-   Navigation links:
    -   Library
    -   Explore GPTs

------------------------------------------------------------------------

## 4. Chat Content Area

### 4.1 Container

-   Centered message column.
-   Max width: 720--900px.
-   Generous vertical spacing.
-   Scrollable independently from sidebar.

### 4.2 Message Structure

#### User Message

-   Right-aligned bubble.
-   Rounded corners.
-   Subtle background tint.

#### Assistant Message

-   Left-aligned block or bubble.
-   White or neutral background.
-   Optional small avatar indicator.

### 4.3 Message Actions

-   Inline action icons under assistant messages:
    -   Copy
    -   Like
    -   Dislike
    -   Regenerate
-   Icons appear on hover or low-opacity by default.

------------------------------------------------------------------------

## 5. Input Area

-   Fixed at bottom of chat area.
-   Rounded input container.
-   Multi-line textarea.
-   Send button icon.
-   Placeholder text.

Behavior: - Auto-expand height. - Enter to send. - Shift + Enter for
newline. - Disabled state during response generation.

------------------------------------------------------------------------

## 6. Visual System

### 6.1 Colors

-   Light neutral background.
-   White chat surface.
-   Single accent color for:
    -   Active states
    -   Buttons
    -   Highlights
-   Neutral gray scale for text hierarchy.

### 6.2 Typography

-   Modern sans-serif font.
-   Clear hierarchy:
    -   Heading
    -   Body
    -   Secondary metadata

### 6.3 Spacing

-   8px spacing scale.
-   Consistent padding across components.
-   Balanced whitespace between sections.

------------------------------------------------------------------------

## 7. Interaction & Behavior

-   Smooth hover transitions (150--250ms).
-   Subtle message appearance animation.
-   Loading indicator for assistant response.
-   Keyboard accessible navigation.
-   Visible focus states.

------------------------------------------------------------------------

## 8. Responsiveness

-   Desktop: Sidebar visible.
-   Tablet: Collapsible sidebar.
-   Mobile:
    -   Sidebar hidden by default.
    -   Header remains compact.
    -   Input fixed and usable.

------------------------------------------------------------------------

## 9. Accessibility

-   WCAG-compliant contrast.
-   Keyboard navigation support.
-   Proper ARIA roles for chat, messages, and input.
