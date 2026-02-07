# Security and Access Rights

Goal: prevent data exposure while keeping models flexible.

## 1) Security folder (trustless modeling)
- Put sensitive formulas in the **Security folder**.
- Restrict **Define Application Security** permission to trusted users.
- Prevent formula changes from revealing sensitive data.

## 2) Access Rights metrics and rules
- Use access rights rules to control user visibility.
- Test access rights metrics against real user roles.

## 3) ACCESSRIGHTS function usage
- Use `ACCESSRIGHTS()` when defining access rights values.
- Prefer **BLANK** over **FALSE** for performance in sparse access rights metrics.

## 4) Security review checklist
- Sensitive blocks in Security folder
- Access rights metrics validated
- Permissions restricted to trusted roles
- Performance impact checked

## Sources (Pigment KB)
```
https://kb.pigment.com/docs/security-folder-trustless-modeling
https://kb.pigment.com/docs/introduction-access-rights
https://kb.pigment.com/docs/create-access-rights-metric-rules
https://kb.pigment.com/docs/accessrights-function
https://kb.pigment.com/docs/about-dimension-replacement-access-rights-rules
https://kb.pigment.com/docs/add-remove-access-rights-inheritance
https://kb.pigment.com/docs/review-access-rights-with-impersonate
```
