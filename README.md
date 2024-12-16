Welcome to the Trapi Demo Backend Repo!

Here we have a mainly python backend template you can use to test out the Trapi automated integration tool.

Theres not much in here... just some blank boilerplate files to put into Trapi so that you can see the code get generated.

You'll need to get hold of our sandbox API keys for any API you want to test out. Or get in touch if you're having trouble doing that.

## New Endpoint Added

- **Endpoint**: `/duffel-flights-list-offers`
- **Method**: POST
- **Description**: This endpoint allows you to list flight offers using the Duffel API.
- **Request Body**: JSON object containing flight search criteria.
- **Environment Variable Required**: `DUFFEL_API_KEY`