import grpc
from clients import game_of_life_client
from sequence_logger import init_log

init_log()

# Sequence logic
stream_result = game_of_life_client.stream_measure()

try:
    for xy_data, generation in stream_result:
        print("Generation: ", generation)
        
        if generation == 10:    # condition for cancellation
            game_of_life_client.cancel()
            print("Cancelling measurement...")
            
except grpc.RpcError as e:     
    if e.code() == grpc.StatusCode.CANCELLED:   # handle when a cancelled measurement is accessed
        print("Measurement has been cancelled.")
        
except Exception as e:
    raise Exception(f"Unexpected error occured : {e}")