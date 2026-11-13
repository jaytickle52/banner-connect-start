# Automations (workflows)

Menu: Automations > Workflows
Use when: What the prebuilt workflows do (after an inquiry, after a visit, open house follow-up, cold inquiry revival, stalled families), the staff follow-up email after a visit, what's safe to change, and why an email didn't send.
Page for people: https://demo.banner61.com/help/articles/automations/
Last reviewed: 2026-11-03
Related: https://demo.banner61.com/help/articles/smart-lists.md, https://demo.banner61.com/help/articles/marketing.md, https://demo.banner61.com/help/articles/calendars.md, https://demo.banner61.com/help/articles/pipeline.md

Go to **Automations**, then **Workflows**. Workflows are the follow-up that happens on its own. Banner 61 builds them for you. Before building anything new, look through what's already running.

## What's already built

| Workflow | Starts when | What it does |
|---|---|---|
| Request Info Packet / Lead Nurture | A family submits the Request Info Packet form | Adds them to New Inquiry and sends a short series of follow-up emails |
| Request Tuition Info | The Request Tuition Info form is submitted | Sends your tuition information email |
| Request Financial Aid Info | The Request Financial Aid Info form is submitted | Sends your financial aid email |
| General Inquiry (contact form) | The General Inquiry form is submitted | Adds the family to New Inquiry and follows up |
| Request a Visit | A family books on the Schedule a Visit calendar (online or by staff) | Confirmation, reminders, moves them to Visit Scheduled, then emails your staff after the visit |
| Event Registration | A family registers on the Event Registration calendar | Confirmation, 24-hour and 1-hour reminders, staff email after the event |
| Cold Inquiry Revival | Someone adds the Cold Inquiry Revival tag | A series of re-engagement emails for older inquiries |
| Stalled Leads / Remove Stalled Tag | A family sits in one stage for over a week | Tags them as stalled, and removes the tag when they move |

Which ones are turned on depends on the forms and calendars your school uses. Ask Banner 61 if you're not sure.

## After a visit: the staff follow-up email

After each scheduled visit, your staff get an email with three links. Click the one that fits:
- **They showed and are a good fit**: moves the family to Visit Attended and sends the Visit Feedback Survey.
- **They showed but aren't a good fit**: records it, no email to the family.
- **They didn't show**: sends an email encouraging them to reschedule.

The link opens Banner Connect so you can check the result. The Event Registration staff email works the same way for events.

## Win back quiet families

To restart conversations with older inquiries who never booked a visit, add the **Cold Inquiry Revival** tag to the family (from their contact record, or from the pipeline). The Cold Inquiry Revival emails then send on their own. Review those templates first in **Marketing**, then **Emails**, then **Templates**.

## How a workflow works

Every workflow has:
1. **A trigger**: what starts it, such as a form submitted, a visit booked, a tag added or a trigger link clicked.
2. **Filters** (optional): who it counts for, such as only the Request Info Packet form.
3. **Actions**: the steps, in order. Common ones are Wait, Send Email, Send Internal Notification (alert a staff member), Add Contact Tag, Add Task and Add to Workflow.

Each workflow also has a **Settings** tab with:
- **Allow Re-entry**: whether someone can go through it more than once.
- **Stop on Response**: removes a family from the workflow as soon as they reply to one of its emails or texts, so a person can take over.
- **Time window**: the hours messages are allowed to send.

**Save** keeps your changes. The **Draft/Publish** switch decides whether it runs; a workflow in Draft never sends anything.

## Before you change a workflow

Workflows send real emails to real families, and many of them depend on each other (for example, on exact stage names, tag names and templates). It's easy to send families duplicate or wrong emails by accident. Safe changes a school can make on its own:
- editing the wording of the email templates a workflow uses,
- changing the staff email address in a notification step (like Internal Staff Email in Event Registration).

For anything else, such as new workflows, new triggers, or turning a workflow on or off, ask the Banner 61 team. We'll build or change it with you.

## "Why didn't this send?"

Common reasons:
- The workflow is in **Draft**.
- The family doesn't match the trigger's filters (for example, they used a different form).
- They're set to Do Not Disturb or unsubscribed.
- **Stop on Response** removed them because they replied.
- They already went through it once and Allow Re-entry is off.

Each trigger has stats showing how many contacts were checked, matched and not matched in the last 30 days, with the reason for each one that didn't match. If you're stuck, send the family's name and the workflow name to the Banner 61 team.
