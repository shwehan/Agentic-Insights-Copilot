# Retrieval Notes

## Prompt 1
Question: How should we segment customers by engagement and profitability?

Assessment:
Mostly relevant. Retrieved customer value/activity and rewards strategy sections, which are directionally useful. Also pulled customer experience and retention content, which felt broader than needed.

Issues:
- Some unrelated adjacent sections included
- Duplicate chunks appeared

After fixing the duplicates, 
What worked:
- Customer value/activity segmentation is highly relevant.
- Rewards strategy segmentation is also directionally useful.
- Retrieval is semantically related to the prompt.

Issues:
- It still retrieves adjacent sections that are less central to the question.
- The context is broader than necessary.
- Retrieval quality is acceptable for MVP but not yet sharply targeted.

## Prompt 2
Question: What is the best segmentation approach for a rewards strategy use case?

Assessment:
Relevant overall. Retrieved rewards strategy and customer value sections, plus general segmentation definitions.

Issues:
- Heavy duplication of the same chunks
- Retrieval feels repetitive rather than diverse

After fixing the duplciates, 
Assessment:
Strongest result so far. The retriever returned rewards strategy segmentation, customer value/activity segmentation, segmentation definitions, output sections, and business rules.

What worked:
- Rewards strategy content was surfaced clearly.
- Supporting definitions and segmentation rules were useful and relevant.
- Retrieval looks cleaner and more focused than before.

Issues:
- Customer value/activity segmentation appears before or alongside rewards strategy, which is useful but slightly broader than ideal.
- Could be improved with better ranking or more structured source documents.

## Prompt 3
Question: How should we define digital engagement segments for a customer experience initiative?

Assessment:
Partially relevant but weaker. Retrieved customer experience survey and retention/lifecycle sections. Did not clearly prioritize digital engagement segmentation as expected.

Issues:
- Missed the most specific intended section
- Retrieval appears too broad and repetitive

After fixing the dupliciates, 
Assessment:
Partially relevant. The retriever returned customer experience survey segmentation, retention/lifecycle segmentation, customer value/activity segmentation, rewards strategy segmentation, and finally digital engagement segmentation guidance.

What worked:
- Retrieval is no longer duplicating the same chunks over and over.
- The returned context is directionally related to segmentation and customer behavior.

Issues:
- The most relevant section, digital engagement segmentation, appeared too late in the context.
- Query wording with "customer experience initiative" appears to bias retrieval toward survey/customer experience sections.
- Retrieval is still somewhat broad and not sharply prioritizing the exact intended use case.


## Overall Takeaway 1
Retrieval is functioning and semantically relevant, but current results suggest:
1. duplicate entries in the vector store
2. retrieval is too repetitive
3. section targeting could be improved with better source document structure

## Overall Takeaway 2

The duplicate chunk problem appears to be fixed after deleting and rebuilding the vector store.

Current retrieval is:
- semantically relevant
- usable for a V1 generation pipeline
- still too broad for precise use-case targeting

Main remaining issues:
1. Query phrasing can pull the retriever toward semantically adjacent sections.
2. Chunking is likely too coarse or too mixed.
3. The source file structure may not separate use cases strongly enough for clean retrieval ranking.

Conclusion:
Retrieval is good enough to proceed to generation for V1, but it should be improved in a later iteration with better chunking, more structured documents, or use-case-specific source files.