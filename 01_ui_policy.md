# UI Policy — High Impact Control

Table: Incident
Active: true

Condition:
- Field: Impact
- Operator: is
- Value: 1 - High

UI Policy Action — Assignment group:
- Mandatory: true
- Reverse if false: true

UI Policy Action — Urgency:
- Read-only: true
- Visible: Leave as is
- Reverse if false: true
