# Best Prompts for PrivacyAI Toolkit

## Privacy Cleaner - By Use Case

### Medical Records
```
Remove all personally identifiable information from this medical document.
Keep all medical terms, diagnoses, medications, and treatment details intact.
Replace names with [PATIENT], dates with [DATE] format, and locations with [LOCATION].
Preserve the medical structure and all clinical information.
```

### Legal Documents
```
Strip all identifying information from this legal document.
Replace names with [PARTY A] / [PARTY B] etc.
Mask addresses to city level only.
Keep all legal terms, case numbers (last 4 digits), and legal references.
```

### Customer Support Transcripts
```
Clean this support ticket transcript.
Remove customer name, email (replace with [CUSTOMER]), phone, address.
Keep the issue description and resolution intact.
Keep agent identifiers if they're company employees.
```

### Financial Reports
```
Remove all PII from this financial document.
Mask account numbers to last 4 digits.
Remove SSNs, but keep transaction amounts and dates.
Replace names with [ACCOUNT HOLDER].
```

### HR Documents
```
Strip employee PII from this HR document.
Use [EMPLOYEE], [MANAGER], [HR STAFF] as placeholders.
Keep job titles, departments, and dates of employment.
Remove salary specifics if not needed for the task.
```

---

## Summarizer - By Output Type

### Executive Summary
```
Provide a 2-3 sentence executive summary that captures:
1. What this document is about
2. The key decision or action needed
3. The most critical finding or recommendation

Write in plain business English, no jargon.
```

### Bullet Points
```
Summarize the key points as 5-7 bullet points.
Each bullet should be a complete thought.
Prioritize: problems/challenges > solutions > next steps.
Use consistent action verbs.
```

### Key Findings Only
```
List only the top 3 most important findings or takeaways.
For each, provide 1 sentence of context and 1 sentence of implication.
Format as: [Finding]: [Implication]
```

### TL;DR Version
```
Give me a Twitter-length (280 char) summary first.
Then provide a 2-paragraph detailed summary.
Finally, list 3 actionable takeaways.
```

### Meeting Notes
```
Extract and organize:
- Decisions made
- Action items (with responsible party if identifiable)
- Key discussion points
- Next steps

Format as meeting minutes.
```

---

## Email Generator - By Scenario

### Follow-up After Meeting
```
Tone: [professional/friendly]
Context: Following up after a [meeting/call/demo]
Include: specific reference to what was discussed
Mention: next steps or requested action
Length: 150-200 words
```

### Cold Outreach
```
Tone: [professional but warm]
Goal: Start a conversation, not close a sale
Hook: [specific reference to their work/company/pain point]
Value: Brief mention of how you can help
CTA: Single, low-commitment ask
Length: 150 words max
```

### Invoice/Payment Reminder
```
Tone: [professional, not aggressive]
Reference: Invoice #[NUMBER] dated [DATE]
Amount due: [AMOUNT]
Due date: [DATE]
Payment link: [URL or instructions]
Keep it to 100 words max.
```

### Apology/Service Recovery
```
Tone: Sincere, specific
Acknowledge: exactly what went wrong
Take responsibility: no excuses
Remedy: what you're doing to fix it
Compensation: if offering any
Reassure: what will be different going forward
Length: 100-150 words
```

---

## Privacy Checker - Best Practices

### Pre-Document Review
```
Analyze this document and identify ALL potential privacy risks.
For each risk, rate: critical / high / medium / low
Give specific line or section references where possible.
Recommend exact redaction or modification for each item.
```

### GDPR Compliance Check
```
Check this document for GDPR-relevant personal data:
- Direct identifiers (names, SSNs, emails, phone numbers)
- Indirect identifiers (IP addresses, device IDs, location data)
- Sensitive categories (health, financial, biometric, racial/ethnic origin)

Flag anything that requires explicit consent or legal basis.
```

### Research Data Anonymization
```
For this research dataset or publication:
1. Identify all potential re-identification risks
2. Flag quasi-identifiers (age + zip + gender combinations)
3. Recommend k-anonymity or differential privacy techniques
4. Suggest appropriate anonymization level for your field
```