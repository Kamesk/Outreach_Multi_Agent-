from boto3.dynamodb.conditions import Key,Attr
from src.clients.aws.dynamodb import get_table
from src.services.comments.llm import generate_reply
from src.services.comments.replier import reply

def process_comment_payload(post_id,post_text):
    table=get_table(); response=table.query(IndexName="SK-index",KeyConditionExpression=Key("SK").eq(post_id),FilterExpression=Attr("llm_response").not_exists()|Attr("llm_response").eq(None)|Attr("llm_response").eq(""))
    items=response.get("Items",[])
    if not items:return None
    comment=sorted(items,key=lambda x:x["timestamp"],reverse=True)[0]; text=generate_reply(comment["comment_text"],post_text)
    if not text:return None
    if reply(comment["activity_id"],comment["PK"],text):
        table.update_item(Key={"PK":comment["PK"],"SK":post_id},UpdateExpression="SET llm_response = :r, replied_to_linkedin = :t",ExpressionAttributeValues={":r":text,":t":True})
        return text
    return None
