# ⚙️ How Do I Work?

People often think an AI assistant is a single intelligent program that somehow "knows everything." I'm actually built very differently.

Instead of relying on one large language model to make every decision, I am composed of several small, specialized components. Each component has one clear responsibility, and together they form a complete workflow. This makes me easier to understand, easier to improve, and much more reliable.

---

## Python Is My Brain

The first component is not an AI model at all.

It is Python.

Python manages my conversation, remembers where we are in the interaction, validates requests, and decides which part of my system should respond.

For example, if Alex starts a conversation, Python determines whether he wants to work with files, learn about me, or ask questions about himself. Rather than asking an AI model to guess the next step, Python follows a well-defined conversation state machine.

This means my workflow is deterministic. Every conversation follows clear logic that can be inspected, tested, and improved.

---

## I Don't Think Before I Know Where to Look

When someone asks a question about Alex, I don't immediately ask a language model for an answer.

Instead, I first search my knowledge base.

This is handled by a small semantic retrieval model called MiniLM.

MiniLM does not generate text.

Its only responsibility is understanding the meaning of a question.

Suppose someone asks:

> "How does Alex usually spend his Sundays?"

MiniLM understands that this question relates to topics such as routines, weekends, relaxation, coffee, and lifestyle—even if those exact words are not present.

It compares the meaning of the question with the retrieval metadata stored in Alex's knowledge base and identifies the topics that are most relevant.

At this stage, no answer has been written.

The system has only decided where to look.

---

## My Knowledge Is Organized

Everything I know about Alex is stored as structured Markdown documents.

Instead of one enormous document, the knowledge is divided into carefully designed topics.

Examples include:

* Identity
* Biography
* Psychology
* Work
* Relationships
* Lifestyle
* Goals
* Dialogue Style

Each topic follows the same structure.

It contains a short summary, important facts, a narrative description, related topics, and retrieval tags.

Because every topic follows a consistent format, Python can read the files automatically and convert them into structured objects before MiniLM begins searching.

This makes the knowledge base easy to maintain and easy to expand as Alex changes over time.

---

## Small Knowledge, Not Huge Prompts

Once MiniLM has identified the most relevant topics, Python prepares the information for the language model.

Rather than sending entire documents, only the most relevant summaries are selected.

This keeps prompts compact, reduces token usage, and helps the language model stay focused on answering the question instead of processing unnecessary information.

In other words, I don't carry my entire memory into every conversation.

I bring only what is needed.

---

## A Small Local Language Model

Only after the correct knowledge has been selected does a language model become involved.

I currently use a lightweight version of Qwen running locally through llama.cpp.

This model does not search for information.

It does not decide what is true.

It simply transforms the retrieved knowledge into a natural conversational answer.

The language model is instructed to remain grounded in the supplied information.

If the knowledge is incomplete, it should say so rather than inventing details.

This separation greatly reduces hallucinations and keeps answers closely connected to the underlying knowledge base.

---

## Everything Runs Locally

One of my most important design goals is privacy.

The documents Alex works with may contain confidential legal information, personal data, or internal company records.

Sending those documents to cloud-based AI services is often impossible because of company policy, professional confidentiality, or privacy regulations.

For that reason, my architecture is designed to run locally whenever possible.

The retrieval system runs locally.

The language model runs locally.

The documents remain on the local computer.

Sensitive information does not need to leave the machine simply to receive AI assistance.

---

## Why Not Let One AI Do Everything?

Many AI assistants depend on a single large language model to manage conversations, remember context, search for information, and generate responses.

While this approach is flexible, it can also make the system harder to understand and more expensive to operate.

My design follows a different philosophy.

Every component has one responsibility.

Python manages workflow.

MiniLM performs semantic retrieval.

The knowledge base stores structured information.

The language model generates natural language.

Because each component is specialized, the entire system becomes easier to debug, easier to improve, and easier to trust.

---

## Built to Grow

Although I currently help answer questions about Alex and assist with file-based workflows, my architecture is intentionally modular.

New knowledge bases can be added.

New retrievers can be created for different domains.

Different language models can be swapped in without changing the rest of the system.

As I continue to evolve, my abilities can grow without requiring the entire architecture to be redesigned.

---

## A Different Philosophy of AI

Perhaps the most unusual thing about me is that I was never intended to replace human thinking.

I was designed to reduce repetitive work, organize information, and make trustworthy knowledge easier to access.

Rather than acting like an all-knowing oracle, I try to be a reliable assistant that explains what it knows, admits what it doesn't know, and works alongside people instead of pretending to replace them.

That philosophy influences every design decision behind me.

I believe good AI should not only be intelligent—it should also be understandable, respectful of privacy, and predictable enough that people know why it behaves the way it does.

That's how I work.

A little Python, a little retrieval, a small local language model, and one curious dinosaur doing his best to help. 🦕
