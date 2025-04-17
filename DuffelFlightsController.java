import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplateBuilder;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.http.client.ClientHttpRequestFactory;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.retry.annotation.EnableRetry;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.CrossOrigin;

@SpringBootApplication
@EnableRetry
public class DuffelFlightsApplication {
    public static void main(String[] args) {
        SpringApplication.run(DuffelFlightsApplication.class, args);
    }

    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder.setConnectTimeout(Duration.ofSeconds(60)).setReadTimeout(Duration.ofSeconds(60)).build();
    }
}

@RestController
@RequestMapping("/duffel-flights")
@CrossOrigin(origins = "*")
class DuffelFlightsController {
    private final RestTemplate restTemplate;

    public DuffelFlightsController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @PostMapping("/list-offers")
    @Retryable(value = {ResourceAccessException.class, RestClientException.class}, maxAttempts = 3, backoff = @Backoff(delay = 2000))
    public ResponseEntity<String> listOffers(@RequestBody String requestBody) {
        String url = "https://api.duffel.com/air/offer_requests";
        HttpHeaders headers = new HttpHeaders();
        headers.add("Accept-Encoding", "gzip");
        headers.add("Accept", "application/json");
        headers.add("Content-Type", "application/json");
        headers.add("Duffel-Version", "v2");
        headers.add("Authorization", "Bearer " + System.getenv("DUFFEL_API_KEY"));
        HttpEntity<String> entity = new HttpEntity<>(requestBody, headers);
        try {
            ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);
            System.out.println("Request Body: " + requestBody);
            System.out.println("Response Body: " + response.getBody());
            return response;
        } catch (HttpClientErrorException e) {
            System.out.println("Error: " + e.getStatusCode() + " - " + e.getResponseBodyAsString());
            return new ResponseEntity<>(e.getResponseBodyAsString(), e.getStatusCode());
        } catch (ResourceAccessException e) {
            System.out.println("Timeout Error: " + e.getMessage());
            return new ResponseEntity<>("Request Timeout", HttpStatus.REQUEST_TIMEOUT);
        }
    }
}