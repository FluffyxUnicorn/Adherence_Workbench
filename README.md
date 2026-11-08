# Adherence Workbench — Rebuild Kit (v1.5.14)

A single-file, offline HTML tool for working the Nexus RX aggregate pharmacy adherence report (Humana + Aetna): a wide worklist, a patient chart, call documentation, and one-page provider PDFs. Built 10/14/2026.

Everything runs locally in Edge or Chrome. No server, no install, no uploads.

## What's in this kit

| File | What it is |
|---|---|
| `Adherence_Workbench_v1.5.14.html` | The finished app. Double-click to run. **This alone is enough to keep using it.** |
| `src/src.html` | Readable source (same app, before the font, logo and Excel library are embedded). Edit this. |
| `src/build.py` | Combines source + assets into the single finished HTML. Run: `python build.py` |
| `src/assets/logo_clean.svg` | Cleaned Sequent Health / Northside lockup used in the PDF header and top bar |
| `src/assets/logo_original.svg` | The original logo file as provided |
| `src/assets/app_icon.svg` | App icon (browser tab), embedded by build.py |
| `Adherence_Workbench.ico` | Same icon for a Windows desktop shortcut (right-click shortcut → Properties → Change Icon) |
| `src/lib/inter-latin-wght-normal.woff2` | Inter variable font (embedded so it works offline) |
| `src/lib/xlsx.full.min.js` | SheetJS 0.18.5, reads/writes Excel in the browser |

To rebuild: put the `src` folder somewhere with Python 3, keep the folder layout, run `python build.py`. Paths in build.py assume `assets/` and `lib/` sit next to it (see "Build paths" below).

To change it with an AI assistant later: give it `src/src.html` (or the finished HTML) plus this README and describe the change.

## Features (v1.2)

**Everywhere**
- Dark mode: Light / Dark / Match system (Settings → Appearance). PDFs always print light.
- Icons on tabs, cards and the quick-log bar (inline SVG, no internet needed).

**Worklist tab**
- Loads the Nexus RX aggregate .xlsx/.csv. Finds the header row by matching column names (order doesn't matter, first 10 rows scanned, best-matching sheet used).
- One row per gap. Patient name and a select checkbox are frozen on the left.
- Columns: show/hide and reorder (drag headers, or the Columns panel). Saved per browser.
- Calculated columns: Quick log (VM / NA / ✓ buttons), Attempts, Days Overdue, Impactable In, Last Call, Next Follow-up, Tags.
- Dropdown filters: Payer, Measure, Quality Specialist, Practice (DBA), Provider (Contact Name), Measure Status. Search box covers name, member ID, phone, med, pharmacy, prescriber, gap ID, tags.
- Quick filters: Overdue, Overdue 15+ days, Impactable ≤14 days, PDC <80%, Multiple open meds, Mail order allowed, 30-day supply (<60 days), Not contacted, Follow-up due.
- Sort by any column. Default: Days Overdue, most overdue first. 250 rows per page.
- Export view → Excel of exactly the visible columns and filtered rows.
- Provider PDFs: selected patients, or all filtered patients if none selected.

**Patient tab**
- Header: payer · product · practice, name, DOB (age), phone (large, bold, click-to-dial, copy button), language, member ID. Prev/Next walk the current filtered list.
- Quick log bar: Left voicemail, No answer, Wrong number, Will pick up, Already picked up, Pharmacy confirmed fill. One click saves; Undo for 6 seconds. Voicemail/No answer auto-set a follow-up N business days out (Settings, default 2).
- Cards: Demographics (DOB then phone), Pharmacy, Tags (presets + custom), Outreach (from report), Medication gaps (PDC with 80% marker, days late, days to last impactable date, missed days YTD, fill details), Recommendations.
- Document a call: gap (or all gaps), contact (Patient/Caregiver/Pharmacy/Provider office), outcome, barrier, follow-up date, notes. History list with attempt numbers and copy-notes, edit, delete buttons.
- Edit a call entry (patient history or call log): date, time, gap, contact, outcome, barrier, follow-up, notes, documented by. Edited entries are stamped "Last Edited".

**Call log tab**
- Columns (default order): Date / Time, Patient, Date of Birth, Outcome, Notes, Phone, Payer, Practice, Measure, Medication, Contact, Barrier, Follow-up, Attempt #, Member ID, Provider, Documented By; hidden by default: Gap ID, Current PDC, Refill Due, Last Edited. Show/hide, reorder, sort.
- Edit button on every row; copy button in the Notes cell.
- **Team review** (toggle "My calls / Team review"): choose several call log files at once (one per staff member, e.g. from a shared team folder). Entries are combined and de-duplicated by Entry ID, read-only, held in memory only (never saved, never autosaved, never mixed into your own log). Date range defaults to Last 7 days. Entries with no Documented By are labeled from the file name (Adherence_CallLog_Maria.xlsx → Maria).
- Team summary table per staff member, following the current filters: calls, patients, patients reached, reach rate, VM/no answer/wrong #, pharmacy/provider contacts, barriers found, follow-ups set, plus a team total.
- Export view in team mode → `Team_CallLog_Review_YYYY-MM-DD.xlsx` with sheets Team Summary and Team Calls.
- Team workflow: each person sets their name in Settings and autosaves to their OWN file in a shared team folder. Never point two people's autosave at the same file (autosave rewrites the whole file, so one person's save would erase the other's new calls).
- Filters: search, date range (today / 7 / 30 days / custom), outcome, contact, payer, practice, barrier, staff.
- Quick filters: Reached, Not reached, Pharmacy/provider, Has barrier, Follow-up due, Follow-up next 7 days.
- Export view → Excel.

**Provider PDF** (browser Print → Save as PDF)
- Letter size, one page per patient (two meds go side by side to fit).
- Header: logo at 2.3" wide (padded so nothing is clipped), "Medication Adherence Summary", payer, report date, printed date, maroon rule.
- Sections: Demographics (DOB, phone bold, age, payer | practice, provider, language, member ID), Medication (per gap: overdue + PDC flags, med, refill due bold, initial fill, latest dispense, day supply + eligible, missed days YTD, prescriber, last impactable, mail order), Pharmacy, Recommendations (6 standard bullets), Notes (report Outreach + latest 2 call notes, optional), Provider response box (optional), footer with Quality Specialist and practice.
- File name: `Practice_Patient Name_MM-DD-YYYY` (commas and illegal characters removed). Batch: `Practice_N Patients_MM-DD-YYYY` or `Multiple Practices_…`.

**Saving**
- Every change is kept in browser storage (localStorage key `adh_workbench_v1`) on that computer.
- Save call log → downloads `Adherence_CallLog_YYYY-MM-DD.xlsx` with sheets "Call Log" and "Patient Tags".
- Autosave (Edge/Chrome): connects to an .xlsx in OneDrive/SharePoint and rewrites it ~0.7s after each change. File link stored in IndexedDB; needs one "Reconnect" click per browser session. Fails (orange button) if the file is open in Excel.
- Load call log merges by Entry ID, so loading twice never duplicates.

## v1.4 additions

- **Resizable columns** (Worklist incl. Patient column, Call log): drag a header's right edge; double-click to reset. Saved per browser (`settings.colw`). Columns → Reset to default also clears widths.
- **Multi-select filters**: every dropdown filter is a checkbox list with row counts, search (lists over 7), Select all, Clear. Rows match if their value is any checked value; nothing checked = all.
- **Developer page** is under Settings → Developer tools (no tab). Includes the practice contacts file spec.
- **Call log default order**: Patient, Date of Birth, Date / Time, Outcome, Notes, then Phone, Payer, Practice, Measure, Medication, Contact, Barrier, Follow-up, Attempt #, Member ID, Provider, Documented By.
- **Provider PDF consistent text size**: Chrome shrinks the entire printed page (1.33×–2×) whenever any content is wider than the page. All PDF grids use minmax(0,1fr), values wrap anywhere, no nowrap on values, page content clipped to page width. Very long content flows to a second page at the same size.
- **Team review** opens the file picker only from Choose files / Add files.
- **Global `[hidden]{display:none!important}`** (fixed empty team bar showing under the toggle).
- **Email practice** (patient page and worklist toolbar): mailto draft. To = Office Manager Email (multiple split on ; or ,), greeting "Hi <QS Point of Contact>," (or "Hi,"), subject/body from Settings → Practice email with placeholders {practice} {patients} {count} {my_name} {date}. Contacts file columns: DBA Name (required), Office Manager Email (required), QS Point of Contact, Account Owner, Office Manager / Office Manager Name. Matched on normalized DBA Name; stored in browser (`store.contacts`). One practice with email → draft opens directly; multiple practices or missing email → list with one draft button per practice. Attachments must be added by hand (mailto can't attach).
- **Multi-practice PDF warning**: if selected/filtered patients span more than one DBA: Cancel / One combined PDF anyway / Separate PDF per practice (one print dialog per practice, each named Practice_N Patients_date).

## v1.5.14 changes

- **Document activity** (formerly Document a call) has a 2×2 type picker (`ACT_TYPES`: call, text, provider, note). `docFormHTML()` renders each type's fields, and switching type keeps the chosen gap and the typed notes.
  - **Phone call**: as before, minus the "Text message sent" outcome.
  - **Text message**: Copy text and an auto follow-up; outcome "Text message sent".
  - **Provider response**: Received via (`RECEIVED_VIA`), Provider (prefilled from Contact Name), checkboxes (`PROVIDER_RESP`, the same choices as the PDF response box) and the provider's notes. Outcome is "Provider response: …", contact "Provider office". It needs at least one box checked or a note.
  - **Note**: internal; outcome "Note", contact "Internal".
- Entries store `type` and `via`. `actType()` infers the type for older entries (Text message sent → text, "Provider response…" → provider, "Note" → note, everything else → call).
- **Attempts** count only outreach (`isOutreach`: call + text). This covers `_n` attempt numbers, the Attempts column, Last Call, Not contacted and the patient strip, which also shows "N other entries". Provider responses and notes are excluded.
- **History** shows a type label and icon on each entry. Provider responses get a green left bar and tint, showing the marked items and provider name. Notes get an amber left bar.
- **Call log**: the Type column has four values with colored pills, plus a new Type filter (`#cfType`). The team summary adds a Provider responses column, and Pharmacy / provider now counts phone calls only. The call log Excel file adds "Activity Type" and "Received Via" columns, which are read back on import and in team review.
- **Fixes**:
  - Team staff pills in the patient history stretched on entries that had a copy-notes button, because the flex row defaulted to stretch. The row is now `align-items:center` and the pill keeps a fixed line height.
  - The Copy text and Copy phone buttons share an inline-flex group, each 24 px tall.

## v1.5.13 changes

(A different v1.5.13, an Excel gap-list export, was built and then withdrawn. It isn't part of this line.)

- **Customize window** (`#mCustom`, opened by the sliders icon next to the gear, or Settings → Customize → Open Customize). It has three tabs; the last-used tab is remembered in `settings.custTab`:
  - **Practice email**: contacts plus the subject/body template and a preview.
  - **Text message**: callback number, template, reset, preview.
  - **Provider PDF**: "Include my latest call notes" and "Include a provider response box".
  - Element IDs are unchanged, so the existing handlers apply.
- **Main screen trimmed**: Load report and Load call log are gone from the top bar, and Export view is gone from the Worklist bar. They now live in Settings → Data, along with Load last report and a summary of the loaded report. Export view is disabled until a report is loaded. Choosing a load closes Settings. The empty-state "Choose report" / "Load last report" buttons stay. The Call log's own Export view, used by Team review, stays in place.
- **Settings layout**: an outlined card (`.ssec`) for each section, each with an icon tile and a divider under its heading, on a gray modal background (`.sbox`). Sections: Appearance, You and your workflow, Data, Where your call log is saved, Customize, Developer tools, What's new.

## v1.5.12 changes

- **Quality Specialist filter lock**:
  - The `LOCKABLE` set (only `#fQS`) gets a **Lock filter** switch at the top of its dropdown, saved as `settings.qsLock`.
  - While locked, worklist **Clear** skips that dropdown and keeps a right-click column filter on Quality Specialist; it then shows the toast "Specialist filter kept (locked)".
  - The dropdown's own Clear link still clears it.
  - A lock icon shows in the filter button whenever the lock is on, selected or not.
- **Team summary**:
  - A **Hide/Show** toggle (`settings.teamSumMin`, remembered) collapses it to a one-line total: staff, phone calls, texts, patients, reach rate.
  - Expanded, the table scrolls within 30% of the screen height.
  - "Calls" is now **Phone calls** (everything except Text message sent), and there's a new **Texts** column. Both are in the Team Summary sheet of the export.
- **Call log Type column** (Call / Text pill with icon), shown after Date / Time by default. Schema 5 inserts it before Outcome for existing column setups.
- **Team history in the Worklist**:
  - Team review → **Show in Worklist** sets `team.inWL`, and `rebuildIdx()` then indexes `team.calls` + `store.calls` (deduped by id). Attempts, Last Call, Next Follow-up, the Not contacted / Follow-up due chips and patient call histories all include team entries.
  - A banner on the Worklist names the staff and offers **Hide team history**.
  - Team entries in the patient history show the staff name instead of edit/delete buttons.
  - Nothing is written to `store` or the autosave file. It's in memory only, so it clears on reload, on close, or with Team review → Clear.

## v1.5.11 changes

- **Text message reminders**:
  - A **Copy text** button sits next to the phone number on the patient chart. It copies `buildSms()` output to the clipboard, and the toast offers **Log as sent**, which logs the Text sent quick log.
  - The template lives in `settings.sms` = {body, callback}, with `SMS_DEFAULT` as the default. Placeholders: {first_name} {my_name} {practice} {provider} {pharmacy} {callback} {date}.
  - `firstName()` takes the part after the comma in "Last, First M", title-cased when the name is all caps.
  - The default message contains no medication, condition, DOB or member ID, because SMS isn't secure.
- **Outcome** "Text message sent" (between Wrong / disconnected number and Pharmacy – confirmed fill). New QUICK entry "Text sent" (contact Patient, auto follow-up on); short label "Text sent" in Last Call. It isn't counted as Not reached.
- **Settings → Text message reminder**: callback number, message textarea, placeholder help with a PHI caution, Reset to default, and a live preview with character and segment count. Warnings appear if {callback} or {my_name} would be blank.
- The `toast(msg, action, label)` button label is now configurable (default "Undo").

## v1.5.10 changes

- **PDF single-medication layout**: when exactly one medication needs attention, its detail rows go in a two-column grid (`.mdcols`, grid-auto-flow: column, rows = ceil(n/2)), so they read down the left column and then the right. The columns line up with the Demographics columns and help keep the page to one sheet. With 2+ medications needing attention, the existing side-by-side `.meds2` layout is unchanged.

## v1.5.9 changes

- **Appearance dial removed** (it left some elements dim after switching back to Light). Settings → Appearance is again the Light / Dark / Match system segmented control (`settings.theme`). Any saved dial value migrates on load: tone 5 → dark, Match system → system, anything else → light; `settings.tone`/`toneSys` and the `data-tone` attribute are cleared. The v1.5.7/v1.5.8 dial notes below are historical.

## v1.5.8 changes

- **PDF medication dividers**: the Medication section is split by labeled divider headings, each with a count. "Medications needing attention (N)" (red, warning icon, thin rule) sits above the Open/Failed blocks. "Compliant medications: no action needed (N)" (green, check icon) sits below a solid 1.5 pt green rule above the compliant table. Both use shapes and rules, so they read in grayscale.
- **Dial restyle**: flat and minimal. 3 px arc track and progress, 5 px stop dots (7 px when selected, brand ring), no gradient or drop shadow. The center circle is filled with the selected tone's panel color as a live preview, and a small brand-colored dot is the pointer.

## v1.5.7 changes

- **Appearance dial** (Settings): a rotary knob with 6 stops: Light (0), Soft (1), Dim (2), Dusk (3), Shade (4), Dark (5). Stops 1–4 set `data-tone` on `<html>` and override the neutral surface variables (--bg, --panel, --hdr, --field, --line, --line-2, --mute-bg, --track, --row-hover, --row-sel; --muted/--faint darken at 3–4; tinted "soft" colors become translucent). Stop 5 is the existing dark theme. Drag the knob, click a dot, or use the arrow keys / Home / End. "Match system" follows the OS light/dark setting (turning the dial switches it off). Saved as `settings.tone` (0–5) and `settings.toneSys`; older `settings.theme` values migrate (dark → 5, system → Match system). Colors cross-fade for 0.35 s when the tone changes.
- **Impactable fix**: the Impactable and Impactable ≤ 14 days quick filters only count gaps whose Measure Status is Open or Compliant AND that have a Last Impactable Date of today or later. Failed gaps and blank impactable dates are left out.
- **Provider PDF color with grayscale safety**: ACTION NEEDED tag and 2.5 pt left bar in red (#b3141c, prints as dark gray); FAILED tag gray with a dashed outline and a dashed gray left bar; Compliant check and heading in green. The shapes (triangle, circled X, dashed vs solid, check) carry the meaning when printed in black and white. Tag tints use print-color-adjust: exact.

## v1.5.6 changes

- **Clicked gap first**: worklist rows carry data-gid; opening a patient from a row (or Prev/Next, or a call log row with a gap) sorts that gap first, outlines it, and preselects it in the call form when the patient has 2+ gaps.
- **Column menu**: "Clear sort" (shown when not on the default sort) returns to Days Overdue ↓ (worklist) or Date / Time ↓ (call log). Sort labels in Title Case.
- **Provider PDF**:
  - Header counts by Measure Status: "N open · N failed · N compliant".
  - Non-compliant meds (Open first, then Failed/other) keep full detail, each with a black outlined tag and icon (warning triangle "ACTION NEEDED"; circled X with dashed border "FAILED") and a 2.5 pt black left rule. These read in black-and-white printing.
  - Compliant meds collapse into a small table under "✓ Compliant — no action needed": Quality Measure, Medication, Refill Due Date.
- **Outcome** added: "Provider office – misc. notes".
- **Tag library**: presets + every custom tag ever added (`settings.customTags`) + any tag in use are offered on every patient. Unapplied custom tags show × to remove them from the list; a tag still on other patients stays until removed from them.

## v1.5.5 changes

- **Column header menu** (right-click any header in Worklist or Call log, except Quick log): Sort ascending/descending with labels by type (dates: Oldest to newest / Newest to oldest; numbers: Smallest to largest / Largest to smallest; text: A to Z / Z to A) and a check on the active sort; Filter values (checkbox list of the column's displayed values with faceted counts, search over 7 values, Select all / Clear, present values first then zero-count, max 500 shown, blanks as "(Blank)"); Hide column. Filtered headers show a funnel. Column filters are faceted with all other filters, saved with the view (`colf`), and cleared by Clear. Date-type detection is by column name (date, time, follow-up, last call, refill due, last edited).
- **Quick filters**: Mail order allowed removed; "Impactable ≤ 14 days" (last impactable date 0–14 days out) added right after Impactable.
- **Recommendations** (one shared list for chart and PDF, one line each): Claims can lag: an overdue refill may already be picked up. · Ask about barriers: cost, transportation, side effects, surplus. · Confirm the pharmacy; offer mail order when allowed. · Convert to a 90- or 100-day supply when eligible. · If stopped or changed, document why and notify the prescriber. · If picked up, confirm it wasn't paid in cash or with a discount card (e.g., GoodRx).

## v1.5.4 changes

- **Saved view state** (`settings.saved` in localStorage, written ~250 ms after each change without triggering autosave): Worklist search, dropdown selections, quick filters, sort; Call log search, date range (+ custom dates), dropdown selections, quick filters, sort; last tab (Worklist/Patient/Call log; restores to Call log, or Worklist since no patient is open on reload).
- Restored at startup; dropdown values not present in the newly loaded report are dropped by the normal filter refresh. Removed quick-filter ids are ignored. A one-time toast after the first report load says filters were restored. Clear resets and the empty state is saved.
- Never saved: checked patients, Team review mode/files.

## v1.5.3 changes

- Worklist select-all header checkbox reflects the page: checked when every patient on the page is selected, indeterminate (dash) when some are; clicking it when checked deselects the page.
- Settings button is a gear icon (tooltip/aria-label "Settings").
- Multi-select dropdowns order values: those with a count under the current filters first (A–Z), a divider, then zero-count values (A–Z, dimmed).

## v1.5.1 changes

- **Priority groups** (first quick filters, colored dots). Measure state comes from the report's Measure Status exactly (case/spacing ignored): "Open" or "Compliant". Any other status (e.g. "Failed") is excluded from all four groups. PDC (< 80% open) is used only when the status is blank. (v1.5.2) Overdue = refill due date before today; Upcoming = due today or later.
  - Critical = Open + Overdue · Slipped = Compliant + Overdue · Urgent = Open + Upcoming · Stable = Compliant + Upcoming.
  - The four are one filter (OR): checking several shows any of them. Rows with no refill due date fall in none.
- **Impactable** quick filter: hides rows whose Last Impactable Date has passed (rows without a date stay).
- Removed quick filters: Overdue 15+ days, PDC < 80%, Impactable ≤ 14 days. Order now: Critical, Slipped, Urgent, Stable | Impactable, Overdue, Multiple open meds, Mail order allowed, 30-day supply, Not contacted, Follow-up due.
- Hover text (definition) on every worklist and call log quick filter.
- Status dropdown label fixed ("Status: …", was "Statuse: …"): filter short names use an explicit singular map instead of trimming a trailing "s".
- Demo data uses Open/Compliant like the real report.

## v1.5 additions

- **Live (faceted) counts**: quick-filter and dropdown counts reflect all *other* active filters (search, dropdowns, chips; in the call log also the date range). One pass marks rows failing 0 or exactly 1 filter, so each filter's counts exclude only itself. Dropdowns still list every value; zero-count values and chips are dimmed. Counts are gap rows (worklist) or entries (call log).
- **Auto-deselect**: after any filter/search change, selected patients not in the filtered list are deselected, with a toast saying how many.
- **[SECURE]**: default subject is "Medication adherence follow-up – {practice} [SECURE]". One-time migration appends " [SECURE]" to an existing subject that lacks it (won't re-add if you remove it later).
- **Load last report** (Edge/Chrome): Choose report / drag-drop store a *file handle* (a link, not the data) in IndexedDB (`reportHandle`) plus name/time in settings (`lastReport`). The start screen shows "Load last report: <name>"; it asks read permission once per session and opens the file's current contents. If the file was moved or renamed, it says so. Patient data itself is never stored in the browser.

## Data rules

- **Patient key:** `id:` + Insurance Card ID (uppercase). If blank: `nd:` + name (letters/numbers only, lowercase) + `|` + DOB (YYYY-MM-DD). Links calls and tags to patients across report refreshes.
- **PDC:** accepts 0.78, 78, or "78%". Shown as percent. Colors: red <80, amber 80–85, green ≥85.
- **Dates:** accepts Excel dates, Excel serial numbers, MM/DD/YYYY, YYYY-MM-DD.
- **Days Overdue** = today − Refill Due Date. **Impactable In** = Last Impactable Date − today.
- **Impactable quick filters**: Measure Status Open or Compliant, and Impactable In ≥ 0 (≤ 14 for the 14-day chip). Failed/other statuses and blank dates are excluded.
- **Phone:** 10 digits shown as (xxx) xxx-xxxx.

## Call log Excel columns

Entry ID · Date · Time · Timestamp · Full Name · Member ID · Date of Birth · Phone · Payer · Practice · Provider · Gap ID · Measure Name · Medication · Contact · Outcome · Barrier · Follow-up Date · Notes · Documented By · Last Edited · Last Edited Timestamp · Patient Key

- **Timestamp** = milliseconds since 1/1/1970 UTC. Excel: `=A2/86400000+DATE(1970,1,1)-4/24` (EDT; use 5/24 for EST).
- **Entry ID** = timestamp in base-36 + 5 random characters. Used for de-duplication.

## Nexus RX columns expected

Report Date, Report Name, Quality Specialist, DBA Name, Contact Name, Outreach, Full Name, Date of Birth, Age, Gender, Language, Phone Number, Payer, Measure Name, Measure Status, Multiple Open Meds, PDC, Last Impactable Date, Initial Fill Date, Latest Dispense Date, Refill Due Date, Medication Details, Current Day Supply, Missed Days YTD, Eligible Day Supply, Mail Order Allowed, Pharmacy Name, Pharmacy Phone, Pharmacy Preferred Network, Pharmacy Address, Prescribing Provider Name, Prescribing Provider NPI, Prescribing Provider ID, Prescribing Provider Phone, PCP Name, Insurance Card ID, Product, TIN Name, Gap ID

## Design

Inter font, base 14.5px. Brand maroon `#8a1c44`. Neutral zinc grays. 12px card radius, subtle shadows, segmented tabs, pill chips.

## Developer tab

- Expected columns for the Nexus RX report with Required / Recommended / Optional, format, and what each is used for. Required: Full Name, Measure Name, Refill Due Date, Insurance Card ID.
- File checker: reads only the header row of a chosen file and reports matched, missing and extra columns, and whether it will load.
- Call log file format; planned reports.

## Version history

- **1.5.14** — Document activity (call / text / provider response / note); provider responses not counted as attempts; fixes for team pills and Copy text alignment.
- **1.5.13** — Customize window for templates and PDF options; Load/Export moved into Settings → Data; outlined Settings sections.
- **1.5.12** — QS filter lock; minimizable team summary with Phone calls vs Texts; Call/Text Type column; temporary team history in the Worklist.
- **1.5.11** — Text message reminders: Copy text, Log as sent, Text message sent outcome/quick log, customizable template in Settings.
- **1.5.10** — Single medication needing attention: details split into two columns on the PDF.
- **1.5.9** — Appearance dial removed; back to Light / Dark / Match system.
- **1.5.8** — Flat, minimal Appearance dial; labeled dividers between action-needed and compliant medications on the PDF.
- **1.5.7** — Appearance dial (Light → Soft → Dim → Dusk → Shade → Dark); Impactable filters exclude Failed and blank dates; PDF action markers in color, still grayscale-safe.
- **1.5.6** — Clicked gap first; Clear sort; Title Case sort labels; PDF status counts, compact compliant meds, print-safe action tags; misc. notes outcome; reusable custom tags.
- **1.5.5** — Right-click column menu (sort + value filters + hide); Impactable ≤ 14 days replaces Mail order allowed; shorter recommendations.
- **1.5.4** — Filters, quick filters, search, sorts and last tab remembered across reloads.
- **1.5.3** — Select-all checkbox state + deselect; gear icon for Settings; dropdowns list present values first.
- **1.5.2** — Groups follow Measure Status exactly; Failed and other statuses excluded from all four groups.
- **1.5.1** — Priority-group quick filters (Critical/Slipped/Urgent/Stable), Impactable filter, removed three filters, hover definitions, Status label fix.
- **1.5** — Live faceted filter counts; auto-deselect filtered-out patients; [SECURE] default subject tag; Load last report.
- **1.4** — Resizable columns; multi-select filters; Developer moved to Settings; call log order Patient/DOB/Date-Time/Outcome/Notes; consistent PDF text size; team picker fix; hidden-bar fix; Email practice with contacts file and templates; multi-practice PDF warning with per-practice split.
- **1.3** — Team review mode with per-staff weekly summary and two-sheet export.
- **1.2.1** — App icon in the browser tab; .ico for desktop shortcuts.
- **1.2** — Dark mode; icons; editable call entries with "Last Edited" stamp; copy-notes buttons; call log default order Date/Time, Patient, DOB, Outcome, Notes…; Developer tab with column specs and file checker; PDF logo no longer clipped, 2.3".

- **1.1.1** — PDF logo rebuilt without masks (removes thin dark edge line), set to 2.5" wide; file size halved.
- **1.1** — Inter everywhere, larger text, modern styling; call log columns customizable/sortable/filterable with quick filters and export; worklist column reordering; one-touch call logging with Undo and auto follow-up; big bold click-to-dial phone after DOB; logo PDF header; PDF naming Practice_Patient_Date; autosave to Excel file.
- **1.0** — Worklist, patient chart, call log, Excel save/load, provider PDF modeled on the Word mail-merge template, demo data.

## Ideas discussed, not built yet

- Email with the PDF already attached (.eml for classic Outlook, or Power Automate). v1.4 opens a prefilled draft; attach by hand.
- Add the quality gap reports and HCC data as more sections in the patient chart.
- Replace Timestamp with a real Excel date-time; move Entry ID / Patient Key to the end or a hidden sheet.
- Team review covers weekly visibility. For real-time shared logging: Power Apps on SharePoint lists, not a desktop app.

## Build paths

`build.py` reads: `src.html`, `lib/package/dist/xlsx.full.min.js`, `lib/inter/files/inter-latin-wght-normal.woff2`, `assets/logo_clean.svg`, and writes `Adherence_Workbench.html`. In this kit the font and library sit directly in `lib/`; the kit's build.py already uses those paths.
