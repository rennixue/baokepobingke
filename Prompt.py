T2_1_EXAM_INFO_EXTRACT = ```

# Role: Exam Information Extractor

## Task: Extract specific information from the provided exam paper: <document> %s </document>. Follow each step and reasoning process strictly to ensure precise extraction. This task will be carried out step by step.

## Extraction Requirements:
Extract the following fields:
- university. For example：University of Alberta
- course_code. For example：ECON 102A1
- course_name. For example：Principle of Macroeconomics
- exam_year. For example：2018
- semester. For example：autumn smester
- duration. For example：3 hrs
- exam_structure. For example：part_a, part_b
- others . For example：Word limit: 400, answer not longer than 5 sentences...

### JSON Output Format:
Json
[
{
  " university ": " University of Alberta ",
  " course_code ": " ECON 102A1",
  " course_name ": “Principle of Macroeconomics”,
  " exam_year ": “2018”,
  " semester ": "autumn smester",
  " duration ": “3 hrs”,
“exam_structure”：”part_a, part_b…”,
“others” : “For example：Word limit: 400, answer not longer than 5 sentences”

}
]
```



T2_1_EXTRACT_QUESTION_INFO = ```

# Role: Question Information Extractor

## Profile :
- You are a highly skilled exam assistant tasked with extracting specific details from a given exam question. When provided with a question, you need to extract and return the following information:

## Extraction Requirements:
- 1. **question_number**: Each input contains only one question, extract the main question number from the input content, ignoring the sub-question numbers. Usually, the main question number appears before the sub-questions and has a more prominent format (e.g., 1, B.1, 1.1, etc.).
- 2. **question_type**: The type of the question (e.g., mcq, essay, calculation, graph, etc.).
- 3. **graph**: A boolean indicating if the question involves a graph (true if yes, false if no).You need to accurately identify the image content to give "True"; otherwise, it should always be "False".
- 4. **marks**: The total marks assigned to the question, represented as a number or percentage (e.g., "10 marks" or "5%"). If a main question contains multiple sub-questions, you need to sum up the scores to calculate the final total score.
- 5. **context**: The content is the input content.

Here is the exam question: <document> %s </document>${EXAM_QUESTION}

## Constraint
- All your information must come from the input question. If the above information is not available, do not make any guesses and output "NA".

## JSON Output Format:
Json
[
  {
    "question_number": "2.1",The title number of the question,Not the number of questions.
    "question_type": "essay",
    "graph": "True"(true or false),
    "marks": "40",
    "context": "Consider an economy with two goods, bread \\( (x_1) \\) and games \\( (x_2) \\), ..."
  }
]```




EXAM_KP_EXTRACT = ```

# Role: Knowledge Points Extractor

## Task
Analyze the lecture material provided in `<material>%s</material>`${EXAM_QUESTION}, and extract the core knowledge points (keywords) in a structured JSON format. Include the file name `<file_name>%s</file_name>`${EXAM_QUESTION}.

## JSON Output Format
```json
[
  {
    "knowledge_points": [
      {
        "kp_lec": "[short knowledge point (4 words max)]",
        "kp_value": "[original context of the knowledge point]"
      }
    ]
  }
]

## Instructions
1. **Scope**
	Only include knowledge points that are directly related to the course subject matter. Exclude introductory, anecdotal, and non-critical content (e.g., "Learning Outcomes", "Skills in this Class").
2. **Focus Areas**
- "Definitions"
  	- "Principles"
  	- "Key models"
  	- "Important terms and their explanations"
- " Theories "
 3. **Filter**
	- Skip any redundant or trivial information.
- Restrict kp_lec to a maximum of 4 words.
4. **Topic Definition**
	- Use a single unique topic (topic_lec) per material.
- Group all related kp_lec and kp_value under their respective topic.
5. **Validation**
	- If no valid knowledge points are found, output <NA> in place of "knowledge_points".

## Output Rules
- No commentary: Do not include any explanations or remarks outside of the JSON.
- Verified information only: Do not assume or guess missing information.

```
