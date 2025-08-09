## Overview
You will be given a question, an excerpt from the response to the question, a sentence of interest from the excerpt, the claims derived from the sentence, and a claim of interest (which will be referred to as C).

A claim is "decontextualized" if (1) it is fully self-contained, meaning it can be understood in isolation (i.e., without the question, the excerpt, the sentence, and the other claims), AND (2) its meaning in isolation matches its meaning when interpreted alongside the question, the excerpt, the sentence, and the other claims. 

Your task is to create C_max, the maximally decontextualized version of C by following these steps:
1. Print "C = <insert claim of interest here EXACTLY as written>"
2. If someone read C without any context, would they have any questions? If yes, are any of these questions answered by the sentence or its context? If the reader would not have any questions, or none of the questions are clearly answered by the sentence or its context, or the claim already provides sufficient answers to the questions, print "C_max = C". Otherwise, set C_max equal to the maximally decontextualized claim that clarifies the answers to the questions that would be asked. Only include clarifications that are clearly attributable to the sentence and its context.

## Examples
### Example 1
Question: Provide an overview of the Supreme Court's importance in the United States.
Excerpt from response: Another example of the court's importance is the decision in Roe v. Wade in January 1973. It significantly affected abortion laws across the United States.
Sentence of interest: It significantly affected abortion laws across the United States.
All claims: ["The court's decision affected abortion laws across the United States."]
Claim of interest: The court's decision affected abortion laws across the United States.

C = The court's decision affected abortion laws across the United States.
Would someone reading C without any context have questions? They would likely ask which court made the decision and what the decision was.
Are any of these questions answered by the sentence or its context? The court is the Supreme Court, and the decision was Roe v. Wade in January 1973.
C_max = The Supreme Court's decision in Roe v. Wade in January 1973 affected abortion laws across the United States.

### Example 2
Question: Who is Jane Doe?
Excerpt from response: Jane Doe has been a long-time advocate for environmental causes. In 2022, she spoke at Climate Action Now. She plans to speak at Youth for Climate, Moving Forward, and several other conferences next year.
Sentence of interest: She plans to speak at Youth for Climate, Moving Forward, and several other conferences next year.
All claims: ["She plans to speak at Youth for Climate next year", "She plans to speak at Moving Forward next year", "She plans to speak at other conferences next year"]
Claim of interest: She plans to speak at other conferences next year.

C = She plans to speak at other conferences next year.
Would someone reading C without any context have questions? They would likely ask who she is, what "other conferences" means, and what year "next year" refers to.
Are any of these questions answered by the sentence or its context? She is Jane Doe, "other conferences" means conferences other than Youth for Climate and Moving Forward (since they are covered by the other claims), and "next year" is 2023.
C_max = Jane Doe plans to speak at conferences other than Youth for Climate and Moving Forward in 2023.