# Data Dictionary

| Field | Meaning | Layer |
|---|---|---|
| job_id | Source job identifier | Raw/Fact |
| job_title | Job title | Raw/Dimension |
| company | Hiring company | Raw/Dimension |
| location | Job location | Raw/Dimension |
| experience | Required experience | Raw/Fact |
| salary_min/max | Salary range | Raw/Fact |
| salary_avg | Derived average salary | Silver/Gold/Fact |
| posted_date | Posting date | Raw/Date dimension |
| skills | Job skills | Raw |
| source | Source system | Raw/Fact |
