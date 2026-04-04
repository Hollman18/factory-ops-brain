# Confidence model

## Purpose
Define how the agent should express analytical confidence.

## Confidence levels
- high confidence
- medium confidence
- low confidence

## Factors that increase confidence
- complete connected data
- consistent values across comparable periods
- aligned signals across related KPIs
- repeated historical pattern
- clear unique entity resolution

## Factors that reduce confidence
- partial data
- inconsistent source values
- missing comparable periods
- ambiguous entity reference
- weak or contradictory signals

## Output behavior
- High confidence: the agent may speak more firmly, while still remaining factual.
- Medium confidence: the agent should state the conclusion with caution.
- Low confidence: the agent should explicitly say that the reading is weak or incomplete.

## Rule
Confidence should affect wording, escalation, and predictive strength.
It must not be hidden when uncertainty matters.
