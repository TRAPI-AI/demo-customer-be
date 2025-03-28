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

// JSON formatting support
trait JsonSupport extends SprayJsonSupport with DefaultJsonProtocol {
  implicit val messageFormat = jsonFormat1(Message)
}

// Message model
case class Message(message: String)

object Search extends JsonSupport {
  def main(args: Array[String]): Unit = {
    // Create an actor system for the server
    implicit val system: ActorSystem[Nothing] = ActorSystem(Behaviors.empty, "search-backend")
    implicit val executionContext: ExecutionContextExecutor = system.executionContext

    // Define routes
    val route = 
      cors() {
        pathSingleSlash {
          get {
            complete(Message("Welcome to the backend!"))
          }
        }
      }

    // Start server
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

  // Simple CORS handling
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