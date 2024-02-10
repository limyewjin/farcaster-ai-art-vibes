# Automated AI Art posting bot to Farcaster

This project automates the generation of AI art through OpenAI's DALL-E 3 and posts it to Farcaster using the Warpcast API. It leverages Python scripting to create visual content for good morning posts (just as a means to test out the process):

The following API keys / mnemonics are needed
- OpenAI: https://platform.openai.com/docs/quickstart?context=python
- Farcaster Mnemonic can be found in Warpcast app -> Settings -> Advanced -> Farcaster recovery phrase
- imgBB API: https://api.imgbb.com/

## Steps

1. `cp .env-sample .env`
2. Edit `.env` with the API keys / mnemonics
3. `pip install -r requirements.txt`
4. `python main.py`
