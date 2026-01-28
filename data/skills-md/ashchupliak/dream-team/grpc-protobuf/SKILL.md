---
name: grpc-protobuf
description: gRPC and Protocol Buffers - use for service-to-service communication, API definitions, streaming, and inter-service contracts
---

# gRPC and Protocol Buffers Patterns

## Proto File Structure

```protobuf
syntax = "proto3";

package orca.environment.v1;

option java_package = "orca.server.grpc.environment";
option java_multiple_files = true;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Service definition
service EnvironmentService {
  // Unary RPCs
  rpc CreateEnvironment(CreateEnvironmentRequest) returns (Environment);
  rpc GetEnvironment(GetEnvironmentRequest) returns (Environment);
  rpc ListEnvironments(ListEnvironmentsRequest) returns (ListEnvironmentsResponse);
  rpc DeleteEnvironment(DeleteEnvironmentRequest) returns (google.protobuf.Empty);

  // Server streaming
  rpc WatchEnvironment(WatchEnvironmentRequest) returns (stream EnvironmentEvent);

  // Bidirectional streaming
  rpc StreamLogs(stream LogRequest) returns (stream LogResponse);
}

// Messages
message Environment {
  string id = 1;
  string name = 2;
  EnvironmentStatus status = 3;
  google.protobuf.Timestamp created_at = 4;
  google.protobuf.Timestamp updated_at = 5;
  map<string, string> labels = 6;
}

enum EnvironmentStatus {
  ENVIRONMENT_STATUS_UNSPECIFIED = 0;
  ENVIRONMENT_STATUS_PENDING = 1;
  ENVIRONMENT_STATUS_RUNNING = 2;
  ENVIRONMENT_STATUS_STOPPED = 3;
  ENVIRONMENT_STATUS_FAILED = 4;
}

message CreateEnvironmentRequest {
  string name = 1;
  string description = 2;
  map<string, string> labels = 3;
}

message GetEnvironmentRequest {
  string id = 1;
}

message ListEnvironmentsRequest {
  int32 page_size = 1;
  string page_token = 2;
  string filter = 3;  // e.g., "status=RUNNING"
}

message ListEnvironmentsResponse {
  repeated Environment environments = 1;
  string next_page_token = 2;
  int32 total_count = 3;
}

message DeleteEnvironmentRequest {
  string id = 1;
}

message WatchEnvironmentRequest {
  string id = 1;
}

message EnvironmentEvent {
  Environment environment = 1;
  EventType type = 2;
  google.protobuf.Timestamp timestamp = 3;

  enum EventType {
    EVENT_TYPE_UNSPECIFIED = 0;
    EVENT_TYPE_CREATED = 1;
    EVENT_TYPE_UPDATED = 2;
    EVENT_TYPE_DELETED = 3;
  }
}
```

## Spring gRPC Server Implementation

```kotlin
@GrpcService
class EnvironmentGrpcService(
    private val environmentService: EnvironmentService
) : EnvironmentServiceGrpcKt.EnvironmentServiceCoroutineImplBase() {

    override suspend fun createEnvironment(
        request: CreateEnvironmentRequest
    ): Environment {
        val result = environmentService.create(request.toDomain())
        return result.toProto()
    }

    override suspend fun getEnvironment(
        request: GetEnvironmentRequest
    ): Environment {
        val id = UUID.fromString(request.id)
        val env = environmentService.findById(id)
            ?: throw StatusException(Status.NOT_FOUND.withDescription("Environment not found: ${request.id}"))
        return env.toProto()
    }

    override suspend fun listEnvironments(
        request: ListEnvironmentsRequest
    ): ListEnvironmentsResponse {
        val page = environmentService.findAll(
            pageSize = request.pageSize,
            pageToken = request.pageToken.ifEmpty { null }
        )

        return ListEnvironmentsResponse.newBuilder()
            .addAllEnvironments(page.items.map { it.toProto() })
            .setNextPageToken(page.nextToken ?: "")
            .setTotalCount(page.total)
            .build()
    }

    override fun watchEnvironment(
        request: WatchEnvironmentRequest
    ): Flow<EnvironmentEvent> = flow {
        val id = UUID.fromString(request.id)

        environmentService.watchEvents(id).collect { event ->
            emit(event.toProto())
        }
    }
}
```

## gRPC Client Implementation

```kotlin
@Component
class ComputeClient(
    @GrpcClient("compute")
    private val stub: ComputeServiceGrpcKt.ComputeServiceCoroutineStub
) {

    suspend fun createInstance(request: CreateInstanceRequest): Instance {
        return try {
            stub.createInstance(request)
        } catch (e: StatusException) {
            when (e.status.code) {
                Status.Code.NOT_FOUND -> throw ResourceNotFoundRestException("Instance template not found")
                Status.Code.ALREADY_EXISTS -> throw ConflictRestException("Instance already exists")
                Status.Code.RESOURCE_EXHAUSTED -> throw ServiceUnavailableException("Quota exceeded")
                else -> throw InternalServerException("Compute service error: ${e.message}")
            }
        }
    }

    suspend fun getInstance(id: String): Instance? {
        return try {
            stub.getInstance(GetInstanceRequest.newBuilder().setId(id).build())
        } catch (e: StatusException) {
            if (e.status.code == Status.Code.NOT_FOUND) null
            else throw e
        }
    }
}
```

## Error Handling with gRPC Status

```kotlin
// Mapping domain exceptions to gRPC status
@GrpcAdvice
class GrpcExceptionHandler {

    @GrpcExceptionHandler(ResourceNotFoundRestException::class)
    fun handleNotFound(e: ResourceNotFoundRestException): StatusException =
        StatusException(
            Status.NOT_FOUND
                .withDescription(e.message)
                .withCause(e)
        )

    @GrpcExceptionHandler(ValidationRestException::class)
    fun handleValidation(e: ValidationRestException): StatusException =
        StatusException(
            Status.INVALID_ARGUMENT
                .withDescription(e.message)
                .withCause(e)
        )

    @GrpcExceptionHandler(ConflictRestException::class)
    fun handleConflict(e: ConflictRestException): StatusException =
        StatusException(
            Status.ALREADY_EXISTS
                .withDescription(e.message)
                .withCause(e)
        )
}
```

## Interceptors

```kotlin
// Server interceptor for logging/metrics
@Component
class LoggingServerInterceptor : ServerInterceptor {

    override fun <ReqT, RespT> interceptCall(
        call: ServerCall<ReqT, RespT>,
        headers: Metadata,
        next: ServerCallHandler<ReqT, RespT>
    ): ServerCall.Listener<ReqT> {
        val method = call.methodDescriptor.fullMethodName
        val startTime = System.currentTimeMillis()

        logger.info("gRPC call started: $method")

        return object : ForwardingServerCallListener.SimpleForwardingServerCallListener<ReqT>(
            next.startCall(call, headers)
        ) {
            override fun onComplete() {
                val duration = System.currentTimeMillis() - startTime
                logger.info("gRPC call completed: $method (${duration}ms)")
                super.onComplete()
            }
        }
    }
}

// Client interceptor for auth
@Component
class AuthClientInterceptor(
    private val tokenProvider: TokenProvider
) : ClientInterceptor {

    override fun <ReqT, RespT> interceptCall(
        method: MethodDescriptor<ReqT, RespT>,
        callOptions: CallOptions,
        next: Channel
    ): ClientCall<ReqT, RespT> {
        return object : ForwardingClientCall.SimpleForwardingClientCall<ReqT, RespT>(
            next.newCall(method, callOptions)
        ) {
            override fun start(responseListener: Listener<RespT>, headers: Metadata) {
                headers.put(
                    Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER),
                    "Bearer ${tokenProvider.getToken()}"
                )
                super.start(responseListener, headers)
            }
        }
    }
}
```

## Proto to Domain Mapping

```kotlin
// Domain to Proto
fun orca.server.domain.Environment.toProto(): Environment =
    Environment.newBuilder()
        .setId(id.toString())
        .setName(name)
        .setStatus(status.toProto())
        .setCreatedAt(createdAt.toProtoTimestamp())
        .apply { updatedAt?.let { setUpdatedAt(it.toProtoTimestamp()) } }
        .putAllLabels(labels)
        .build()

fun EnvironmentStatus.toProto(): orca.grpc.EnvironmentStatus =
    when (this) {
        EnvironmentStatus.PENDING -> orca.grpc.EnvironmentStatus.ENVIRONMENT_STATUS_PENDING
        EnvironmentStatus.RUNNING -> orca.grpc.EnvironmentStatus.ENVIRONMENT_STATUS_RUNNING
        EnvironmentStatus.STOPPED -> orca.grpc.EnvironmentStatus.ENVIRONMENT_STATUS_STOPPED
        EnvironmentStatus.FAILED -> orca.grpc.EnvironmentStatus.ENVIRONMENT_STATUS_FAILED
    }

fun Instant.toProtoTimestamp(): Timestamp =
    Timestamp.newBuilder()
        .setSeconds(epochSecond)
        .setNanos(nano)
        .build()

// Proto to Domain
fun CreateEnvironmentRequest.toDomain() = CreateEnvironmentDomainRequest(
    name = name,
    description = description.ifEmpty { null },
    labels = labelsMap
)
```

## Streaming Patterns

```kotlin
// Server streaming
override fun watchEnvironment(request: WatchRequest): Flow<Event> = flow {
    val channel = eventBus.subscribe(request.id)

    try {
        for (event in channel) {
            emit(event.toProto())
        }
    } finally {
        channel.cancel()
    }
}

// Bidirectional streaming
override fun chat(requests: Flow<ChatMessage>): Flow<ChatResponse> = flow {
    requests.collect { message ->
        val response = processMessage(message)
        emit(response)
    }
}
```
