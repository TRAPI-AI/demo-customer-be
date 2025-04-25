import asyncio
from providers.existing_provider import ExistingProvider
from providers.new_provider import NewProvider

class Aggregator:
    def __init__(self):
        self.providers = [ExistingProvider(), NewProvider()]

    async def fetch_from_provider(self, provider):
        try:
            response = await provider.fetch_data()
            if self.validate_response(response):
                return self.map_response(response)
        except Exception as e:
            print(f"Error fetching data from {provider}: {e}")
        return None

    def validate_response(self, response):
        # Implement validation logic
        return 'required_field' in response

    def map_response(self, response):
        # Map the response to a common format
        return {
            'field1': response.get('field1'),
            'field2': response.get('field2'),
            # Add all required fields
        }

    async def agg_text(self):
        tasks = [self.fetch_from_provider(provider) for provider in self.providers]
        results = await asyncio.gather(*tasks)
        # Filter out None results and combine them
        combined_results = [result for result in results if result is not None]
        return combined_results

# Example usage
# aggregator = Aggregator()
# asyncio.run(aggregator.agg_text())
