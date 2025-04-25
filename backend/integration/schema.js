// Schema for new integration

export const newIntegrationSchema = {
    type: 'object',
    properties: {
        id: { type: 'string' },
        name: { type: 'string' },
        // Add more properties as needed
    },
    required: ['id', 'name']
};