---
id: bulk-actions
title: "Bulk actions (do one thing to many families)"
menu: "CRM > Contacts > Bulk Actions"
use_when: "Doing one thing to a whole group of families at once: tagging or untagging a list, moving a group to a new pipeline stage, starting an automation for a list, a quick email to a list, naming a bulk job and checking whether it finished."
also_called: ["bulk", "mass update", "all at once", "select all", "everyone on the list", "whole list", "group of families", "batch", "tag everyone", "move everyone", "bulk tag", "bulk stage", "mass tag", "bulk actions page", "did it finish"]
related: [contacts, marketing, pipeline, automations]
plan: ""  # SchoolBox, Full or All
reviewed: 2026-11-13
---
# Bulk actions (do one thing to many families)

A bulk action does one job to a whole group of families in one step, like tagging everyone from the fall fair. Start it from a list in **CRM**, then **Contacts**, and track it on **CRM**, then **Contacts**, then **Bulk Actions**.

## Select a whole list of families

To act on a group, open a list, check the families, then pick an action from the toolbar that appears.

1. Go to **CRM**, then **Contacts**, then **Smart Lists**, and click the list you want, such as **Current Families**.
2. Check the box next to each family, or check the box at the top of the name column to select everyone on the page.
3. If the list runs longer than one page, click the blue **Select all** button, which shows the full count.
4. Pick an action from the toolbar (**Export**, **Trigger automation**, **Send email**, **Add tags**, **Delete**) or from **More** (**Send SMS**, **Manage opportunities**, **Remove tags**, **Merge**, **Verify email addresses**). Schools can ignore **Send WhatsApp**, **Request reviews** and **Manage companies**.

Every bulk action asks for an **Action name**. Lead with what you did and who it was for, then the month, because only the first few words show in the log: "Tag fall fair families: attended event (Nov 2026)".

How to check it worked: the toolbar shows "Selected" with the number of families you meant to pick before you choose an action.

## Tag every family on a list

To tag a group, select the families in **CRM**, then **Contacts**, and click **Add tags**.

1. Go to **CRM**, then **Contacts**, then **Smart Lists**, open the list and select the families (check the top box, then **Select all** for a long list).
2. Click **Add tags** in the toolbar.
3. Type an **Action name**, such as "Tag open house families: attended event (Nov 2026)".
4. Under **Tags**, pick one or more tags that already exist.
5. Click **Add tags**.

Some tags start automations: adding **Cold Inquiry Revival** starts those emails for every family you tagged. Check with the Banner 61 team before adding a tag you don't recognize or creating a new one.

How to check it worked: go to **CRM**, then **Contacts**, then **Bulk Actions**. Your job shows by name with the status Complete, and the tag shows on each family's record.

## Remove a tag from a group of families

To take a tag off many families, select them in **CRM**, then **Contacts**, open **More** and choose **Remove tags**.

1. Go to **CRM**, then **Contacts**, then **Smart Lists**, open the list and select the families.
2. Open **More** and choose **Remove tags**.
3. Type an **Action name**.
4. Under **Tags**, pick the tag or tags to remove, then click **Remove tags**.

Leave the **Remove all tags** switch off. It strips every tag from every selected family, which can break automations and smart lists; check with the Banner 61 team first. Removing a tag doesn't undo emails an automation already sent.

How to check it worked: on **CRM**, then **Contacts**, then **Bulk Actions**, the job shows Complete, and the tag is gone from the families' records.

## Update the pipeline for a whole list of families

To update the pipeline for a whole group from a contact list, select them in **CRM**, then **Contacts**, open **More** and choose **Manage opportunities**.

1. Go to **CRM**, then **Contacts**, then **Smart Lists**, open a list that holds only the families to update, and select them.
2. Open **More** and choose **Manage opportunities**.
3. Type an **Action name**, such as "Update toured families: Application Sent (Nov 2026)".
4. Under **Select pipeline**, choose **Inquiry to Enrollment** (or the **Re-Enrollment Pipeline** or **Sibling Enrollment Fast Track** if that's the one you mean).
5. Under **Select stage**, pick the column they belong in now.
6. Click **Add/update opportunity**.

This action adds or updates: a family with a card in that pipeline is updated, and a family without one gets a new card. Run it only on a list you trust.

You can also do this from the pipeline board. See [Update many families at once](/help/articles/pipeline/#update-many-families-at-once).

How to check it worked: go to **CRM**, then **Opportunities**. The families show in their new column, and the total number of cards hasn't grown unless you meant to add families.

## Start an automation for a list of families

To put a group of families into a workflow by hand, select them in **CRM**, then **Contacts**, and click **Trigger automation**.

1. Go to **CRM**, then **Contacts**, then **Smart Lists**, open the list and select the families.
2. Click **Trigger automation**.
3. Type an **Action name**, such as "Start re-engagement: spring inquiries (Nov 2026)".
4. Under **Workflow**, choose the workflow.
5. Choose **Send all at once**, **Send at scheduled time**, or **Send in drip mode** (a few families at a time).
6. Click **Add to automation**.

Workflows send real emails and texts to every family you selected, and a workflow in Draft won't run. Check with the Banner 61 team before starting one for a big group.

How to check it worked: on **CRM**, then **Contacts**, then **Bulk Actions**, the job shows Complete. Open the workflow in **Automations**, then **Workflows** to see the families enrolled.

## Send a quick email to a list

For a newsletter, an invitation or anything you want to look polished and measure, use an email campaign instead: see [Email campaigns](/help/articles/marketing/#email-campaigns-one-time-emails-to-a-group). For a short, one-time note to a list, you can send straight from **CRM**, then **Contacts**.

1. Go to **CRM**, then **Contacts**, then **Smart Lists**, open the list and select the families.
2. Click **Send email**.
3. Check the **Confirm recipient list** window. It shows how many families you selected and how many were filtered out because the address is invalid or the family unsubscribed. Click **Confirm and proceed**.
4. Type an **Action name**, the From name and From email, a **Subject** and an optional **Pre-header**.
5. Write the message with **Quick compose**, or choose **Select existing template**.
6. Under **Mode**, send now, at a scheduled time, or in batches.
7. Under **Test emails**, send yourself a test.
8. Check the box confirming these families agreed to hear from you, then click **Send email**.

Each family gets their own copy. A sent email can't be called back. If you're not sure which sending address to use, check with the Banner 61 team first.

How to check it worked: on **CRM**, then **Contacts**, then **Bulk Actions**, your send shows Complete. Open a family's record to see the email in their conversation.

## Check whether a bulk action finished

Every bulk job is listed on **CRM**, then **Contacts**, then **Bulk Actions**, with its name, type, status, who ran it and when it started and finished.

1. Go to **CRM**, then **Contacts**, then **Bulk Actions**.
2. Use the filters at the top to narrow by date, status, type of action or the person who ran it.
3. Click the chart icon in the **Statistics** column to see every family the job touched and whether each one succeeded or failed.
4. The menu at the end of a row opens **View details**.

A large list can take a few minutes. Changes made from the pipeline board are tracked separately, under **CRM**, then **Opportunities**.

How to check it worked: the job's status reads Complete and the Statistics window shows no errors.
