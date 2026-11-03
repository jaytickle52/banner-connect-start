# Advanced and settings

Menu: Advanced; Settings
Use when: Custom values (school name, address, phone used in every email), custom fields (grade of interest and other details), merge fields for personalizing messages, Business Profile, Users and access for staff, Integrations and Audit Logs.
Page for people: https://demo.banner61.com/help/articles/advanced-and-settings/
Last reviewed: 2026-11-03
Related: https://demo.banner61.com/help/articles/forms-and-docs.md, https://demo.banner61.com/help/articles/tasks.md, https://demo.banner61.com/help/articles/conversations.md

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

- **Media Storage**: logos and photos used in emails and forms.
- **Domains** and **Brand Boards**: your web addresses and brand colors. Banner 61 manages these.
- **Object Settings**: how records like Students are set up. Banner 61 manages this.

## Settings

- **My Profile**: your name, email, phone and password, your email connection (two-way sync), your calendar connections, and your notifications (including task notifications).
- **Users**: the people on your team. See [Users and access](#users-and-access) below.
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
