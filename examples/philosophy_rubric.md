---
criteria:
  - name: "Introductory paragraph"
    points: 10
    description: "Does the introduction clearly state the topic and plan?"
  - name: "Extraction Validity"
    points: 10
    description: "Do the premises of the argument logically entail the conclusion?"
  - name: "Extraction Accuracy"
    points: 15
    description: "Does the extracted argument accurately reflect the source text?"
  - name: "Justifications Structure"
    points: 10
    description: "Is each premise individually justified (not the conclusion)?"
  - name: "Justifications Content"
    points: 15
    description: "Are the justifications on-track and well-reasoned?"
  - name: "Evaluation Structure"
    points: 10
    description: "Does the evaluation take the right form (assessing premise truth)?"
  - name: "Evaluation Content"
    points: 15
    description: "Is the evaluation accurate and well-supported?"
  - name: "Clarity"
    points: 10
  - name: "Grammar"
    points: 5
  - name: "Overall"
    points: 100
    description: "Sum of all the above"
---
Grade the following philosophy essay according to the rubric below.

For each criterion, provide a brief assessment and then a numerical score in
the exact format "X/Y" (e.g. "8/10").

## Rubric

- **Introductory paragraph**: /10
- **Extraction Validity**: /10 (do the premises logically entail the conclusion?)
- **Extraction Accuracy**: /15 (does the argument accurately reflect the source text?)
- **Justifications Structure**: /10 (each premise individually justified? only premises, not the conclusion?)
- **Justifications Content**: /15 (are the justifications on-track?)
- **Evaluation Structure**: /10 (does it evaluate whether the premises are true?)
- **Evaluation Content**: /15 (is the evaluation accurate?)
- **Clarity**: /10
- **Grammar**: /5
- **Overall**: /100 (sum of all the above)

After scoring, provide a short comment on ways to improve the paper.

{% if instructions %}
## Assignment Instructions

{{ instructions }}
{% endif %}

{% if reference_text %}
## Reference Text

{{ reference_text }}
{% endif %}

## Student Essay

{{ essay }}

Now grade the paper according to the rubric above.
