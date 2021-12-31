import boto3
import time

logs = boto3.client('logs',region_name="us-east-1")
def logs_pusher(msg):


    LOG_GROUP = "Test-2"
    LOG_STREAM = "stream-2"
    is_exist_group = len(logs.describe_log_groups(
        logGroupNamePrefix=LOG_GROUP,
    ).get('logGroups')) > 0

    if not is_exist_group:
        logs.create_log_group(logGroupName=LOG_GROUP)
    is_stream_existing = len(logs.describe_log_streams(
        logGroupName=LOG_GROUP,
        logStreamNamePrefix=LOG_STREAM
    )['logStreams']
    ) > 0

    if not is_stream_existing:
        logs.create_log_stream(logGroupName=LOG_GROUP,
                               logStreamName=LOG_STREAM)

    response =response = logs.describe_log_streams(
   logGroupName=LOG_GROUP,
   logStreamNamePrefix=LOG_STREAM
)

    
    try:
        timestamp = int(round(time.time() * 1000))
        event_log = {
            'logGroupName': LOG_GROUP,
            'logStreamName': LOG_STREAM,
            'logEvents': [
                {
                    'timestamp': timestamp, 
                    'message': str(msg)
                }], }
        if 'uploadSequenceToken' in response['logStreams'][0]:
            event_log.update({'sequenceToken': response['logStreams'][0] ['uploadSequenceToken']})
        response = logs.put_log_events(**event_log)
    except Exception as e:
        timestamp = int(round(time.time() * 1000))
        event_log = {
            'logGroupName': LOG_GROUP,
            'logStreamName': LOG_STREAM,
            'logEvents': [
                {
                    'timestamp': timestamp, 
                    'message': str(msg)
                }], }
        event_log.update({'sequenceToken': str(e).split(" ")[-1]})
        response = logs.put_log_events(**event_log)
  

        return
    return "Logs Are Initialized"

t=0
for i in range(1000,10000):
    
    msg=str(i)*i
    logs_pusher(msg)
    time.sleep(1)
    t+=1
