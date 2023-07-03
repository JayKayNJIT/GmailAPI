from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os, base64, email, time, logging, os.path

SCOPES = ['https://mail.google.com/']

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        def get_new_email():
            logging.basicConfig(filename='bloomberg_gmailAPI.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            try:
                service = build('gmail', 'v1', credentials=creds)
                query = 'from:jatin199k@bloomberg.net in:inbox'
                threads = service.users().threads().list(userId='me', q=query).execute().get('threads', [])
                if not threads:
                    return None
                newest_thread_id = threads[0]['id']
                thread = service.users().threads().get(userId='me', id=newest_thread_id).execute()
                message_ids = [message['id'] for message in thread['messages']]
                message = service.users().messages().get(userId='me', id=message_ids[0]).execute()
                headers = message['payload']['headers']
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
                body_parts = message['payload']['parts']
                body = ''
                for part in body_parts:
                    if part.get('parts'):
                        for subpart in part['parts']:
                            if subpart['mimeType'] == 'text/plain':
                                body += subpart['body']['data']
                    else:
                        if part['mimeType'] == 'text/plain':
                            body += part['body']['data']
                body = base64.urlsafe_b64decode(body).decode('UTF-8')
                service.users().messages().delete(userId='me', id=message_ids[0]).execute()
                logging.info(f'Subject: {subject}')
                logging.info(f'Body: {body}')
                return (subject, body)
            except HttpError as error:
                logging.error(f'An error occurred: {error}')
                return None

        while True:
            try:
                result = get_new_email()
                time.sleep(2)
            except:
                logging.exception('An error occurred in get_new_email(), continuing with next iteration')
                continue
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
