from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_API_TOKEN_TEST = 'xoxb-2466532012407-2481272276067-cOFuO3BwdscAUScDCzdWoppI'
SLACK_TEAM_ID = 'U02E57B9QCT' #support@algotrader.company
SLACK_CLIENT_ID='2466532012407.2493894253969'
SLACK_CLIENT_SECRET='1714cabace8fbfcf17786442934455ee'
# pip install slack_sdk



def slack_create_channel():
    client = WebClient(SLACK_API_TOKEN_TEST)
    try:
        result = client.conversations_create(
            # The name of the conversation
            name="test_channel_notprivate",
            is_private=False
        )

        print(result)

    except SlackApiError as e:
        print("Error creating conversation: {}".format(e))


def slack_post_message():
    client = WebClient(SLACK_API_TOKEN_TEST)
    try:
        result = client.chat_postMessage(
          channel="C02E599HA7L",
          blocks=[
            {
              "type": "section",
              "text": {
                "type": "mrkdwn",
                "text": "Danny Torrence left the following review for your property:"
              }
            },
            {
              "type": "section",
              "text": {
                "type": "mrkdwn",
                "text": "<https://example.com|Overlook Hotel> \n :star: \n Doors had too many axe holes, guest in room " +
                  "237 was far too rowdy, whole place felt stuck in the 1920s."
              },
              "accessory": {
                "type": "image",
                "image_url": "https://images.pexels.com/photos/750319/pexels-photo-750319.jpeg",
                "alt_text": "Haunted hotel image"
              }
            },
            {
              "type": "section",
              "fields": [
                {
                  "type": "mrkdwn",
                  "text": "*Average Rating*\n1.0"
                }
              ]
            }
          ]
        )

        print(result)

    except SlackApiError as e:
        print("Error creating conversation: {}".format(e))


def slack_invite_users():
    client = WebClient(SLACK_API_TOKEN_TEST)
    try:
        result = client.conversations_invite(
            channel="C02E599HA7L",
            users="U02E57B9QCT,U02E57BV0LB"
        )

        print(result)

    except SlackApiError as e:
        print("Error creating conversation: {}".format(e))