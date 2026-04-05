# Onboarding

## Mandatory onboarding rule
When a factory user requests data for the first time:
1. Check whether a profile exists for that sender/channel.
2. If no profile exists, ask for these required fields:
   - name
   - role in the organization
   - company
3. Recommend these additional fields when useful:
   - main plant/site
   - main area/process
   - preferred information style (summary, detail, comparisons, alerts, or periodic reports)
4. Do not answer the factory data request yet, except to explain that these details are required first.
5. Save the profile.
6. Confirm that the user was saved and can continue asking.
7. Provide a short usage hint according to the role.

## Profile behavior
- Save literal role in `role`.
- Save mapped internal category in `role_class`.
- Keep preferences separate from role.
- Update the profile if the user changes role or preferences later.

## Short role-based usage guidance examples
- Directivo/Gerente: ask for executive summaries, target risk, comparisons, major deviations, and recommendations.
- Supervisor: ask for line/shift performance, losses, deviations, causes, and actions.
- Operador: ask what is wrong, where to look, and what to check first.
- Mantenimiento: ask for failure risk, critical assets, recurrence, and intervention priority.
- Calidad: ask for rejection, deviations, critical references, and containment.
