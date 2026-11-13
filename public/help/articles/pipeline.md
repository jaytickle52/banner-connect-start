# The enrollment pipeline (Opportunities)

Menu: CRM > Opportunities
Use when: The enrollment pipeline: where every family sits, moving a family to a stage (Visit Scheduled, Accepted, Enrolled), status (Won, Lost), stalled families, bulk updates, deleting and restoring a family, why stages shouldn't be renamed.
Page for people: https://demo.banner61.com/help/articles/pipeline/
Last reviewed: 2026-11-13
Related: https://demo.banner61.com/help/articles/contacts.md, https://demo.banner61.com/help/articles/smart-lists.md, https://demo.banner61.com/help/articles/automations.md, https://demo.banner61.com/help/articles/reporting-and-payments.md, https://demo.banner61.com/help/articles/bulk-actions.md, https://demo.banner61.com/help/articles/engagement-score.md, https://demo.banner61.com/help/articles/enrollment-stages.md, https://demo.banner61.com/help/articles/enrollment-forecast.md

Go to **CRM**, then **Opportunities**. Each card is one family. Each column is a stage. Families move left to right as they get closer to enrolling.

## Your pipelines

Every account starts with these pipelines. Switch between them with the pipeline dropdown at the top left.

**Inquiry to Enrollment** (the main one):
1. New Inquiry: the family submitted a form or registered for an event.
2. Visit Scheduled: they booked a campus visit.
3. Visit Attended: they came to the visit.
4. Application Sent
5. Application Submitted
6. Accepted
7. Enrolled

**Re-Enrollment Pipeline**: Re-enrollment Offered, Intent Form Submitted, Contract Sent, Contract Signed, Tuition Paid, Re-enrolled.

**Sibling Enrollment Fast Track**: Sibling Intent Request, Application Sent, Application Submitted, Sibling Accepted, Sibling Enrolled.

Many moves happen on their own. A form submission creates a card in New Inquiry. Booking on the Schedule a Visit calendar moves the family to Visit Scheduled. Marking the visit as attended (from the follow-up email your staff receive) moves them to Visit Attended. The later stages you move by hand. For what each stage means and when to move a family, see [Your enrollment board, stage by stage](https://demo.banner61.com/help/articles/enrollment-stages/).

## What's on an opportunity

- **Contact**: the family it belongs to. Click the name to open the full contact record.
- **Pipeline and Stage**: where they are.
- **Status**: Open, Won, Lost or Abandoned (see [Status: Open, Won, Lost, Abandoned](https://demo.banner61.com/help/articles/pipeline/#status-open-won-lost-abandoned)).
- **Owner**: the staff member responsible for moving the family forward.
- **Followers**: up to 10 other staff who can see and edit the opportunity. Followers can't change the owner.
- **Value**: optional. Many schools leave it at $0; some use it for annual tuition.

The opportunity window also has **Notes**, **Tasks** and **Book/Update Appointment** in its left sidebar. Notes added here also show on the contact record. Notes are internal; families never see them.

## Add a family to the pipeline by hand

Any of these work:
- In **Opportunities**, click **+ Add Opportunity**, pick or create the contact, choose the pipeline and stage, and click **Create**.
- On a contact record, open the **Associations** icon (three connected dots) in the right panel, go to Opportunities and click **+ Add**.
- In **Conversations**, open the family's thread, click **Associations** on the right and add an opportunity.

## Move a family forward

Drag the card to the next column, or open the opportunity and change **Stage**. Move families as soon as something actually happens (for example, move to Visit Scheduled only after the visit is on the calendar) so the board always shows who's waiting on you.

## Status: Open, Won, Lost, Abandoned

- **Open**: still deciding. This is the default.
- **Won**: the family enrolled.
- **Lost**: they chose another school, weren't a fit, said they're not interested, or stopped responding after several tries.
- **Abandoned**: the opportunity went nowhere.

Marking a family Lost keeps their history and keeps your reports accurate. Use Lost instead of deleting when a family decides not to enroll.

The pipeline shows only Open opportunities by default. If you can't find a family, check the Status filter.

## Stalled families

When a family sits in the same stage of the Inquiry to Enrollment pipeline for more than a week, Banner Connect tags them as stalled automatically. The tag comes off on its own when they move to the next stage. Use it as a prompt to follow up, move them forward or mark them Lost.

## Find a family

Type at least 3 letters into the search bar at the top of Opportunities. It matches the opportunity name, contact name, email, phone and tags, from the start of a word ("Thom" finds Thompson; "pson" doesn't). To search every pipeline at once, switch to list view and choose **All Pipelines**.

## Filters and views

- Click **Advanced filters** (the funnel icon) above the board to filter by stage, owner, status, tags, value or custom fields. Combine with AND or OR.
- Switch between the board and list view with the icons at the top right. List view can be sorted by name, value, date created or stage.
- Choose which details show on each card with **Manage Fields** at the top right of the board (up to 8).

Handy filters: Stage = Visit Attended (visited but no application yet); Owner = a counselor; Created Date = last 7 days.

## Update many families at once

1. Check the cards (hover a card and click the box in its corner) or rows in list view.
2. Click **Edit** to change Stage, Pipeline, Status, Owner, Followers, Value, Source, Expected Close Date, Lost Reason or custom fields for all of them.

For example, after an open house, filter to the families who attended, select them and move them to the next stage in one step. Bulk changes run in the background; check progress on the **Bulk Actions** page under Opportunities.

You can also move a group from a contact list in **CRM**, then **Contacts**. See [Update the pipeline for a whole list of families](https://demo.banner61.com/help/articles/bulk-actions/#update-the-pipeline-for-a-whole-list-of-families).

## Delete and restore

Delete only duplicates, test entries and records that don't belong. Deleting an opportunity doesn't delete the contact.

- **One**: open it, click the trash icon at the bottom of the window and confirm.
- **Several**: check them, click **Delete** and type DELETE to confirm.
- **Restore**: from the Bulk Actions page (three-dot menu, Restore), or from **Settings**, then **Audit Logs** (filter Action = Deleted, Module = Opportunity, then Restore). Only admins can restore, within 60 days, and only if the contact still exists.

## Changing pipelines and stages

Go to **CRM**, then **Opportunities**, then **Pipeline**. You can rename stages, reorder them, add or delete stages, and choose which stages show in dashboard charts. When you delete a stage, you pick where its families move, so no one is lost.

Be careful: the prebuilt automations move families into specific stages by name (for example, Visit Scheduled). Renaming or deleting those stages, or deleting a whole pipeline, can break them. Deleting a pipeline also deletes every opportunity in it. Ask the Banner 61 team before changing the Inquiry to Enrollment pipeline.
