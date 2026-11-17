---
id: advanced-and-settings
title: "Advanced and settings"
menu: "Advanced; Settings"
use_when: "Swapping the PDF linked in an automatic email (new tuition sheet or info packet), custom values (school name, address, phone used in every email), custom fields (grade of interest and other details), merge fields for personalizing messages, Business Profile, Users and access for staff, Integrations and Audit Logs."
also_called: ["new tuition PDF", "update the info packet", "replace PDF", "change the link in the email", "media storage", "upload a file", "field", "grade", "grade of interest", "custom field", "school address", "school phone", "merge field", "personalize", "first name", "staff", "staff member", "employee", "assistant", "teacher", "user", "access", "permissions", "remove a user", "audit log", "who deleted"]
related: [forms-and-docs, tasks, conversations, tuition-page, marketing]
plan: ""  # SchoolBox, Full or All, once the feature map is filled in
reviewed: 2026-11-17
---
# Advanced and settings

Most of what's under Advanced is set once by Banner 61 and rarely touched.

## Custom values (your school's details)

Go to **Advanced**, then **Custom Values**. These hold your school's name, address, phone number and similar details. Every email and page uses them, so a change here updates everything at once. Check that your school name, address and phone number are right. Example: the visit calendar uses {{custom_values.school_full_address}} as the visit location.

## Custom fields (extra details you track)

Go to **Advanced**, then **Custom Fields**, and choose Contact or Opportunity at the top.

- **Contact fields** describe the family or student and stay with them: Student Name, Grade(s) of Interest, Current School, How did you hear about us? These can go on forms.
- **Opportunity fields** describe one enrollment: Application Status, Admissions Priority, Enrollment Year. These can't go on forms.

**Create a field:** search first to make sure it doesn't exist, click **Create field**, choose the type (dropdowns keep answers consistent), set the name and folder, and save. Each field gets a **Key**, which is how emails insert it, like {{contact.grade_level_applying_for}}.

Be careful:
- You can't change a field's type, or move it between Contact and Opportunity, after it's created.
- Changing a field's Key breaks any email or text that uses the old one.
- Deleting a field permanently deletes its data from every record. There's no undo. Export first if you might need it, or move the field to an "Archive" folder instead.
- Fields can be used in forms, workflows and Smart Lists. Check those before changing or deleting a field.

Not sure whether you need a new field? Ask the Banner 61 team; we're happy to create it.

## Merge fields (personalizing messages)

Merge fields fill in each family's details when a message sends. Insert them with the merge field picker in the email or text editor rather than typing them, because they're case-sensitive.

- Contact: {{contact.first_name}}, {{contact.last_name}}, {{contact.email}}, {{contact.phone}}
- Appointment (only in visit confirmations and reminders): {{appointment.start_time}}, {{calendar.name}}
- Your school: {{location.name}}, {{location.phone}}, {{location.email}}
- Custom fields: {{contact.<field key>}}. Find the key in Advanced, then Custom Fields.

Empty fields come through blank. In emails, add fallback text to a merge field (click it in the editor), such as "there" so "Hi there," replaces "Hi ,". In texts, only use fields your forms always collect, like first name.

## Other Advanced pages

- **Media Storage**: logos, photos and PDFs used in emails and forms. To swap a PDF that an automatic email links to, see [Swap the PDF linked in an automatic email](#swap-the-pdf-linked-in-an-automatic-email).
- **Domains** and **Brand Boards**: your web addresses and brand colors. Banner 61 manages these.
- **Object Settings**: how records like Students are set up. Banner 61 manages this.

## Swap the PDF linked in an automatic email

Upload the new PDF in **Advanced**, then **Media Storage**, copy its link, and paste that link into the email in **Marketing**, then **Emails**, then **Templates**. Most schools do this once a year, when tuition or the info packet changes.

1. Go to **Advanced**, then **Media Storage**, click **Upload** at the top right and choose your new PDF.
2. Hover over the new file, click its three-dot menu and choose **Get Link**. The link is copied.
3. Go to **Marketing**, then **Emails**, then the **Templates** tab, and open the folder for that email, for example **Request Tuition Info (sends on its own)** or **Request Info Packet / Lead Nurture (sends on its own)**. Click the email to open it.
4. Click the words that link to the old file, click the link icon in the toolbar, and paste the new link in place of the old one. Repeat for every link to the old file in that email.
5. Click **Save** at the top right.

How to check it worked: fill out the matching form on your website with your own email address. The email that arrives should open the new PDF.

Good to know:
- Families who asked before your change already have the old link. Only new requests get the new file.
- Keep the old file in **Media Storage** until you've checked the new link. Moving it to the trash breaks the link in emails families already have.
- Change only the link and wording. These emails send on their own from workflows, so check with the Banner 61 team before changing anything else. Banner 61 can also swap the file for you.
- Sending a link to a web page instead of a PDF saves this step every year. See [Should we send families a tuition page or a PDF?](/help/articles/tuition-page/#should-we-send-families-a-tuition-page-or-a-pdf).

## Settings

- **My Profile**: your name, email, phone and password, your email connection (two-way sync), your calendar connections, and your notifications (including task notifications).
- **Users**: the people on your team. See [Users and access](#users-and-access).
- **Business Profile**: your school's name, logo, address, phone and time zone.
- **Communications**: phone numbers (Phone System), email sending and WhatsApp. Banner 61 sets these up.
- **Integrations**: connect Facebook, Instagram and Google Business Profile.
- **Audit Logs**: a record of who changed or deleted what, and where admins restore deleted opportunities and tags within 60 days.

## Users and access

Go to **Settings**, then **Users**, to see everyone on your team.

- **Add a user**: add their name, email (used to sign in) and phone, and choose their role and permissions. They get an email to set their password. If you don't have access to add users, ask the Banner 61 team.
- **Change someone's access**: click the edit icon next to their name.
- **Remove someone who left**: delete their user so they can no longer sign in.

Give each person only the access they need, keep admin access to a few trusted people, and review your list each term. Every person who answers families should have their own user, so tasks and conversations can be assigned to them.

Some users only see the families assigned to them. Adding them as a follower on an opportunity lets them see that family too.
