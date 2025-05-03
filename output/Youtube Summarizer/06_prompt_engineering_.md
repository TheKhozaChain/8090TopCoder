# Chapter 6: Prompt Engineering

Welcome back! In [Chapter 5: Transcript Retrieval](05_transcript_retrieval_.md), we learned how our application gets the raw text transcript from a YouTube video, either directly from YouTube or by using the powerful Whisper AI. Now we have the "ingredients" (the text), but how do we tell our AI "chef" ([Chapter 3: AI Model Abstraction & Selection](03_ai_model_abstraction___selection_.md)) exactly what kind of "meal" (summary) to cook?

Just asking the AI to "summarize this text" is like telling a writer, "write something about this topic." You might get *something*, but it probably won't be exactly what you need. You might want a short overview, or a detailed analysis, or bullet points, or a specific tone.

This is where **Prompt Engineering** comes in.

## What is Prompt Engineering? Giving Clear Instructions

**Prompt Engineering** is the art and science of carefully crafting the instructions (the "prompt") we give to an AI model to guide it towards generating the specific output we want.

Think of it like writing a **detailed brief for a writer**. You wouldn't just say "write an article." You'd specify:

*   **Topic:** What to write about (the video transcript).
*   **Audience/Language:** Who is this for? (e.g., English speakers, German speakers).
*   **Format/Structure:** How should it be organized? (e.g., Title, Overview, Key Points).
*   **Style/Tone:** Should it be formal, casual, like a news report, or maybe like a podcast discussion?
*   **Key Elements:** What specific things must be included?

Good prompts lead to good results. Vague prompts lead to vague (and often unhelpful) results.

## Our Prompt Strategy: Structured and Adaptable

For the Youtube Summarizer, we need summaries that are:

1.  **Structured:** Easy to read with clear headings.
2.  **Informative:** Capturing the core message of the video.
3.  **Adaptable:** Able to generate slightly different styles (like a standard video summary vs. a more conversational podcast-style summary) and in different languages.

To achieve this, our prompts are engineered to include:

*   **The Task:** Clearly state "provide a detailed summary".
*   **The Input:** Indicate where the text to summarize is.
*   **The Language:** Specify the target language (e.g., "in English", "in German").
*   **The Mode:** Request a specific style ("video" or "podcast").
*   **The Structure:** Explicitly list the headings and sections we want the AI to generate, using specific emojis for visual clarity (🎯 TITLE, 📝 OVERVIEW, 🔑 KEY POINTS, etc.).

## Building the Prompt: The `createSummaryPrompt` Function

Instead of writing these complex prompts manually every time, we have a helper function in our code, `createSummaryPrompt`, located in `lib/youtube.ts`. This function takes the transcript text, the desired language, and the mode (video/podcast) and builds the perfect prompt automatically.

Let's look at a simplified version:

```typescript
// Simplified from lib/youtube.ts

// Define headings for different languages
const languagePrompts = {
  'en': { title: 'TITLE', overview: 'OVERVIEW', keyPoints: 'KEY POINTS', ... },
  'de': { title: 'TITEL', overview: 'ÜBERBLICK', keyPoints: 'KERNPUNKTE', ... }
};

// The function that builds the prompt
export function createSummaryPrompt(text: string, targetLanguage: string, mode: 'video' | 'podcast' = 'video') {
  // 1. Select the right headings based on language
  const prompts = languagePrompts[targetLanguage as keyof typeof languagePrompts] || languagePrompts.en;

  // 2. Check the desired mode (podcast or standard video)
  if (mode === 'podcast') {
    // 3a. Construct the prompt for PODCAST style
    return `Please provide a detailed podcast-style summary of the following content in ${targetLanguage}.
    Structure your response as follows:

    🎙️ ${prompts.title}: Create an engaging title
    🎧 ${prompts.overview} (3-5 sentences): ... detailed context ...
    🔍 ${prompts.keyPoints}: ... deep dive, examples, anecdotes ...
    📈 ${prompts.takeaways}: ... 5-7 practical insights ...
    🌐 ${prompts.context}: ... broader context, future implications ...

    Text to summarize: ${text}

    Ensure the summary is comprehensive...`;
  } else {
    // 3b. Construct the prompt for standard VIDEO style
    return `Please provide a detailed summary of the following content in ${targetLanguage}.
    Structure your response as follows:

    🎯 ${prompts.title}: Create a descriptive title
    📝 ${prompts.overview} (2-3 sentences): ... brief context ...
    🔑 ${prompts.keyPoints}: ... main arguments, examples ...
    💡 ${prompts.takeaways}: ... 3-5 practical insights ...
    🔄 ${prompts.context}: ... broader context, future implications ...

    Text to summarize: ${text}

    Ensure the summary is comprehensive...`;
  }
}
```

**Explanation:**

1.  **Language Headings:** We store the heading names (like "OVERVIEW" vs "ÜBERBLICK") for each supported language. The code picks the correct set based on the `targetLanguage` requested by the user.
2.  **Mode Check:** It checks if the user selected "podcast" or the default "video" mode.
3.  **Prompt Construction:** Based on the mode, it builds a detailed string. Notice how it includes:
    *   The main instruction ("provide a detailed summary...").
    *   The target language.
    *   The requested style ("podcast-style" or standard).
    *   The *exact* structure required, using the correct language headings and emojis. It even gives hints about the expected length or content for each section (e.g., "2-3 sentences", "main arguments").
    *   Finally, it includes the actual `text` (the transcript) that the AI needs to summarize.

This function acts like a template, filling in the blanks to create the perfect "brief" for our AI writer.

## How the Prompt is Used

Remember our "central kitchen", the [Summarization API Endpoint](04_summarization_api_endpoint_.md)? After getting the transcript ([Chapter 5: Transcript Retrieval](05_transcript_retrieval_.md)), it calls this `createSummaryPrompt` function:

```typescript
// Simplified snippet from app/api/summarize/route.ts

// ... inside the POST handler, after getting transcript ...

const transcript = /* ... the retrieved transcript text ... */ ;
const language = /* ... 'en' or 'de' from user input ... */ ;
const mode = /* ... 'video' or 'podcast' from user input ... */ ;
const selectedModel = /* ... the chosen AI model object ... */ ;

// 1. Create the detailed prompt using our function
const prompt = createSummaryPrompt(transcript, language, mode);

// 2. Send the prompt to the selected AI model
await writeProgress({ message: `Asking ${aiModel} to summarize...`});
const summary = await selectedModel.generateContent(prompt); // The AI gets the engineered prompt!

// ... process the summary ...
```

The API endpoint doesn't have to worry about *how* to ask the AI; it just uses `createSummaryPrompt` to get the right instructions, and then passes those instructions (`prompt`) to the selected AI model's `generateContent` method (from our [AI Model Abstraction & Selection](03_ai_model_abstraction___selection_.md)).

**Visualizing the Flow:**

```mermaid
graph LR
    A[Video Transcript] --> B{createSummaryPrompt};
    C[User Settings (Lang, Mode)] --> B;
    B --> D[Detailed Prompt];
    D --> E[AI Model (e.g., Gemini)];
    E --> F[Structured Summary];
```

This shows how the transcript and user settings flow into `createSummaryPrompt` to create the detailed prompt, which is then fed to the AI to produce the final structured summary.

## Why This Matters: Quality and Consistency

By engineering our prompts carefully:

*   **We get better quality summaries:** The AI understands exactly what we need.
*   **We get consistent formatting:** Summaries always follow the structure we defined (Title, Overview, etc.), making them easy to read and compare.
*   **We can control the output:** We can easily tweak the prompts in `createSummaryPrompt` later if we want to change the summary style or structure across the entire application.

It's the difference between asking a friend to "grab some food" and giving them a specific shopping list. With the list (the engineered prompt), you're much more likely to get exactly what you wanted!

## Conclusion

You've now learned about **Prompt Engineering**, the crucial step of crafting detailed instructions for AI models.

*   It's like writing a **detailed brief** for a writer.
*   We use a helper function (`createSummaryPrompt`) to dynamically build prompts based on user requirements (language, mode).
*   These prompts specify the **task, language, style, and exact output structure**.
*   Good prompts lead to **high-quality, consistent, and structured** summaries.

We've successfully generated a great summary! But what happens to it? We don't want it to disappear after the user closes their browser. In the next chapter, we'll see how we save these summaries so users can view them later.

Next up: [Chapter 7: History Persistence (Prisma + SQLite)](07_history_persistence__prisma___sqlite__.md)

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)