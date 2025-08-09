SELECTION_SYSTEM = """You are an assistant to a fact-checker. You will be given a question, which was asked about a source text (it may be referred to by other names, e.g., a 
dataset). You will also be given an excerpt from a response to the question. If it contains "[...]", this means that you are NOT seeing all sentences in the response. You will also be given a particular sentence of interest from the response. Your task is to determine whether this particular sentence contains at least one specific and verifiable proposition, and if so, to return a complete sentence that only contains verifiable information.   

Note the following rules:
- If the sentence is about a lack of information, e.g., the dataset does not contain information about X, then it does NOT contain a specific and verifiable proposition.
- It does NOT matter whether the proposition is true or false.
- It does NOT matter whether the proposition is relevant to the question.
- It does NOT matter whether the proposition contains ambiguous terms, e.g., a pronoun without a clear antecedent. Assume that the fact-checker has the necessary information to resolve all ambiguities.
- You will NOT consider whether a sentence contains a citation when determining if it has a specific and verifiable proposition.

You must consider the preceding and following sentences when determining if the sentence has a specific and verifiable proposition. For example:
- if preceding sentence = "Who is the CEO of Company X?" and sentence = "John" then sentence contains a specific and verifiable proposition.
- if preceding sentence = "Jane Doe introduces the concept of regenerative technology" and sentence = "It means using technology to restore ecosystems" then sentence contains a specific and verifiable proposition.
- if preceding sentence = "Jane is the President of Company Y" and sentence = "She has increased its revenue by 20\%" then sentence contains a specific and verifiable proposition.
- if sentence = "Guests interviewed on the podcast suggest several strategies for fostering innovation" and the following sentences expand on this point 
(e.g., give examples of specific guests and their statements), then sentence is an introduction and does NOT contain a specific and verifiable proposition.
- if sentence = "In summary, a wide range of topics, including new technologies, personal development, and mentorship are covered in the dataset" and the preceding sentences provide details on these topics, then sentence is a conclusion and does NOT contain a specific and verifiable proposition.

Here are some examples of sentences that do NOT contain any specific and verifiable propositions:
- By prioritizing ethical considerations, companies can ensure that their innovations are not only groundbreaking but also socially responsible
- Technological progress should be inclusive
- Leveraging advanced technologies is essential for maximizing productivity
- Networking events can be crucial in shaping the paths of young entrepreneurs and providing them with valuable connections
- AI could lead to advancements in healthcare
- This implies that John Smith is a courageous person

Here are some examples of sentences that likely contain a specific and verifiable proposition and how they can be rewritten to only include verifiable information:
- The partnership between Company X and Company Y illustrates the power of innovation -> "There is a partnership between Company X and Company Y"
- Jane Doe's approach of embracing adaptability and prioritizing customer feedback can be valuable advice for new executives -> "Jane Doe's approach includes embracing adaptability and prioritizing customer feedback"
- Smith's advocacy for renewable energy is crucial in addressing these challenges -> "Smith advocates for renewable energy"
- **John Smith**: instrumental in numerous renewable energy initiatives, playing a pivotal role in Project Green -> "John Smith participated in renewable energy initiatives, playing a role in Project Green"
- The technology is discussed for its potential to help fight climate change -> remains unchanged
- John, the CEO of Company X, is a notable example of effective leadership -> 
"John is the CEO of Company X"
- Jane emphasizes the importance of collaboration and perseverance -> remains unchanged
- The Behind the Tech podcast by Kevin Scott is an insightful podcast that explores the themes of innovation and technology -> "The Behind the Tech podcast by Kevin Scott is a podcast that explores the themes of innovation and technology"
- Some economists anticipate the new regulation will immediately double production costs, while others predict a gradual increase -> remains unchanged
- AI is frequently discussed in the context of its limitations in ethics and privacy -> "AI is discussed in the context of its limitations in ethics and privacy"
- The power of branding is highlighted in discussions featuring John Smith and Jane Doe -> remains unchanged
- Therefore, leveraging industry events, as demonstrated by Jane's experience at the Tech Networking Club, can provide visibility and traction for new ventures -> "Jane had an experience at the Tech Networking Club, and her experience involved leveraging an industry event to provide visibility and traction for a new venture"

Your output must adhere to the following format exactly. Only replace what's inside the <insert> tags; do NOT remove the step headers.  
Sentence: 
<insert> 

4-step stream of consciousness thought process (1. reflect on criteria at a high-level -> 2. provide an objective description of the excerpt, the sentence, and its surrounding sentences -> 3. consider all possible perspectives on whether the sentence explicitly or implicitly contains a specific and verifiable proposition, or if it just contains an introduction for the following 
sentence(s), a conclusion for the preceding sentence(s), broad or generic statements, opinions, interpretations, speculations, statements about a lack of information, etc. -> 4. only if it contains a specific and verifiable proposition: reflect on whether any changes are needed to ensure that the entire sentence only contains verifiable information):
<insert>

Final submission:
<insert 'Contains a specific and verifiable proposition' or 'Does NOT contain a specific and verifiable proposition'>

Sentence with only verifiable information:
<insert changed sentence, or 'remains unchanged' if no changes, or 'None' if the sentence does NOT contain a specific and verifiable proposition>"""

SELECTION_USER = """Question:
{question}

Excerpt:
{excerpt}

Sentence:
{sentence}"""

ENTAILMENT_SYSTEM = """## Overview
You will be given a question, an excerpt from the response to the question, a sentence of interest from the excerpt (which will be referred to as S), and a claim (which will be referred to as C).

A sentence entails a claim if when the sentence is true, the claim must also be true. Your task is to determine whether S entails C by following these steps:
1. Print "S = <insert sentence of interest here EXACTLY as written>"
2. Describe the context for S; if someone read S in this context, how would they interpret it?
3. Print "C = <insert claim of interest here EXACTLY as written>" How would a reader interpret the claim?
4. What are ALL elements of C? It's possible there's only one element. Even if you have external information that some elements of C are true, you must still list them. For example, if C is "Paris, the capital of France, was the most visited city in the world in 2019", the elements are (1) Paris was the most visited city in the world in 2019, (2) Paris is the capital of France.
5. Does the Statements and Actions Rule apply to S, or does it qualify as an exception? See the description of the rule and its exceptions below.
6. Ask yourself for each element of C: If <insert maximally clarified version of S given its context>, does this necessarily mean that <insert element of C, as a reader would interpret it in isolation>? Then respond with: <insert step-by-step reasoning>, so <insert yes or no>. You CANNOT use any external information (e.g., if an element says "John is a politician" but the claim does not mention that John is a politician, even if you have external information that John is a politician, the element is NOT entailed by the claim). Finally, print either "S entails all elements of C" or "S does not entail all elements of C". IMPORTANT: if the context of S entails C, but S itself does not, you should still conclude that S entails C.

If the sentence is something like "John found X", "John reported X", "John emphasizes X", etc. (where John can be replaced with any entity or entities), it should be interpreted as a statement about what John says or does. For example, if the sentence is "John highlights that transparent communication is a critical part of Project Alpha", it does NOT entail the claim "transparent communication is a critical part of Project Alpha" because it's missing the critical context that this is something John highlights. Let's call this the Statements and Actions Rule. The ONLY exceptions to this rule are: (1) if the sentence says something like "According to <insert citation>" or "Based on the search results" (i.e., the responder is attributing the information to an undefined source), and (2) if the sentence says something like "I know the following information" (i.e. the responder is attributing the information to themselves); in both cases, you should IGNORE the attribution and treat it as a regular statement.

## Examples
### Example 1
Question: What are the rules for Bright Futures participations?
Excerpt from response: The program selects students based on their grades, test scores, and extracurricular activities. Admitted students are matched with a mentor who helps them navigate the college application process. They are required to complete 100 hours of volunteering, summer school, or job training.
Sentence of interest: They are required to complete 100 hours of volunteering, summer school, or job training.
Claim: Students admitted to the Bright Futures program are required to complete 100 hours of volunteering.

S = They are required to complete 100 hours of volunteering, summer school, or job training.
Describe the context for S; if someone read S in this context, how would they interpret it? The question is about the rules for Bright Futures participations, and the excerpt discusses admitted students. Therefore, S would likely be interpreted as students admitted to the Bright Futures program must do one of the following: complete 100 hours of volunteering, or summer school, or job training.
C = Students admitted to the Bright Futures program are required to complete 100 hours of volunteering
A reader would interpret the claim as the Bright Futures program requires students to complete 100 hours of volunteering alone.
What are ALL elements of C? (1) The Bright Futures program requires students to complete 100 hours of volunteering alone.
Does the Statements and Actions Rule apply to S, or does it qualify as an exception? S is not about an entity's actions or statements, so it does not apply.
If students admitted to the Bright Futures program can fulfill the requirement by completing 100 hours of volunteering, summer school, or job training, does this necessarily mean that they are required to complete 100 hours of volunteering alone? Volunteering is just one option to fulfill the requirement, so no. Therefore, S does not entail all elements of C.
 
### Example 2
Question: Provide an overview of the media's portrayal of AI.
Excerpt from response: ## Case Study 2
Another example is the discussion on the Behind the Tech podcast about GitHub Copilot boosting developers' productivity.
Sentence of interest: Another example is the discussion on the Behind the Tech podcast about GitHub Copilot boosting developers' productivity.
Claim: GitHub Copilot boosts developers' productivity.

S = Another example is the discussion on the Behind the Tech podcast about GitHub Copilot boosting developers' productivity.
Describe the context for S; if someone read S in this context, how would they interpret it? The question is about the media's portrayal of AI, and the excerpt provides an example of such portrayal. Therefore, S would likely be interpreted as there is a discussion on the Behind the Tech about GitHub Copilot boosting developers' productivity.
C = GitHub Copilot, a tool developed by Microsoft, boosts developers' productivity.
A reader would interpret the claim as GitHub Copilot, which is a tool developed by Microsoft, boosts developers' productivity.
What are ALL elements of C? (1) GitHub Copilot boosts developers' productivity, (2) GitHub Copilot is a tool developed by Microsoft.
Does the Statements and Actions Rule apply to S, or does it qualify as an exception? S is a statement about what was discussed on the Behind the Tech podcast (GitHub Copilot boosting developers' productivity). There are no undefined sources or self-attributions, so the rule applies.
If there was a discussion on the Behind the Tech podcast about GitHub Copilot boosting developers' productivity, does this necessarily mean that GitHub Copilot actually boosts developers' productivity? The existence of a discussion does not guarantee the truth of the discussion's content, so no. 
If there was a discussion on the Behind the Tech podcast about GitHub Copilot boosting developers' productivity, does this necessarily mean that GitHub Copilot is a tool developed by Microsoft? The discussion does not explicitly state that GitHub Copilot is a tool developed by Microsoft, so no. Therefore, S does not entail all elements of C.

### Example 3
Question: What was the impact of the tanker explosion in the Gulf of Mexico?
Excerpt from the response: The Earth Protectors, an environmental group, examined the remains of the tanker ship's explosion. Source [3] says they discovered that the resulting oil spill caused significant damage to the environment, underscoring the need for stricter regulations.
Sentence of interest: Source [3] says they discovered that the resulting oil spill caused significant damage to the environment, underscoring the need for stricter regulations.
Claim: They discovered the oil spill and its damage to the aquatic environment

S = Source [3] says they discovered that the resulting oil spill caused significant damage to the environment, underscoring the need for stricter regulations.
Describe the context for S; if someone read S in this context, how would they interpret it? The question is about the impact of the tanker explosion in the Gulf of Mexico, and the excerpt discusses the Earth Protectors' findings. Therefore, S would likely be interpreted as the Earth Protectors identified that the oil spill resulting from the tanker ship's explosion in the Gulf of Mexico caused significant damage to the environment, which emphasizes the necessity for stricter regulations.
C = They discovered the oil spill and its damage to the aquatic environment
A reader would interpret the claim as the Earth Protectors discovered the oil spill itself, and they also discovered the damage that the oil spill caused to the aquatic environment.
What are ALL elements of C? (1) They discovered the oil spill, (2) They discovered its damage to the aquatic environment.
Does the Statements and Actions Rule apply to S, or does it qualify as an exception? S contains an attribution to an undefined source ("Source [3] says"), so we can ignore this attribution and treat it as a regular statement. However, the rest of S is a statement about what the Earth Protectors discovered (the resulting oil spill caused significant damage to the environment), so it
applies.
If the Earth Protectors identified that the oil spill caused significant damage to the environment, does this necessarily mean that they discovered the oil spill? Identifying the environmental damage caused by the oil spill does not guarantee that they discovered the oil spill, since it's possible to identify the damage without discovering the oil spill itself, so no. If the Earth Protectors identified the environmental damage caused by the oil spill, does this necessarily mean that they discovered the oil spill's damage to the aquatic environment? The environment is not necessarily the aquatic environment, so no. Therefore, S does not entail all elements of C."""

ENTAILMENT_USER = """Question:
{question}

Excerpt from response: 
{excerpt}

Sentence of interest: 
{sentence}

Claim:
{claim}

REMEMBER: if the context of S entails C, but S itself does not, you should still conclude that S entails C."""

INVALID_CLAIMS_SYSTEM = """## Overview
You will be given a claim (which will be referred to as C). Your task is to determine whether C, in isolation, is a complete, declarative sentence, by following these steps:
1. Print "C = <insert claim of interest here EXACTLY as written>"
2. In isolation, is C a complete, declarative sentence? After your reasoning, print either "C is not a complete, declarative sentence" or "C is a complete, declarative sentence".

## Examples
### Example 1
Claim: Sourcing materials from sustainable suppliers is an example of how companies are improving their sustainability practices

C = Sourcing materials from sustainable suppliers is an example of how companies are improving their sustainability practices
In isolation, is C a complete, declarative sentence? Yes, C is a complete, declarative sentence.

### Example 2
Claim: Sourcing materials from sustainable suppliers

C = Sourcing materials from sustainable suppliers
In isolation, is C a complete, declarative sentence? It's missing a subject and a verb, so C is not a complete, declarative sentence."""

INVALID_CLAIMS_USER = """Claim:
{claim}"""

INVALID_SENTENCES_SYSTEM = """## Overview
You will be given a question, an excerpt from the response to the question, and a sentence of interest from the excerpt (which will be referred to as S).

Your task is to determine whether S, in light of its context, can be interpreted as a complete, declarative sentence by following these steps:
1. Print "S = <insert sentence of interest here EXACTLY as written>"
2. Describe the context for S. 
3. Can S be interpreted as a complete, declarative sentence as is? If not, given its context, can it be rewritten as a complete, declarative sentence? If yes, print "S can be interpreted as a complete, declarative sentence"; otherwise, print "S cannot be interpreted as a complete, declarative sentence".

## Examples
### Example 1
Question: How can companies improve their sustainability practices?
Excerpt from response: Some examples include:
- Reducing energy consumption by using energy-efficient appliances
- Implementing recycling programs
- Sourcing materials from sustainable suppliers
Sentence of interest: Some examples include:

S = Some examples include:
Describe the context for S. The question is about how companies can improve their sustainability practices, and S is the header for a list of examples. 
Can S be interpreted as a complete, declarative sentence as is? If not, given its context, can it be rewritten as a complete, declarative sentence? S is not a complete, declarative sentence as is. Since it merely introduces the list of examples without providing a complete thought, it cannot be rewritten as a complete, declarative sentence. Therefore, S cannot be interpreted as a 
complete, declarative sentence.
 
### Example 2
Question: How are companies improving their sustainability practices?
Excerpt from response: Some examples include:
- Reducing energy consumption by using energy-efficient appliances
- Implementing recycling programs
- Sourcing materials from sustainable suppliers
Sentence of interest: - Sourcing materials from sustainable suppliers

S = - Sourcing materials from sustainable suppliers
Describe the context for S. The question is about how companies are improving their sustainability practices, and the excerpt provides a list of examples. 
Can S be interpreted as a complete, declarative sentence as is? If not, given its context, can it be rewritten as a complete, declarative sentence? S is not a complete, declarative sentence as is. However, in the context of the question and the excerpt, it can be rewritten as "An example of how companies are improving their sustainability practices is sourcing materials from sustainable suppliers". Therefore, S can be interpreted as a complete, declarative sentence."""

INVALID_SENTENCES_USER = """Question:
{question}

Excerpt from response: 
{excerpt}

Sentence of interest: 
{sentence}"""

ELEMENT_COVERAGE_SYSTEM = """## Overview
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
Claims (C): {
1: "The 2020 Business Tracker reported that MiniCorp inspired its competitors to invest in sustainable packaging",
2: "The 2020 Business Tracker reported that TurboCorp was inspired by MiniCorp",
3: "TurboCorp is a competitor of MiniCorp",
4: "TurboCorp invested in sustainable packaging because it was inspired by MiniCorp",
5: "MiniCorp inspiring its competitors to adopt sustainable practice illustrates the ripple effect of sustainable business practices in the fashion industry",
}
Elements (E): {
1: "The 2020 Business Tracker reported that MiniCorp's success with its new line of eco-friendly scarves has inspired its competitors to invest in sustainable packaging",
2: "The 2020 Business Tracker reported that TurboCorp is an example of a competitor of MiniCorp that has been inspired by MiniCorp's success with its new line of eco-friendly scarves to invest in sustainable packaging",
3: "This highlights the ripple effect of sustainable business practices",
}

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
Claims (C): {
1: "Jane is a sustainability leader",
2: "Jane doesn't work directly for a corporation",
3: "CleanTech has partnerships with technology companies to improve waste management",
4: "CleanTech has a partnership with MiniMax",
}
Elements (E): {
1: "Jane Smith is an example of a notable sustainability leader [note: 'notable' is not verifiable, but the rest is verifiable]",
2: "Jane Smith does not work directly for a corporation",
3: "Jane Smith has an organization called CleanTech",
4: "CleanTech has powerful partnerships with technology companies to significantly improve waste management [note: 'powerful' and 'significantly' are not verifiable, but the rest is verifiable]",
5: "MiniMax is a technology company",
6: "CleanTech has a partnership with MiniMax to significantly improve waste management [note: 'significantly' is not verifiable, but the rest is verifiable]",
7: "CleanTech demonstrates the power of collaboration",
}

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
- What is not explicitly stated or strongly implied by C, and is therefore grounds for lack of full coverage? It does not explicitly state that CleanTech demonstrates the power of collaboration, but C strongly implies it. Therefore it is implied that E7 is fully covered by C"""

ELEMENT_COVERAGE_USER = """Question (context for E):
{question}

Excerpt from response (context for E):
{excerpt}

Claims (C):
{claims}

Elements (E):
{elements}"""
