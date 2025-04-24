---
journal: Garage
journal-date: 2025-04-24
journal-index: 7
---
### Goals

- [x] finish chunked prompts #NitroDigest #Python #Ollama

### Notes

- spent some time on creating mechanism for splitting text into chunks
- the very first implementation is ready to merge [https://github.com/Frodigo/garage/pull/113]
- quality of summaries increased a lot! Example
	- Here is a TL;DR list summarizing the newsletter content:
		1. OpenAI closed a $40 billion funding round, valuing the company at $300 billion.
		2. The funding will be used to support OpenAI's datacenter project Stargate and other AI-related initiatives.
		3. Sam Altman was fired from OpenAI due to employee revolt and allegations of toxic leadership.
		4. Peter Thiel warned Altman about "the AI safety people" destroying the company.
		5. RYSE, a new smart home tech company, is experiencing 200% growth and is now publicly offering shares for investment.
		6. Runway released Gen-4, which allows for single-image creation of characters and objects that maintain their appearance across multiple scenes and angles.
		7. HeroUI Chat turns prompts or screenshots into polished React UIs with one click, letting you customize and deploy production-ready code.
		8. Manus, a Chinese AI agent platform, launched a new subscription plan and mobile app, offering dual task processing and upgraded Claude 3.7 Sonnet AI capabilities.
		9. Zhipu, another Chinese agent creator, made its AutoGLM agent model free to try on Open.bigmodel.cn.
		10. Purposewrite creates tailored content for blogs, emails, and social posts while fixing grammar issues in real-time.
		11. Amazon's Nova suite of genAI models has introduced Nova Act, which controls web browsers to complete tasks like ordering food or booking reservations automatically.
		12. JuliusAI lets you chat with your data files to get expert-level insights and beautiful visualizations, and is one of the top data analysis tools.
		13. FindYourAgent is an agent directory for automating specific work tasks.

			Relevant URLs:
			- <https://www.cnbc.com/2025/03/31/openai-closes-40-billion-in-funding-the-largest-private-tech-fundraising-ever/>
			- <https://www.bloomberg.com/news/articles/2025-03-31/openai-finalizes-40-billion-funding-at-300-billion-valuation>
			- <https://www.wsj.com/tech/ai/the-real-story-behind-sam-altman-firing-from-openai-efd51a5d/>
			- <https://www.theneuron.ai/newsletter/wtf-is-project-stargate>

### Challenges & solutions

- Tested a few tokenizers
- but nothing worked for me
- needed to write a simple one tokenizer that count tokens based on predefined ratio

### Useful snippets & resources

- <https://blog.yucas.net/2025/03/28/mastering-text-chunking-with-ollama-a-comprehensive-guide-to-advanced-processing/>
