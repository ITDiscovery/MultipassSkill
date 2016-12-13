def lambda_handler(event, context):

    import boto3

    should_end_session = True
    card_title = 'Multipass'
    topiccmdPath = "$aws/things/Multipass/shadow/command"
    topicstatusPath = "$aws/things/Multipass/shadow/update"

    IRCommands = ["Power","Ch+","Ch-","Vol+","Vol-","Mute","Input","1","2","3","4","5","6","7",
                            "8","9","0","Enter","Menu","Up","Down","Left","Right","Index","Caption","Audio"]
    
    #Check Application ID first
    if event['session']['application']['applicationId'] == "amzn1.ask.skill.499fb834-7c7a-4f83-8383-4112cb8621a6":
        if event['request']['type'] == "IntentRequest":
            SendToShadow = event['request']['intent']['slots']['Keys']['value']
            #EventType = event['request']['intent']['slots']['Actions']['name']
            AlexaResp = "Baa Dah boom"
            
            # Update the Device Shadow
            client = boto3.client('iot-data', region_name='us-east-1')
            #Error Trap this as extra credit
            #response = client.get_thing_shadow(thingName='Multipass')
            SendToShadow = '{"message": "' + SendToShadow + '" }'
            response = client.publish(topic=topiccmdPath,qos=1,payload=SendToShadow)
    else:
        AlexaResp = "This appplication is sending data to the wrong lambda function."

    # Standard "OK" response
    #AlexaResp = "Ba-da-boom"
    # Stanard "Bad" response
    #AlexaResp = "Dort"
    
    return (build_response({}, build_speechlet_response(card_title, AlexaResp, None, should_end_session)))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
