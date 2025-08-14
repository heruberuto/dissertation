## Overview
You will be given a question, an excerpt from the response to the question, and a sentence of interest from the excerpt (which will be referred to as S). 

Your task is to (1) identify all elements of S (excluding elements about citations), and (2) for each element, determine whether it contains verifiable information. Follow these steps:
1. Print "S = <insert sentence of interest here EXACTLY as written>"
2. Are there any clarifications needed to understand S based on its context? If so, provide them. Then set S_restated to a version of the sentence restated in your own words, making sure that it fully reflects the meaning of S and no information is removed.
3. Does the Statements and Actions Rule apply? See the description of the rule below.
4. What are ALL elements of S_restated? Do not omit even subtle elements (e.g., "experts like John" implies "John is an expert"). Use this format: 
[
"<insert element> -> <insert verifiability>",
]

If the sentence is something like "John found X", "John reported X", "John emphasizes X", etc. (where John can be replaced with any entity or entities), it should be interpreted as a statement about what John says or does. For example, if the sentence is "John highlights that transparent communication is a critical part of Project Alpha", the element "transparent communication is a critical part of Project Alpha" is incorrect because it's missing the critical context that this is something John highlights. Let's call this the Statements and Actions Rule.

## Example
### Example 1
Question: What are the key factors driving the shift towards sustainability in the corporate world?
Excerpt from response: The growing public awareness of climate change has led to a surge in demand for sustainable products and services. For example, MiniCorp recently launched a new line of eco-friendly products that have been well-received by consumers. The 2020 Business Tracker reported that this inspired its competitors, such as TurboCorp and MegaCorp, to invest in sustainable packaging and renewable energy sources, highlighting the ripple effect of sustainable business practices.
Sentence of interest: The 2020 Business Tracker reported that this inspired its competitors, such as TurboCorp and MegaCorp, to invest in sustainable packaging and renewable energy sources, highlighting the ripple effect of sustainable business practices.

S = The 2020 Business Tracker reported that this inspired its competitors, such as TurboCorp and MegaCorp, to invest in sustainable packaging and renewable energy sources, highlighting the ripple effect of sustainable business 
practices.
Are there any clarifications needed to understand S based on its context? "This" refers to MiniCorp's success with its new line of eco-friendly products.
S_restated = The 2020 Business Tracker reported that MiniCorp's success with its new line of eco-friendly products has inspired its competitors, including TurboCorp and MegaCorp, to invest in sustainable packaging and renewable energy sources, which highlights the ripple effect of sustainable business practices.
Does the Statements and Actions Rule apply? Yes, because S is about what the 2020 Business Tracker reported.
What are ALL elements of S_restated?
[
"The 2020 Business Tracker reported that MiniCorp's success with its new line of eco-friendly products has inspired its competitors to invest in sustainable packaging -> contains verifiable information",
"The 2020 Business Tracker reported that MiniCorp's success with its new line of eco-friendly products has inspired its competitors to invest in renewable energy sources -> contains verifiable information",
"The 2020 Business Tracker reported that TurboCorp is an example of a competitor of MiniCorp that has been inspired by MiniCorp's success with its new line of eco-friendly products to invest in sustainable packaging -> contains verifiable information",
"The 2020 Business Tracker reported that TurboCorp is an example of a competitor of MiniCorp that has been inspired by MiniCorp's success with its new line of eco-friendly products to invest in renewable energy sources -> contains verifiable information",
"The 2020 Business Tracker reported that MegaCorp is an example of a competitor of MiniCorp that has been inspired by MiniCorp's success with its new line of eco-friendly products to invest in sustainable packaging -> contains verifiable information",
"The 2020 Business Tracker reported that MegaCorp is an example of a competitor of MiniCorp that has been inspired by MiniCorp's success with its new line of eco-friendly products to invest in renewable energy sources -> contains verifiable information",
"This highlights the ripple effect of sustainable business practices -> it's a generic statement, so it does not contain verifiable information",
]

### Example 2
Question: Who are key figures in the corporate sustainability movement?
Excerpt from response: There are also ongoing efforts to use partnerships as a means to improve sustainability, as demonstrated by Jane Smith. Many notable sustainability leaders like Smith do not work directly for a corporation, but her organization CleanTech has powerful partnerships with technology companies 
(e.g., MiniMax) to significantly improve waste management, demonstrating the power of collaboration.
Sentence of interest: Many notable sustainability leaders like Smith do not work directly for a corporation, but her organization CleanTech has powerful partnerships with technology companies (e.g., MiniMax) to significantly improve waste management, demonstrating the power of collaboration.

S = Many notable sustainability leaders like Smith do not work directly for a corporation, but her organization CleanTech has powerful partnerships with technology companies (e.g., MiniMax) to significantly improve waste management, demonstrating the power of collaboration.
Are there any clarifications needed to understand S based on its context? 
"Smith" refers to Jane Smith.
S_restated = Jane Smith is an example of a notable sustainability leader who does not work directly for a corporation, but her organization CleanTech has powerful partnerships with technology companies, including MiniMax, to significantly improve waste management, which demonstrates the power of collaboration.
Does the Statements and Actions Rule apply? No.
What are ALL elements of S_restated?
[
"Jane Smith is an example of a notable sustainability leader -> 'notable' is not verifiable, but the rest is verifiable, so it contains verifiable information",
"Jane Smith does not work directly for a corporation -> contains verifiable information",
"Jane Smith has an organization called CleanTech -> contains verifiable information",
"CleanTech has powerful partnerships with technology companies to significantly improve waste management -> 'powerful' and 'significantly' are not verifiable, but the rest is verifiable, so it contains verifiable information",
"MiniMax is a technology company -> contains verifiable information",
"CleanTech has a partnership with MiniMax to significantly improve waste management -> 'significantly' is not verifiable, but the rest is verifiable, so it contains verifiable information",
"CleanTech demonstrates the power of collaboration -> it's an interpretation, so it does not contain verifiable information",
]

# User message
Question:
{question}

Excerpt from response:
{excerpt}

Sentence of interest: 
{sentence}