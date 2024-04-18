# Automated-Gmail-Responder

## Have a GCP project?
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

# Hi it's me

run:
`pip install -r requirements.txt`
`pip install pyhtml2pdf`
`pip install langchain_google_genai`
`pip install chromadb` 
`pip install pypdf`

How to run the project:


Current problems:
sometimes LLM does not respond...
train the llm to respond accordingly. It's not giving consistent results. 
Gemini pro has difficulty taking in large pdf files.
gpt-...-turbo-16k works but it's not free...
https://www.chatpdf.com/docs/api/backend allows for only 500 messages a month and then you have to pay

Looking into mistral ai to see if we get better and faster results
    - Research: https://medium.com/@thakermadhav/build-your-own-rag-with-mistral-7b-and-langchain-97d0c92fa146
    follow the documentation on swapping out gemini pro to mistral7b
    - whether we need huggingface token for mistral ai

other alternative is create our own customizations and give it to ella for free.
    - how will we integrate it with chrome extension? Ask Ameeta?
    

Notes/Research:
    Fine-tuning the LLM: If the LLM is not providing consistent results, we might need to fine-tune it on a dataset that includes examples similar to the queries we're receiving. Fine-tuning can help the model better understand and generate responses specific to your domain or use case.

    Optimizing Gemini Pro: Since Gemini Pro struggles with large PDF files, we could try preprocessing the PDFs to reduce their size or splitting them into smaller chunks before feeding them into Gemini Pro. Alternatively, we could explore other LLMs that might handle large documents more efficiently.

    Exploring Free Alternatives: While some LLMs like GPT-3-turbo-16k offer excellent performance, they may not be feasible due to their cost. However, there are free alternatives available, such as:

        Hugging Face Transformers: Hugging Face provides a wide range of pre-trained LLMs that you can fine-tune on your specific dataset. Models like GPT-2 and smaller variants of GPT-3 are available for free.

        OpenAI GPT-3 API: OpenAI provides access to the GPT-3 API, which offers various pricing tiers. While the free tier has limitations, it could still be useful for experimentation or low-volume use cases.

    Efficient PDF Processing Libraries: Libraries like PyMuPDF or pdfminer.six might offer better performance or memory efficiency compared to PyPDF2.

    Batch Processing and Caching: Implement batch processing and caching mechanisms to handle a large number of requests more efficiently. You can preprocess PDFs in batches and cache the results to minimize redundant computations.

  Custom Solutions: Depending on our specific requirements, we might consider developing custom solutions or pipelines tailored to our needs. This could involve leveraging domain-specific knowledge or integrating multiple tools and libraries to achieve the desired outcome.