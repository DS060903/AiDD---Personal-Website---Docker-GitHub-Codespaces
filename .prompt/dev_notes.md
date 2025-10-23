# AI Prompts and Reflection (Developer Notes)



This file documents how I used AI during this project. It includes three concrete prompts with the AI's outputs and what I did with them, followed by a short reflection on how AI helped (and where it didn't).

## Prompt Log

### 1) "Tidy up the resume experience layout so the company is on the right and the date sits below it, matching the Kiewit entry."
- AI Output: Suggested converting the header to a two-column grid, placing `.company` on the right and `.duration` beneath it, with CSS updates to `.exp-header` and `.duration`.
- My Action: Accepted with minor tweaks (font-weight and spacing). It aligned all entries consistently.

### 2) "Make the Resume Download PDF button clearly visible on the page header without requiring hover."
- AI Output: Proposed a higher-contrast secondary button, adding a subtle shadow and hover lift.
- My Action: Accepted. The button is now obvious on dark backgrounds and passes contrast checks.

### 3) "Projects page: remove redundant RECAP card and fold its details into the Intelligent Document Querying card. Also remove project images."
- AI Output: Advised deleting the duplicate block, rewriting the remaining card title/description, and hiding `.project-image` via CSS.
- My Action: Accepted with edits. Kept the project as "Project RECAP," consolidated content, and hid thumbnails to simplify the grid.

### 4) "Clarify the 5K+ stat on the home page so it reads less vague."
- AI Output: Recommended changing the label to something more descriptive, e.g., "Regulatory pages parsed and analyzed by my systems."
- My Action: Accepted verbatim. It reads clearer and anchors the number in real work.

### 5) "Fix contact page alignment so Email/Phone and Location/LinkedIn line up cleanly across rows."
- AI Output: First suggested small spacing tweaks; later recommended converting items into uniform cards with a grid and equal min-heights.
- My Action: Modified and accepted the second approach. The card pattern finally made the layout feel consistent on desktop and mobile.

## Reflection (~170 words)
AI sped up a lot of the busywork that normally eats time, especially layout polishing and naming consistency across pages. I found it particularly helpful for CSS grid suggestions: instead of trial-and-error, I got a solid first draft that I could tweak quickly. It also helped me remember small accessibility details (contrast, focus states), which is easy to overlook when you're moving fast.

That said, AI wasn't perfect. It occasionally suggested styles that looked fine in isolation but clashed with my existing scale and spacing. For the contact page, the first attempts didn't align well across rows, so I had to rethink the structure and convert each item into a uniform "card." Another limitation: AI sometimes over-generalized, proposing heavier changes than needed; I had to trim back to keep the design cohesive.

Overall, I used AI like a fast pair-programmer: generate, review, then apply selectively. I accepted good defaults, modified anything visually off, and rejected suggestions that complicated the UX. That balance kept me productive without losing control of the final look and feel.
