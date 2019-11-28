# Rule-Based Paraphrase Generation in Hindi

## Aim

Paraphrases are two sentence which have the same proposition (meaning). Although it is almost impossible for two different sentence to mean exactly the same, the aim is to generate sentences which have close meaning to the original sentence

## Dataset

Hindi-Urdu Multi-Representational Treebanks (Bhatt et al., 2009)
Link: http://ltrc.iiit.ac.in/hutb_release/
<br>
News Artices manually annotated in SSF format.
*Total sentences = 3497*

## Methods

### Synonym & Antonym replacement

+ Synonyms and antonyms lists were scraped from hindistudent.com. Stored in JSON format in funtions/paryavachis.txt and functions/vilom_shabds.txt 
+ Basic string matching and replacement with a few extra cases

  - Proper nouns or parts of compund words can **not** be replaced
  - Head verb needs to be negated in case of antonym replacement
  - Apply same morphology if the original word is inflected and similar to replaced word
+ Verb negation with antonym replacement gave the poorest results as the generated sentences often had a proposition much different from original sentence
+ Code: *functions/syn_antn.py*

### Word order rearrangement
+ Used the fact that hindi is a free word-order language
+ Generated tree (based on dependency between chunks) where siblings can be freely permtated
+ Code: *functions/re_arrange.py* 

### Active to Passive voice
+ followed rules for converting from krytvachya to karmvachya
  * Found non-copula verbs with distinct K1 and K2 (check karaka relations)
  * Remove postpositions from k1 and K2 chunks. And added "द्वारा" to K1
  * pronouns in K1 need be replaced to appropiate form
  * "जा" is added to verb. The verb phrases is then inflected for passive tense and K2 gender
+ Code: *functions/active_to_passive.py* 

# How to run

Python version 3.6 or above is required

```
pip install -r requirements.txt

python runner.py
```