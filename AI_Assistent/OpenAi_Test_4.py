import openai
openai.api_key = "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"
completion = openai.Completion()


def reply(question):
    prompt = f"hey: {question}\n"
    response = completion.create(prompt=prompt, engine="text-davinci-002", max_tokens=1000)
    answer = response.choices[0].text.strip()
    print(answer)


reply("Mention the cndocrine function of kidney")
