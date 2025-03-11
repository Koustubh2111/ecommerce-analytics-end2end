#### Issues
*  **Issue** Deserialization failed because the consumer was unable to correctly deserialize the message produced by the Kafka producer. Resulting in the error `'NoneType' object has no attribute 'topic'`. This happened because the deserializer did not receive the correct context to handle the schema information for the message.
**Fix** The `JSONDeserializer` relies on the `SerializationContext` to properly parse the message. Adding the `SerializationContext` explicitly while calling the `json_deserializer` provided the necessary context (like the schema information and message field) for deserialization. 



