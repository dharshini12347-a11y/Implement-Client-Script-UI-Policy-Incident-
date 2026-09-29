# Client Scripts — Incident

## onChange: Auto set urgency for high impact
Table: Incident | Type: onChange | Field: Impact | Active: true

```javascript
function onChange(control, oldValue, newValue, isLoading) {
  if (isLoading || newValue == '') {
    return;
  }

  if (newValue == '1') {
    g_form.setValue('urgency', '1');
    g_form.addInfoMessage('Urgency set to High for High impact incident.');
  }
}
```

## onSubmit: Prevent save if Assigned To missing
Table: Incident | Type: onSubmit | Active: true

```javascript
function onSubmit() {
  if (g_form.getValue('impact') == '1' &&
      g_form.getValue('assigned_to') == '') {
    g_form.showErrorBox(
      'assigned_to',
      'Assigned To is mandatory for High impact incidents.'
    );
    return false;
  }

  return true;
}
```

## onCellEdit: Prevent state change via list edit
Table: Incident | Type: onCellEdit | Field: State | Active: true

```javascript
function onCellEdit(sysIDs, table, oldValues, newValue, callback) {
  alert('State cannot be updated using list editing. Please open the Incident.');
  callback(false);
}
```
