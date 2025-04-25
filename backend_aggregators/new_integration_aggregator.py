# New Integration Aggregator

class NewIntegrationAggregator:
    def __init__(self, adapter):
        self.adapter = adapter

    def aggregate(self):
        # Logic to aggregate data from the adapter
        data = self.adapter.fetch_data()
        processed_data = self.adapter.process_data(data)
        return processed_data

# Example usage
# adapter = NewIntegrationAdapter(config)
# aggregator = NewIntegrationAggregator(adapter)
# aggregated_data = aggregator.aggregate()