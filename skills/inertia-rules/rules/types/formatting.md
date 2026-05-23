# Backend-owned formatting & translation

Laravel owns user-facing text and locale-sensitive formatting. The
frontend renders **display-ready** strings that arrive in page props. This
keeps copy, money, dates, and enum labels consistent, translatable, and
testable in one place — the backend.

Laravel sources of truth: lang files (copy, labels, validation messages,
empty states), PHP enums/value objects (values + labels + options),
Spatie Data (serialized display/value DTOs), Form Requests (validation
rules + messages), policies/gates (capability booleans), Wayfinder
(routes/actions).

## Rule: no user-facing formatting in render paths

In page, feature, or app-component render code, do not format user-facing
text. Banned:

```txt
new Intl.NumberFormat(...) / new Intl.DateTimeFormat(...)
date-fns / dayjs / luxon formatting for user-facing text
hard-coded enum label maps
hard-coded validation messages
frontend translation-key construction or i18n dictionaries as the default
route string / controller action construction
```

**Why:** every one of these is a backend decision re-implemented in the
browser. It will disagree with the server (locale, rounding, wording),
duplicate translation, and drift. The backend already computes the
display string — render it.

```tsx
// Good — render the backend-provided display value
<span>{vehicle.price.formatted}</span>      // "EUR 1,299.00" from PHP
<span>{vehicle.status.label}</span>          // "Active" from PHP

// Bad — frontend re-derives money and labels
<span>{new Intl.NumberFormat('en', { style: 'currency', currency: 'EUR' }).format(vehicle.price)}</span>
<span>{vehicle.status === 'active' ? 'Active' : 'Inactive'}</span>
```

## Rule: DTOs carry both machine value and display value

Backend display DTOs send a raw value for behavior **and** a formatted
value for rendering. Use the raw value for IDs, comparisons, sorting,
filtering, form submission, and HTML input values; use the display value
for anything a human reads.

```json
{
  "status": { "value": "active", "label": "Active" },
  "price":  { "amount": 129900, "currency": "EUR", "formatted": "EUR 1,299.00" },
  "createdAt": { "iso": "2026-05-22T12:00:00Z", "formatted": "22 May 2026", "relative": "2 hours ago" }
}
```

**Why:** the frontend legitimately needs the raw value (to sort, submit,
or compare) and the formatted value (to display). Sending both means the
frontend never has to format — and never has to parse a formatted string
back into a value.

## What frontend formatting *is* allowed

- Rendering backend-provided display strings.
- Passing raw values through controls that require a machine format
  (`yyyy-mm-dd` for `input[type=date]`).
- Comparing/branching/sorting/filtering on raw values.
- Visual-only CSS (truncation, wrapping, responsive hiding) that doesn't
  change source text.
- Generic accessibility fallback text inside a primitive when no domain
  copy is available.
- Story/test fixture copy that is clearly not production copy.

Any production exception must be deliberately allowlisted with an owner
and reason. The default answer is to add the value/copy to the backend
Data class.

## Checklist

- No `Intl`/date-library formatting of user-facing text in render paths.
- No hard-coded enum labels, validation messages, or frontend i18n
  dictionaries.
- Display strings (money, dates, labels, copy) come from page props.
- Raw values used only for behavior (compare/sort/filter/submit/input).
- Routes/actions via Wayfinder, not handwritten strings.
- Any frontend-format exception is allowlisted with owner + reason.
