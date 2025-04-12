import akka.actor.typed.ActorSystem
import akka.actor.typed.scaladsl.Behaviors
import akka.http.scaladsl.Http
import akka.http.scaladsl.model._
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport
import spray.json._
import scala.concurrent.ExecutionContextExecutor
import scala.io.StdIn
import scala.util.Properties
import com.typesafe.config.ConfigFactory
import java.security.MessageDigest

trait JsonSupport extends SprayJsonSupport with DefaultJsonProtocol {
  implicit val messageFormat = jsonFormat1(Message)
  implicit val offerRequestFormat = jsonFormat1(OfferRequest)
}

case class Message(message: String)
case class OfferRequest(data: JsValue)

object Search extends JsonSupport {
  def main(args: Array[String]): Unit = {
    implicit val system: ActorSystem[Nothing] = ActorSystem(Behaviors.empty, "search-backend")
    implicit val executionContext: ExecutionContextExecutor = system.executionContext

    val route = 
      cors() {
        pathSingleSlash {
          get {
            complete(Message("Welcome to the backend!"))
          }
        } ~
        path("duffel-flights-list-offers") {
          post {
            entity(as[OfferRequest]) { offerRequest =>
              val responseFuture = Http().singleRequest(HttpRequest(
                method = HttpMethods.POST,
                uri = "https://api.duffel.com/air/offer_requests",
                headers = List(
                  headers.Accept(MediaTypes.`application/json`),
                  headers.`Accept-Encoding`(HttpEncodings.gzip),
                  headers.`Content-Type`(ContentTypes.`application/json`),
                  headers.RawHeader("Duffel-Version", "v2"),
                  headers.Authorization(OAuth2BearerToken(Properties.envOrElse("DUFFEL_API_KEY", "")))
                ),
                entity = HttpEntity(ContentTypes.`application/json`, offerRequest.toJson.compactPrint)
              ))
              onComplete(responseFuture) { response =>
                complete(response)
              }
            }
          }
        }
      }

    val host = "0.0.0.0"
    val port = 5000
    val bindingFuture = Http().newServerAt(host, port).bind(route)

    println(s"Server now online at http://$host:$port/")
    println("Press RETURN to stop...")
    StdIn.readLine()
    
    bindingFuture
      .flatMap(_.unbind())
      .onComplete(_ => system.terminate())
  }

  private def cors() = {
    respondWithHeaders(
      headers.`Access-Control-Allow-Origin`.*,
      headers.`Access-Control-Allow-Credentials`(true),
      headers.`Access-Control-Allow-Headers`("Authorization", "Content-Type", "X-Requested-With")
    ) {
      options {
        complete(StatusCodes.OK)
      } ~ 
      get {
        extractRequest { _ =>
          mapResponse { response =>
            response.withHeaders(
              headers.`Access-Control-Allow-Origin`.*,
              headers.`Access-Control-Allow-Credentials`(true)
            )
          }
        }
      }
    }
  }
}