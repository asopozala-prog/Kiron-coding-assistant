# Alex's Prompts to the Coding Assistant

## Prompt 1
read messy_case_data.txt, find the case ID or reference number from the court letter. Fill it into the Case ID field in case_file_template.txt

## Prompt 2
"Look through all the emails and documents. Who is our actual client? Fill in **Client Name** in the template. Then find their contact email or phone number and put it in **Client Contact**."

## Prompt 3
"Find the opposing party's name in the emails and letters. Put it in **Opposing Party**. Then find their contact information and add it to **Opposing Party Contact**."

## Prompt 4
"What is this case about? Read the court letter and the first email from opposing counsel. Write a brief summary for **Matter Description** in the template."

## Prompt 5
"What is the main legal issue or dispute? From the emails, identify what Markus Richter is claiming versus what Schmidt GmbH says. Put this in **Key Issue**."

## Prompt 6
"When was the original contract signed? Find the date and put it in **Contract/Agreement Date**. Also note the contract amount in **Amount in Dispute**."

## Prompt 7
"Create a timeline from the messy data. Find all important dates (contract signing, invoice dates, payment dates, court filing, emails) and fill in the **Timeline** table with dates and events."

## Prompt 8
"From the document summary at the end of the messy data, list all documents we have on file. Check the boxes in the **Documents on File** section for what we actually have."

## Prompt 9
"What is the current status of this case? Check the most recent email and the court letter. Is it filed? Waiting for response? Put the status in **Current Status** and suggest what the next action should be."

## Prompt 10
"Who is the supervising attorney handling this case? If you find it in my notes or emails, fill in **Responsible Attorney**. If not, mark it as 'TBD - awaiting supervisor assignment'. Add today's date to **Last Updated**."

# Alex's Prompts to Fill in the Contract (From Case File Template)

## Prompt 1
"Using the information from the filled case file template, find the Client Name and Opposing Party name. Use Client Name as the Service Provider in the contract, and use Opposing Party as the Client. Fill in [CLIENT NAME] and [OPPOSING PARTY] in the contract header."

## Prompt 2
"From the case file template, locate the Amount in Dispute field and the Contract/Agreement Date field. Use these to fill in [AMOUNT IN DISPUTE] and [CONTRACT/AGREEMENT DATE] in the contract template."

## Prompt 3
"Look at the Timeline table in the case file template. Find the service start date and service completion date. Use these dates to replace [DATE FROM TIMELINE] in the Timeline section of the contract to show when services actually began and ended."
