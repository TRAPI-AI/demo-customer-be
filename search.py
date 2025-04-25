import asyncio
from providers.existing_provider import ExistingProvider
from providers.new_provider import NewProvider

class Aggregator:
    def __init__(self):
        self.providers = [ExistingProvider(), NewProvider()]

    async def fetch_from_provider(self, provider, query):
        try:
            response = await provider.search(query)
            if self.validate_response(response):
                return self.map_response(response)
        except Exception as e:
            print(f"Error fetching from provider {provider}: {e}")
        return None

    def validate_response(self, response):
        # Implement validation logic
        return 'required_field' in response

    def map_response(self, response):
        # Map the response to a common format
        return {
            'field1': response.get('required_field'),
            'field2': response.get('another_field')
        }

    async def agg_text(self, query):
        tasks = [self.fetch_from_provider(provider, query) for provider in self.providers]
        results = await asyncio.gather(*tasks)
        # Filter out None results and combine
        return [result for result in results if result is not None]

# Example usage
# aggregator = Aggregator()
# results = asyncio.run(aggregator.agg_text('search query'))
# print(results)
