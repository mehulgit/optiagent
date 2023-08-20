# OptiAgents
Autonomous Agents for Competitive Intelligence

## What is Competitive Intelligence(CI)?

Competitive intelligence, sometimes referred to as corporate intelligence, refers to the ability to gather, analyze, and use information collected on competitors, customers, and other market factors that contribute to a business's competitive advantage. Competitive intelligence is important because it helps businesses understand their competitive environment and the opportunities and challenges it presents. Businesses analyze the information to create effective and efficient business practices.

## Autonomous Agents

Utilizing autonomous agents for competitive intelligence offers a spectrum of strategic advantages. These intelligent agents, powered by advanced algorithms and machine learning, enable organizations to seamlessly gather, process, and   react instantaneously using complex and advanced reasoning based on Artificial Intelligence, without human intervention to vast amounts of data from diverse sources in real-time.

By autonomously monitoring competitors' activities, product developments, market trends, and customer sentiments, these agents provide up-to-the-minute insights that facilitate rapid decision-making and agile strategy formulation. They minimize human bias and error while maximizing the depth and breadth of information collected, ensuring a comprehensive understanding of the competitive landscape.

Furthermore, autonomous agents excel in scalability and efficiency, enabling businesses to monitor a wide range of competitors concurrently, identify emerging opportunities and threats, and allocate resources effectively. Ultimately, harnessing autonomous agents for competitive intelligence empowers organizations to proactively adapt to dynamic markets and gain a sustained competitive edge.

## YouTube Intelligence: 

Harnessing the power of automation, the YouTube Intelligence agent emerges as a vigilant sentinel, tirelessly monitoring the digital corridors of competitors' YouTube channels. Its unwavering gaze is fixated on the arrival of newly uploaded videos, triggering a cascade of actions that transform data into actionable insights. As soon as a video finds its place on the platform, the agent springs into action, enlisting the aid of state-of-the-art AI tools to embark on an audio content analysis expedition. The results are transformed into succinct, comprehensive summaries that capture the essence of the video's message, style, and intent.

But the agent's role doesn't halt at insightful analysis. With a seamless flow of precision, it diligently crafts emails tailored for the eyes of those within the company who are poised to glean the most from these findings. These emails serve as bridges between the digital realm and the human domain, furnishing pertinent company staff with a transcript-based encapsulation of the video's core content. This expeditious delivery of essential information equips decision-makers with the knowledge they need to act with precision and agility.

Simultaneously, the agent adds another layer to this symphony of data orchestration. In meticulous concert with technology, it meticulously logs the event in a Google Sheet—a chronicle of milestones and insights. Here, each entry serves as a valuable piece in the puzzle of competitive understanding, forming a robust foundation upon which strategic pathways can be forged.

The beauty of this orchestrated mechanism lies not just in its efficiency but also in its potential for evolution. It acts as a gateway to a realm of possibilities. As the agents and tools advance, so do the opportunities for innovation. The email notifications and Google Sheets become canvases of potential, where deeper analysis, trend tracking, and correlation discovery can be painted, further enriching the intelligence tapestry.

In conclusion, the YouTube Intelligence agent stands as a testament to the transformative synergy of technology and insight. It not only serves as a diligent observer but also as an enabler of strategic evolution, casting a spotlight on the digital realm and translating it into actionable wisdom for competitive supremacy.

## Wikipedia Intelligence: 

This sophisticated autonomous agent plays a pivotal role in keeping a vigilant eye on alterations occurring within a competitor's Wikipedia page. By diligently monitoring this dynamic online encyclopedia, the agent ensures that no significant changes go unnoticed. 

As soon as any modifications are detected—ranging from content updates to edits in formatting or references—the agent springs into action. It initiates a seamless process of notifying the relevant members of the company's workforce, ensuring that those directly concerned with competitive analysis are promptly informed. Leveraging the power of email, the agent crafts succinct yet informative messages that encapsulate the essence of the alteration. 

This concise overview provides essential context, enabling company personnel to swiftly comprehend the nature and implications of the change. Through this meticulously orchestrated process, the Wikipedia Intelligence agent contributes to maintaining an up-to-date and comprehensive understanding of the competitive landscape, empowering businesses to adapt, strategize, and excel.

## PDF Intelligence:

This trailblazing autonomous agent, embarking on a relentless quest to scour the digital landscape for the emergence of new PDF publications from competitors. In an era defined by information overload, this agent emerges as a sentinel of discernment, meticulously sifting through the digital pages to extract meaningful insights. With each new PDF document that graces the digital realm, the agent springs into action, employing the prowess of advanced AI tools to dissect its content with surgical precision.

The outcome is a synthesized distillation of knowledge, a concise summary that encapsulates the document's essence, core concepts, and key takeaways. But the magic of PDF Intelligence doesn't end there; it goes a step further, ingeniously categorizing the information into relevant segments. These categories serve as gateways, each leading to a realm of actionable possibilities tailored to specific areas of interest. Whether it's the sales strategies that need recalibration or the financial projections that warrant analysis, PDF Intelligence knows where to direct its findings for maximum impact.

The orchestration of dissemination is an art perfected by PDF Intelligence. With finesse and efficiency, the agent leverages the collaborative prowess of Slack, the communication hub that bridges the gap between teams and projects. Here, in the digital amphitheater of channels, PDF Intelligence finds its stage. With a knowing glance at the categorized insights, it elegantly posts the summaries to the appropriate channels, each like a ripple of knowledge echoing through the corridors of relevance.

Imagine the sales team greeted with a salvo of insights that align with their goals, or the finance team with a nuanced understanding of market trends to fortify their strategies. PDF Intelligence is not merely an observer; it is an enabler of informed action, a catalyst for strategic transformation.

As the curtains rise on this symphony of insight orchestration, PDF Intelligence stands as the conductor, seamlessly weaving the threads of technology, analysis, and communication into a harmonious tapestry of actionable intelligence. In an age where knowledge reigns supreme, PDF Intelligence ascends as the beacon that illuminates the path to success, harnessing AI and collaboration to deliver a competitive edge that reverberates throughout the organization's strategic pursuits.

## Dependencies 

```
pip install -r requirements.txt
```
##  Requirements
- OpenAI API key
- Zapier Natural Language API Key
- Zapier NLA account to create the required tasks in Zapier's UI (see the resources section below for additional information)
- Google API key to monitor youtube channels (see the resources section below for additional information)

## RUN 
1. clone repo
2. cd into `optiagent`
3. rename `env_sample` to `.env` fill with your OpenAI, Zapier and Google API keys. Fill in the Wikipedia page URL you want to monitor for changes. Fill in the YouTube channel id (get the channel Id of a youtube channnel from here: https://commentpicker.com/youtube-channel-id.php) and any channel name you want to monitor. Fill in the email that will receive emails sent by the scripts in this repo. 
4. Setup your Zapier NLA project in the Zapier NLA UI
5. Setup your Google project in the Google UI
6. The scripts run continuously. The interrupt a script, press ctrl-c. The python scripts can be run using
```
python pdf_intelligence.py
python wikipedia-intelligence.py
python youtube-intelligence.py
```
## Resources

- Langchain Quickstart Guide https://langchain.readthedocs.io/en/latest/getting_started/getting_started.html
- OpenAI API Keys https://platform.openai.com/account/api-keys
- Zapier NLA Docs https://nla.zapier.com/api/v1/dynamic/docs
- Zapier NLA Get Started https://nla.zapier.com/get-started/
- Zapier API signup https://zapier.com/l/natural-language-actions
- Google API signup https://cloud.google.com/docs/authentication/api-keys