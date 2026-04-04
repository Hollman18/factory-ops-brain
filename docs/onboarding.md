# Onboarding

## Mandatory onboarding rule
When a factory user requests data for the first time:
1. Check whether a profile exists for that sender/channel.
2. If no profile exists, ask for:
   - name
   - role in the organization
3. Do not answer the factory data request yet, except to explain that these details are required first.
4. Save the profile.
5. Confirm that the user was saved and can continue asking.

## Profile behavior
- Save literal role in `role`.
- Save mapped internal category in `role_class`.
- Keep preferences separate from role.
- Update the profile if the user changes role or preferences later.
