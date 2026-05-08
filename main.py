from browser_use import Agent, Browser, ChatBrowserUse
from browser_use import ChatAnthropic 
import asyncio

async def main():
    # testing list profiles 
    profiles = Browser.list_chrome_profiles()
    for p in profiles:
        print(f"{p['directory']}: {p['name']}")

    browser = Browser.from_system_chrome(profile_directory="Profile 1")

    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
    )

    agent = Agent("go to linkedin.com, select the jobs tab, search for 'full stack developer', ignore all jobs that have use linkedin easy apply, record the first ten jobs and their job title, location, compensation, sponsorship information. return the results in a comma separated format, if any information is not found, simply put 'not found'.",
        llm=llm,
        browser=browser,
    )
    agent_result = await agent.run()

if __name__ == "__main__":
    asyncio.run(main())