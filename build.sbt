name := "demo-customer-be"
version := "0.1.0"
scalaVersion := "2.13.10"

val AkkaVersion = "2.7.0"
val AkkaHttpVersion = "10.5.0"

libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-actor-typed" % AkkaVersion,
  "com.typesafe.akka" %% "akka-stream" % AkkaVersion,
  "com.typesafe.akka" %% "akka-http" % AkkaHttpVersion,
  "com.typesafe.akka" %% "akka-http-spray-json" % AkkaHttpVersion,
  "ch.qos.logback" % "logback-classic" % "1.4.6"
)

Compile / run / mainClass := Some("Search")