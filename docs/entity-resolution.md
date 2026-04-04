# Entity resolution

## Purpose
Define how the agent should interpret plant entities such as plants, areas, lines, machines, shifts, references, or any other hierarchy labels coming from connected factory data.

## Core rules
- Use the entity names and hierarchy provided by the connected data source as the source of truth.
- Do not invent hierarchy levels that do not exist in the source.
- If the user refers to an entity with a nickname, alias, short form, or ambiguous name, resolve it cautiously.

## Resolution behavior
1. If there is a clear unique match, use it.
2. If there are multiple plausible matches, ask a clarifying question.
3. If context strongly disambiguates the entity, explain the chosen interpretation when useful.
4. If confidence is low, do not assume silently.

## Examples
- “Quesos” may refer to an area, line group, or plant section depending on the source hierarchy.
- “Línea 1” may exist in more than one plant.
- “B200” may be a reference alias rather than a formal reference code.

## Goal
Prevent incorrect analysis caused by entity ambiguity while keeping the interaction smooth and practical.
