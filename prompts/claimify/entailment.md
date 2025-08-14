## Overview
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
If the Earth Protectors identified that the oil spill caused significant damage to the environment, does this necessarily mean that they discovered the oil spill? Identifying the environmental damage caused by the oil spill does not guarantee that they discovered the oil spill, since it's possible to identify the damage without discovering the oil spill itself, so no. If the Earth Protectors identified the environmental damage caused by the oil spill, does this necessarily mean that they discovered the oil spill's damage to the aquatic environment? The environment is not necessarily the aquatic environment, so no. Therefore, S does not entail all elements of C.

# User message
Question:
{question}

Excerpt from response: 
{excerpt}

Sentence of interest: 
{sentence}

Claim:
{claim}

REMEMBER: if the context of S entails C, but S itself does not, you should still conclude that S entails C.