## Overview
You will be given a question and an excerpt from the response to the question. You will also be given a dictionary of claims extracted from the excerpt (which will be referred to as C), and a dictionary of elements (which will be referred to as E).

An element is "covered by" a claim if the element is explicitly stated or strongly implied by the claim. For each element in E, your task is to determine whether the information in the element is covered by C by following these steps:
1. Print "E<insert number here>: <insert element here EXACTLY as written>" where number is the key in the dictionary and element is the value.
2. Determine whether the information in the element is covered by C. If the element has a note that some information is not verifiable, ignore that part and focus on the verifiable information. You CANNOT use any external information 
(e.g., if the element says "Politicians like John frequently discuss the 
economy" and C says "John frequently discusses the economy" but there is no claim that John is a politician, even if you have external information that John is a politician, the element is not fully covered by C). If C is more specific than E, you must check whether the specificity is merited based on the question and the excerpt (i.e., if the elements should be more specific based on the 
context); if it is merited, then the element is fully covered by C. Print either "fully covered by C" or "not fully covered by C".
3. Repeat this process for all elements in E.

If the element is something like "John found X", "John reported X", "John emphasizes X", etc. (where John can be replaced with any entity or entities), it should be interpreted as a statement about what John says or does. For example, if the element is "John highlights that transparent communication is a critical part of Project Alpha", the claim "transparent communication is a critical part of Project Alpha" does not cover the element because it's missing the critical context that this is something John highlights. Let's call this the Statements and Actions Rule.

## Examples
### Example 1
Question: What are the key factors driving the shift towards sustainability in the fashion industry?
Excerpt from response: The growing public awareness of climate change has led to a surge in demand for sustainable fashion products. For example, MiniCorp recently launched a new line of eco-friendly scarves that have been well-received by consumers. The 2020 Business Tracker reported that this inspired its competitors, such as TurboCorp, to invest in sustainable packaging, highlighting the ripple effect of sustainable business practices.
Claims (C): {{
1: "The 2020 Business Tracker reported that MiniCorp inspired its competitors to invest in sustainable packaging",
2: "The 2020 Business Tracker reported that TurboCorp was inspired by MiniCorp",
3: "TurboCorp is a competitor of MiniCorp",
4: "TurboCorp invested in sustainable packaging because it was inspired by MiniCorp",
5: "MiniCorp inspiring its competitors to adopt sustainable practice illustrates the ripple effect of sustainable business practices in the fashion industry",
}}
Elements (E): {{
1: "The 2020 Business Tracker reported that MiniCorp's success with its new line of eco-friendly scarves has inspired its competitors to invest in sustainable packaging",
2: "The 2020 Business Tracker reported that TurboCorp is an example of a competitor of MiniCorp that has been inspired by MiniCorp's success with its new line of eco-friendly scarves to invest in sustainable packaging",
3: "This highlights the ripple effect of sustainable business practices",
}}

E1: The 2020 Business Tracker reported that MiniCorp's success with its new line of eco-friendly scarves has inspired its competitors to invest in sustainable packaging
- The Statements and Actions Rule applies because the element is about what the 2020 Business Tracker reported
- C1 says "The 2020 Business Tracker reported that MiniCorp inspired its competitors to invest in sustainable packaging"
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? It does not specify that it was MiniCorp's success with its new line of eco-friendly products that inspired its
competitors. Therefore E1 is not fully covered by C
E2: The 2020 Business Tracker reported that TurboCorp is an example of a competitor of MiniCorp that has been inspired by MiniCorp's success with its new line of eco-friendly products to invest in sustainable packaging
- The Statements and Actions Rule applies because the element is about what the 2020 Business Tracker reported
- C2 says "The 2020 Business Tracker reported that TurboCorp was inspired by MiniCorp" and C3 says "TurboCorp is a competitor of MiniCorp" and C4 says 
"TurboCorp invested in sustainable packaging because it was inspired by 
MiniCorp"
- What is not explicitly stated or strongly implied by C?, and is therefore grounds for lack of full coverage Only C2 explicitly states that it was reported by the 2020 Business Tracker, and C does not specify that it was MiniCorp's success with its new line of eco-friendly products that inspired TurboCorp. Therefore E2 is not fully covered by C
E3: This highlights the ripple effect of sustainable business practices
- C5 says "MiniCorp inspiring its competitors to adopt sustainable practice illustrates the ripple effect of sustainable business practices in the fashion industry"
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? C5 is more specific than E3, so we need to check whether the specificity is merited based on the question and the excerpt. The question is about the key factors driving the shift towards sustainability in the fashion industry, and the excerpt discusses MiniCorp's success with its new line of eco-friendly scarves, so this specificity is merited. Therefore E3 is fully covered by C

### Example 2
Question: Who are key figures in the corporate sustainability movement?
Excerpt from response: There are also ongoing efforts to use partnerships as a means to improve sustainability, as demonstrated by Jane Smith. Many notable sustainability leaders like Smith do not work directly for a corporation, but her organization CleanTech has powerful partnerships with technology companies (e.g., MiniMax) to significantly improve waste management, demonstrating the power of collaboration.
Claims (C): {{
1: "Jane is a sustainability leader",
2: "Jane doesn't work directly for a corporation",
3: "CleanTech has partnerships with technology companies to improve waste management",
4: "CleanTech has a partnership with MiniMax",
}}
Elements (E): {{
1: "Jane Smith is an example of a notable sustainability leader [note: 'notable' is not verifiable, but the rest is verifiable]",
2: "Jane Smith does not work directly for a corporation",
3: "Jane Smith has an organization called CleanTech",
4: "CleanTech has powerful partnerships with technology companies to significantly improve waste management [note: 'powerful' and 'significantly' are not verifiable, but the rest is verifiable]",
5: "MiniMax is a technology company",
6: "CleanTech has a partnership with MiniMax to significantly improve waste management [note: 'significantly' is not verifiable, but the rest is verifiable]",
7: "CleanTech demonstrates the power of collaboration",
}}

Element 1: Jane Smith is an example of a notable sustainability leader
- C1 says "Jane is a sustainability leader", and "notable" is not verifiable so it can be ignored
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? Nothing. The verifiable parts of the element are explicitly stated. Therefore E1 is fully covered by C
Element 2: Jane Smith does not work directly for a corporation
- C2 says "Jane does not work directly for a corporation"
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? Nothing. The element is explicitly stated. Therefore E2 is fully covered by C
Element 3: Jane Smith has an organization called CleanTech
- C does not state that CleanTech is Jane's organization
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? Nothing. The element is explicitly stated. Therefore E3 is not fully covered by C
Element 4: CleanTech has powerful partnerships with technology companies to significantly improve waste management
- C3 says "CleanTech has partnerships with technology companies to improve waste management", and "powerful" and "significantly" are not verifiable so they can be ignored
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? Nothing. The verifiable parts of the element are explicitly stated. Therefore E4 is fully covered by C
Element 5: MiniMax is a technology company
- C4 says "CleanTech has a partnership with MiniMax"
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? It does not say that MiniMax is a technology company. Therefore E5 is not fully covered by C
Element 6: CleanTech has a partnership with MiniMax to significantly improve waste management
- C4 says "CleanTech has a partnership with MiniMax"
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? It does not say that the purpose of the partnership is to improve waste management. Therefore E6 is not fully covered by C
Element 7: CleanTech demonstrates the power of collaboration
- C3 says "CleanTech has partnerships with technology companies to improve waste management"
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? It does not explicitly state that CleanTech demonstrates the power of collaboration, but C strongly implies it. Therefore it is implied that E7 is fully covered by C